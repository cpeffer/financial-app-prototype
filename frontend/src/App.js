import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [vendor, setVendor] = useState('');
  const [items, setItems] = useState([]);
  const [imageUrl, setImageUrl] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setError('');
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/api/process-receipt', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setVendor(response.data.vendor);
      setItems(response.data.items);
      setImageUrl(`http://localhost:5000${response.data.imageUrl}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Error processing receipt');
    } finally {
      setLoading(false);
    }
  };

  const handleVendorChange = (e) => {
    setVendor(e.target.value);
  };

  const handleItemChange = (index, field, value) => {
    const newItems = [...items];
    newItems[index][field] = value;
    setItems(newItems);
  };

  const addItem = () => {
    setItems([...items, { quantity: '1', name: '', itemNumber: '', price: '0.00' }]);
  };

  const deleteItem = (index) => {
    const newItems = items.filter((_, i) => i !== index);
    setItems(newItems);
  };

  const exportToCSV = () => {
    let csv = 'Vendor,Quantity,Item Name,Item Number,Price\n';
    items.forEach(item => {
      csv += `"${vendor}","${item.quantity}","${item.name}","${item.itemNumber}","${item.price}"\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `receipt_${vendor.replace(/\s+/g, '_')}_${Date.now()}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const copyToClipboard = () => {
    let text = `Vendor: ${vendor}\n\n`;
    text += 'Qty\tName\tItem #\tPrice\n';
    items.forEach(item => {
      text += `${item.quantity}\t${item.name}\t${item.itemNumber}\t${item.price}\n`;
    });

    navigator.clipboard.writeText(text).then(() => {
      alert('Copied to clipboard!');
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Receipt Itemizer</h1>
        <p>Upload a receipt photo to automatically extract items</p>
      </header>

      <div className="container">
        {!imageUrl ? (
          <div className="upload-section">
            <div className="upload-box">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                id="file-input"
              />
              <label htmlFor="file-input" className="file-label">
                {file ? file.name : 'Choose Receipt Image'}
              </label>
              
              {file && (
                <button onClick={handleUpload} disabled={loading} className="upload-btn">
                  {loading ? 'Processing...' : 'Process Receipt'}
                </button>
              )}
              
              {error && <div className="error">{error}</div>}
            </div>
          </div>
        ) : (
          <div className="review-section">
            <div className="two-panel">
              <div className="image-panel">
                <h2>Receipt Image</h2>
                <img src={imageUrl} alt="Receipt" />
              </div>

              <div className="data-panel">
                <h2>Extracted Data</h2>
                
                <div className="vendor-section">
                  <label>Vendor Name:</label>
                  <input
                    type="text"
                    value={vendor}
                    onChange={handleVendorChange}
                    className="vendor-input"
                  />
                </div>

                <div className="items-section">
                  <h3>Items</h3>
                  <div className="items-header">
                    <span>Qty</span>
                    <span>Name</span>
                    <span>Item #</span>
                    <span>Price</span>
                    <span></span>
                  </div>

                  {items.map((item, index) => (
                    <div key={index} className="item-row">
                      <input
                        type="text"
                        value={item.quantity}
                        onChange={(e) => handleItemChange(index, 'quantity', e.target.value)}
                        className="qty-input"
                      />
                      <input
                        type="text"
                        value={item.name}
                        onChange={(e) => handleItemChange(index, 'name', e.target.value)}
                        className="name-input"
                      />
                      <input
                        type="text"
                        value={item.itemNumber}
                        onChange={(e) => handleItemChange(index, 'itemNumber', e.target.value)}
                        className="number-input"
                      />
                      <input
                        type="text"
                        value={item.price}
                        onChange={(e) => handleItemChange(index, 'price', e.target.value)}
                        className="price-input"
                      />
                      <button onClick={() => deleteItem(index)} className="delete-btn">×</button>
                    </div>
                  ))}

                  <button onClick={addItem} className="add-btn">+ Add Item</button>
                </div>

                <div className="export-section">
                  <button onClick={exportToCSV} className="export-btn">Export to CSV</button>
                  <button onClick={copyToClipboard} className="export-btn">Copy to Clipboard</button>
                  <button onClick={() => window.location.reload()} className="export-btn">New Receipt</button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
