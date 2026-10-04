from groq import Groq
from backend.app.core.config import GROQ_API_KEY
client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "openai/gpt-oss-120b"

def generate_answer(question: str, context: str,) -> str:
    """
    Generate an answer using the retrieved document context.
    """

    prompt = f"""
You are a research assistant.

Answer the user's question using only the provided context.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided documents."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content