from decision_engine import DecisionEngine
from jev_adapter import JevAdapter
from models import CustomerMessage


engine = DecisionEngine(provider=JevAdapter())

message = CustomerMessage(
    message="I was charged twice for my subscription."
)

decision = engine.analyze(message)

print("Category:", decision.category)
print("Urgency:", decision.urgency)
print("Escalation:", decision.escalate_probability)