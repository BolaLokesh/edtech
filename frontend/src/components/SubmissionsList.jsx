import React, { useEffect, useState } from 'react';
import api from '../api';

const SubmissionsList = () => {
  const [submissions, setSubmissions] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const response = await api.get('/submissions');
      setSubmissions(response.data);
    };
    fetchData();
  }, []);

  return (
    <ul>
      {submissions.map((submission, idx) => (
        <li key={idx}>{submission.content}</li>
      ))}
    </ul>
  );
};

export default SubmissionsList;
