import React, { useState } from 'react';

function FileUpload() {

    const [selectedFile, setSelectedFile] = useState();
    const [isFilePicked, setIsFilePicked] = useState(false);

    const changeHandler = (event) => {
        const file = event.target.files[0];
        if (file) {
            setSelectedFile(file);
            setIsFilePicked(true);
        } else {
            setSelectedFile(null);
            setIsFilePicked(false);
        }
    };

    const handleSubmission = () => {
    };

    return (
        <div className="file-upload-container">
            <label htmlFor="file-upload" className="file-input-button">Choose File</label>
            <input id="file-upload" type="file" name="file" onChange={changeHandler} />
            {isFilePicked ? (
                <div className="file-details">
                    <p>Filename: {selectedFile.name}</p>
                    <p> Filetype: {selectedFile.type}</p>
                </div>
            ) : (
                <p>Select a file to show details</p>
            )}

            <div>
                <button onClick={handleSubmission}>Upload</button>
            </div>
        </div>
    )
}

export default FileUpload;