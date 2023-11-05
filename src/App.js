import './App.css';
import ScrollableBox from './text';
import FileUpload from './upload.js';
import React, { useState } from 'react';

function App() {
  const [textInput, setTextInput] = useState('');

  const handleInputChange = (event) => {
    setTextInput(event.target.value);
  }

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const data = { text: textInput };
      const response = await fetch('http://localhost:8000/answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        mode: 'cors',
      });

      if (response.ok) {
        console.log('Text submitted successfully');
        console.log(data);
      } else {
        console.error('Failed to submit text');
      }
    } catch (error) {
      console.error('Error submitting text:', error);
    }
  }

  return (
    <div className="App">
      <container className="App-header">
        <h1>subAI</h1>
      </container>
      <p>Please select a video or audio file from your computer</p>
      <FileUpload />
      <form onSubmit={handleSubmit}>
        <ScrollableBox />
        <div>
          <p>Enter any questions: </p>
          <input
            type="text"
            value={textInput}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
      <div>
        <button>Generate Practice Problem</button>
      </div>
    </div>
  );
}

export default App;
