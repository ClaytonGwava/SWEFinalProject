## Collaboration Diagram

```mermaid
flowchart LR

    Student --> Dashboard
    Dashboard --> QuestionRouter
    QuestionRouter --> RAGService
    RAGService --> FAISS
    RAGService --> LLMService
    LLMService --> OpenAI
    QuestionRouter --> Database
    Database --> QuestionHistory
    RAGService --> Sources
    Sources --> Dashboard

    ```