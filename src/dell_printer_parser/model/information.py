"""Status representation with all properties."""
from dataclasses import dataclass


@dataclass
class Information:
    modelName: str = None
    dellServiceTagNumber: str = None
    assetTagNumber: str = None
    printerSerialNumber: str = None
    memoryCapacity: str = None
    processorSpeed: str = None

    firmwareVersion: str = None
    networkFirmwareVersion: str = None


    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(DELL service tag={self.dellServiceTagNumber}, printer serial={self.printerSerialNumber})"
        )