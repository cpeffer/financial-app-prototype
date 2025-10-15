# Receipt Tracker - Flask Prototype with OCR

A Flask-based receipt tracking application that automatically extracts itemized data from receipt images using Google's Gemini Vision API.

## Features

- **Automatic OCR**: Upload a receipt photo and the app automatically extracts all line items, prices, vendor, date, and totals
- **User Authentication**: Email/password registration and login
- **Image Upload**: Upload receipt images from photo library or camera
- **Smart Data Extraction**: AI-powered extraction of:
  - Vendor/store name
  - Purchase date
  - Individual line items with quantities and prices
  - Subtotal, tax, and total amounts
- **Review & Edit**: Review and edit extracted data before saving
- **Itemized View**: See detailed line-by-line breakdown of each receipt
- **Expense List**: View all logged expenses in chronological order
- **Spending Summary**: Dashboard with spending breakdown by category for the current month
- **Expense Management**: View detailed expense information and delete expenses

## Setup Instructions

### 1. Get a Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 2. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set Your API Key

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
GEMINI_API_KEY=your-api-key-here
```

### 4. Run the Application

```bash
python app.py
```

Or use the startup script:
```bash
./run.sh
```

### 5. Access the App

Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Register/Login**: Create an account or log in with existing credentials
2. **Add Expense**: Click "Add Expense" and upload a receipt image
3. **Auto-Extract**: The app will automatically extract all items and costs from the receipt
4. **Review**: Review and edit the extracted data on the review page
5. **Save**: Confirm to save the expense with all itemized data
6. **View Details**: Click on any expense to see the full itemized breakdown

## How OCR Works

The application uses Google's Gemini Vision API to analyze receipt images and extract structured data including:
- Store name and purchase date
- Individual items with names, quantities, and prices
- Subtotal, tax, and total amounts

The extracted data is presented in an editable review form where you can make corrections before saving.

## Project Structure

```
financial-app-prototype/
├── app.py                 # Main Flask application with OCR logic
├── requirements.txt       # Python dependencies
├── expenses.db           # SQLite database (created on first run)
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── add_expense.html
│   ├── review_expense.html  # NEW: Review extracted data
│   ├── expenses.html
│   └── view_expense.html    # Updated: Shows itemized data
└── static/              # Static files
    ├── css/
    │   └── style.css
    └── uploads/         # Receipt images (created on first run)
```

## Database Schema

### Users Table
- id, email, password, created_at

### Expenses Table
- id, user_id, vendor, amount, date, category, image_path, created_at

### Line Items Table (NEW)
- id, expense_id, item_name, quantity, unit_price, total_price

## Categories

- Groceries
- Dining
- Transport
- Shopping
- Entertainment
- Utilities
- Healthcare
- Other

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Authentication**: Werkzeug password hashing
- **OCR**: Google Gemini Vision API

## Notes

This is a prototype application for demonstration purposes. It includes:
- AI-powered receipt OCR with Google Gemini
- Itemized receipt data extraction
- Review and edit functionality
- Basic security features (password hashing, session management)
- Simple SQLite database for data persistence
- Responsive design for mobile and desktop
- Image upload with file validation

## Troubleshooting

**No OCR extraction?**
- Make sure your `GEMINI_API_KEY` is set correctly
- Check that the image is clear and readable
- Verify you have internet connectivity

**API errors?**
- Check your API key is valid
- Ensure you haven't exceeded your API quota
- Try with a clearer receipt image

For production use, consider adding:
- HTTPS encryption
- More robust authentication (OAuth, 2FA)
- PostgreSQL instead of SQLite
- Database migrations
- Input validation and sanitization
- Rate limiting
- Automated testing
- Error logging and monitoring
