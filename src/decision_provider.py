from abc import ABC, abstractmethod

from src.models import CustomerMessage, Decision

class DecisionProvider(ABC):

    @abstractmethod
    def analyze(self, message: CustomerMessage) -> Decision:
        pass