import os

from src.decision_provider import DecisionProvider
from src.models import CustomerMessage, Decision
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
        "Determine whether this customer support situation requires "
        "intervention from a human support agent rather than being "
        "handled through the normal support workflow.\n\n"

        "Escalation is warranted when the nature or circumstances of "
        "the issue indicate that normal support handling is insufficient.\n\n"

        "For BILLING issues, distinguish routine clarification from "
        "financial intervention:\n"
        "- Escalate unauthorized charges, duplicate charges, charges "
        "after cancellation, unexpected renewals requiring investigation, "
        "incorrect charges requiring correction, or disputed transactions "
        "that require investigation or human review.\n"
        "- Escalate when an automated billing or refund process has failed "
        "and human intervention is needed to resolve the financial issue.\n"
        "- Do not escalate routine questions about invoices, taxes, "
        "payment methods, billing amounts, refunds, or charges merely "
        "because the customer describes something as different, unexpected, "
        "wrong, or unclear.\n"
        "- Do not infer escalation solely from words such as 'charge', "
        "'refund', 'invoice', 'wrong', 'unexpected', or 'different'. "
        "Look for evidence that investigation, correction, dispute "
        "resolution, or human intervention is actually required.\n\n"

        "For TECHNICAL issues:\n"
        "- Escalate severe failures that prevent the customer from using "
        "a core or important function, even if the customer does not "
        "explicitly mention multiple users, production, or a deadline.\n"
        "- Escalate outages, persistent failures, severe crashes, or "
        "technical problems that materially block important work.\n"
        "- A technical issue does not need to affect an entire team or "
        "production system to warrant escalation if the affected function "
        "is essential and the customer cannot reasonably continue.\n"
        "- Do not escalate minor bugs, cosmetic issues, inconveniences, "
        "intermittent problems, or issues with a practical workaround "
        "unless other circumstances indicate that human intervention is "
        "necessary.\n\n"

        "For GENERAL or ACCOUNT issues:\n"
        "- Escalate when the customer explicitly requires human review "
        "or intervention, when normal account or recovery procedures "
        "cannot resolve the issue, or when the request has remained "
        "unresolved despite repeated attempts or an unusually long wait.\n"
        "- Do not escalate ordinary informational or administrative "
        "questions merely because they are time-sensitive or important "
        "to the customer.\n\n"

        "Urgency and escalation are related but separate judgments. "
        "A highly urgent issue does not automatically require escalation, "
        "and a low-urgency issue can still require escalation when human "
        "intervention is necessary.\n\n"

        "Base the decision on the actual circumstances described in the "
        "message. Do not infer escalation solely from the presence of "
        "billing language, technical language, urgency, or emotional "
        "language."
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

