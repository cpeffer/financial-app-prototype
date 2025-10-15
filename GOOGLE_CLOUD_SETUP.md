# Setting Up Google Cloud Vision API for Receipt OCR

## Why You Need This

The receipt itemizer app uses Google Cloud Vision API to extract text from receipt images. Without it, the app can only use mock/sample data and won't actually read your receipts.

## Step-by-Step Setup

### 1. Create a Google Cloud Account

1. Go to https://console.cloud.google.com
2. Sign in with your Google account
3. Accept the terms of service
4. Google offers $300 in free credits for new accounts

### 2. Create a New Project

1. Click on the project dropdown at the top of the page
2. Click "New Project"
3. Name it something like "receipt-itemizer"
4. Click "Create"

### 3. Enable the Vision API

1. In the search bar at the top, type "Vision API"
2. Click on "Cloud Vision API"
3. Click the "Enable" button
4. Wait for it to enable (takes a few seconds)

### 4. Create an API Key

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "API Key"
3. Copy the API key that appears (it looks like: `AIzaSyB...`)
4. (Optional but recommended) Click "Restrict Key":
   - Under "API restrictions", select "Restrict key"
   - Select only "Cloud Vision API"
   - Click "Save"

### 5. Set Up the API Key in Your App

**Option A: Environment Variable (Recommended for testing)**

```bash
# On Mac/Linux:
export GOOGLE_VISION_API_KEY='AIzaSyB...'

# On Windows (Command Prompt):
set GOOGLE_VISION_API_KEY=AIzaSyB...

# On Windows (PowerShell):
$env:GOOGLE_VISION_API_KEY='AIzaSyB...'
```

**Option B: .env File (Recommended for development)**

1. Create a `.env` file in the project root:
```bash
cd /path/to/financial-app-prototype
nano .env
```

2. Add this line:
```
GOOGLE_VISION_API_KEY=AIzaSyB...
```

3. Save and close

4. Install python-dotenv (already in requirements.txt):
```bash
source venv/bin/activate
pip install python-dotenv
```

### 6. Test Your Setup

Run the test script with one of your receipt images:

```bash
cd /path/to/financial-app-prototype
source venv/bin/activate
export GOOGLE_VISION_API_KEY='your-key-here'  # if not using .env
python test_receipt.py examples/receipt_1.jpeg
```

You should see:
- ✅ Extracted text from the receipt
- ✅ Parsed vendor name
- ✅ List of items with quantities and prices

## Using the Web App

Once the API key is set up:

1. Make sure the environment variable is set or .env file exists
2. Start the backend:
```bash
source venv/bin/activate
python app.py
```

3. Start the frontend (in another terminal):
```bash
cd frontend
npm start
```

4. Open http://localhost:3000
5. Upload a receipt image
6. The app will now use real OCR instead of mock data!

## Costs

Google Cloud Vision API pricing:
- First 1,000 requests per month: **FREE**
- After that: ~$1.50 per 1,000 images

For this prototype with occasional testing, you'll likely stay in the free tier.

## Troubleshooting

### "API key not found" error
- Make sure you exported the environment variable in the same terminal where you run the app
- OR make sure your .env file exists and is in the project root
- Restart your Flask server after setting the variable

### "API not enabled" error
- Go back to Google Cloud Console
- Make sure Vision API is enabled for your project

### "Quota exceeded" error
- You've used your free credits or exceeded the free tier
- Check your quota at: https://console.cloud.google.com/apis/api/vision.googleapis.com/quotas

### API key not working
- Make sure you copied the entire key (no spaces)
- Check if you restricted the key - make sure Vision API is allowed
- Try creating a new unrestricted key for testing

## Alternative: Use Mock Data

If you don't want to set up Google Cloud:
- The app will work with sample/mock data
- It won't actually read your receipts
- Good for testing the UI and edit features
- Not useful for real receipt processing

## Security Note

⚠️ **Never commit your API key to Git!**
- The `.env` file is already in `.gitignore`
- Don't hardcode the key in your code
- Don't share your API key publicly
- Rotate your key if it's accidentally exposed

## Next Steps

After setting up the API:
1. Test with the receipts in the `examples/` folder
2. Try uploading your own receipt photos
3. If parsing isn't accurate, we can fine-tune the parsing logic
4. The app learns which lines are items vs. headers/footers
