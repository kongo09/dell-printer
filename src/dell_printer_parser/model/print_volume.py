"""Print volume representation with all properties."""
from dataclasses import dataclass


@dataclass
class PrintVolume:
    printerPageCount: int = 0

    paperUsedLetter: int = 0
    paperUsedB5: int = 0
    paperUsedA5: int = 0
    paperUsedA4: int = 0
    paperUsedExecutive: int = 0
    paperUsedFolio: int = 0
    paperUsedLegal: int = 0
    paperUsedEnvelope: int = 0
    paperUsedMonarch: int = 0
    paperUsedDL: int = 0
    paperUsedC5: int = 0
    paperUsedOthers: int = 0


    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(printer page count={self.printerPageCount})"
        )