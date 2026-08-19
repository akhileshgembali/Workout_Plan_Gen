import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(
    page_title="FitnessPlanet | Workout Plan Generator",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --ink: #17201d;
        --muted: #68746d;
        --paper: #f5f4ee;
        --panel: #fffef9;
        --lime: #c9f269;
        --line: #d9ddd3;
        --coral: #ef755f;
    }

    .stApp {
        background: var(--paper);
        color: var(--ink);
        font-family: 'Space Grotesk', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: #e7eadf;
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 2rem; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; letter-spacing: 0; }
    h1 { font-size: clamp(2.8rem, 7vw, 6.8rem); line-height: .92; margin: .3rem 0 1rem; }
    h2 { font-size: 1.8rem; }
    .eyebrow, .mono { font-family: 'DM Mono', monospace; text-transform: uppercase; letter-spacing: 0; }
    .eyebrow { color: var(--coral); font-size: .75rem; font-weight: 500; }
    .hero-copy { color: var(--muted); font-size: 1.1rem; max-width: 40rem; line-height: 1.5; }
    .hero-rule { border-top: 1px solid var(--line); margin: 2rem 0 2.5rem; }
    .section-label { font-family: 'DM Mono', monospace; font-size: .72rem; color: var(--muted); margin-bottom: 1rem; }
    .field-label { color: var(--ink); font-size: .92rem; font-weight: 600; margin: 1rem 0 .35rem; }
    .field-label:first-of-type { margin-top: 0; }
    .brand { font-size: 2rem; font-weight: 700; letter-spacing: -.08rem; }
    .sidebar-note { color: var(--muted); font-size: .9rem; line-height: 1.45; margin-top: 3rem; }
    .stButton > button { background: var(--ink); color: white; border: 0; border-radius: 0; min-height: 3rem; font-weight: 600; }
    .stButton > button:hover { background: var(--coral); color: white; }
    [data-testid="stDownloadButton"] > button {
        background: #000000;
        color: #ffffff;
        border-color: #000000;
    }
    [data-testid="stDownloadButton"] > button:hover,
    [data-testid="stDownloadButton"] > button:focus,
    [data-testid="stDownloadButton"] > button:active {
        background: #000000;
        color: #ffffff;
        border-color: #000000;
    }
    [data-testid="stDownloadButton"] > button p {
        color: #ffffff;
    }
    [data-testid="stTextArea"] textarea { color: white !important; }
    [data-testid="stMetric"] { background: transparent; border: 0; }
    .disclaimer { color: var(--muted); font-size: .78rem; line-height: 1.4; border-top: 1px solid var(--line); padding-top: 1rem; margin-top: 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def build_prompt(goal: str, experience: str, days: int, equipment: str, limitations: str) -> str:
    limitations_text = limitations.strip() or "None reported"
    return f"""You are an expert strength and conditioning coach. Create a safe, practical,
personalized weekly workout plan from these inputs:
- Fitness goal: {goal}
- Experience level: {experience}
- Days available per week: {days}
- Equipment access: {equipment}
- Injuries or limitations: {limitations_text}

Return markdown only. Start with a short plan overview, then give a day-by-day breakdown
for exactly {days} training day(s). For each training day include: warm-up, exercises in
an ordered list with sets x reps (and rest), and a brief cool-down. Include rest or active
recovery guidance for non-training days, progression advice, and one concise safety note.
Adapt every movement to the available equipment and limitations. Do not diagnose injuries;
recommend professional medical guidance when a limitation may require it."""


def generate_plan(goal: str, experience: str, days: int, equipment: str, limitations: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    if not api_key or api_key == "your_groq_api_key_here":
        raise ValueError("Add your Groq API key to the .env file before generating a plan.")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You create clear, evidence-informed workout plans."},
            {"role": "user", "content": build_prompt(goal, experience, days, equipment, limitations)},
        ],
        temperature=0.65,
        max_tokens=3000,
    )
    return response.choices[0].message.content or "The model returned an empty plan. Please try again."


with st.sidebar:
    st.markdown('<div class="brand">FitnessPlanet<span style="color:#ef755f">.</span></div>', unsafe_allow_html=True)
    st.markdown('<p class="mono" style="font-size:.7rem; color:#68746d">Personal training, generated</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sidebar-note">A training plan shaped around your goal, your schedule, and the equipment you actually have.</p>',
        unsafe_allow_html=True,
    )

st.title("Train with intent.")
st.markdown('<p class="hero-copy">Tell us what you are working toward. FitnessPlanet will map the week into a plan you can actually follow.</p>', unsafe_allow_html=True)
st.markdown('<div class="hero-rule"></div>', unsafe_allow_html=True)

form_column, output_column = st.columns([0.9, 1.4], gap="large")
with form_column:
    st.markdown('<div class="section-label">Your training profile</div>', unsafe_allow_html=True)
    st.markdown('<div class="field-label">Fitness goal</div>', unsafe_allow_html=True)
    goal = st.selectbox("Fitness goal", ["Build muscle", "Lose fat", "General fitness", "Improve endurance"], label_visibility="collapsed")
    st.markdown('<div class="field-label">Experience level</div>', unsafe_allow_html=True)
    experience = st.selectbox("Experience level", ["Beginner", "Intermediate", "Advanced"], label_visibility="collapsed")
    st.markdown('<div class="field-label">Days available per week</div>', unsafe_allow_html=True)
    days = st.slider("Days available per week", min_value=1, max_value=7, value=3, label_visibility="collapsed")
    st.markdown('<div class="field-label">Equipment access</div>', unsafe_allow_html=True)
    equipment = st.selectbox("Equipment access", ["No equipment", "Home dumbbells", "Full gym"], label_visibility="collapsed")
    st.markdown('<div class="field-label">Injuries or limitations (optional)</div>', unsafe_allow_html=True)
    limitations = st.text_area(
        "Injuries or limitations (optional)",
        placeholder="e.g. bad knees, no overhead pressing",
        height=100,
        label_visibility="collapsed",
    )
    generate = st.button("Generate plan  →", use_container_width=True, type="primary")
    st.markdown('<p class="disclaimer">This is general fitness information, not medical advice. Stop if you feel pain and consult a qualified professional about injuries or health conditions.</p>', unsafe_allow_html=True)

with output_column:
    if generate:
        with st.spinner("Building your plan..."):
            try:
                plan = generate_plan(goal, experience, days, equipment, limitations)
            except Exception as error:
                st.error(str(error))
            else:
                st.markdown(plan)
                st.download_button(
                    "Download plan",
                    data=plan,
                    file_name="forge-workout-plan.md",
                    mime="text/markdown",
                )
    else:
        st.markdown("### Your plan will appear here once you Generate Plan")
        st.markdown("Complete your profile and generate a week built for your current goal.")
