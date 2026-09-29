import os
import html
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

# ============================================================
# REMEDY — ENTERPRISE INCIDENT INTELLIGENCE CONSOLE
# Frontend-first Streamlit application
# ============================================================

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BANK_ID = "remedy-memory"

st.set_page_config(
    page_title="REMEDY | Enterprise Incident Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CLIENTS
# ============================================================
@st.cache_resource
def get_clients():
    hindsight = Hindsight(
        base_url="https://api.hindsight.vectorize.io",
        api_key=HINDSIGHT_API_KEY,
    )
    groq = Groq(api_key=GROQ_API_KEY)
    return hindsight, groq


hindsight, groq = get_clients()

# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "page": "Command Center",
    "answer": None,
    "memories": [],
    "question": "",
    "history": [],
    "incidents": [],
    "last_run": None,
    "selected_incident": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CSS — ENTERPRISE UI
# ============================================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #08111f;
    --navy2: #0d1b2e;
    --blue: #0078d4;
    --blue2: #106ebe;
    --cyan: #00a4ef;
    --green: #16a34a;
    --amber: #d97706;
    --red: #dc2626;
    --text: #0f172a;
    --muted: #64748b;
    --border: #e2e8f0;
    --surface: #ffffff;
    --soft: #f6f9fc;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 80% -5%, rgba(0,120,212,.10), transparent 28%),
        linear-gradient(180deg, #f7faff 0%, #ffffff 45%, #f5f8fb 100%);
}

[data-testid="stHeader"] {
    background: rgba(255,255,255,.82);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07101e, #0b1728);
    border-right: 1px solid #20324b;
}

section[data-testid="stSidebar"] * {
    color: #e7eef8;
}

.sidebar-logo {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -1px;
}

.sidebar-sub {
    color: #8293aa !important;
    font-size: 11px;
    line-height: 1.5;
    margin-bottom: 24px;
}

.nav-caption {
    color: #6f829b !important;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    font-size: 9px;
    font-weight: 800;
    margin: 18px 0 8px;
}

.status-panel {
    background: rgba(255,255,255,.045);
    border: 1px solid #233751;
    border-radius: 14px;
    padding: 12px;
    margin-top: 8px;
}

.status-line {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 11px;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,255,255,.06);
}

.status-line:last-child { border-bottom: none; }

.online {
    width: 7px;
    height: 7px;
    background: #22c55e;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    box-shadow: 0 0 9px rgba(34,197,94,.65);
}

/* Hero */
.hero {
    padding: 6px 0 12px;
}

