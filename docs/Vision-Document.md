# 1. Project Overview

EduAI is an AI-powered academic assistant designed to help university students understand course material and obtain answers to academic questions.

The system allows faculty members to create courses and upload course materials such as PDF, DOCX, and PPTX documents. The uploaded materials are processed and indexed into course-specific FAISS vector stores.

Students can register, log in, enroll in courses, ask questions about their enrolled courses, view AI-generated answers, view the source material used to generate answers, and review their recent question history.

EduAI uses Retrieval-Augmented Generation (RAG) to retrieve relevant course material before sending the retrieved context to an AI language model. This helps the system provide answers that are grounded in the course materials rather than relying only on general knowledge.

---

# 2. Problem Statement

University students often need to search through large amounts of lecture notes, presentations, textbooks, and other course materials to find answers to academic questions.

Traditional approaches require students to manually search through documents, which can be time-consuming and inefficient.

Faculty members also need a simple way to organize course learning materials and make those materials accessible to students.

EduAI addresses this problem by providing an academic question-answering system that uses course-specific documents as the knowledge source.

---

# 3. Project Purpose

The purpose of EduAI is to provide a centralized academic assistant that:

- Allows faculty to manage courses.
- Allows faculty to upload course learning materials.
- Automatically processes and indexes course documents.
- Allows students to enroll in courses.
- Allows students to ask questions about course material.
- Uses RAG to retrieve relevant course content.
- Uses an LLM to generate understandable answers.
- Displays the sources used to answer questions.
- Stores students' question history.
- Provides role-based access for students and faculty.

---

# 4. Project Vision

EduAI aims to become an intelligent academic support platform that connects students directly with their course materials through natural-language interaction.

Instead of manually searching through multiple documents, a student should be able to ask:

> "What are the main principles of software engineering?"

and receive an answer based on the learning materials uploaded for that course.

The long-term vision is to provide students with a reliable, transparent, and easy-to-use academic assistant while allowing faculty to control the course knowledge base.

---

# 5. Stakeholders

## Students

Students are the primary users of the academic assistant.

They can:

- Register accounts.
- Log in.
- View available courses.
- Enroll in courses.
- Unenroll from courses.
- Select an enrolled course.
- Ask academic questions.
- View AI-generated answers.
- View sources used by the RAG system.
- View recent question history.

## Faculty

Faculty members manage the academic content used by EduAI.

They can:

- Register as faculty.
- Log in.
- Create courses.
- Upload course materials.
- Index course documents.
- Manage course learning content.

## University / Academic Institution

The university benefits from:

- Improved student access to learning materials.
- Automated academic assistance.
- Centralized course knowledge.
- Reduced time spent manually searching course documents.

---

# 6. Project Scope

## In Scope

The current implementation includes:

- User registration.
- User authentication.
- JWT-based authentication.
- Student and faculty roles.
- Course creation.
- Course listing.
- Student enrollment.
- Student unenrollment.
- Faculty course ownership.
- Faculty document upload.
- PDF document processing.
- DOCX document processing.
- PPTX document processing.
- Course-specific document indexing.
- FAISS vector search.
- Retrieval-Augmented Generation.
- LLM-based answer generation.
- Source display.
- Question history.
- React web interface.
- FastAPI backend.
- SQLite database.
- Automated testing.

## Out of Scope

The following features are not currently implemented:

- Cloud deployment.
- Mobile application.
- Real-time collaboration.
- Online examinations.
- Assignment submission.
- Grade management.
- Payment processing.
- Video conferencing.
- Advanced analytics dashboards.

---

# 7. Major Features

## 7.1 Authentication

Users can register and log in.

Supported roles:

- Student
- Faculty

Passwords are stored as password hashes rather than plain text.

Authentication uses JWT access tokens.

---

## 7.2 Role-Based Access

EduAI distinguishes between students and faculty.

Students can access student functionality such as:

- Course enrollment.
- Course unenrollment.
- Asking questions.
- Viewing question history.

Faculty can access faculty functionality such as:

- Creating courses.
- Uploading course documents.

Backend dependencies enforce role restrictions.

---

## 7.3 Course Management

Faculty members can create courses containing:

- Course code
- Course name
- Description

Example:


Course Code: CS425
Course Name: Software Engineering
Description: Software engineering principles and practices

---

## 7.4 Course Enrollment

Students can view available courses and enroll in courses.

The system prevents duplicate enrollment.

Students can also unenroll from courses.

## 7.5 Course Document Upload

Faculty members can upload course materials.

Supported formats:

PDF
DOCX
PPTX

Uploaded files are stored in course-specific directories.

Example:

uploads/
    course_1/
        Lesson2-SWEprinciples.pdf

## 7.6 Document Processing

Uploaded documents are processed into smaller text chunks.

The chunks are converted into vector embeddings and stored in a FAISS vector index.

This allows EduAI to efficiently retrieve relevant course material when a student asks a question.

## 7.7 Retrieval-Augmented Generation

EduAI uses Retrieval-Augmented Generation (RAG).

The general flow is:

Student Question
       |
       v
Selected Course
       |
       v
FAISS Vector Search
       |
       v
Relevant Course Documents
       |
       v
Retrieved Context
       |
       v
LLM
       |
       v
Generated Answer
       |
       v
Answer + Sources

The system retrieves course-specific content before generating the response.

## 7.8 AI Question Answering

Students can ask questions using natural language.

Example:

What are software engineering processes?

EduAI retrieves relevant course material and generates an answer using the LLM.

The system is instructed to:

Prefer course material.
Avoid inventing facts.
Clearly indicate when information is unavailable.
Explain concepts in a student-friendly manner.

## 7.9 Source Display

EduAI displays the documents used by the RAG system.

Sources can include:

Document filename.
Retrieved content.
Page number when available.

Example:

Sources

Lesson2-SWEprinciples.pdf

Page 6

The software development community needs
a controlled way of working...

This improves transparency and allows students to verify the answer against the original course material.

## 7.10 Question History

EduAI stores students' recent questions and answers.

The dashboard displays:

Recent Questions

Question
Answer
Course ID
Date and Time

This allows students to review previous interactions.

# 7.11. Assumptions

The project assumes:

Users have access to a modern web browser.
Faculty members upload valid academic documents.
Internet access is available when using the OpenAI API.
The OpenAI API key is configured locally through environment variables.
Course documents contain text that can be extracted.
Students are authorized to access courses in which they are enrolled.
The local machine has sufficient storage for uploaded documents and vector indexes.

# 7.12. Constraints

The project has the following constraints:

The application currently runs locally.
The system depends on an external LLM API for answer generation.
AI-generated responses may occasionally require verification.
Only PDF, DOCX, and PPTX files are supported.
The application currently uses SQLite.
Cloud deployment is not included.
Large document collections may require additional optimization.