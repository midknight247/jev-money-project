from fastapi import FastAPI
from pydantic import BaseModel

from src.decision_engine import DecisionEngine
from src.jev_adapter import JevAdapter
from src.models import CustomerMessage


ESCALATION_THRESHOLD = 0.5


app = FastAPI(
    title="JEV Support Triage API",
    version="0.1.0",
)


class MessageRequest(BaseModel):
    message: str


class DecisionResponse(BaseModel):
    category: str
    urgency: float
    escalation_probability: float
    action: str


engine = DecisionEngine(
    provider=JevAdapter()
)


def get_action(escalation_probability: float) -> str:
    if escalation_probability >= ESCALATION_THRESHOLD:
        return "ESCALATE"

    return "NORMAL SUPPORT"


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/analyze", response_model=DecisionResponse)
def analyze_message(request: MessageRequest):
    customer_message = CustomerMessage(
        message=request.message
    )

    decision = engine.analyze(
        customer_message
    )

    action = get_action(
        decision.escalate_probability
    )

    return DecisionResponse(
        category=decision.category,
        urgency=decision.urgency,
        escalation_probability=decision.escalate_probability,
        action=action,
    )
