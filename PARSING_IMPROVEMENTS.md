# Receipt Parsing Improvements

## What Was Changed

The receipt parsing logic has been significantly enhanced to better handle real-world receipt formats.

## Key Improvements

### 1. Better Vendor Detection
- Scans first 10 lines for store name
- Skips common header words (receipt, invoice, etc.)
- Ignores lines with only numbers/dates

### 2. Smarter Item Detection
- **Skip Keywords**: Automatically filters out:
  - Subtotals, totals, tax lines
  - Payment information (cash, credit, card numbers)
  - Footer text (thank you, address, phone)
  - Non-item metadata

### 3. Multiple Price Pattern Recognition
- Matches: `$12.99`, `12.99`, `12,99` (European format)
- Handles negative amounts: `$12.99-`, `-12.99`
- Uses last price on line (extended price vs unit price)

### 4. Quantity Detection
- Identifies quantities at start of line: `2 APPLES $3.99`
- Validates quantity is reasonable (<100)
- Defaults to `1` if not found

### 5. Item Number Extraction
- Multiple patterns supported:
  - `#123` or `# 123`
  - `SKU: 456` or `SKU 456`
  - `012345` (long number at start)
  - `(789)` (in parentheses)

### 6. Name Cleaning
- Removes extracted prices from name
- Removes item numbers from name
- Cleans up extra whitespace
- Filters out invalid names (too short, all numbers, etc.)

### 7. Validation
- Skips lines that are too short
- Ignores lines with only special characters
- Returns friendly message if no items detected

## Before vs After

### Before (Basic Regex)
```
Vendor: WHOLE FOODS MARKET
Items:
1. "BANANAS $1.98 SUBTOTAL $38.42"
2. "TAX $2.69"
```

### After (Improved Parsing)
```
Vendor: WHOLE FOODS MARKET
Items:
1. Qty: 2 | ORGANIC BANANAS        | #      | $1.98
2. Qty: 1 | GREEK YOGURT           | #789   | $5.99
3. Qty: 1 | SOURDOUGH BREAD        | #      | $4.50
4. Qty: 3 | AVOCADOS               | #456   | $5.97
5. Qty: 1 | SPARKLING WATER 12PK   | #      | $6.99
6. Qty: 1 | OLIVE OIL EXTRA VIRGIN | #      | $12.99
```

## Testing Your Receipts

Use the test script to see how your receipts are parsed:

```bash
# Make sure you have your API key set
export GOOGLE_VISION_API_KEY='your-key-here'

# Run the test
python test_receipt.py examples/receipt_1.jpeg
```

This will show you:
1. The raw OCR text extracted
2. The parsed vendor name
3. All detected items with details
4. A JSON file with the results

## Common Receipt Formats Supported

### Grocery Stores
```
WHOLE FOODS
2 BANANAS                    $1.98
MILK 2% SKU:123             $4.99
```

### Restaurants
```
THE BURGER JOINT
1 CHEESEBURGER              $12.99
2 FRIES                      $6.00
```

### Retail
```
TARGET
QTY ITEM                    PRICE
2   NOTEBOOK #789          $5.98
1   PEN SET (456)          $3.99
```

### Hardware Stores
```
HOME DEPOT
012345 HAMMER               $24.99
098765 NAILS BOX            $8.99
```

## Still Having Issues?

If items aren't being detected correctly:

1. **Check the OCR text**: Run `test_receipt.py` to see what Vision API extracts
2. **Look for patterns**: Are items in an unusual format?
3. **Adjust skip keywords**: Add common words from your receipts to the `skip_keywords` list in `app.py`
4. **Manual editing**: The UI allows you to add/edit any items that weren't detected

## Fine-Tuning for Your Receipts

If you have specific receipt formats that aren't working:

1. Run `test_receipt.py` on your receipt
2. Look at the raw OCR text in the output
3. Open `app.py` and modify the `parse_receipt_text()` function
4. Add your specific patterns to the regex patterns
5. Test again

### Example: Adding a Custom Pattern

If your receipts have items like `ITEM: ABC - $12.99`:

```python
# In parse_receipt_text() function, add to item_num_patterns:
item_num_patterns = [
    r'#\s*(\d+)',
    r'SKU:?\s*(\d+)',
    r'^(\d{5,})\s',
    r'\((\d+)\)',
    r'ITEM:\s*([A-Z0-9]+)',  # <-- Add this line
]
```

## Next Steps

1. Set up Google Cloud Vision API (see GOOGLE_CLOUD_SETUP.md)
2. Test with your example receipts
3. Review the parsed results
4. Fine-tune if needed
5. Use the web app to process receipts with real OCR
