# RESUMEFORGE.AI Backend

A robust, free-tier friendly FastAPI backend ready to handle resume uploads, authentication, and multi-agent AI pipeline integration.

## Setup Instructions

1. **Create and Activate a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup:**
   Copy `.env.example` to `.env` and configure as needed.
   *(By default, the backend will gracefully fallback to SQLite and a dummy secret key)*

4. **Run the Server Locally:**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **API Documentation:**
   Once running, visit:
   - Swagger / OpenAPI Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
