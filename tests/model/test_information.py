import pytest
from dell_printer_parser.model.information import Information

@pytest.mark.asyncio
async def test_informaiton():
    information = Information()
    information.dellServiceTagNumber = 'xd4e0vb3'
    information.printerSerialNumber = '0192837465'
    assert "Information(DELL service tag=xd4e0vb3, printer serial=0192837465)" == information.__str__()
