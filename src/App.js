import './App.css';
import FileUpload from './upload.js';
import React, { useState } from 'react';
import ScrollableBox from "./text.js";


function App() {

  const [textInput, setTextInput] = useState('');

  const handleInputChange = (event) => {
    setTextInput(event.target.value);
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Submitted text:', textInput)
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
