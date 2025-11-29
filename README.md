# QA Agent Backend

This is the backend service for the Autonomous QA Agent, built with FastAPI.

## Deployment on Render

1.  Create a new **Web Service** on Render.
2.  Connect this repository.
3.  **Settings**:
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
    *   **Root Directory**: (Leave Blank)
4.  **Environment Variables**:
    *   `GROQ_API_KEY`: Your Groq API Key.
