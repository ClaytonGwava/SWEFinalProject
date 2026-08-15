import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY is not configured in the .env file."
    )


client = OpenAI(api_key=api_key)


def ask_llm(
    question: str,
    context: str = ""
) -> str:

    system_prompt = """
You are EduAI, an academic assistant for university students.

Answer questions using the provided course material whenever
course material is provided.

Rules:
1. Be accurate and clear.
2. Prefer the provided course material over general knowledge.
3. If the answer cannot be found in the provided material,
   clearly say that the information was not found in the
   available course material.
4. Do not invent facts or references.
5. Explain concepts in a way that is appropriate for students.
"""

    user_prompt = f"""
Course material:

{context}

Student question:

{question}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return response.output_text