import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel
from services.explainer import generate_explanation

# 1. Load the secrets from .env
load_dotenv()

# 2. Initialize the App
app = FastAPI(title="LearnFlow API")

# 3. Connect to Database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    print("❌ ERROR: Missing Supabase URL or Key in .env file")
else:
    print("✅ Supabase Credentials Loaded")

# Initialize Supabase Client
try:
    supabase: Client = create_client(url, key)
    print("✅ Connected to Supabase")
except Exception as e:
    print(f"❌ Failed to connect to Supabase: {e}")

# 4. The Health Check (To test if it works)
@app.get("/")
def read_root():
    return {"status": "active", "message": "LearnFlow Backend is Online 🚀"}

# 5. Test Database Connection Endpoint
@app.get("/test-db")
def test_db():
    try:
        # Fetch the first row from 'profiles' just to see if we can read data
        response = supabase.table("profiles").select("*").limit(1).execute()
        return {"db_status": "connected", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- NEW: AI Endpoint ---

class ExplainRequest(BaseModel):
    text: str
    interests: list = ["general"]
    book_type: str = "general"

@app.post("/api/explain")
def explain_text(request: ExplainRequest):
    print(f"🧠 Generating explanation for: {request.book_type}")
    
    result = generate_explanation(
        content=request.text,
        interests=request.interests,
        book_type=request.book_type
    )
    
    return result

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)