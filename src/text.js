import React, { useState, useEffect } from 'react';

function ScrollableBox() {
  const [text, setText] = useState('');

  useEffect(() => {
    // Fetch data from your API
    fetch('http://localhost:8000/answer')
      .then((response) => response.json())
      .then((data) => {
        setText(data.text); // Assuming your API response has a 'text' property
      })
      .catch((error) => {
        console.error('Error fetching data: ', error);
      });
  }, []);

  return (
    <div style={{ width: '300px', height: '200px', overflow: 'auto' }}>
      <p>{text}</p>
    </div>
  );
}

export default ScrollableBox;
