# Quick Start Guide

## Getting Started in 4 Steps

### 1. Get Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

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

Then run:
```bash
python app.py
```

Or update `run.sh` to include your API key:
```bash
#!/bin/bash
export GEMINI_API_KEY="your-api-key-here"
source venv/bin/activate
python app.py
```

### 4. Access the Application
Open your browser and go to: **http://localhost:5000**

## Start Using

1. **Register** a new account with your email and password
2. **Login** with your credentials
3. **Upload a receipt** - Take a photo or upload an image
4. **Magic happens!** - The app automatically extracts all items and costs
5. **Review & edit** - Check the extracted data and make any corrections
6. **Save** - Your expense is saved with full itemized breakdown
7. **View dashboard** - See spending summary by category

## Features at a Glance

✅ **AI-Powered OCR** - Automatically extracts items and prices from receipts  
✅ **Itemized Breakdown** - See individual line items with quantities and costs  
✅ **Smart Extraction** - Recognizes vendor, date, subtotal, tax, and total  
✅ **Review & Edit** - Verify and correct extracted data before saving  
✅ **User Authentication** - Secure registration & login  
✅ **Spending Dashboard** - Visual breakdown by category  
✅ **Mobile-Responsive** - Works on any device  

## How It Works

1. **Upload** - Take a photo or upload a receipt image
2. **AI Analysis** - Google Gemini Vision API reads the receipt
3. **Extraction** - All items, prices, vendor, and date are extracted
4. **Review** - You get a chance to review and edit the data
5. **Save** - Expense is saved with full itemized breakdown

## Example Receipt Data Extracted

```json
{
  "vendor": "Whole Foods Market",
  "date": "2025-10-15",
  "items": [
    {"name": "Organic Bananas", "quantity": 2, "unit_price": 1.99, "total": 3.98},
    {"name": "Almond Milk", "quantity": 1, "unit_price": 4.99, "total": 4.99},
    {"name": "Sourdough Bread", "quantity": 1, "unit_price": 5.49, "total": 5.49}
  ],
  "subtotal": 14.46,
  "tax": 1.16,
  "total": 15.62
}
```

## Default Categories
- Groceries
- Dining
- Transport
- Shopping
- Entertainment
- Utilities
- Healthcare
- Other

## Technical Details
- **Framework**: Flask (Python)
- **OCR**: Google Gemini Vision API
- **Database**: SQLite (auto-created on first run)
- **UI**: Bootstrap 5
- **Authentication**: Werkzeug password hashing

## Mobile Access

To access from your phone on the same network:
1. Find your computer's IP address
2. Open `http://YOUR_IP_ADDRESS:5000` on your phone's browser
3. Use your phone's camera to take receipt photos!

Example: `http://192.168.1.100:5000`

## Troubleshooting

**API Key Issues?**
```bash
# Make sure your API key is set
echo $GEMINI_API_KEY

# Set it if empty
export GEMINI_API_KEY="your-key-here"
```

**OCR Not Working?**
- Verify your API key is correct
- Check internet connection
- Try with a clearer receipt image
- Ensure the receipt has good lighting and isn't blurry

**Port already in use?**
```bash
# Kill the process using port 5000
lsof -ti:5000 | xargs kill -9
```

**Database issues?**
```bash
# Delete and recreate database
rm expenses.db
python app.py
```

**Missing dependencies?**
```bash
pip install --upgrade -r requirements.txt
```

## Tips for Best Results

📸 **Take Clear Photos**
- Good lighting
- Receipt flat and in focus
- Entire receipt visible in frame
- No shadows or glare

🎯 **Best Receipt Types**
- Printed thermal receipts (most common)
- Credit card receipts
- Restaurant bills
- Grocery store receipts

## What's Next?

After you have some expenses logged:
- Check your **Dashboard** for spending breakdown
- View **All Expenses** to see your history
- Click any expense to see **itemized details**
- Delete expenses you don't need

## API Costs

Google Gemini API has a generous free tier:
- Free tier: 15 requests per minute
- Great for prototyping and personal use
- Check [Google AI Studio](https://aistudio.google.com/) for current pricing

Enjoy your smart receipt tracking! 🎉
