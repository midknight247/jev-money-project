from decision_provider import DecisionProvider
from mock_jev_adapter import MockJevAdapter
from models import CustomerMessage, Decision


class DecisionEngine:

    def __init__(self, provider: DecisionProvider | None = None):
        self.provider = provider or MockJevAdapter()

    def analyze(self, message: CustomerMessage) -> Decision:
        return self.provider.analyze(message)