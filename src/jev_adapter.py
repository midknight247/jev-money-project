import os

from decision_provider import DecisionProvider
from models import CustomerMessage, Decision
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient


class JevAdapter(DecisionProvider):
    """
    Real TypeSafe/Jev implementation.

    Handles:
    - category classification
    - urgency scoring
    - escalation probability
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TYPESAFE_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "TYPESAFE_API_KEY is not configured."
            )

    def analyze(self, message: CustomerMessage) -> Decision:

        with TypeSafeClient(api_key=self.api_key) as client:

            response = client.system_one(
                state=message.message,
                questions={
                    "category": Choice(
                        instructions=(
                            "What is the primary category of this "
                            "customer support message?"
                        ),
                        criteria={
                            "billing": (
                                "The customer is reporting or asking about "
                                "an actual financial transaction or problem, "
                                "such as a charge, payment failure, refund, "
                                "unauthorized payment, or purchase."
                            ),
                            "technical": (
                                "The customer is reporting a software problem, "
                                "error, crash, outage, or broken functionality."
                            ),
                            "general": (
                                "The customer is asking for information or "
                                "account help without reporting a financial "
                                "transaction problem or a technical problem. "
                                "This includes questions about plans, subscription "
                                "renewal dates, features, policies, or how the "
                                "service works."
                            ),
                        },
                    ),
                    "urgency": Score(
    instructions=(
        "Assess the urgency of this customer support "
        "message. Focus on how immediately the customer "
        "needs the issue addressed, not merely how broken "
        "or technically severe the issue is."
    ),
    criteria=[
        (
            "Very low urgency. "
            "The message is informational or the customer "
            "can comfortably wait."
        ),
        (
            "Low urgency. "
            "There is a minor issue or inconvenience, with "
            "no stated immediate consequence or time pressure."
        ),
        (
            "Moderate urgency. "
            "The customer has a meaningful problem that "
            "affects their use of the service, but there is "
            "no clear immediate deadline, severe consequence, "
            "or urgent time pressure."
        ),
        (
            "High urgency. "
            "The problem significantly prevents the customer "
            "from working or using an important service "
            "function, especially when prompt resolution "
            "would materially reduce the impact."
        ),
        (
            "Critical urgency. "
            "There is an immediate and severe consequence, "
            "explicit urgent time pressure, or a broad outage "
            "that requires immediate attention."
        ),
    ],
),

                    "escalate": Noul(
                        instructions=(
                            "Does this situation require intervention "
                            "from a human support agent rather than being "
                            "handled through normal support?"
                        ),
                    ),
                },
            )

        category_answer = response.answers["category"]
        urgency_answer = response.answers["urgency"]
        escalate_answer = response.answers["escalate"]

        # Jev's Score uses positions 0–4.
        # Our Decision model uses a 1–5 urgency scale.
        urgency = urgency_answer.score + 1

        return Decision(
            category=category_answer.choice,
            urgency=urgency,
            escalate_probability=escalate_answer.noul,
        )