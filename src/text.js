import React, { useState } from 'react';

function ScrollableBox() {
  const [text, setText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

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

  return (
    <div>
      <button onClick={fetchDataFromApi} disabled={isLoading}>
        {isLoading ? 'Loading...' : 'Fetch Data'}
      </button>
      <div style={{ width: '300px', height: '200px', overflow: 'auto' }}>
        <p>{text}</p>
      </div>
    </div>
  );
}

export default ScrollableBox;
