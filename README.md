# Forge Workout Plan Generator

A single-page Streamlit app that generates personalized weekly workout plans with Groq.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Add your credentials in `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Start the app:

```powershell
streamlit run app.py
```
