from decision_engine import DecisionEngine
from jev_adapter import JevAdapter
from models import CustomerMessage

ESCALATION_THRESHOLD = 0.5



def analyze_message(engine, message):

    customer_message = CustomerMessage(
        message=message
    )

    decision = engine.analyze(
        customer_message
    )

    action = get_action(
    decision.escalate_probability
)

    return decision, action

def get_urgency_label(urgency):

    if urgency < 1.5:
        return "VERY LOW"
    elif urgency < 2.5:
        return "LOW"
    elif urgency < 3.5:
        return "MODERATE"
    elif urgency < 4.5:
        return "HIGH"
    else:
        return "CRITICAL"

def get_action(escalation_probability):

    if escalation_probability >= ESCALATION_THRESHOLD:
        return "ESCALATE"

    return "NORMAL SUPPORT"

def main():

    print("=" * 50)
    print("CUSTOMER SUPPORT DECISION ENGINE")
    print("=" * 50)

    engine = DecisionEngine(
        provider=JevAdapter()
    )

    while True:

        message = input(
            "\nEnter customer message "
            "(or type 'quit' to exit): "
        )

        if message.lower() == "quit":
            print("\nGoodbye.")
            break

        decision, action = analyze_message(
            engine,
            message
        )

        urgency_label = get_urgency_label(
            decision.urgency
        )

        print("\nDecision")
        print("-" * 50)

        print(
            f"Category: {decision.category}"
        )

        print(
            f"Urgency: {decision.urgency:.2f} / 5 "
            f"({urgency_label})"
        )

        print(
            f"Escalation probability: "
            f"{decision.escalate_probability:.0%}"
        )

        print(
            f"Action: {action}"
        )


if __name__ == "__main__":
    main()