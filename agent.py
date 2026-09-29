import os
from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

load_dotenv()

# -----------------------------
# Configuration
# -----------------------------
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BANK_ID = "remedy-memory"

# -----------------------------
# Clients
# -----------------------------
hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=HINDSIGHT_API_KEY
)

groq = Groq(api_key=GROQ_API_KEY)


# -----------------------------
# REMEDY Agent
# -----------------------------
def ask_remedy(question):

    # 1. Recall relevant past incidents
    memories = hindsight.recall(
        bank_id=BANK_ID,
        query=question
    )

    # 2. Convert memories into text
    memory_text = ""

    for memory in memories.results:
        memory_text += f"- {memory.text}\n"

    # 3. Ask Groq to reason using the memories
    prompt = f"""
You are REMEDY, an organizational incident-learning AI agent.

Your job is to help teams solve recurring technical problems
using their organization's previous experiences.

IMPORTANT:
- Use the recalled memories as historical experience.
- Do not invent previous incidents.
- Clearly distinguish known history from your reasoning.
- If there is no relevant historical memory, say so.
- Prefer solutions that previously worked.
- Warn the user about approaches that previously failed.

Previous organizational memories:
{memory_text}

Current user question:
{question}

Give a practical response with:
1. Relevant previous incident
2. What failed before
3. What worked before
4. Recommended next investigation steps
"""

    # 4. Generate answer with Groq
    response = groq.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are REMEDY, an AI incident-learning assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# -----------------------------
# Test
# -----------------------------
question = input("\nAsk REMEDY: ")

answer = ask_remedy(question)


print("\n========== REMEDY ==========\n")
print(answer)

hindsight.close()