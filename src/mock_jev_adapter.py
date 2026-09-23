from src.decision_provider import DecisionProvider
from src.models import CustomerMessage, Decision


class MockJevAdapter(DecisionProvider):
    """
    Rule-based baseline.

    This is intentionally NOT an AI model.
    It gives us something measurable to compare
    against Jev later.
    """

    def analyze(
        self,
        message: CustomerMessage
    ) -> Decision:

        text = message.message.lower()

        # -------------------------------------------------
        # GENERAL — informational payment questions
        # -------------------------------------------------

        if (
            "payment methods" in text
            or "do you accept" in text
            or "support international payments" in text
        ):
            return Decision(
                category="general",
                urgency=1.0,
                escalate_probability=0.05,
            )

        # -------------------------------------------------
        # GENERAL — informational subscription questions
        # -------------------------------------------------

        if (
            "how your subscription works" in text
            or "how does your subscription work" in text
        ):
            return Decision(
                category="general",
                urgency=1.0,
                escalate_probability=0.05,
            )

        # -------------------------------------------------
        # BILLING
        # -------------------------------------------------

        billing_signals = [
            "charged",
            "charge",
            "refund",
            "payment",
            "credit card",
            "purchased",
            "purchase",
            "subscription",
        ]

        if any(
            signal in text
            for signal in billing_signals
        ):

            if (
                "charged three times" in text
                or "charged twice" in text
                or "charged but" in text
                or "nobody has responded" in text
            ):
                return Decision(
                    category="billing",
                    urgency=4.0,
                    escalate_probability=0.90,
                )

            return Decision(
                category="billing",
                urgency=2.0,
                escalate_probability=0.20,
            )

        # -------------------------------------------------
        # TECHNICAL
        # -------------------------------------------------

        technical_signals = [
            "crash",
            "crashes",
            "error",
            "bug",
            "down",
            "unavailable",
            "broken",
            "broke",
            "upload",
        ]

        if any(
            signal in text
            for signal in technical_signals
        ):

            if (
                "completely down" in text
                or "unavailable for" in text
            ):
                return Decision(
                    category="technical",
                    urgency=4.0,
                    escalate_probability=0.90,
                )

            return Decision(
                category="technical",
                urgency=3.0,
                escalate_probability=0.30,
            )

        # -------------------------------------------------
        # GENERAL — fallback
        # -------------------------------------------------

        return Decision(
            category="general",
            urgency=1.5,
            escalate_probability=0.10,
        )