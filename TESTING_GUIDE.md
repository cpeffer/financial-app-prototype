# Testing Your Receipts - Quick Guide

## Overview

This guide shows you how to test the receipt itemizer with your own receipt images to verify the parsing works correctly.

## Prerequisites

✅ Python virtual environment activated
✅ Google Cloud Vision API key obtained
✅ Receipt images ready to test (in `examples/` folder)

## Step-by-Step Testing Process

### 1. Set Up Your API Key

Choose one method:

**Method A: .env file (recommended)**
```bash
# Create .env file in project root
echo "GOOGLE_VISION_API_KEY=AIzaSyB..." > .env
```

**Method B: Environment variable**
```bash
export GOOGLE_VISION_API_KEY='AIzaSyB...'
```

Don't have an API key yet? See [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md)

### 2. Test a Single Receipt

```bash
# Activate virtual environment
source venv/bin/activate

# Test one receipt
python test_receipt.py examples/receipt_1.jpeg
```

**What you'll see:**
```
EXTRACTED TEXT FROM OCR
======================================================================
WHOLE FOODS MARKET
123 Main Street
2 ORGANIC BANANAS               $1.98
...
======================================================================

PARSED RECEIPT DATA
======================================================================
Vendor: WHOLE FOODS MARKET

Items found: 6

Item Details:
----------------------------------------------------------------------
#    Qty   Name                                Item #     Price
----------------------------------------------------------------------
1    2     ORGANIC BANANAS                     #          $  1.98
2    1     GREEK YOGURT                        #789       $  5.99
...
======================================================================

✅ Results saved to: examples/receipt_1_parsed.json
```

### 3. Test All Receipts

```bash
python batch_test.py
```

**What you'll see:**
```
[1/3] Processing: examples/receipt_1.jpeg
----------------------------------------------------------------------
✅ Vendor: WHOLE FOODS MARKET
✅ Items found: 6
   1. 2x ORGANIC BANANAS                  $1.98
   2. 1x GREEK YOGURT                     $5.99
   ... and 4 more items

[2/3] Processing: examples/receipt_2.jpeg
...

BATCH PROCESSING SUMMARY
======================================================================
Total receipts processed: 3
Total items extracted: 18

✅ Detailed results saved to: batch_test_results.json
```

### 4. Review the Results

Check the JSON files created:
```bash
# View parsed results
cat examples/receipt_1_parsed.json

# View batch results
cat batch_test_results.json
```

### 5. Verify Accuracy

For each receipt, check:
- ✅ Is the vendor name correct?
- ✅ Are all items detected?
- ✅ Are quantities correct?
- ✅ Are prices accurate?
- ✅ Are item numbers extracted?
- ✅ Are subtotals/tax/totals excluded?

### 6. Use the Web App

Once testing looks good:

```bash
# Terminal 1 - Start backend
source venv/bin/activate
python app.py

# Terminal 2 - Start frontend
cd frontend
npm start
```

Open http://localhost:3000 and upload your receipts!

## Troubleshooting

### Problem: "No API key found"
**Solution:** 
```bash
# Check if .env exists
ls -la .env

# Or set environment variable
export GOOGLE_VISION_API_KEY='your-key-here'
```

### Problem: "No items detected"
**Solution:**
1. Check the "EXTRACTED TEXT FROM OCR" section
2. Is the text extracted correctly?
3. Does it look like a receipt?
4. If OCR text is good but parsing fails, the receipt format might need custom patterns

### Problem: Wrong items detected
**Solution:**
1. Look at the raw OCR text
2. Identify the pattern of your items
3. Modify `app.py` → `parse_receipt_text()` function
4. Add your pattern to `item_num_patterns` or adjust skip keywords

### Problem: Prices are wrong
**Solution:**
1. Check if receipt has multiple prices per line
2. Parser uses LAST price on line (extended price)
3. If your format is different, adjust the price extraction logic

## Common Receipt Issues

### Issue: European number format (12,99 instead of 12.99)
The parser handles this! It converts commas to periods.

### Issue: Items without prices on same line
Example:
```
ORGANIC BANANAS
   2 @ $0.99                    $1.98
```
The parser will still find the price ($1.98).

### Issue: Multi-line item descriptions
Example:
```
PREMIUM ORGANIC
WHOLE GRAIN BREAD               $4.99
```
This might be detected as 2 items. You can manually merge in the UI.

### Issue: Item codes without keywords
Example: `012345 APPLE $1.99`
The parser detects long numbers (5+ digits) at line start as item codes.

## Testing Checklist

Before deploying to production:

- [ ] Tested with at least 5 different receipts
- [ ] Verified vendor names are correct
- [ ] Checked item detection accuracy >80%
- [ ] Confirmed prices are accurate
- [ ] Tested in web app UI
- [ ] Verified export to CSV works
- [ ] Tested copy to clipboard
- [ ] Confirmed edit functionality works

## Tips for Better Results

### 1. Receipt Photo Quality
- Take photo in good lighting
- Ensure receipt is flat (not crumpled)
- Include entire receipt in frame
- Avoid shadows and glare
- Higher resolution = better OCR

### 2. Supported Formats
- JPEG, PNG, PDF (converted to image)
- Printed receipts work better than handwritten
- Thermal receipts work well if not faded
- Clear, high-contrast text preferred

### 3. Fine-Tuning
If a specific store's receipts don't parse well:
1. Process 2-3 receipts from that store
2. Note the patterns in the JSON output
3. Add store-specific patterns to `app.py`
4. Re-test to verify improvement

## Example Test Session

```bash
# Complete test workflow
cd /Users/cpeffer1/Desktop/financial-app-prototype

# Activate environment
source venv/bin/activate

# Set API key (if not using .env)
export GOOGLE_VISION_API_KEY='AIzaSyB...'

# Test individual receipts
python test_receipt.py examples/receipt_1.jpeg
python test_receipt.py examples/receipt_2.jpeg

# Test all at once
python batch_test.py

# Review results
cat batch_test_results.json | python -m json.tool | head -50

# If results look good, start the app
python app.py  # In terminal 1
cd frontend && npm start  # In terminal 2

# Open browser and test!
```

## Success Criteria

✅ **Good parsing** = 80%+ of items correctly extracted
✅ **Excellent parsing** = 95%+ of items correctly extracted
✅ **Perfect parsing** = 100% of items correctly extracted (rare, but possible!)

Remember: The UI allows manual editing, so 80%+ is acceptable for V1!

## Need Help?

1. Check [PARSING_IMPROVEMENTS.md](PARSING_IMPROVEMENTS.md) for technical details
2. Review [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md) for API setup
3. Read [IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md) for overview
4. Check the JSON output files for debugging

---

**Happy testing! 🧾**
