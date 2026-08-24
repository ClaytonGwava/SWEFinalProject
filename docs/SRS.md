# System Requirements
Functional Requirements

## FR1 – User Registration

The system shall allow users to create an account.

## FR2 – User Login

The system shall authenticate registered users.

## FR3 – Role Selection

The system shall support student and faculty roles.

## FR4 – Course Creation

The system shall allow faculty members to create courses.

## FR5 – Course Listing

The system shall display available courses.

## FR6 – Course Enrollment

The system shall allow students to enroll in courses.

## FR7 – Course Unenrollment

The system shall allow students to unenroll from courses.

## FR8 – Document Upload

The system shall allow authorized faculty members to upload course documents.

## FR9 – Document Validation

The system shall only accept supported document types.

## FR10 – Document Indexing

The system shall process uploaded documents and create searchable vector indexes.

## FR11 – Question Submission

The system shall allow students to submit academic questions.

## FR12 – Course-Specific Retrieval

The system shall retrieve relevant material from the selected course.

## FR13 – AI Answer Generation

The system shall generate answers using retrieved course context.

## FR14 – Source Display

The system shall display the source documents used for an answer.

## FR15 – Question History

The system shall store and display previous student questions and answers.

# 9. Nonfunctional Requirements

## NFR1 – Usability

The system should provide a simple web interface that students and faculty can use without specialized technical knowledge.

## NFR2 – Security

Passwords should not be stored as plain text.

Authentication tokens should be validated by the backend.

Role restrictions should be enforced server-side.

## NFR3 – Maintainability

The application should separate routing, business logic, database access, and data models.

## NFR4 – Reliability

The application should return meaningful errors for invalid requests.

## NFR5 – Performance

FAISS vector search should provide efficient retrieval of relevant document chunks.

## NFR6 – Scalability

The architecture should allow additional courses, documents, and users to be added.

## NFR7 – Transparency

The system should display sources used to generate AI answers.
