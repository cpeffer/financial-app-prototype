#!/usr/bin/env python3
"""
Batch test multiple receipt images
Usage: python batch_test.py
"""

import os
import sys
import glob

sys.path.insert(0, '.')
from test_receipt import process_with_vision_api, parse_receipt_text

def main():
    api_key = os.getenv('GOOGLE_VISION_API_KEY', '')
    
    if not api_key:
        print("="*70)
        print("⚠️  ERROR: No Google Cloud Vision API key found")
        print("="*70)
        print("\nPlease set your API key:")
        print("  export GOOGLE_VISION_API_KEY='your-key-here'")
        print("\nSee GOOGLE_CLOUD_SETUP.md for instructions")
        sys.exit(1)
    
    # Find all receipt images
    image_patterns = [
        'examples/*.jpeg',
        'examples/*.jpg',
        'examples/*.png',
    ]
    
    image_files = []
    for pattern in image_patterns:
        image_files.extend(glob.glob(pattern))
    
    # Remove duplicates and sort
    image_files = sorted(list(set(image_files)))
    
    if not image_files:
        print("No receipt images found in examples/ directory")
        sys.exit(1)
    
    print("="*70)
    print(f"Found {len(image_files)} receipt images to process")
    print("="*70)
    
    results = []
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] Processing: {image_path}")
        print("-" * 70)
        
        # Process with Vision API
        extracted_text = process_with_vision_api(image_path, api_key)
        
        if not extracted_text:
            print(f"❌ Failed to extract text")
            continue
        
        # Parse the text
        parsed_result = parse_receipt_text(extracted_text)
        
        print(f"✅ Vendor: {parsed_result['vendor']}")
        print(f"✅ Items found: {len(parsed_result['items'])}")
        
        # Show first 3 items
        for j, item in enumerate(parsed_result['items'][:3], 1):
            print(f"   {j}. {item['quantity']}x {item['name'][:30]:30} ${item['price']}")
        
        if len(parsed_result['items']) > 3:
            print(f"   ... and {len(parsed_result['items']) - 3} more items")
        
        results.append({
            'file': image_path,
            'vendor': parsed_result['vendor'],
            'item_count': len(parsed_result['items']),
            'items': parsed_result['items']
        })
    
    # Summary
    print("\n" + "="*70)
    print("BATCH PROCESSING SUMMARY")
    print("="*70)
    print(f"Total receipts processed: {len(results)}")
    print(f"Total items extracted: {sum(r['item_count'] for r in results)}")
    print("\nReceipts:")
    for r in results:
        print(f"  • {os.path.basename(r['file']):30} - {r['vendor']:25} ({r['item_count']} items)")
    print("="*70)
    
    # Save summary
    import json
    with open('batch_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Detailed results saved to: batch_test_results.json")

if __name__ == '__main__':
    main()
