import os
import json
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.genai as genai      # NEW SDK

# -----------------------------
# Load API Key
# -----------------------------
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3-flash-preview"


# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(title="Resume Analyzer Backend (Gemini Latest API)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# -----------------------------
# Request Models
# -----------------------------
class ExtractRequest(BaseModel):
    jd_text: str

class AnalyzeRequest(BaseModel):
    resume_text: str
    jd_keywords: List[str]

class SuggestRequest(BaseModel):
    missing_keywords: List[str]
    jd_text: str
    resume_text: str


# -----------------------------
# Helper: Clean AI JSON
# -----------------------------
def parse_ai_json(text: str):
    try:
        return json.loads(text)
    except:
        return None


# -----------------------------
# 1️⃣ Extract Keywords
# -----------------------------
@app.post("/extract_keywords")
async def extract_keywords(request: ExtractRequest):
    prompt = f"""
You are a strict technical skill extractor.

JOB DESCRIPTION:
{request.jd_text}

TASK:
Extract ONLY the *technical* skills:
- programming languages
- frameworks
- libraries
- tools
- ML/AI terms
- cloud, DevOps, DBs
- technical certifications

RULES:
- DO NOT include soft skills.
- DO NOT include generic words (“software”, “development”).
- DO NOT explain anything.
- Output strictly this JSON format:

{{
  "keywords": ["...", "..."]
}}
"""

    try:
        result = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        raw_text = result.text.strip()

        data = parse_ai_json(raw_text)
        if not data or "keywords" not in data:
            return {"keywords": []}

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# 2️⃣ Analyze Resume
# -----------------------------
@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        resume_text = request.resume_text.lower()

        matched = []
        missing = []

        for kw in request.jd_keywords:
            if kw.lower() in resume_text:
                matched.append(kw)
            else:
                missing.append(kw)

        score = round((len(matched) / len(request.jd_keywords)) * 100) if request.jd_keywords else 0

        return {
            "matched": matched,
            "missing": missing,
            "score": score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# 3️⃣ Suggest Improvements
# -----------------------------
@app.post("/suggest")
async def suggest(request: SuggestRequest):
    if not request.missing_keywords:
        return {"suggestions": ["Your resume perfectly covers all technical requirements!"]}

    prompt = f"""
You are a resume optimization expert.
Provide **specific and actionable** resume improvements.

MISSING KEYWORDS:
{request.missing_keywords}

JOB DESCRIPTION (shortened):
{request.jd_text[:700]}

RESUME (shortened):
{request.resume_text[:700]}

OUTPUT STRICTLY THIS JSON:
{{
  "suggestions": [
    "....",
    "...."
  ]
}}
"""

    try:
        result = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        raw_text = result.text.strip()

        data = parse_ai_json(raw_text)
        if not data or "suggestions" not in data:
            return {"suggestions": ["Consider adding a project involving: " + ", ".join(request.missing_keywords[:3])]}

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------
# Run local server
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
