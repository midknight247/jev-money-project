from decision_engine import DecisionEngine
from mock_jev_adapter import MockJevAdapter
from models import CustomerMessage


def handle_decision(decision):
    if decision.escalate_probability >= 0.85:
        print("\n🚨 HUMAN REVIEW REQUIRED")

    elif decision.urgency >= 3:
        print("\n⚠️ HIGH PRIORITY")

    else:
        print("\n✅ NORMAL QUEUE")


def main():

    engine = DecisionEngine(
        provider=MockJevAdapter()
    )

    message = CustomerMessage(
        message="What payment methods do you accept?"
    )

    decision = engine.analyze(message)

    print("Customer message:")
    print(message.message)

    print("\nDecision:")
    print(f"Category: {decision.category}")
    print(f"Urgency: {decision.urgency}")
    print(
        f"Escalation probability: "
        f"{decision.escalate_probability:.2f}"
    )

    handle_decision(decision)


if __name__ == "__main__":
    main()
