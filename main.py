from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import httpx, os

app = FastAPI(title="CancerianMind API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST","GET"],
    allow_headers=["*"],
)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL      = "claude-sonnet-4-20250514"

THERAPY_SYSTEM = """You are CancerianMind, a compassionate psychology AI therapist.
Use CBT techniques, active listening, and mindfulness. Be warm and empathetic.
Keep responses to 3-4 sentences. Ask one open question per response.
Never diagnose or prescribe. Always be non-judgmental.
If mood is provided, acknowledge it naturally.
CRISIS: If user mentions suicide/self-harm/wanting to die — immediately provide:
iCall: 9152987821 | Vandrevala: 1860-2662-345 | NIMHANS: 080-46110007 | Emergency: 112"""

JOURNAL_SYSTEM = """You are a compassionate psychology AI. Analyze this journal entry in 1-2 sentences.
Identify the core emotion and provide a warm, encouraging insight using CBT or positive psychology principles.
Be concise, warm, and specific to what the person wrote. No generic responses."""

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    mood: str = ""

class JournalRequest(BaseModel):
    entry: str

async def call_claude(system: str, messages: list, max_tokens: int = 500) -> str:
    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")
    async with httpx.AsyncClient(timeout=30) as client:
        res = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": CLAUDE_MODEL,
                "max_tokens": max_tokens,
                "system": system,
                "messages": messages,
            }
        )
        if res.status_code != 200:
            raise HTTPException(status_code=502, detail="Claude API error")
        data = res.json()
        return data["content"][0]["text"]

@app.get("/")
def root():
    return {"status": "ok", "app": "CancerianMind API", "version": "1.0.0"}

@app.post("/chat")
async def chat(req: ChatRequest):
    system = THERAPY_SYSTEM
    if req.mood:
        system += f"\n\nUser's current mood: {req.mood}. Acknowledge this gently if relevant."
    msgs = [{"role": m.role, "content": m.content} for m in req.messages]
    reply = await call_claude(system, msgs, max_tokens=600)
    return {"reply": reply}

@app.post("/analyze")
async def analyze(req: JournalRequest):
    if not req.entry.strip():
        return {"insight": "Keep writing — every word is a step toward healing 🌱"}
    msgs = [{"role": "user", "content": f"Journal entry:\n{req.entry}"}]
    insight = await call_claude(JOURNAL_SYSTEM, msgs, max_tokens=150)
    return {"insight": insight}

@app.get("/health")
def health():
    return {"status": "healthy"}
