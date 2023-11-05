import './App.css';
import FileUpload from './upload.js';
function App() {
  return (
    <div className="App">
      <h1>subAI</h1>
      <p>Please select a video or audio file from your computer</p>
      <FileUpload />
    </div>
  );
}

export default App;
