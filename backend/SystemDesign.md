EdTech Assignment Tracker: System Design
Objective
To design and implement a simplified assignment tracking system for an EdTech platform, allowing teachers to post assignments and students to submit them.

Part A: System Design
1. Core Entities and Their Relationships
We will define three primary entities: User, Assignment, and Submission.

User: Represents individuals interacting with the system. Each user has a role (either 'teacher' or 'student').

Attributes:

id (Integer, Primary Key, Auto-increment)

email (String, Unique)

password_hash (String - stores hashed password)

name (String)

role (String, Enum: 'teacher', 'student')

token (String, Unique, Nullable - for session management)

created_at (Timestamp)

updated_at (Timestamp)

Assignment: Represents a task created by a teacher for students to complete.

Attributes:

id (Integer, Primary Key, Auto-increment)

teacher_id (Integer, Foreign Key to User.id - where User.role='teacher')

title (String)

description (Text)

due_date (DateTime)

created_at (Timestamp)

updated_at (Timestamp)

Submission: Represents a student's completed work for a specific assignment.

Attributes:

id (Integer, Primary Key, Auto-increment)

assignment_id (Integer, Foreign Key to Assignment.id)

student_id (Integer, Foreign Key to User.id - where User.role='student')

content (Text - for text-based submissions; could be a URL/path for file uploads in a scaled system)

submitted_at (DateTime)

grade (Float, Optional)

feedback (Text, Optional)

created_at (Timestamp)

updated_at (Timestamp)

Relationships:

One-to-Many (User to Assignment): A Teacher (User with role='teacher') can create multiple Assignments. (User.id -> Assignment.teacher_id)

Many-to-Many (Assignment to Student via Submission): An Assignment can have multiple Submissions from different Students. A Student (User with role='student') can make Submissions to multiple Assignments.

One-to-One (Student to Submission per Assignment): Typically, a student submits only one Submission per Assignment (enforced by application logic).

2. API Endpoints
We will follow RESTful principles for our API design. All responses will be structured JSON.

Authentication & User Management:

POST /api/signup

Description: Registers a new user (teacher or student).

Request Body: {"email": "...", "password": "...", "name": "...", "role": "teacher" | "student"}

Response: {"message": "User created successfully", "user_id": 123}

Error Responses: {"error": "Email already registered"}

POST /api/login

Description: Authenticates a user and issues an access token.

Request Body: {"email": "...", "password": "..."}

Response: {"message": "Login successful", "token": "abc123xyz", "user_id": 123, "role": "student", "name": "John Doe"}

Error Responses: {"error": "Invalid credentials"}

GET /api/user

Description: Retrieves details of the currently authenticated user.

Headers: Authorization: Bearer <token>

Response: {"user_id": 123, "email": "...", "name": "...", "role": "..."}

Error Responses: {"error": "Unauthorized"}

Assignment Management (Teacher Only for Creation/Management, All for Viewing):

POST /api/assignments

Description: Teacher creates a new assignment.

Headers: Authorization: Bearer <token>

Request Body: {"title": "...", "description": "...", "due_date": "YYYY-MM-DDTHH:MM:SS"}

Response: {"message": "Assignment created", "assignment_id": 456}

Error Responses: {"error": "Unauthorized", "details": "Only teachers can create assignments"}

GET /api/assignments

Description: Retrieves a list of all assignments.

Headers: Authorization: Bearer <token>

Response: [{"id": 456, "title": "...", "description": "...", "due_date": "...", "teacher_name": "..."}]

Submission Management (Student for Submission, Teacher for Viewing/Grading):

POST /api/assignments/<int:assignment_id>/submit

Description: Student submits work for a specific assignment.

Headers: Authorization: Bearer <token>

Request Body: {"content": "..."}

Response: {"message": "Assignment submitted", "submission_id": 789}

Error Responses: {"error": "Unauthorized", "details": "Only students can submit assignments"}

Error Responses: {"error": "Assignment not found"}

GET /api/assignments/<int:assignment_id>/submissions

Description: Teacher views all submissions for a specific assignment.

Headers: Authorization: Bearer <token>

Response: [{"id": 789, "student_id": 124, "student_name": "...", "content": "...", "submitted_at": "...", "grade": null, "feedback": null}]

