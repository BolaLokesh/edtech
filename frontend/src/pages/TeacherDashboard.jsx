import React from 'react';
import AssignmentForm from '../components/AssignmentForm';
import SubmissionsList from '../components/SubmissionsList';

const TeacherDashboard = () => (
  <div>
    <h2>Teacher Dashboard</h2>
    <AssignmentForm />
    <SubmissionsList />
  </div>
);

export default TeacherDashboard;
