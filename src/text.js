import React, { useState, useEffect } from 'react';

function ScrollableBox() {
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [textInput, setTextInput] = useState('');
  const [response, setResponse] = useState('');

  const fetchDataFromApi = () => {
    setIsLoading(true);

    // Fetch data from your API
    fetch('http://localhost:8000/answer')
      .then((response) => response.json())
      .then((data) => {
        setText(data.text);
      })
      .catch((error) => {
        console.error('Error fetching data: ', error);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  const handleTextSend = async () => {
    try {
      const data = { text: textInput }; // Data to send
      const response = await fetch('http://localhost:8000/answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        mode:'cors',
      });

      if (response.ok) {
        const result = await response.json();
        setResponse(result.text);
      } else {
        setResponse('Failed to send text');
      }
    } catch (error) {
      console.error('Error sending text:', error);
    }
  };

  useEffect(() => {
    fetchDataFromApi();
  }, []);

  return (
    <div>
      <button onClick={fetchDataFromApi} disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Fetch Data'}
      </button>
      <div style={{ width: '300px', height: '200px', overflow: 'auto' }}>
        <p>{text}</p>
      </div>
      <input
        type="text"
        value={textInput}
        onChange={(e) => setTextInput(e.target.value)}
      />
      <button onClick={handleTextSend}>Send Text</button>
      <div>{response}</div>
    </div>
  );
}

export default ScrollableBox;
