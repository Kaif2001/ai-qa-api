import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, HTTPException
from google.genai import errors
from prometheus_client import Counter, generate_latest
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette.responses import Response

from app.auth import create_access_token, get_current_user
from app.database import get_db
from app.llm_gateway import generate_answer
from app.models import ChatHistory
from app.redis_client import redis_client

load_dotenv()

app = FastAPI()


chat_requests = Counter(
    "chat_requests_total",
    "Total number of chat requests",
)

chat_errors = Counter(
    "chat_errors_total",
    "Total number of chat errors",
)


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain",
    )


@app.post("/auth/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username != "admin" or password != "admin123":
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
    chat_requests.inc()

    rate_limit_key = f"chat_rate:{current_user}"

    request_count = redis_client.get(rate_limit_key)

    if request_count is None:
        redis_client.set(rate_limit_key, 1, ex=60)
    elif int(request_count) >= 10:
        chat_errors.inc()
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later.",
        )
    else:
        redis_client.incr(rate_limit_key)

    try:
        answer = generate_answer(request.question)

    except errors.RateLimitError:
        chat_errors.inc()
        raise HTTPException(
            status_code=429,
            detail="LLM rate limit exceeded. Please try again later.",
        )

    except Exception:
        chat_errors.inc()
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

    return {
        "user": current_user,
        "question": request.question,
        "answer": answer,
        "chat_id": chat_history.id,
    }