import pytest
from os import stat
import aiohttp
from aioresponses import aioresponses

from dell_printer_parser.const import STATUS_URL, INFORMATION_URL, PRINT_VOLUME_URL
from dell_printer_parser.printer_parser import DellPrinterParser
from dell_printer_parser.model.information import Information
from dell_printer_parser.model.print_volume import PrintVolume
from dell_printer_parser.model.status import Status

FAKE_TEST_IP = "192.168.0.0"


@pytest.mark.asyncio
async def test_parsing_with_fake_data(response_information, response_printer_volume, response_status):
    """Test parsing with fake data loaded from fixture response files."""
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mocked:
            mocked.get("http://" + FAKE_TEST_IP + STATUS_URL, status=200, payload=response_status)
            mocked.get("http://" + FAKE_TEST_IP + INFORMATION_URL, status=200, payload=response_information)
            mocked.get("http://" + FAKE_TEST_IP + PRINT_VOLUME_URL, status=200, payload=response_printer_volume)

            printer_parser = DellPrinterParser(session, FAKE_TEST_IP)
            await printer_parser.load_data()

            _validate_status(printer_parser.status)
            _validate_information(printer_parser.information)
            _validate_print_volume(printer_parser.printVolume)

def _validate_status(status: Status) -> None:
    """Validate status against fixture"""
    assert status.blackLevel == 48
    assert status.cyanLevel == 60
    assert status.magentaLevel == 69
    assert status.yellowLevel == 59
    assert status.multiPurposeFeederStatus == "Bereit"
    assert status.multiPurposeFeederSize == "A4 (210 x 297 mm)"
    assert status.multiPurposeFeederCapacity == "150 sheets"
    assert status.outputTrayStatus == "OK"
    assert status.outputTrayCapacity == "150  sheets"
    assert status.printerType == "Color Laser"
    assert status.printingSpeed == "12 Pages/Minute (Color), 15 Pages/Minute (Monochrome)"
    assert status.adfCoverStatus == "Geschlossen"
    assert status.rearCoverStatus == "Geschlossen"

def _validate_information(information: Information) -> None:
    """Validate information against fixture"""
    assert information.assetTagNumber == ""
    assert information.dellServiceTagNumber == "GQXR3Y1"
    assert information.firmwareVersion == "01.22.00"
    assert information.memoryCapacity == "128MB"
    assert information.networkFirmwareVersion == "20110809150U"
    assert information.printerSerialNumber == "ZHJ020393"
    assert information.processorSpeed == "295Mhz"

def _validate_print_volume(printer_volume: PrintVolume) -> None:
    """Validate printer volume against fixture"""
    assert printer_volume.paperUsedA4 == 7167
    assert printer_volume.paperUsedA5 == 31
    assert printer_volume.paperUsedB5 == 0
    assert printer_volume.paperUsedC5 == 0
    assert printer_volume.paperUsedDL == 72
    assert printer_volume.paperUsedEnvelope == 2
    assert printer_volume.paperUsedExecutive == 0
    assert printer_volume.paperUsedFolio == 0
    assert printer_volume.paperUsedLegal == 0
    assert printer_volume.paperUsedLetter == 1573
    assert printer_volume.paperUsedMonarch == 0
    assert printer_volume.paperUsedOthers == 17
    assert printer_volume.printerPageCount == 8862