Error Responses: {"error": "Unauthorized", "details": "Only teachers can view submissions"}

Error Responses: {"error": "Assignment not found"}

Error Responses: {"error": "Forbidden", "details": "You do not own this assignment"}

PUT /api/submissions/<int:submission_id>/grade

Description: Teacher grades a specific submission and provides feedback.

Headers: Authorization: Bearer <token>

Request Body: {"grade": 95.0, "feedback": "Excellent work!"}

Response: {"message": "Submission graded successfully"}

Error Responses: {"error": "Unauthorized", "details": "Only teachers can grade submissions"}

Error Responses: {"error": "Submission not found"}

Error Responses: {"error": "Forbidden", "details": "You do not own the assignment for this submission"}

3. Authentication Strategy (Role-Based)
Mechanism: Token-based authentication.

Login/Signup: Upon successful login or signup, the server generates a unique, random token for the user. This token is stored in the User table and sent back to the client.

Client Storage: The client stores this token (e.g., in localStorage).

Subsequent Requests: For every subsequent API request that requires authentication, the client includes the token in the Authorization header as Bearer <token>.

Server Verification: The server intercepts these requests, extracts the token, looks up the user associated with that token in the database.

Authorization: Based on the role attribute of the authenticated User, the server determines if the user has permission to perform the requested action.

Teacher Role: Can create assignments, view all submissions for their own assignments, and grade submissions for their own assignments.

Student Role: Can view available assignments, submit assignments, and view their own submissions.

4. Suggestions for Scaling the System in the Future
Database Scaling:

PostgreSQL: Migrate from SQLite to PostgreSQL for better concurrency, robustness, and features like replication and sharding.

Read Replicas: For read-heavy operations (e.g., students viewing assignments), use read replicas to offload queries from the primary database.

Database Sharding/Partitioning: Distribute data across multiple database instances based on criteria (e.g., by institution, course, or user ID ranges) to handle increased load.

Backend Architecture:

Microservices: Break down the monolithic Flask application into smaller, independent services (e.g., User Service, Assignment Service, Submission Service). Each service can be developed, deployed, and scaled independently. This improves fault isolation and team agility.

API Gateway: Introduce an API Gateway (e.g., Nginx, Kong, AWS API Gateway) to handle request routing, authentication, rate limiting, and caching before requests reach individual microservices.

Caching:

CDN (Content Delivery Network): Cache static assets (HTML, CSS, JS, images) closer to users for faster delivery.

In-memory Caching: Use tools like Redis or Memcached to cache frequently accessed data (e.g., assignment lists, user profiles) to reduce database load and improve response times.

Load Balancing:

Distribute incoming network traffic across multiple application servers to ensure no single server becomes a bottleneck, improving availability and responsiveness.

Asynchronous Processing:

Message Queues: Use message queues (e.g., RabbitMQ, Kafka, Celery with Redis/RabbitMQ) for long-running or non-real-time tasks (e.g., sending email notifications for new assignments, processing file uploads, generating reports). This prevents blocking the main application thread.

File Storage:

For file uploads (e.g., student submissions), integrate with cloud storage solutions like AWS S3, Google Cloud Storage, or Azure Blob Storage, storing only file URLs in the database.

Monitoring & Logging:

Implement robust monitoring and logging solutions (e.g., Prometheus, Grafana, ELK Stack) to track system performance, identify bottlenecks, and troubleshoot issues proactively.

Security Enhancements:

Implement stricter rate limiting, CSRF protection, and more comprehensive input validation.

Regular security audits and penetration testing.

Search and Analytics:

Integrate with dedicated search engines (e.g., Elasticsearch) for complex search queries on assignments or submissions.

Use data warehousing solutions for analytics and reporting.

+------------+       +----------------+        +-----------------+
|   User     |<----- |   Assignment   | <----- |   Submission    |
+------------+       +----------------+        +-----------------+
| id         |       | id             |        | id              |
| name       |       | title          |        | assignment_id FK|
| email      |       | description    |        | student_id FK   |
| password   |       | due_date       |        | content         |
| role       |       | created_by FK  |        | submitted_at    |
+------------+       +----------------+        +-----------------+
