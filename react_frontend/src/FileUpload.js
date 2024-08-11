import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  withCredentials: true,
});

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [fileContent, setFileContent] = useState('');
  const [summary, setSummary] = useState('');
  const [summarizing, setSummarizing] = useState(false);
  const [error, setError] = useState(null);
  const [processStopped, setProcessStopped] = useState(false);
  const [stopButtonText, setStopButtonText] = useState('Stop Summarization');
  const [stopButtonDisabled, setStopButtonDisabled] = useState(false);

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const onFileUpload = async () => {
    if (!file) {
      setError('Please select a file first.');
      return;
    }

    if (!['pdf', 'docx', 'txt'].includes(file.name.split('.').pop().toLowerCase())) {
      setError('Invalid file format. Accepted formats are: PDF, DOCX, TXT.');
      return;
    }

    setError(null);
    setSummarizing(true);
    setProcessStopped(false);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await api.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.error) {
        setError(response.data.error);
        setSummarizing(false);
        return;
      }

      setFileContent(response.data.content);

      // Start summarization
      const summarizeResponse = await api.post('/summarize', {
        filename: response.data.filename,
      });

      if (summarizeResponse.data.error) {
        setError(summarizeResponse.data.error);
        setSummarizing(false);
        return;
      }

      // Start polling for summary status
      pollSummaryStatus();
    } catch (error) {
      console.error('Error uploading or summarizing the file:', error);
      setError('An error occurred. Please check the console for details.');
      setSummarizing(false);
    }
  };

  const pollSummaryStatus = async () => {
    try {
      const response = await api.get('/summarize/status');
      if (response.data.status === 'completed') {
        setSummary(response.data.summary);
        setSummarizing(false);
        resetStopButton();
      } else if (response.data.status === 'error') {
        setError(response.data.error);
        setSummarizing(false);
        resetStopButton();
      } else if (response.data.status === 'stopped') {
        setSummary(response.data.summary);
        setSummarizing(false);
        setProcessStopped(true);
        resetStopButton();
      } else {
        // Continue polling
        setTimeout(pollSummaryStatus, 1000);
      }
    } catch (error) {
      console.error('Error checking summary status:', error);
      setError('An error occurred while checking the summary status.');
      setSummarizing(false);
      resetStopButton();
    }
  };

  const onStopSummarization = async () => {
    try {
      setStopButtonText('Please wait, processing...');
      setStopButtonDisabled(true);

      const response = await api.post('/stop');
      if (response.data.summary) {
        setSummary(response.data.summary);
      }
      setSummarizing(false);
      setProcessStopped(true);
      resetStopButton();
    } catch (error) {
      console.error('Error stopping the summarization process:', error);
      setError('An error occurred while stopping the summarization process.');
      setSummarizing(false);
      resetStopButton();
    }
  };

  const resetStopButton = () => {
    setStopButtonText('Stop Summarization');
    setStopButtonDisabled(false);
  };

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        setError(null);
      }, 10000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  return (
    <div className="container">
      <div 
        className="loader-overlay" 
        style={{ visibility: summarizing && !processStopped ? 'visible' : 'hidden', opacity: summarizing && !processStopped ? 1 : 0 }}
      >
        <div className="loader"></div>
      </div>
      <div 
        className="summary-loader" 
        style={{ visibility: summarizing && !processStopped ? 'visible' : 'hidden', opacity: summarizing && !processStopped ? 1 : 0 }}
      >
        <div className="loader"></div>
      </div>
      {error && (
        <div className="error-message">{error}</div>
      )}

      <div className="upload-box">
        <h1>Summarization</h1>
        <p className="accepted-types">(Accepted file types: PDF, DOCX, TXT)</p>
        <input type="file" onChange={onFileChange} />
        <button onClick={onFileUpload} className="upload-button">Upload and Summarize</button>
        {summarizing && !processStopped && (
          <button 
            onClick={onStopSummarization} 
            className="stop-button" 
            disabled={stopButtonDisabled}
          >
            {stopButtonText}
          </button>
        )}
      </div>
      <div className="content-box">
        <h2>File Content:</h2>
        <pre className="content-text">{fileContent}</pre>
      </div>
      <div className="summary-box">
        <h2>Summary:</h2>
        <p className="summary-text">{summary}</p>
      </div>
    </div>
  );
};

export default FileUpload;
