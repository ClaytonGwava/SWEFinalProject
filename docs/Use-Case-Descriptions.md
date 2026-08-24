

# 12. Use Cases
UC1 – Register

Actor: Student / Faculty

Description:
A user creates an EduAI account.

Main Flow
User opens registration.
User enters username.
User enters email.
User enters password.
User selects role.
System validates the information.
System creates the account.
System returns the user information.
Alternative Flow

If the username or email already exists, the system returns an error.

# 13. UC2 – Login

Actor: Student / Faculty

Description:
A registered user logs into EduAI.

Main Flow
User enters username.
User enters password.
System validates credentials.
System creates a JWT access token.
User is authenticated.
Alternative Flow

If credentials are invalid, the system returns:

Invalid username or password

# 14. UC3 – Create Course

Actor: Faculty

Main Flow
Faculty logs in.
Faculty opens the course creation form.
Faculty enters course code.
Faculty enters course name.
Faculty enters description.
System validates the request.
Course is stored in the database.

# 15. UC4 – Upload Course Material

Actor: Faculty

Main Flow
Faculty selects a course.
Faculty selects a document.
System validates the file type.
System saves the document.
System creates a database record.
System extracts document content.
System creates document chunks.
System creates the course vector index.
System reports the number of chunks created.

# 16. UC5 – Enroll in Course

Actor: Student

Main Flow
Student views available courses.
Student selects a course.
Student clicks Enroll.
System creates an enrollment record.
Course appears under My Courses.
Alternative Flow

If the student is already enrolled, the system returns an error.

# 17. UC6 – Unenroll from Course

Actor: Student

Main Flow
Student opens My Courses.
Student selects a course.
Student clicks Unenroll.
System removes the enrollment.
Course is removed from My Courses.

# 18. UC7 – Ask Academic Question

Actor: Student

Main Flow
Student selects an enrolled course.
Student enters a question.
Student submits the question.
System identifies the selected course.
System searches the course's vector store.
Relevant document chunks are retrieved.
Retrieved context is sent to the LLM.
LLM generates an answer.
System displays the answer.
System displays the sources.
Question and answer are stored in history.

# 19. UC8 – View Question History

Actor: Student

Main Flow
Student opens the dashboard.
System retrieves previous questions.
System displays questions and answers.
System displays course and timestamp information.