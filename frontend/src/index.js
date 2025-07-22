import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

// File: src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  withCredentials: true,
});

export default api;

// File: src/styles.css
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

form {
  display: flex;
  flex-direction: column;
  max-width: 300px;
  margin: 1rem;
}

input, textarea, button {
  margin-bottom: 0.5rem;
  padding: 0.5rem;
}
