from abc import ABC, abstractmethod

from models import CustomerMessage, Decision


class DecisionProvider(ABC):

    @abstractmethod
    def analyze(self, message: CustomerMessage) -> Decision:
        pass