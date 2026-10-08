import hashlib
import logging
import time
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.decision_engine import DecisionEngine
from src.jev_adapter import JevAdapter
from src.models import CustomerMessage


ESCALATION_THRESHOLD = 0.40


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger("jev")


# -----------------------------------------------------------------------------
# App
# -----------------------------------------------------------------------------

app = FastAPI(
    title="JEV Support Triage API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Models
# -----------------------------------------------------------------------------

class MessageRequest(BaseModel):
    message: str


class DecisionResponse(BaseModel):
    category: str
    urgency: float
    escalation_probability: float
    action: str


# -----------------------------------------------------------------------------
# Decision Engine
# -----------------------------------------------------------------------------

engine = DecisionEngine(
    provider=JevAdapter()
)


def get_action(escalation_probability: float) -> str:
    if escalation_probability >= ESCALATION_THRESHOLD:
        return "ESCALATE"

    return "NORMAL SUPPORT"


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/analyze", response_model=DecisionResponse)
def analyze_message(request: MessageRequest):
    request_id = str(uuid.uuid4())
    started_at = time.perf_counter()

    message_hash = hashlib.sha256(
        request.message.encode("utf-8")
    ).hexdigest()

    try:
        customer_message = CustomerMessage(
            message=request.message
        )

        decision = engine.analyze(
            customer_message
        )

        action = get_action(
            decision.escalate_probability
        )

        latency_ms = round(
            (time.perf_counter() - started_at) * 1000,
            2,
        )

        logger.info(
            "triage_request | "
            "request_id=%s | "
            "timestamp=%s | "
            "message_hash=%s | "
            "message_length=%d | "
            "category=%s | "
            "urgency=%.2f | "
            "escalation_probability=%.3f | "
            "action=%s | "
            "latency_ms=%.2f",
            request_id,
            datetime.now(timezone.utc).isoformat(),
            message_hash,
            len(request.message),
            decision.category,
            decision.urgency,
            decision.escalate_probability,
            action,
            latency_ms,
        )

        return DecisionResponse(
            category=decision.category,
            urgency=decision.urgency,
            escalation_probability=decision.escalate_probability,
            action=action,
        )

    except Exception:
        latency_ms = round(
            (time.perf_counter() - started_at) * 1000,
            2,
        )

        logger.exception(
            "triage_request_failed | "
            "request_id=%s | "
            "message_hash=%s | "
            "message_length=%d | "
            "latency_ms=%.2f",
            request_id,
            message_hash,
            len(request.message),
            latency_ms,
        )

        raise


@app.get("/")
def root():
    return {
        "name": "JEV Support Intelligence API",
        "status": "running",
        "docs": "/docs"
    }
