import os
import time

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, HTTPException
from google.genai import errors
from prometheus_client import Counter, Histogram, generate_latest
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.auth import create_access_token, get_current_user
from app.database import SessionLocal, get_db
from app.llm_gateway import generate_answer
from app.models import ChatHistory
from app.redis_client import redis_client

load_dotenv()

app = FastAPI()

DEMO_USERNAME = os.getenv("DEMO_USERNAME", "admin")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "admin123")


chat_requests = Counter(
    "chat_requests_total",
    "Total number of chat requests",
)

chat_errors = Counter(
    "chat_errors_total",
    "Total number of chat errors",
)

chat_latency = Histogram(
    "chat_request_duration_seconds",
    "Chat request latency in seconds",
)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


@app.get("/health")
def health_check():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()

        redis_client.ping()

        return {
            "status": "healthy",
            "database": "connected",
            "redis": "connected",
        }

    except Exception:
        return Response(
            content='{"status":"unhealthy"}',
            status_code=503,
            media_type="application/json",
        )


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain",
    )


@app.post("/auth/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username != DEMO_USERNAME or password != DEMO_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = create_access_token(username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@app.post("/chat")
def chat(
    request: ChatRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    start_time = time.perf_counter()
    chat_requests.inc()

    rate_limit_key = f"chat_rate:{current_user}"

    request_count = redis_client.incr(rate_limit_key)

    if request_count == 1:
        redis_client.expire(rate_limit_key, 60)

    if request_count > 10:
        chat_errors.inc()
        chat_latency.observe(time.perf_counter() - start_time)

        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later.",
        )

    try:
        answer = generate_answer(request.question)

    except errors.RateLimitError:
        chat_errors.inc()
        chat_latency.observe(time.perf_counter() - start_time)

        raise HTTPException(
            status_code=429,
            detail="LLM rate limit exceeded. Please try again later.",
        )

    except Exception:
        chat_errors.inc()
        chat_latency.observe(time.perf_counter() - start_time)

        raise HTTPException(
            status_code=503,
            detail="LLM service is temporarily unavailable.",
        )

    chat_history = ChatHistory(
        username=current_user,
        question=request.question,
        answer=answer,
    )

    db.add(chat_history)
    db.commit()
    db.refresh(chat_history)

    chat_latency.observe(time.perf_counter() - start_time)

    return {
        "user": current_user,
        "question": request.question,
        "answer": answer,
        "chat_id": chat_history.id,
    }