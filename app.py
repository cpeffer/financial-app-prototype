from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import sqlite3
from datetime import datetime
from functools import wraps
import base64
import requests
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Google Gemini API configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
GEMINI_MODEL = 'gemini-2.0-flash-exp'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Categories for expenses
CATEGORIES = ['Groceries', 'Dining', 'Transport', 'Shopping', 'Entertainment', 'Utilities', 'Healthcare', 'Other']

def get_db():
    """Get database connection"""
    conn = sqlite3.connect('expenses.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with required tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            vendor TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Line items table for itemized receipt data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS line_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            quantity REAL DEFAULT 1,
            unit_price REAL,
            total_price REAL NOT NULL,
            FOREIGN KEY (expense_id) REFERENCES expenses (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def analyze_receipt_with_gemini(image_path):
    """Use Google Gemini Vision API to extract itemized data from receipt"""
    if not GEMINI_API_KEY:
        return None
    
    try:
        # Read and encode image
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Determine image MIME type
        ext = image_path.lower().split('.')[-1]
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif'
        }
        mime_type = mime_types.get(ext, 'image/jpeg')
        
        # Prepare API request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        
        prompt = """Analyze this receipt image and extract the following information in JSON format:
{
  "vendor": "store name",
  "date": "YYYY-MM-DD",
  "items": [
    {
      "name": "item description",
      "quantity": 1.0,
      "unit_price": 0.00,
      "total": 0.00
    }
  ],
  "subtotal": 0.00,
  "tax": 0.00,
  "total": 0.00
}

Instructions:
- Extract ALL line items from the receipt
- For each item, include name, quantity, unit price, and total
- If quantity is not shown, use 1
- If unit price is not shown, use the total for that item
- Include subtotal, tax, and final total
- Use the exact date format YYYY-MM-DD
- Return ONLY valid JSON, no other text"""

        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_data
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "topK": 32,
                "topP": 0.95,
                "maxOutputTokens": 2048
            }
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            print(f"Gemini API error: {response.status_code} - {response.text}")
            return None
        
        data = response.json()
        
        # Extract text from response
        if 'candidates' in data and len(data['candidates']) > 0:
            candidate = data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                text = candidate['content']['parts'][0].get('text', '')
                
                # Try to extract JSON from the response
                # Remove markdown code blocks if present
                text = text.strip()
                if text.startswith('```json'):
                    text = text[7:]
                if text.startswith('```'):
                    text = text[3:]
                if text.endswith('```'):
                    text = text[:-3]
                text = text.strip()
                
                # Parse JSON
                receipt_data = json.loads(text)
                return receipt_data
        
        return None
        
    except Exception as e:
        print(f"Error analyzing receipt: {str(e)}")
        return None

