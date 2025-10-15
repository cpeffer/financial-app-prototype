# Receipt Tracker - Demo Guide

## What This App Does

This application uses AI to automatically read receipts and extract itemized data. Upload a photo of any receipt, and the app will:

1. ✅ Identify the store/vendor name
2. ✅ Extract the purchase date
3. ✅ List every item purchased
4. ✅ Show quantities and individual prices
5. ✅ Calculate subtotal, tax, and total
6. ✅ Let you review and edit before saving
7. ✅ Store everything in an organized database

## Live Demo Workflow

### Step 1: Get Your API Key (1 minute)
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Step 2: Start the App (30 seconds)
```bash
export GEMINI_API_KEY="paste-your-key-here"
./run.sh
```

### Step 3: Create Account (30 seconds)
1. Open http://localhost:5000
2. Click "Register here"
3. Enter email and password
4. Click "Register"
5. Login with your credentials

### Step 4: Upload a Receipt (1 minute)
1. Click "Add Expense"
2. Upload or take a photo of a receipt
3. Click "Analyze Receipt"
4. Wait 2-3 seconds for AI analysis

### Step 5: Review Extracted Data (30 seconds)
You'll see:
- Receipt image on the left
- Extracted data on the right:
  - Vendor name (editable)
  - Date (editable)
  - Total amount (editable)
  - Category dropdown
  - **All line items with:**
    - Item name
    - Quantity
    - Unit price
    - Total for each item

### Step 6: Edit & Save (30 seconds)
1. Review the extracted data
2. Fix any errors
3. Select a category
4. Click "Save Expense"

### Step 7: View Dashboard (immediate)
See your spending summary:
- Total spent this month
- Breakdown by category
- Recent expenses list

### Step 8: View Details (immediate)
1. Click "View" on any expense
2. See the full itemized breakdown:
   - Receipt image
   - Complete line-by-line items
   - Quantities and prices
   - Total amount

## Example Receipt Output

**Input:** Photo of a Whole Foods receipt

**Extracted Data:**
```
Vendor: Whole Foods Market
Date: 2025-10-15
Category: Groceries

Items:
1. Organic Bananas (2 lbs)     @ $1.99/lb  = $3.98
2. Almond Milk                 @ $4.99     = $4.99
3. Sourdough Bread             @ $5.49     = $5.49
4. Greek Yogurt (2)            @ $1.99     = $3.98
5. Mixed Greens                @ $3.99     = $3.99

Subtotal: $22.43
Tax:      $1.80
Total:    $24.23
```

## Test Receipt Images

You can test with:
- Grocery store receipts (best results)
- Restaurant bills
- Coffee shop receipts
- Gas station receipts
- Any printed receipt with line items

## Features to Show

### 1. Automatic OCR
- Upload receipt → instant itemization
- No manual data entry needed
- AI reads everything automatically

### 2. Smart Extraction
- Recognizes different receipt formats
- Handles various layouts
- Extracts quantities, prices, and totals

### 3. Review & Edit
- All data is editable
- Fix any OCR errors
- Add missing information

### 4. Itemized Storage
- Every item saved separately
- Full breakdown always available
- Track what you actually bought

### 5. Spending Analytics
- Dashboard with category breakdown
- Monthly totals
- Visual percentage bars

### 6. Mobile Ready
- Works on phones and tablets
- Camera integration for photos
- Responsive design

## Common Use Cases

### Personal Finance
- Track grocery spending
- Monitor dining expenses
- See itemized purchases
- Identify spending patterns

### Small Business
- Track business expenses
- Categorize purchases
- Keep receipt records
- Export for accounting

### Shared Expenses
- Roommates splitting costs
- Family budget tracking
- Item-level expense sharing

## Technical Highlights

### For Developers
- Flask backend (Python)
- Google Gemini Vision API
- SQLite with relational data
- Bootstrap 5 UI
- RESTful design
- Session-based auth

### For Users
- No app store needed
- Works in any browser
- Automatic cloud OCR
- Local data storage
- Fast and responsive

## Limitations (Prototype)

⚠️ This is a prototype, so:
- Single-user focus (multi-tenant needs work)
- SQLite (not for high-scale production)
- Basic auth (no OAuth/2FA)
- API key in environment (needs secrets management)
- No data export yet
- No budget alerts yet

## Next Steps

After the demo:
1. Try different receipt types
2. Build up expense history
3. Check dashboard analytics
4. View itemized breakdowns
5. Test mobile camera capture

## Questions to Answer

**Q: Does it work with all receipts?**
A: Works best with printed receipts. Handwritten ones are harder.

**Q: How accurate is the OCR?**
A: Very accurate with clear photos. Always review before saving.

**Q: Can I edit the extracted data?**
A: Yes! Everything is editable on the review page.

**Q: Is my data secure?**
A: Data stored locally in SQLite. Images saved on server.

**Q: Does it work offline?**
A: No, needs internet for Google Gemini API.

**Q: How much does the API cost?**
A: Free tier: 15 requests/min. Plenty for personal use.

## Demo Script (2 minutes)

1. **Show login** (10 sec)
2. **Upload receipt** (20 sec)
3. **Watch OCR magic** (10 sec)
4. **Show extracted items** (30 sec)
5. **Edit and save** (20 sec)
6. **View dashboard** (20 sec)
7. **Show itemized view** (10 sec)

Total: 2 minutes of pure amazement! 🎉

---

Enjoy demonstrating your AI-powered receipt tracker!
