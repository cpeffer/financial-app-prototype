# Receipt Itemizer - V1 Prototype

A web-based application that automatically itemizes receipts from uploaded images. Users can upload a receipt photo, and the app extracts the vendor name and individual line items (quantity, name, item number, and price).

## Features

- **Anonymous Receipt Upload**: Simple drag-and-drop interface for receipt images
- **Automated OCR Processing**: Uses Google Cloud Vision API to extract text from receipts
- **Smart Parsing**: Automatically identifies vendor name and itemizes products
- **Review & Edit Interface**: Two-panel view showing original receipt alongside extracted data
- **Editable Fields**: Modify vendor name, quantities, item names, numbers, and prices
- **Add/Delete Items**: Manually adjust the item list as needed
- **Data Export**: Export to CSV or copy to clipboard

## Tech Stack

**Frontend:**
- React
- Axios for API calls
- Modern CSS with responsive design

**Backend:**
- Python 3.x
- Flask web framework
- Flask-CORS for cross-origin requests
- Google Cloud Vision API for OCR (optional - works with mock data if not configured)

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Clone the repository and navigate to project directory:
```bash
cd financial-app-prototype
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Set up Google Cloud Vision API:
   - Create a Google Cloud project
   - Enable the Vision API
   - Create an API key
   - Copy `.env.example` to `.env` and add your API key

5. Start the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

1. Open your browser to `http://localhost:3000`
2. Click "Choose Receipt Image" and select a receipt photo
3. Click "Process Receipt" to upload and analyze
4. Review the extracted vendor name and items
5. Edit any fields as needed
6. Add or delete items using the buttons
7. Export your data using "Export to CSV" or "Copy to Clipboard"
8. Click "New Receipt" to process another receipt

## Setting Up Google Cloud Vision API

The app uses Google Cloud Vision API for OCR. Without it, only mock data will be returned.

**Quick Setup:**

1. Get a Google Cloud Vision API key (see [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md) for detailed instructions)
2. Create a `.env` file in the project root:
   ```
   GOOGLE_VISION_API_KEY=your_api_key_here
   ```
3. Restart the Flask server

**Test with example receipts:**
```bash
source venv/bin/activate
python test_receipt.py examples/receipt_1.jpeg
```

This will show you the extracted text and parsed items.

See [GOOGLE_CLOUD_SETUP.md](GOOGLE_CLOUD_SETUP.md) for complete setup instructions.

## API Endpoints

### POST `/api/process-receipt`
Upload and process a receipt image.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
```json
{
  "vendor": "Store Name",
  "items": [
    {
      "quantity": "1",
      "name": "Item Name",
      "itemNumber": "12345",
      "price": "9.99"
    }
  ],
  "imageUrl": "/uploads/filename.jpg"
}
```

## Project Structure

```
financial-app-prototype/
├── app.py                  # Flask backend application
├── requirements.txt        # Python dependencies
├── static/
│   └── uploads/           # Uploaded receipt images
├── frontend/
│   ├── src/
│   │   ├── App.js        # Main React component
│   │   └── App.css       # Styling
│   ├── public/
│   └── package.json      # Node dependencies
└── README.md
```

## Notes

- The app works without a Google Cloud Vision API key using mock data
- No database is used - data exists only during the session
- No user authentication - designed for quick prototyping
- Uploaded images are stored in `static/uploads/` directory

## Future Enhancements (Post-V1)

- AWS Textract or Azure Form Recognizer integration
- User accounts and receipt history
- Cloud deployment (Heroku, Vercel, Netlify)
- Mobile app version
- Receipt categorization and spending analytics

## License

MIT