@app.route('/')
def index():
    """Home page - redirect to dashboard or login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('register'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            flash('Email already registered.', 'danger')
            conn.close()
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, password FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('Invalid email or password.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing expense summary"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get current month/year
    current_month = datetime.now().strftime('%Y-%m')
    
    # Get expenses for current month grouped by category
    cursor.execute('''
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id = ? AND date LIKE ?
        GROUP BY category
        ORDER BY total DESC
    ''', (session['user_id'], f'{current_month}%'))
    
    category_totals = cursor.fetchall()
    
    # Get total for current month
    cursor.execute('''
        SELECT SUM(amount) as total
        FROM expenses
        WHERE user_id = ? AND date LIKE ?
    ''', (session['user_id'], f'{current_month}%'))
    
    month_total = cursor.fetchone()['total'] or 0
    
    # Get recent expenses
    cursor.execute('''
        SELECT * FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC, created_at DESC
        LIMIT 10
    ''', (session['user_id'],))
    
    recent_expenses = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         category_totals=category_totals,
                         month_total=month_total,
                         recent_expenses=recent_expenses,
                         current_month=current_month)

@app.route('/expenses')
@login_required
def expenses():
    """View all expenses"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC, created_at DESC
    ''', (session['user_id'],))
    
    all_expenses = cursor.fetchall()
    conn.close()
    
    return render_template('expenses.html', expenses=all_expenses)

@app.route('/add_expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add new expense"""
    if request.method == 'POST':
        # Check if this is coming from the review form (after OCR)
        is_review = request.form.get('is_review') == 'true'
        
        if is_review:
            # Process reviewed data
            vendor = request.form.get('vendor')
            amount = request.form.get('amount')
            date = request.form.get('date')
            category = request.form.get('category')
            image_path = request.form.get('image_path')
            
            # Validate inputs
            if not all([vendor, amount, date, category]):
                flash('All fields are required.', 'danger')
                return redirect(url_for('add_expense'))
            
            try:
                amount = float(amount)
                if amount <= 0:
                    raise ValueError('Amount must be positive')
            except ValueError:
                flash('Invalid amount.', 'danger')
                return redirect(url_for('add_expense'))
            
            # Save expense to database
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO expenses (user_id, vendor, amount, date, category, image_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], vendor, amount, date, category, image_path))
            expense_id = cursor.lastrowid
            
            # Save line items
            line_items_count = int(request.form.get('line_items_count', 0))
            for i in range(line_items_count):
                item_name = request.form.get(f'item_name_{i}')
                item_quantity = request.form.get(f'item_quantity_{i}')
                item_unit_price = request.form.get(f'item_unit_price_{i}')
                item_total = request.form.get(f'item_total_{i}')
                
                if item_name and item_total:
                    try:
                        quantity = float(item_quantity) if item_quantity else 1.0
                        unit_price = float(item_unit_price) if item_unit_price else None
                        total = float(item_total)
                        
                        cursor.execute('''
                            INSERT INTO line_items (expense_id, item_name, quantity, unit_price, total_price)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (expense_id, item_name, quantity, unit_price, total))
                    except ValueError:
                        continue
            
            conn.commit()
            conn.close()
            
            flash('Expense added successfully!', 'success')
            return redirect(url_for('dashboard'))
        
        else:
            # Initial form submission with image upload
            # Handle file upload
            image_path = None
            if 'receipt_image' not in request.files:
                flash('Please upload a receipt image.', 'danger')
                return redirect(url_for('add_expense'))
            
            file = request.files['receipt_image']
            if not file or not file.filename:
                flash('Please upload a receipt image.', 'danger')
                return redirect(url_for('add_expense'))
            
            if not allowed_file(file.filename):
                flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF).', 'danger')
                return redirect(url_for('add_expense'))
            
            # Save the file
            filename = secure_filename(file.filename)
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_path = f"uploads/{filename}"
            
            # Analyze receipt with Gemini
            receipt_data = analyze_receipt_with_gemini(filepath)
            
            if receipt_data:
                # Show review page with extracted data
                return render_template('review_expense.html', 
                                     receipt_data=receipt_data,
                                     image_path=image_path,
                                     categories=CATEGORIES)
            else:
                flash('Could not analyze receipt. Please enter details manually.', 'warning')
                return render_template('add_expense.html', 
                                     categories=CATEGORIES,
                                     image_path=image_path,
                                     manual_mode=True)
    
    return render_template('add_expense.html', categories=CATEGORIES)

@app.route('/expense/<int:expense_id>')
@login_required
def view_expense(expense_id):
    """View individual expense details"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM expenses
        WHERE id = ? AND user_id = ?
    ''', (expense_id, session['user_id']))
    
    expense = cursor.fetchone()
    
    if not expense:
        conn.close()
        flash('Expense not found.', 'danger')
        return redirect(url_for('expenses'))
    
    # Get line items
    cursor.execute('''
        SELECT * FROM line_items
        WHERE expense_id = ?
        ORDER BY id
    ''', (expense_id,))
    
    line_items = cursor.fetchall()
    conn.close()
    
    return render_template('view_expense.html', expense=expense, line_items=line_items)

@app.route('/delete_expense/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get expense to check ownership and delete image
    cursor.execute('SELECT * FROM expenses WHERE id = ? AND user_id = ?', (expense_id, session['user_id']))
    expense = cursor.fetchone()
    
    if expense:
        # Delete image file if exists
        if expense['image_path']:
            image_full_path = os.path.join('static', expense['image_path'])
            if os.path.exists(image_full_path):
                os.remove(image_full_path)
        
        # Delete from database
        cursor.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (expense_id, session['user_id']))
        conn.commit()
        flash('Expense deleted successfully.', 'success')
    else:
        flash('Expense not found.', 'danger')
    
    conn.close()
    return redirect(url_for('expenses'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
