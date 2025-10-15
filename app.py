import os
import base64
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json

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
    """Parse receipt text to extract vendor and items"""
    lines = text.strip().split('\n')
    
    # Extract vendor (usually first non-empty line)
    vendor = 'Unknown'
    for line in lines[:5]:  # Check first 5 lines
        if line.strip():
            vendor = line.strip()
            break
    
    # Parse items - look for lines with prices
    items = []
    price_pattern = r'\d+\.\d{2}'
    
    for line in lines:
        # Skip if line is too short or is the vendor line
        if len(line.strip()) < 3 or line.strip() == vendor:
            continue
        
        # Look for price patterns
        import re
        prices = re.findall(r'\$?(\d+\.\d{2})', line)
        
        if prices:
            # Try to extract components
            parts = line.split()
            quantity = '1'
            item_number = ''
            name = line
            price = prices[-1]  # Use last price found
            
            # Try to identify quantity at start
            if parts and parts[0].isdigit():
                quantity = parts[0]
                name = ' '.join(parts[1:])
            
            # Clean up name (remove price)
            name = re.sub(r'\$?\d+\.\d{2}', '', name).strip()
            
            if name:  # Only add if we have a name
                items.append({
                    'quantity': quantity,
                    'name': name,
                    'itemNumber': item_number,
                    'price': price
                })
    
    return {
        'vendor': vendor,
        'items': items if items else [{'quantity': '1', 'name': 'Item', 'itemNumber': '', 'price': '0.00'}]
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
