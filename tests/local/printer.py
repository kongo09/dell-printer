import aiohttp
import asyncio
from dell_printer_parser.printer_parser import DellPrinterParser

async def main():
    ip = "192.168.0.20"
    async with aiohttp.ClientSession() as session:
        dpp = DellPrinterParser(session, ip)
        await dpp.load_data()
        print(f"printer tag={dpp.information.dellServiceTagNumber}")


if (__name__ == '__main__'):
    asyncio.run(main())