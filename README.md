\# SkillSync



SkillSync is a resume analysis tool that uses the \*\*Gemini 3 API\*\* to compare resumes with job descriptions, identify missing technical keywords commonly used by ATS systems, and provide practical, actionable suggestions to improve resume alignment.



---



\## What It Does



\- Extracts \*\*technical keywords\*\* from job descriptions using Gemini

\- Analyzes resumes to find \*\*matched and missing skills\*\*

\- Calculates an \*\*ATS-style match score\*\*

\- Generates \*\*AI-powered resume improvement suggestions\*\*

\- Runs with a \*\*privacy-first approach\*\* (resume stays client-side)



---



\## Gemini 3 API Usage



SkillSync uses the \*\*Gemini 3 API\*\* (via the 'gemini-flash-latest' model) for:



\- Extracting clean, technical keywords from job descriptions  

\- Generating contextual and actionable resume improvement suggestions  



All keyword-to-resume matching is performed \*\*deterministically in Python\*\* to avoid hallucinations and ensure reliable results.



---



\## How We Built It



\- Frontend: HTML, CSS, JavaScript

\- Backend: Python + FastAPI

\- AI: Google Gemini 3 API

\- Resume parsing: PDF.js

\- Visualization: Chart.js

\- API communication via REST and JSON



The frontend handles resume parsing and visualization, while the backend focuses on AI-powered analysis and suggestions.



---



\## How to Run Locally



1\. Clone this repository

2\. Create a '.env' file inside the 'backend' folder:

GEMINI\_API\_KEY=AIzaSyBZ0m\_WNrOSQS-CarQ0Sd3qIsC3lgsJfRw

3\. Start the backend server:

python -m uvicorn main:app --reload

4\. Open `frontend/index.html` in your browser



---



\## Why SkillSync



SkillSync helps job seekers understand \*\*exactly what technical skills are missing\*\* from their resumes and how to improve them, increasing their chances of passing automated screening systems.



---



\## Future Improvements



\- Semantic keyword matching

\- Resume section–specific suggestions

\- Resume version comparison

\- Deployed backend with authentication





