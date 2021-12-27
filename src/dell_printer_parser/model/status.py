"""Status representation with all properties."""
from dataclasses import dataclass


@dataclass
class Status:
    cyanLevel: int = 0
    magentaLevel: int = 0
    yellowLevel: int = 0
    blackLevel: int = 0

    multiPurposeFeederStatus: str = None
    multiPurposeFeederCapacity: int = 0
    multiPurposeFeederSize: str = None
    outputTrayStatus: str = None
    outputTrayCapacity: int = 0
    rearCoverStatus: str = None
    adfCoverStatus: str = None

    printerType: str = None
    printingSpeed: str = None


    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(printer type={self.printerType}, cyan level={self.cyanLevel}, magenta level={self.magentaLevel}, yellow level={self.yellowLevel}, black level={self.blackLevel})"
        )