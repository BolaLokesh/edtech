Part A: System Design
Core Entities and Relationships
Entities:

User

id (PK)

username

email

password_hash

role (teacher/student)

created_at

Assignment

id (PK)

title

description

due_date

created_at

teacher_id (FK to User)

max_points

Submission

id (PK)

assignment_id (FK to Assignment)

student_id (FK to User)

content (text or file reference)

submitted_at

grade (nullable)

feedback (nullable)

Relationships:

One Teacher (User) can create Many Assignments (1:N)

One Assignment can have Many Submissions (1:N)

One Student (User) can submit Many Submissions (1:N)

API Endpoints

1. Teacher Creates an Assignment

POST /api/assignments
Headers:
  Authorization: Bearer <teacher_token>
  
Request Body:
{
  "title": "Math Homework",
  "description": "Solve problems 1-10",
  "due_date": "2023-12-15T23:59:00Z",
  "max_points": 100
}

Response (201 Created):
{
  "id": "123",
  "title": "Math Homework",
  "description": "Solve problems 1-10",
  "due_date": "2023-12-15T23:59:00Z",
  "created_at": "2023-11-01T10:00:00Z",
  "teacher_id": "teacher123",
  "max_points": 100
}

2. Student Submits Assignment

POST /api/assignments/{assignment_id}/submissions
Headers:
  Authorization: Bearer <student_token>
  
Request Body:
{
  "content": "Here are my solutions...",
  // or for file uploads
  "file_url": "https://storage.example.com/files/submission123.pdf"
}

Response (201 Created):
{
  "id": "sub456",
  "assignment_id": "123",
  "student_id": "student789",
  "content": "Here are my solutions...",
  "submitted_at": "2023-12-14T15:30:00Z",
  "grade": null,
  "feedback": null
}

3. Teacher Views Submissions

GET /api/assignments/{assignment_id}/submissions
Headers:
  Authorization: Bearer <teacher_token>

Response (200 OK):
{
  "assignment": {
    "id": "123",
    "title": "Math Homework",
    "description": "Solve problems 1-10",
    "due_date": "2023-12-15T23:59:00Z"
  },
  "submissions": [
    {
      "id": "sub456",
      "student_id": "student789",
      "student_name": "John Doe",
      "content": "Here are my solutions...",
      "submitted_at": "2023-12-14T15:30:00Z",
      "grade": null,
      "feedback": null
    },
    // ... more submissions
  ]
}

Authentication Strategy
JWT (JSON Web Token) Based Authentication:

Users login with credentials and receive a JWT containing:

User ID

Role (teacher/student)

Expiration time

All API endpoints require a valid JWT in the Authorization header

Role-based access control:

Teacher-only endpoints check for role: teacher

Student-only endpoints check for role: student

Some endpoints may be accessible to both with different behavior

Password storage:

Passwords are hashed with bcrypt or similar before storage

Suggestions for Scaling the System
Database Scaling:

Implement read replicas for the database to handle increased read loads

Consider sharding by school or region if the user base grows large

Add caching (Redis) for frequently accessed assignments and submissions

File Storage:

Use object storage (S3, GCS) for file submissions rather than database storage

Implement a CDN for faster distribution of assignment materials

API Scaling:

Move to microservices architecture as features grow (separate services for assignments, submissions, grading, etc.)

Implement API gateway for routing and rate limiting

Add queue systems (RabbitMQ, SQS) for asynchronous processing of large submissions

Performance:

Add pagination to submission lists

Implement lazy loading for assignment attachments

Consider GraphQL for more efficient data fetching

Monitoring:

Implement comprehensive logging and monitoring

Set up alerts for unusual activity patterns

Availability:

Deploy across multiple availability zones

Implement database failover mechanisms

Future Features:

Add plagiarism detection integration

Implement real-time notifications for new assignments/submissions

Add collaborative features like peer review
