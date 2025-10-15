# Quick Command Reference

## Setup Commands

```bash
# Install Python dependencies
source venv/bin/activate
pip install -r requirements.txt

# Install Node dependencies
cd frontend
npm install
cd ..

# Set up Google Cloud API key (choose one)
echo "GOOGLE_VISION_API_KEY=your_key_here" > .env
export GOOGLE_VISION_API_KEY='your_key_here'
```

## Testing Commands

```bash
# Activate virtual environment first
source venv/bin/activate

# Test a single receipt
python test_receipt.py examples/receipt_1.jpeg

# Test all receipts in examples/
python batch_test.py

# View test results
cat batch_test_results.json | python -m json.tool
```

## Running the App

```bash
# Option 1: Use the start script
./start.sh

# Option 2: Manual (two terminals)
# Terminal 1:
source venv/bin/activate
python app.py

# Terminal 2:
cd frontend
npm start

# Then open: http://localhost:3000
```

## Debugging Commands

```bash
# Check if API key is set
echo $GOOGLE_VISION_API_KEY

# Test Python imports
source venv/bin/activate
python -c "from app import parse_receipt_text; print('OK')"

# Check backend is running
curl http://localhost:5000/api/process-receipt

# View backend logs
# (logs show in terminal where you ran python app.py)

# Check frontend build
cd frontend
npm run build
```

## Common Tasks

```bash
# Add a new receipt to test
cp ~/Downloads/my_receipt.jpg examples/

# Test the new receipt
python test_receipt.py examples/my_receipt.jpg

# Build frontend for production
cd frontend
npm run build

# Clean and reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## File Locations

```
.env                          # Your API key (don't commit!)
app.py                        # Backend code
frontend/src/App.js          # Frontend code
examples/                     # Test receipt images
static/uploads/              # Uploaded images go here
test_receipt.py              # Single receipt test tool
batch_test.py                # Batch test tool
```

## Troubleshooting

```bash
# Backend won't start
source venv/bin/activate
pip install -r requirements.txt
python app.py

# Frontend won't start
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start

# API key not working
ls -la .env                  # Check .env exists
cat .env                     # Verify key is correct
export GOOGLE_VISION_API_KEY='your_key'  # Try manual export

# Port already in use
lsof -ti:5000 | xargs kill   # Kill process on port 5000
lsof -ti:3000 | xargs kill   # Kill process on port 3000
```

## Documentation Quick Links

- **GOOGLE_CLOUD_SETUP.md** - Get your API key
- **TESTING_GUIDE.md** - Complete testing workflow
- **PARSING_IMPROVEMENTS.md** - Technical details
- **README.md** - Full documentation
- **QUICKSTART.md** - Quick start guide

## One-Line Test

```bash
source venv/bin/activate && export GOOGLE_VISION_API_KEY='your_key' && python batch_test.py
```

Replace `your_key` with your actual API key, or use `.env` file instead.
