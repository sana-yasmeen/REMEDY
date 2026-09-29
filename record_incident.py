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


def record_incident():
    print("\n========== RECORD NEW INCIDENT ==========\n")

    service = input("Service name: ")
    problem = input("What happened? ")
    attempts = input("What was tried? ")
    solution = input("What finally worked? ")
    root_cause = input("Root cause: ")
    outcome = input("Outcome: ")

    incident = f"""
Incident Report

Service:
{service}

Problem:
{problem}

Attempts:
{attempts}

Successful Solution:
{solution}

Root Cause:
{root_cause}

Outcome:
{outcome}
"""

    hindsight.retain(
        bank_id=BANK_ID,
        content=incident
    )

    print("\n✅ Incident successfully stored in Hindsight!")
    print("REMEDY has learned from this incident.")



record_incident()

hindsight.close()