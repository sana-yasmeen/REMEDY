import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")

BANK_ID = "remedy-memory"

hindsight = Hindsight(
    base_url="https://api.hindsight.vectorize.io",
    api_key=HINDSIGHT_API_KEY
)


def find_similar_incident():

    print("\n========== SIMILAR INCIDENT DETECTION ==========\n")

    current_problem = input(
        "Describe the current incident: "
    )

    result = hindsight.recall(
        bank_id=BANK_ID,
        query=current_problem
    )

    if not result.results:
        print("\n❌ No similar incidents found.")
        hindsight.close()
        return

    print("\n🔎 Similar incidents found:\n")

    for i, memory in enumerate(result.results, start=1):

        print(f"--- Memory {i} ---")
        print(memory.text)
        print()



find_similar_incident()

hindsight.close()