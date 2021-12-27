from dell_printer_parser.model.status import Status

async def test_status():
    status = Status()
    status.printerType = "Color Laser"
    status.cyanLevel = "62"
    status.magentaLevel = "73"
    status.yellowLevel = "32"
    status.blackLevel = "99"
    assert "Status(printer type=Color Laser, cyan level=62, magenta level=73, yellow level=32, black level=99)" == status.__str__()
