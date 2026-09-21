from dataclasses import dataclass


@dataclass
class CustomerMessage:
    message: str


@dataclass
class Decision:
    category: str
    urgency: float
    escalate_probability: float


@dataclass
class EvaluationResult:
    message_id: int
    message: str
    expected_category: str
    predicted_category: str
    expected_urgency: float
    predicted_urgency: float
    expected_escalate: bool
    predicted_escalate: bool