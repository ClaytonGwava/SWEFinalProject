
# System Architecture

EduAI uses a layered architecture.

```text
+------------------------------------------------+
|                 React Frontend                 |
|                                                |
| Dashboard | Faculty Dashboard | Login | Forms |
+-------------------------+----------------------+
                          |
                          | HTTP / REST
                          v
+------------------------------------------------+
|                 FastAPI Backend                |
|                                                |
| Routers / API Controllers                      |
+------------------------------------------------+
                          |
                          v
+------------------------------------------------+
|                    Services                    |
|                                                |
| Authentication | RAG | LLM | Documents        |
+------------------------------------------------+
             |                       |
             v                       v
+------------------------+   +------------------+
|      SQLite Database   |   |   FAISS Index    |
|                        |   |                  |
| Users                  |   | Course vectors  |
| Courses                |   | Document chunks |
| Enrollments            |   +------------------+
| Documents              |
| Questions              |
+------------------------+
                          |
                          v
                 +----------------+
                 |   OpenAI API   |
                 |      LLM       |
                 +----------------+

```