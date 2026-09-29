import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

BANK_ID = "remedy-memory"

# Store an incident
client.retain(
    bank_id=BANK_ID,
    content="""
    Incident: Payment API failure.

    Root cause: Database connection exhaustion.

    Attempt 1: Restarted payment service. Result: Failed.

    Attempt 2: Increased API timeout. Result: Failed.

    Attempt 3: Increased database connection pool. Result: Successful.

    Final resolution: Increased database connection pool capacity.
    """,
    context="IT incident"
)

print("Incident stored in Hindsight!")

# Recall the incident
result = client.recall(
    bank_id=BANK_ID,
    query="What happened during the previous payment API incident?"
)

print("\nRecalled memories:")
for memory in result.results:
    print("-", memory.text)