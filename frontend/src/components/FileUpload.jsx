import React from 'react'
import { useState, useRef} from 'react';
import axios from "axios";

const FileUpload = () => {
    const fileInputRef = useRef(null);

    const [text, setText] = useState("");

    const handleButtonClick = () => {
        // Trigger the file input when the button is clicked
        fileInputRef.current.click();
      };

    const handleFileChange = async (event) => {
    const selectedFile = event.target.files[0];

    const formData = new FormData();
    formData.append('file', selectedFile);


    try {
        const response = await axios.post('http://127.0.0.1:5000/extract-text', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        });
        setText(response.data.data);
    } catch (error) {
        console.error(error);
    }

    };

      
  return (
    <div>
    <button onClick={handleButtonClick}>
      <span role="img" aria-label="attachment">📎</span>
    </button>
    <input
      ref={fileInputRef}
      type="file"
      accept=".pdf"
      style={{ display: 'none' }}
      onChange={handleFileChange}
    />  
</div>
  )
}

export default FileUpload