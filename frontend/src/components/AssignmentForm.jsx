import React, { useState } from 'react';
import api from '../api';

const AssignmentForm = () => {
  const [title, setTitle] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await api.post('/assignments', { title });
    setTitle('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Assignment Title"
      />
      <button type="submit">Create</button>
    </form>
  );
};

export default AssignmentForm;
