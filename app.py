import os
import base64
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='frontend/build')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Get Google Cloud Vision API key from environment
GOOGLE_VISION_API_KEY = os.getenv('GOOGLE_VISION_API_KEY', '')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_receipt_with_vision_api(image_path):
    """Process receipt using Google Cloud Vision API"""
    if not GOOGLE_VISION_API_KEY:
        # Return mock data if no API key
        return {
            'vendor': 'SAMPLE STORE',
            'items': [
                {'quantity': '1', 'name': 'Sample Item 1', 'itemNumber': '001', 'price': '10.99'},
                {'quantity': '2', 'name': 'Sample Item 2', 'itemNumber': '002', 'price': '5.50'}
            ]
        }
    
    # Read and encode image
    with open(image_path, 'rb') as image_file:
        image_content = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Prepare Vision API request
    url = f'https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}'
    
    payload = {
        'requests': [
            {
                'image': {'content': image_content},
                'features': [
                    {'type': 'DOCUMENT_TEXT_DETECTION'}
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Extract text
        if 'responses' in result and len(result['responses']) > 0:
            text_annotations = result['responses'][0].get('textAnnotations', [])
            if text_annotations:
                full_text = text_annotations[0].get('description', '')
                return parse_receipt_text(full_text)
        
        return {'vendor': 'Unknown', 'items': []}
        
    except Exception as e:
        print(f"Error processing with Vision API: {str(e)}")
        return {'vendor': 'Error', 'items': []}

def parse_receipt_text(text):
    """Parse receipt text to extract vendor and items with improved logic for various formats"""
    import re
    
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    
    # Extract vendor - look for store name in first few lines
    vendor = 'Unknown'
    for i, line in enumerate(lines[:15]):
        # Skip very short lines, lines with only numbers/symbols, and common non-vendor words
        if len(line) < 3:
            continue
        if re.match(r'^[\d\s\-\(\)\.\,\:]+$', line):  # Just numbers and punctuation
            continue
        # Expanded list of words to skip
        skip_words = ['receipt', 'tax invoice', 'invoice', 'order', 'sale', 'your', 'card', 'here', 
                      'fenway', 'park', 'welcome', 'thank', 'visit', 'www', 'http', '.com']
        if line.lower() in skip_words or any(skip in line.lower() for skip in skip_words):
            continue
        # Look for lines that are likely business names (usually 2-4 words, many caps, not too long)
        words = line.split()
        if 1 <= len(words) <= 4 and not re.match(r'^\d', line):
            # Check if it has some capital letters and reasonable length
            if any(c.isupper() for c in line) and 3 <= len(line) <= 30:
                # Additional check: make sure it's not a common header phrase
                if not any(word.lower() in ['table', 'server', 'check', 'guest'] for word in words):
                    vendor = line
                    break
    
    # If vendor is still one of the skip words, try to find a better match
    if vendor.lower() in ['card here', 'your', 'card', 'here']:
        for i, line in enumerate(lines[:20]):
            if len(line) >= 5 and 'bar' in line.lower() or 'restaurant' in line.lower() or 'cafe' in line.lower():
                vendor = line
                break
    
    # Common skip words that indicate non-item lines
    skip_keywords = [
        'subtotal', 'sub total', 'total', 'tax', 'gst', 'hst', 'pst', 'payment', 'change',
        'cash', 'credit', 'debit', 'visa', 'mastercard', 'amex', 'american express', 'discover',
        'thank you', 'receipt', 'invoice', 'order', 'balance', 'tender',
        'card#', 'card #', 'auth', 'approval', 'merchant', 'terminal', 'batch',
        'phone', 'address', 'street', 'city', 'zip', 'postal',
        'gratuity', 'grat', 'tip', 'suggested', 'service charge',
        'table', 'server', 'svrck', 'party', 'guest', 'check',
        'book', 'visit', 'welcome', 'cheque', 'event', 'cards', 'express'
    ]
    
    # Parse items - handle both inline and separate-line price formats
    items = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Skip vendor line
        if line == vendor:
            i += 1
            continue
        
        # Skip lines with skip keywords
        if any(keyword in line.lower() for keyword in skip_keywords):
            i += 1
            continue
        
        # Skip date/time patterns
        if re.search(r'\d{1,2}[:/]\d{1,2}[:/]\d{2,4}', line):
            i += 1
            continue
        
        # Skip very short lines (less than 2 chars)
        if len(line) < 2:
            i += 1
            continue
        
        # Check if this line is just a price (common in restaurant receipts where item and price are on separate lines)
        is_just_price = re.match(r'^\$?\s*(\d+\.\d{2})\s*$', line)
        
        if is_just_price:
            # This is just a price - skip it as it should have been captured with the item above
            i += 1
            continue
        
        # Pattern 1: Quantity + Item + Price on same line (e.g., "2 APPLES $3.99" or "2 APPLES 3.99")
        match = re.match(r'^(\d+)\s+(.+?)\s+(\d+\.\d{2})\s*$', line)
        if match:
            quantity = match.group(1)
            name = match.group(2).strip()
            price = match.group(3)
            
            # Clean up name
            name = re.sub(r'#\s*\d+', '', name)
            name = re.sub(r'SKU:?\s*\d+', '', name, flags=re.IGNORECASE)
            name = re.sub(r'\s+', ' ', name).strip()
            
            if len(name) >= 2 and not re.match(r'^[\d\s\-\.\,\$]+$', name):
                items.append({
                    'quantity': quantity,
                    'name': name,
                    'itemNumber': '',
                    'price': price
                })
            i += 1
            continue
        
        # Pattern 2: Quantity + Item on one line, price on next line (common in restaurant receipts)
        # e.g., "1 HARPOON IPA DRAFT" followed by "9.00"
        match = re.match(r'^(\d+)\s+(.+)$', line)
        if match and i + 1 < len(lines):
            quantity = match.group(1)
            name = match.group(2).strip()
            
            # Check if next line is a price
            next_line = lines[i + 1]
            price_match = re.match(r'^\$?\s*(\d+\.\d{2})\s*$', next_line)
            
            if price_match:
                price = price_match.group(1)
                
                # Clean up name
                name = re.sub(r'#\s*\d+', '', name)
                name = re.sub(r'SKU:?\s*\d+', '', name, flags=re.IGNORECASE)
                name = re.sub(r'\s+', ' ', name).strip()
                
                # Make sure name doesn't contain skip keywords
                if not any(keyword in name.lower() for keyword in skip_keywords):
                    if len(name) >= 2 and not re.match(r'^[\d\s\-\.\,\$]+$', name):
                        items.append({
                            'quantity': quantity,
                            'name': name,
                            'itemNumber': '',
                            'price': price
                        })
                i += 2  # Skip both lines
                continue
        
        # Pattern 3: Item with price on same line (no quantity)
        # e.g., "CHEESE BURGER 17.00" or "CHEESE BURGER $17.00"
        match = re.match(r'^(.+?)\s+\$?\s*(\d+\.\d{2})\s*$', line)
        if match:
            name = match.group(1).strip()
            price = match.group(2)
            
            # Skip if name contains skip keywords
            if any(keyword in name.lower() for keyword in skip_keywords):
                i += 1
                continue
            
            # Clean up name
            name = re.sub(r'^\d+\s+', '', name)  # Remove leading quantity if captured
            name = re.sub(r'#\s*\d+', '', name)
            name = re.sub(r'SKU:?\s*\d+', '', name, flags=re.IGNORECASE)
            name = re.sub(r'\s+', ' ', name).strip()
            
            if len(name) >= 2 and not re.match(r'^[\d\s\-\.\,\$]+$', name):
                items.append({
                    'quantity': '1',
                    'name': name,
                    'itemNumber': '',
                    'price': price
                })
            i += 1
            continue
        
        # If we got here, skip this line
        i += 1
    
    # If no items found, return a default item
    if not items:
        items = [{
            'quantity': '1',
            'name': 'No items detected - please add manually',
            'itemNumber': '',
            'price': '0.00'
        }]
    
    return {
        'vendor': vendor,
        'items': items
    }

@app.route('/api/process-receipt', methods=['POST'])
def process_receipt():
    """Process uploaded receipt image"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Process receipt
        result = process_receipt_with_vision_api(filepath)
        
        # Add image URL
        result['imageUrl'] = f'/uploads/{filename}'
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(UPLOAD_FOLDER, filename)

# Serve React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
