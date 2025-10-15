#!/usr/bin/env python3
"""
Test script to process receipt images and see extraction results
Usage: python test_receipt.py <image_path>
"""

import sys
import os
import base64
import requests
import json

# Add current directory to path
sys.path.insert(0, '.')
from app import parse_receipt_text

def process_with_vision_api(image_path, api_key):
    """Process receipt using Google Cloud Vision API"""
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        return None
    
    # Read and encode image
    with open(image_path, 'rb') as image_file:
        image_content = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Prepare Vision API request
    url = f'https://vision.googleapis.com/v1/images:annotate?key={api_key}'
    
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
    
    print(f"Processing {image_path} with Google Cloud Vision API...")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Extract text
        if 'responses' in result and len(result['responses']) > 0:
            text_annotations = result['responses'][0].get('textAnnotations', [])
            if text_annotations:
                full_text = text_annotations[0].get('description', '')
                return full_text
        
        return None
        
    except Exception as e:
        print(f"Error processing with Vision API: {str(e)}")
        return None

def main():
    api_key = os.getenv('GOOGLE_VISION_API_KEY', '')
    
    if len(sys.argv) < 2:
        print("Usage: python test_receipt.py <image_path>")
        print("\nExample:")
        print("  python test_receipt.py examples/receipt_1.jpeg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not api_key:
        print("="*70)
        print("⚠️  WARNING: No Google Cloud Vision API key found")
        print("="*70)
        print("\nTo test with real OCR, you need to:")
        print("1. Get a Google Cloud Vision API key from:")
        print("   https://console.cloud.google.com/apis/credentials")
        print("2. Set the environment variable:")
        print("   export GOOGLE_VISION_API_KEY='your-key-here'")
        print("\nContinuing without OCR will not extract text from image.")
        print("="*70)
        sys.exit(1)
    
    # Process with Vision API
    extracted_text = process_with_vision_api(image_path, api_key)
    
    if not extracted_text:
        print("Failed to extract text from image")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("EXTRACTED TEXT FROM OCR")
    print("="*70)
    print(extracted_text)
    print("="*70)
    
    # Parse the text
    parsed_result = parse_receipt_text(extracted_text)
    
    print("\n" + "="*70)
    print("PARSED RECEIPT DATA")
    print("="*70)
    print(f"\nVendor: {parsed_result['vendor']}")
    print(f"\nItems found: {len(parsed_result['items'])}")
    print("\nItem Details:")
    print("-" * 70)
    print(f"{'#':<4} {'Qty':<5} {'Name':<35} {'Item #':<10} {'Price':>8}")
    print("-" * 70)
    for i, item in enumerate(parsed_result['items'], 1):
        print(f"{i:<4} {item['quantity']:<5} {item['name']:<35} {item['itemNumber']:<10} ${item['price']:>7}")
    print("="*70)
    
    # Save result to JSON for inspection
    output_file = image_path.replace('.jpeg', '_parsed.json').replace('.png', '_parsed.json').replace('.jpg', '_parsed.json')
    with open(output_file, 'w') as f:
        json.dump({
            'vendor': parsed_result['vendor'],
            'items': parsed_result['items'],
            'raw_text': extracted_text
        }, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")

if __name__ == '__main__':
    main()
