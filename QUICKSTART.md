# Receipt Itemizer - Quick Start Guide

## What You've Built

A fully functional web application that:
- Uploads receipt images
- Extracts vendor name and line items using OCR
- Allows editing of all extracted data
- Exports to CSV or clipboard

## Current Status

✅ **Backend (Flask)**: Running on http://localhost:5000
✅ **Frontend (React)**: Running on http://localhost:3000

Both servers are currently running and ready to use!

## How to Use the App

1. **Open your browser** to: http://localhost:3000

2. **Upload a receipt**:
   - Click "Choose Receipt Image"
   - Select any receipt photo (JPEG, PNG, etc.)
   - Click "Process Receipt"

3. **Review & Edit**:
   - The app will show your receipt image on the left
   - Extracted data appears on the right
   - Edit any field by clicking on it
   - Add items with "+ Add Item"
   - Delete items with the "×" button

4. **Export your data**:
   - Click "Export to CSV" for a downloadable file
   - Click "Copy to Clipboard" to paste elsewhere
   - Click "New Receipt" to start over

## Important Notes

### OCR Processing
The app currently uses **mock data** because no Google Cloud Vision API key is configured. To enable real OCR:

1. Get a Google Cloud Vision API key:
   - Go to https://console.cloud.google.com
   - Create a project and enable Vision API
   - Create an API key

2. Create a `.env` file in the project root:
   ```
   GOOGLE_VISION_API_KEY=your_actual_api_key_here
   ```

3. Restart the Flask server

### Running the Servers Again

If you stopped the servers, restart them with:

**Option 1: Use the start script**
```bash
./start.sh
```

**Option 2: Start manually**

Terminal 1 (Backend):
```bash
source venv/bin/activate
python app.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm start
```

## Project Structure

```
financial-app-prototype/
├── app.py                 # Flask backend (port 5000)
├── requirements.txt       # Python dependencies
├── static/uploads/        # Receipt images stored here
├── frontend/
│   ├── src/
│   │   ├── App.js        # Main React component
│   │   └── App.css       # Styling
│   └── package.json      # Node dependencies
└── README.md             # Full documentation
```

## Next Steps

1. **Test with Real Receipts**: Try uploading various receipt images
2. **Configure OCR**: Set up Google Cloud Vision API for real processing
3. **Customize Styling**: Modify `frontend/src/App.css`
4. **Add Features**: See README.md for enhancement ideas

## Troubleshooting

**Frontend won't start?**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

**Backend errors?**
```bash
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Port already in use?**
- Backend: Change port in `app.py` (line with `app.run()`)
- Frontend: Set `PORT=3001` before running `npm start`

## API Endpoint

The backend exposes one main endpoint:

**POST** `/api/process-receipt`
- Accepts: multipart/form-data with 'file' field
- Returns: JSON with vendor, items array, and imageUrl

Example response:
```json
{
  "vendor": "SAMPLE STORE",
  "items": [
    {
      "quantity": "1",
      "name": "Sample Item",
      "itemNumber": "001",
      "price": "10.99"
    }
  ],
  "imageUrl": "/uploads/receipt.jpg"
}
```

## Production Deployment

For production, you'll need to:
1. Build the React app: `cd frontend && npm run build`
2. Deploy backend to Heroku, Railway, or similar
3. Deploy frontend to Vercel, Netlify, or serve from Flask
4. Set environment variables in production
5. Use a production WSGI server (gunicorn) instead of Flask dev server

See README.md for detailed deployment instructions.

---

**Congratulations!** You've successfully built a receipt itemizer prototype according to the PRD. The app is now running and ready to process receipts.
