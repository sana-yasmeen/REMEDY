# REMEDY
AI-powered incident intelligence agent that uses Hindsight memory and Groq reasoning to learn from past incidents, failed attempts, and successful solutions.
# REMEDY – Organizational Failure Intelligence Agent

> **Fix it once. Remember forever.**

REMEDY is an AI-powered incident intelligence agent that helps engineering teams learn from previous technical incidents instead of starting every investigation from zero.

It uses **Hindsight** as a persistent organizational memory layer and **Groq** for AI reasoning. REMEDY recalls relevant past incidents, including failed troubleshooting attempts and successful solutions, and uses that experience to guide the investigation of new incidents.

---

## 🚀 Problem

Engineering teams often face similar technical incidents repeatedly, such as:

- API failures
- Database connection problems
- Service timeouts
- Performance issues
- Infrastructure failures

During an incident, engineers may try multiple solutions. Some fail, while others work.

However, this experience can become scattered across tickets, documents, reports, or individual knowledge.

When a similar incident happens again, engineers may have to repeat the investigation from the beginning.

**REMEDY solves this by turning previous incident experience into reusable organizational memory.**

---

## 💡 Solution

REMEDY allows an AI agent to:

1. Understand a new incident
2. Recall relevant historical incidents
3. Review previous troubleshooting attempts
4. Identify approaches that failed
5. Identify solutions that worked
6. Use historical context for AI reasoning
7. Recommend what to investigate next
8. Store new incident experiences for future use

---

## 🧠 How REMEDY Works

```text
New Incident
     ↓
Hindsight Recall
     ↓
Historical Incident Evidence
     ↓
Groq AI Reasoning
     ↓
Investigation Recommendation
     ↓
New Incident Experience
     ↓
Hindsight Memory



🔥 Key Features
🧠 Persistent Incident Memory

REMEDY uses Hindsight to retain previous incident experiences so they can be reused later.

🔎 Relevant Memory Recall

When a new incident occurs, REMEDY retrieves relevant historical experiences instead of treating the problem as completely new.

❌ Failure Memory

The system remembers troubleshooting approaches that did not work.

This can help prevent repeated investigation steps.

✅ Successful Resolution Memory

Successful solutions are also retained and can become useful evidence for future incidents.

🤖 AI-Powered Reasoning

Groq processes the current incident together with relevant historical context to generate investigation guidance.

📊 Incident Investigation Dashboard

The Streamlit interface provides:

Command Center
Incident Investigation
Incident History
Memory Explorer
Insights
System information
🏗️ Architecture
                    ┌─────────────────┐
                    │  New Incident   │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Hindsight Recall│
                    └────────┬────────┘
                             ↓
                 ┌───────────────────────┐
                 │ Historical Evidence  │
                 │ • Past Incidents     │
                 │ • Failed Attempts    │
                 │ • Successful Fixes   │
                 └───────────┬───────────┘
                             ↓
                    ┌─────────────────┐
                    │  Groq Reasoning │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Recommendation  │
                    └────────┬────────┘
                             ↓
                    ┌─────────────────┐
                    │ Hindsight Retain│
                    └─────────────────┘
🛠️ Technology Stack
Technology	Purpose
Python	Backend and agent logic
Streamlit	Web interface
Hindsight	Persistent agent memory
Groq	AI reasoning
python-dotenv	Environment configuration
hindsight-client	Hindsight integration
🧪 Example
Previous Incident

Payment API Failure

Problem:

Requests cannot get database connections.

Troubleshooting:

❌ Restarting the service – unsuccessful
❌ Increasing timeout – unsuccessful
✅ Increasing database connection pool – successful

REMEDY stores this experience in Hindsight.

New Similar Incident

When a similar database connection problem occurs, REMEDY recalls the previous experience and provides it as context for the reasoning process.

This allows the agent to consider what was previously attempted instead of starting from scratch.

🔄 Memory → Reasoning Workflow

REMEDY separates two important responsibilities:

Hindsight

Remembers the experience.

It stores and retrieves relevant incident knowledge.

Groq

Reasons over the experience.

It uses the recalled context together with the current incident to generate investigation guidance.

This creates the workflow:

Hindsight remembers → Groq reasons → REMEDY recommends

📁 Project Structure
REMEDY/
│
├── app.py
├── agent.py
├── requirements.txt
├── .env
├── .gitignore
│
├── README.md
│
└── assets/
    └── screenshots/

API keys and other secrets are stored in environment variables and should never be committed to GitHub.

⚙️ Setup
1. Clone the repository
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd REMEDY
2. Create a virtual environment
python -m venv venv
3. Activate the environment

Windows:

venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Configure environment variables

Create a .env file:

HINDSIGHT_API_KEY=your_hindsight_api_key
GROQ_API_KEY=your_groq_api_key
6. Run the application
streamlit run app.py
🔐 Security

Do not commit API keys to GitHub.

The .env file should be included in .gitignore.

Example:

.env
venv/
__pycache__/
*.pyc
📈 Future Improvements

Future versions of REMEDY could include:

Integration with real incident management systems
Automatic incident ingestion
Larger organizational memory banks
Role-based access control
Better incident similarity detection
Automated post-incident learning
Memory quality evaluation
Production monitoring and observability
More advanced incident analytics
🎯 Vision

REMEDY aims to make organizational experience reusable.

Every incident can teach the organization something:

What happened → What was tried → What failed → What worked → What was learned

Instead of allowing that knowledge to disappear after an incident is resolved, REMEDY turns it into memory that can support future investigations.

Don't make the next engineer start from zero.

Fix it once. Remember forever.

👥 Team

Built by our team as an AI agent focused on organizational incident memory and intelligent incident investigation.

📚 Technologies
Hindsight – Persistent AI memory
Groq – LLM inference
Python – Agent implementation
Streamlit – Application interface
