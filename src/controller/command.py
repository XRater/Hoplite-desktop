from abc import ABC, abstractmethod


class Command(ABC):
    """Abstract class for user's commands."""

    @abstractmethod
    def execute(self, target):
        pass
