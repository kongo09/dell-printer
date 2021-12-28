import pytest
from dell_printer_parser.model.print_volume import PrintVolume

@pytest.mark.asyncio
async def test_print_volume():
    printVolume = PrintVolume()
    printVolume.printerPageCount = 194
    assert "PrintVolume(printer page count=194)" == printVolume.__str__()