.eyebrow {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 100px;
    background: #e8f3ff;
    color: #0067b8;
    text-transform: uppercase;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.hero h1 {
    font-size: clamp(38px, 5vw, 64px);
    line-height: .98;
    letter-spacing: -3px;
    margin: 12px 0 10px;
    color: #07111f;
    font-weight: 850;
}

.hero h1 span { color: #0078d4; }

.hero p {
    color: #596a7d;
    max-width: 760px;
    line-height: 1.65;
    font-size: 15px;
}

/* Top command bar */
.commandbar {
    background: rgba(255,255,255,.9);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 10px 14px;
    margin: 12px 0 20px;
    box-shadow: 0 5px 22px rgba(15,23,42,.045);
}

.command-item {
    color: #64748b;
    font-size: 11px;
}

.command-item b { color: #0f172a; }

/* Cards */
.card {
    background: rgba(255,255,255,.95);
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 20px;
    box-shadow: 0 7px 26px rgba(15,23,42,.045);
    margin-bottom: 16px;
}

.card-tight { padding: 15px 17px; }

.kicker {
    color: var(--blue);
    text-transform: uppercase;
    letter-spacing: 1.2px;
    font-size: 9px;
    font-weight: 800;
    margin-bottom: 5px;
}

.card-title {
    color: var(--text);
    font-size: 19px;
    font-weight: 800;
    letter-spacing: -.3px;
}

.card-sub {
    color: var(--muted);
    font-size: 12px;
    margin-top: 3px;
    line-height: 1.5;
}

/* KPI */
.kpi {
    background: white;
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 16px;
    min-height: 112px;
}

.kpi-label {
    color: #718096;
    text-transform: uppercase;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1px;
}

.kpi-value {
    color: #0f172a;
    font-size: 27px;
    font-weight: 850;
    margin-top: 8px;
}

.kpi-delta {
    font-size: 10px;
    color: #16a34a;
    margin-top: 4px;
}

/* Workflow */
.workflow {
    display: flex;
    align-items: center;
    gap: 7px;
    flex-wrap: wrap;
    margin: 12px 0 20px;
}

.workflow .step {
    background: #fff;
    border: 1px solid #dce5ef;
    padding: 9px 12px;
    border-radius: 10px;
    color: #334155;
    font-size: 10px;
    font-weight: 750;
}

.workflow .arrow {
    color: #9aa8b8;
}

/* Severity pills */
.pill {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 100px;
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
}

.pill-green { background:#eaf8ef; color:#15803d; }
.pill-amber { background:#fff7e8; color:#b45309; }
.pill-red { background:#fff0f0; color:#b91c1c; }
.pill-blue { background:#eaf4ff; color:#075985; }

/* Timeline */
.timeline {
    border-left: 2px solid #dbe7f2;
    margin: 12px 0 5px 8px;
    padding-left: 18px;
}

.event {
    position: relative;
    padding-bottom: 18px;
}

.event:before {
    content: '';
    position: absolute;
    left: -25px;
    top: 3px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #0078d4;
    box-shadow: 0 0 0 4px #e9f4fc;
}

.event-title {
    font-size: 12px;
    font-weight: 750;
    color: #1e293b;
}

.event-meta {
    color: #8a98a8;
    font-size: 10px;
    margin-top: 3px;
}

/* Evidence */
.evidence {
    background: #f8fbfe;
    border: 1px solid #dce8f2;
    border-left: 3px solid #0078d4;
    border-radius: 10px;
    padding: 11px 13px;
    margin: 8px 0;
    color: #334155;
    font-size: 11px;
    line-height: 1.55;
}

.evidence-tag {
    color: #0067b8;
    font-size: 8px;
    font-weight: 800;
    letter-spacing: .8px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

/* Insight */
.insight {
    background: linear-gradient(135deg,#eef7ff,#f9fcff);
    border: 1px solid #bfdef6;
    border-radius: 15px;
    padding: 16px;
}

.insight-title {
    font-weight: 800;
    font-size: 13px;
    color: #075985;
}

.insight-text {
    color: #526173;
    font-size: 11px;
    line-height: 1.55;
    margin-top: 4px;
}

/* Alert */
.alert-box {
    border-radius: 13px;
    padding: 14px;
    margin: 10px 0;
    font-size: 11px;
    line-height: 1.5;
}

.alert-warning {
    background: #fff9ed;
    border: 1px solid #f5d99a;
    color: #92400e;
}

.alert-info {
    background: #eff8ff;
    border: 1px solid #bfdef6;
    color: #075985;
}

/* Input */
div[data-testid="stTextArea"] textarea {
    border-radius: 13px !important;
    border: 1px solid #cbd5e1 !important;
    background: #fbfdff !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
    padding: 14px !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #0078d4 !important;
    box-shadow: 0 0 0 2px rgba(0,120,212,.12) !important;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    min-height: 41px;
    font-weight: 750;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-weight: 700;
    font-size: 12px;
}

/* Footer */
.footer {
    text-align:center;
    color:#94a3b8;
    font-size:9px;
    padding:35px 0 12px;
    letter-spacing:.3px;
}

/* Hide some Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================
def esc(value):
    return html.escape(str(value))


def add_incident(question, memories, answer):
    incident = {
        "id": f"REM-{len(st.session_state.incidents)+1042}",
        "title": question[:72] + ("..." if len(question) > 72 else ""),
        "question": question,
        "memories": memories,
        "answer": answer,
        "time": datetime.now().strftime("%d %b %Y · %H:%M"),
        "severity": "Investigating",
    }
    st.session_state.incidents.append(incident)
    st.session_state.selected_incident = incident["id"]


def run_investigation(question):
    memories = hindsight.recall(
        bank_id=BANK_ID,
        query=question,
    )

    memory_items = [m.text for m in memories.results]
    memory_text = "\n".join(f"- {item}" for item in memory_items)
    if not memory_text:
        memory_text = "No relevant historical memory was found."

    prompt = f"""
You are REMEDY, an organizational incident-learning AI agent.

Use the historical memories below to help solve the current incident.

IMPORTANT:
- Clearly distinguish historical facts from your recommendations.
- Do not invent previous incidents.
- Identify what failed previously.
- Identify what worked previously.
- Recommend practical next investigation steps.
- If there is no relevant history, say so.
- Prefer approaches that previously worked when evidence supports them.
- Warn the user when historical experience shows an approach failed.

HISTORICAL MEMORY:
{memory_text}

CURRENT INCIDENT:
{question}

Respond using exactly these sections:

### 1. Relevant Previous Experience
Explain which historical experience is relevant and why.

### 2. What Failed Before
List approaches, conditions, or decisions that previously failed.

### 3. What Worked Before
List approaches that previously helped resolve the issue.

### 4. Recommended Next Steps
Give practical, ordered investigation or remediation steps.
"""

    response = groq.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are REMEDY, an AI assistant for organizational incident learning.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return memory_items, response.choices[0].message.content


def severity_for_text(text):
    t = text.lower()
    if any(x in t for x in ["payment", "database", "production", "outage", "security", "data loss"]):
        return "High"
    if any(x in t for x in ["login", "api", "deployment", "error"]):
        return "Medium"
    return "Low"


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🧠 REMEDY</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-sub">Enterprise Incident Intelligence<br>Memory-driven operational learning</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="nav-caption">Workspace</div>', unsafe_allow_html=True)

    pages = [
        ("⌂", "Command Center"),
        ("🔎", "Investigate"),
        ("🗂", "Incident History"),
        ("🧠", "Memory Explorer"),
        ("📊", "Insights"),
        ("⚙", "System"),
    ]

    for icon, page in pages:
        if st.button(
            f"{icon}  {page}",
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if st.session_state.page == page else "secondary",
        ):
            st.session_state.page = page
            st.rerun()

    st.markdown('<div class="nav-caption">Live services</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="status-panel">
            <div class="status-line">
                <span><span class="online"></span>Memory engine</span>
                <b>Hindsight</b>
            </div>
            <div class="status-line">
                <span><span class="online"></span>Reasoning</span>
                <b>Groq</b>
            </div>
            <div class="status-line">
                <span><span class="online"></span>Memory bank</span>
                <b>Active</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="nav-caption">Environment</div>', unsafe_allow_html=True)
    st.caption("REMEDY / Demo Workspace")
    st.caption("Memory bank: " + BANK_ID)
    st.caption("AI mode: Historical reasoning")


# ============================================================
# TOP BAR
# ============================================================
c1, c2, c3, c4 = st.columns([2.2, 1.2, 1.2, 1.2])
with c1:
    st.markdown(
        '<div class="commandbar"><span class="command-item">WORKSPACE / <b>INCIDENT OPERATIONS</b></span></div>',
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        '<div class="commandbar"><span class="command-item">STATUS / <b style="color:#16a34a">● OPERATIONAL</b></span></div>',
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        '<div class="commandbar"><span class="command-item">MEMORY / <b>CONNECTED</b></span></div>',
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        '<div class="commandbar"><span class="command-item">VERSION / <b>1.0 DEMO</b></span></div>',
        unsafe_allow_html=True,
    )


# ============================================================
# COMMAND CENTER
# ============================================================
if st.session_state.page == "Command Center":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Enterprise Incident Intelligence</div>
            <h1>Fix it once.<br><span>Remember forever.</span></h1>
            <p>
                REMEDY connects today's incidents with your organization's
                historical experience, helping engineering teams investigate
                recurring failures without starting from zero.
            </p>
        </div>

        <div class="workflow">
            <div class="step">01 · Detect incident</div><div class="arrow">→</div>
            <div class="step">02 · Retrieve memory</div><div class="arrow">→</div>
            <div class="step">03 · Reason with AI</div><div class="arrow">→</div>
            <div class="step">04 · Recommend action</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(
            f'<div class="kpi"><div class="kpi-label">Incidents analyzed</div><div class="kpi-value">{len(st.session_state.incidents)}</div><div class="kpi-delta">This workspace</div></div>',
            unsafe_allow_html=True,
        )
    with k2:
        total_memory = sum(len(i["memories"]) for i in st.session_state.incidents)
        st.markdown(
            f'<div class="kpi"><div class="kpi-label">Historical evidence</div><div class="kpi-value">{total_memory}</div><div class="kpi-delta">Retrieved memories</div></div>',
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            '<div class="kpi"><div class="kpi-label">AI layers</div><div class="kpi-value">02</div><div class="kpi-delta">Recall + reasoning</div></div>',
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            '<div class="kpi"><div class="kpi-label">Memory bank</div><div class="kpi-value">LIVE</div><div class="kpi-delta">remedy-memory</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1.65, 1], gap="large")

    with left:
        st.markdown(
            """
            <div class="card">
                <div class="kicker">Start investigation</div>
                <div class="card-title">What is happening right now?</div>
                <div class="card-sub">
                    Describe the technical incident. REMEDY searches organizational memory before generating guidance.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        examples = [
            "Payment API is failing because database connections are exhausted.",
            "Production deployment caused a sudden spike in 500 errors.",
            "Users cannot log in after today's authentication service update.",
        ]

        ecols = st.columns(3)
        for i, ex in enumerate(examples):
            with ecols[i]:
                if st.button(f"Example {i+1}", key=f"dash_ex_{i}", use_container_width=True):
                    st.session_state.question = ex
                    st.session_state.page = "Investigate"
                    st.rerun()

        q = st.text_area(
            "Incident description",
            value=st.session_state.question,
            placeholder="Include service, symptoms, recent changes, errors, impact, and anything already tried...",
            height=145,
        )
        st.session_state.question = q

        if st.button("🧠  Investigate with REMEDY", type="primary", use_container_width=True):
            if not q.strip():
                st.warning("Describe the incident first.")
            else:
                with st.spinner("Retrieving organizational memory and reasoning..."):
                    try:
                        memories, answer = run_investigation(q)
                        st.session_state.memories = memories
                        st.session_state.answer = answer
                        st.session_state.last_run = datetime.now().strftime("%H:%M:%S")
                        st.session_state.history.append(q)
                        add_incident(q, memories, answer)
                        st.session_state.page = "Investigate"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Investigation failed: {e}")

    with right:
        st.markdown(
            """
            <div class="card">
                <div class="kicker">Operational model</div>
                <div class="card-title">Why REMEDY?</div>
                <div class="card-sub">The interface makes the AI's evidence chain visible instead of presenting a black-box answer.</div>
                <br>
                <div class="insight">
                    <div class="insight-title">🧠 Memory before generation</div>
                    <div class="insight-text">Historical organizational experience is retrieved before the reasoning layer responds.</div>
                </div>
                <div class="insight" style="margin-top:10px;">
                    <div class="insight-title">🔍 Evidence-aware guidance</div>
                    <div class="insight-text">Past failures and successful approaches are separated from current recommendations.</div>
                </div>
                <div class="insight" style="margin-top:10px;">
                    <div class="insight-title">⚡ Faster incident learning</div>
                    <div class="insight-text">Teams can start from what the organization already learned instead of repeating investigation from zero.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.incidents:
        st.markdown(
            '<div class="card"><div class="kicker">Latest activity</div><div class="card-title">Incident activity</div></div>',
            unsafe_allow_html=True,
        )

        for incident in st.session_state.incidents[-3:][::-1]:
            sev = severity_for_text(incident["question"])
            pill = "pill-red" if sev == "High" else "pill-amber" if sev == "Medium" else "pill-green"
            st.markdown(
                f"""
                <div class="card card-tight">
                    <span class="pill {pill}">{sev}</span>
                    <b style="margin-left:8px;font-size:12px;">{esc(incident["id"])}</b>
                    <div style="font-size:12px;color:#334155;margin-top:8px;">{esc(incident["title"])}</div>
                    <div style="font-size:9px;color:#94a3b8;margin-top:6px;">{esc(incident["time"])} · {len(incident["memories"])} memories retrieved</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# INVESTIGATE
# ============================================================
elif st.session_state.page == "Investigate":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Investigation Workspace</div>
            <h1>Understand the <span>failure.</span></h1>
            <p>Move from incident symptoms to historical evidence and practical next actions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.answer:
        st.info("No investigation has been run yet. Enter an incident below to begin.")

    q = st.text_area(
        "Current incident",
        value=st.session_state.question,
        height=130,
        placeholder="Describe the incident...",
    )
    st.session_state.question = q

    b1, b2, b3 = st.columns([1.1, .75, .75])
    with b1:
        investigate = st.button("🧠 Run investigation", type="primary", use_container_width=True)
    with b2:
        if st.button("Clear", use_container_width=True):
            st.session_state.answer = None
            st.session_state.memories = []
            st.session_state.question = ""
            st.rerun()
    with b3:
        if st.button("← Command Center", use_container_width=True):
            st.session_state.page = "Command Center"
            st.rerun()

    if investigate:
        if not q.strip():
            st.warning("Enter an incident.")
        else:
            with st.spinner("Searching memory → reasoning → generating guidance..."):
                try:
                    memories, answer = run_investigation(q)
                    st.session_state.memories = memories
                    st.session_state.answer = answer
                    st.session_state.last_run = datetime.now().strftime("%H:%M:%S")
                    st.session_state.history.append(q)
                    add_incident(q, memories, answer)
                    st.rerun()
                except Exception as e:
                    st.error(f"Investigation failed: {e}")

    if st.session_state.answer:
        st.divider()

        tabs = st.tabs(["🎯 Executive View", "🧠 Evidence", "🔬 Full Analysis"])

        with tabs[0]:
            a, b, c = st.columns(3)
            with a:
                st.markdown(
                    f'<div class="kpi"><div class="kpi-label">Severity signal</div><div class="kpi-value">{severity_for_text(q)}</div><div class="kpi-delta">Derived from incident text</div></div>',
                    unsafe_allow_html=True,
                )
            with b:
                st.markdown(
                    f'<div class="kpi"><div class="kpi-label">Evidence retrieved</div><div class="kpi-value">{len(st.session_state.memories)}</div><div class="kpi-delta">Historical memories</div></div>',
                    unsafe_allow_html=True,
                )
            with c:
                st.markdown(
                    f'<div class="kpi"><div class="kpi-label">Last analysis</div><div class="kpi-value">{st.session_state.last_run or "—"}</div><div class="kpi-delta">Current session</div></div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            l, r = st.columns([1.55, 1], gap="large")
            with l:
                st.markdown(
                    '<div class="card"><div class="kicker">Recommendation</div><div class="card-title">AI incident analysis</div></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(st.session_state.answer)

            with r:
                st.markdown(
                    '<div class="card"><div class="kicker">Decision trail</div><div class="card-title">How REMEDY reached this</div></div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    """
                    <div class="timeline">
                        <div class="event">
                            <div class="event-title">Incident captured</div>
                            <div class="event-meta">Current technical context received</div>
                        </div>
                        <div class="event">
                            <div class="event-title">Historical memory searched</div>
                            <div class="event-meta">Hindsight organizational memory</div>
                        </div>
                        <div class="event">
                            <div class="event-title">Evidence synthesized</div>
                            <div class="event-meta">Past failures + successful approaches</div>
                        </div>
                        <div class="event">
                            <div class="event-title">Action guidance generated</div>
                            <div class="event-meta">Groq reasoning layer</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with tabs[1]:
            st.markdown(
                f"""
                <div class="card">
                    <div class="kicker">Organizational evidence</div>
                    <div class="card-title">{len(st.session_state.memories)} historical memories retrieved</div>
                    <div class="card-sub">These memories were retrieved before the AI generated its response.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.session_state.memories:
                for idx, memory in enumerate(st.session_state.memories, 1):
                    st.markdown(
                        f"""
                        <div class="evidence">
                            <div class="evidence-tag">Evidence {idx:02d} · Historical memory</div>
                            {esc(memory)}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    '<div class="alert-box alert-warning">No relevant historical experience was retrieved. Recommendations should be treated as current reasoning rather than organizational precedent.</div>',
                    unsafe_allow_html=True,
                )

        with tabs[2]:
            st.markdown(
                '<div class="card"><div class="kicker">Detailed reasoning output</div><div class="card-title">REMEDY analysis</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown(st.session_state.answer)


# ============================================================
# INCIDENT HISTORY
# ============================================================
elif st.session_state.page == "Incident History":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Operational Memory</div>
            <h1>Incident <span>History.</span></h1>
            <p>A searchable session-level view of investigations performed in this workspace.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.incidents:
        st.info("No incidents have been analyzed in this session yet.")
    else:
        search = st.text_input("Search incidents", placeholder="Search by incident description or ID...")

        filtered = st.session_state.incidents
        if search:
            s = search.lower()
            filtered = [
                x for x in filtered
                if s in x["question"].lower() or s in x["id"].lower()
            ]

        st.markdown(
            f'<div class="card"><div class="kicker">Records</div><div class="card-title">{len(filtered)} incidents</div></div>',
            unsafe_allow_html=True,
        )

        for incident in filtered[::-1]:
            sev = severity_for_text(incident["question"])
            pill = "pill-red" if sev == "High" else "pill-amber" if sev == "Medium" else "pill-green"

            with st.expander(f"{incident['id']}  ·  {incident['title']}"):
                c1, c2 = st.columns([2.2, 1])
                with c1:
                    st.markdown(
                        f'<span class="pill {pill}">{sev}</span> &nbsp; <span style="color:#64748b;font-size:10px">{incident["time"]}</span>',
                        unsafe_allow_html=True,
                    )
                    st.markdown("**Incident**")
                    st.write(incident["question"])
                with c2:
                    st.metric("Memories", len(incident["memories"]))

                st.markdown("**Analysis**")
                st.markdown(incident["answer"])

                if st.button("Open in investigation", key=f"open_{incident['id']}"):
                    st.session_state.question = incident["question"]
                    st.session_state.answer = incident["answer"]
                    st.session_state.memories = incident["memories"]
                    st.session_state.page = "Investigate"
                    st.rerun()


# ============================================================
# MEMORY EXPLORER
# ============================================================
elif st.session_state.page == "Memory Explorer":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Organizational Knowledge</div>
            <h1>Memory <span>Explorer.</span></h1>
            <p>Query the organizational memory layer directly and inspect what historical context is available.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    q = st.text_input(
        "Search organizational memory",
        placeholder="e.g. database connection failures, authentication incidents, deployment rollback...",
    )

    if st.button("🔎 Search memory", type="primary", use_container_width=True):
        if not q.strip():
            st.warning("Enter a memory search query.")
        else:
            with st.spinner("Searching organizational memory..."):
                try:
                    result = hindsight.recall(bank_id=BANK_ID, query=q)
                    found = [m.text for m in result.results]
                    st.session_state.memories = found
                except Exception as e:
                    st.error(f"Memory search failed: {e}")

    if st.session_state.memories:
        st.markdown(
            f'<div class="card"><div class="kicker">Memory results</div><div class="card-title">{len(st.session_state.memories)} memories available</div></div>',
            unsafe_allow_html=True,
        )

        for idx, memory in enumerate(st.session_state.memories, 1):
            st.markdown(
                f"""
                <div class="evidence">
                    <div class="evidence-tag">Memory {idx:02d}</div>
                    {esc(memory)}
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# INSIGHTS
# ============================================================
elif st.session_state.page == "Insights":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Operational Intelligence</div>
            <h1>Team <span>Insights.</span></h1>
            <p>Turn incident activity into a high-level view of recurring operational themes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total = len(st.session_state.incidents)
    high = sum(severity_for_text(x["question"]) == "High" for x in st.session_state.incidents)
    medium = sum(severity_for_text(x["question"]) == "Medium" for x in st.session_state.incidents)
    low = sum(severity_for_text(x["question"]) == "Low" for x in st.session_state.incidents)

    a, b, c, d = st.columns(4)
    metrics = [
        ("Investigations", total, "Session"),
        ("High signals", high, "Text-derived"),
        ("Medium signals", medium, "Text-derived"),
        ("Low signals", low, "Text-derived"),
    ]

    for col, (label, value, sub) in zip([a,b,c,d], metrics):
        with col:
            st.markdown(
                f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-delta">{sub}</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    l, r = st.columns(2)

    with l:
        st.markdown(
            """
            <div class="card">
                <div class="kicker">Operating model</div>
                <div class="card-title">Memory-driven learning loop</div>
                <div class="timeline">
                    <div class="event"><div class="event-title">Capture</div><div class="event-meta">Record the current incident context.</div></div>
                    <div class="event"><div class="event-title">Recall</div><div class="event-meta">Retrieve relevant organizational experience.</div></div>
                    <div class="event"><div class="event-title">Reason</div><div class="event-meta">Compare historical failures and successful approaches.</div></div>
                    <div class="event"><div class="event-title">Act</div><div class="event-meta">Generate practical investigation steps.</div></div>
                    <div class="event"><div class="event-title">Learn</div><div class="event-meta">Feed resolved incidents back into organizational memory.</div></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with r:
        st.markdown(
            """
            <div class="card">
                <div class="kicker">Hackathon story</div>
                <div class="card-title">From reactive support to institutional memory</div>
                <br>
                <div class="alert-box alert-info">
                    <b>Problem:</b> Engineering teams repeatedly solve similar failures because useful context is scattered across people, tickets, and old incidents.
                </div>
                <div class="alert-box alert-info">
                    <b>REMEDY:</b> Retrieve the organization's prior experience before generating a recommendation.
                </div>
                <div class="alert-box alert-info">
                    <b>Outcome:</b> Make historical learning visible at the exact moment a team is investigating a new incident.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# SYSTEM
# ============================================================
elif st.session_state.page == "System":

    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Platform Configuration</div>
            <h1>System <span>Status.</span></h1>
            <p>REMEDY's connected services and runtime configuration.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="card">
                <div class="kicker">Memory layer</div>
                <div class="card-title">Hindsight</div>
                <br>
                <div class="status-panel" style="background:#f8fafc;border-color:#e2e8f0;">
                    <div class="status-line" style="color:#334155;">
                        <span>Connection</span><b style="color:#16a34a">● Active</b>
                    </div>
                    <div class="status-line" style="color:#334155;">
                        <span>Bank</span><b>{esc(BANK_ID)}</b>
                    </div>
                    <div class="status-line" style="color:#334155;">
                        <span>Role</span><b>Recall historical context</b>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="card">
                <div class="kicker">Reasoning layer</div>
                <div class="card-title">Groq</div>
                <br>
                <div class="status-panel" style="background:#f8fafc;border-color:#e2e8f0;">
                    <div class="status-line" style="color:#334155;">
                        <span>Connection</span><b style="color:#16a34a">● Active</b>
                    </div>
                    <div class="status-line" style="color:#334155;">
                        <span>Model</span><b>gpt-oss-120b</b>
                    </div>
                    <div class="status-line" style="color:#334155;">
                        <span>Role</span><b>Reason + recommend</b>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="card">
            <div class="kicker">Architecture</div>
            <div class="card-title">REMEDY request lifecycle</div>
            <br>
            <div class="workflow">
                <div class="step">User incident</div><div class="arrow">→</div>
                <div class="step">Hindsight recall</div><div class="arrow">→</div>
                <div class="step">Historical context</div><div class="arrow">→</div>
                <div class="step">Groq reasoning</div><div class="arrow">→</div>
                <div class="step">REMEDY guidance</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    '<div class="footer">REMEDY · ENTERPRISE INCIDENT INTELLIGENCE · MEMORY → REASONING → ACTION</div>',
    unsafe_allow_html=True,
)