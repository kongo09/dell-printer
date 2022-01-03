"""Status representation with all properties."""
from dataclasses import dataclass


@dataclass
class Events:
    eventLocation: str = None
    eventDetails: str = None


    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(event location={self.eventLocation}, event details={self.eventDetails})"
        )