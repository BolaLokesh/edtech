import React, { useState } from 'react';
import api from '../api';

const SubmissionForm = () => {
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post('/submissions', { content });
    setContent('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Submission Content"
      />
      <button type="submit">Submit</button>
    </form>
  );
};

export default SubmissionForm;
