"""Parse district responses from DELL printer interface."""
from bs4 import BeautifulSoup as bs

import aiohttp

from dell_printer_parser.const import (
    INFORMATION_URL,
    PRINT_VOLUME_URL,
    STATUS_URL,
)

from dell_printer_parser.model.information import Information
from dell_printer_parser.model.print_volume import PrintVolume
from dell_printer_parser.model.status import Status


class DellPrinterParser:
    def __init__(self, session: aiohttp.ClientSession, ip: str):
        self.session = session
        self.ip = ip
        self.information = Information()
        self.printVolume = PrintVolume()
        self.status = Status()
    
    async def load_data(self) -> None:
        """load all data and merge results."""
        await self._load_information()
        await self._load_print_volume()
        await self._load_status()

    async def _load_from_printer(self, url: str) -> str:
        # response = await self.session.get(self.base_url + url)
        get_url = "http://" + self.ip + url
        response = await self.session.request(method="GET", url=get_url)
        response.raise_for_status()
        body = await response.text()
        return body

    async def _load_information(self) -> None:
        data = await self._load_from_printer(INFORMATION_URL)
        self._extract_information(data)
    
    async def _load_print_volume(self) -> None:
        data = await self._load_from_printer(PRINT_VOLUME_URL)
        self._extract_print_volume(data)

    async def _load_status(self) -> None:
        data = await self._load_from_printer(STATUS_URL)
        self._extract_status(data)

    def _strip(self, text) -> str:
        """For whatever reason, BeautifulSoup doesn't do a beautful strip"""
        text = text.strip()
        if text[-2:] == '\\n':
            text = text[:-2]
        if text[:2] == '\\n':
            text = text[2:]
        return text.strip()
    

    def _extract_information(self, data) -> None:
        soup = bs(data, 'html.parser')

        self.information.modelName = self._strip(soup.title.string).lstrip("Dell ")

        data_items = soup.select_one("body > table > tr > td > table:nth-of-type(4) > tr > td > table")  
        self.information.dellServiceTagNumber = self._strip(data_items.select_one("tr:nth-of-type(1) > td:nth-of-type(2) > font").string)
        self.information.assetTagNumber = self._strip(data_items.select_one("tr:nth-of-type(2) > td:nth-of-type(2) > font").string)
        self.information.printerSerialNumber = self._strip(data_items.select_one("tr:nth-of-type(3) > td:nth-of-type(2) > font").string)
        self.information.memoryCapacity = self._strip(data_items.select_one("tr:nth-of-type(4) > td:nth-of-type(2) > font").string)
        self.information.processorSpeed = self._strip(data_items.select_one("tr:nth-of-type(5) > td:nth-of-type(2) > font").string)

        data_items = soup.select_one("body > table > tr > td > table:nth-of-type(5) > tr > td > table")
        self.information.firmwareVersion = self._strip(data_items.select_one("tr:nth-of-type(3) > td:nth-of-type(2) > font").get_text(" ", strip=True))
        self.information.networkFirmwareVersion = self._strip(data_items.select_one("tr:nth-of-type(4) > td:nth-of-type(2) > font").string)


    def _extract_print_volume(self, data) -> None:
        soup = bs(data, 'html.parser')
        
        data_items = soup.select_one("body > table > tr > td > table:nth-of-type(2) > tr > td > table")
        self.printVolume.printerPageCount = int(self._strip(data_items.select_one("tr > td:nth-of-type(2) > font").string))

        data_items = soup.select_one("body > table > tr > td > table:nth-of-type(3) > tr > td > table")
        self.printVolume.paperUsedLetter = int(self._strip(data_items.select_one("tr:nth-of-type(1) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedB5 = int(self._strip(data_items.select_one("tr:nth-of-type(2) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedA5 = int(self._strip(data_items.select_one("tr:nth-of-type(3) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedA4 = int(self._strip(data_items.select_one("tr:nth-of-type(4) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedExecutive = int(self._strip(data_items.select_one("tr:nth-of-type(5) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedFolio = int(self._strip(data_items.select_one("tr:nth-of-type(6) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedLegal = int(self._strip(data_items.select_one("tr:nth-of-type(7) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedEnvelope = int(self._strip(data_items.select_one("tr:nth-of-type(8) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedMonarch = int(self._strip(data_items.select_one("tr:nth-of-type(9) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedDL = int(self._strip(data_items.select_one("tr:nth-of-type(10) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedC5 = int(self._strip(data_items.select_one("tr:nth-of-type(11) > td:nth-of-type(2) > font").string))
        self.printVolume.paperUsedOthers = int(self._strip(data_items.select_one("tr:nth-of-type(12) > td:nth-of-type(2) > font").string))


    def _extract_status(self, data) -> None:
        soup = bs(data, 'html.parser')

        data_items = soup.select_one("body > table > tr > td > table:nth-of-type(4) > tr > td > table")
        self.status.cyanLevel = int(int(data_items.select_one("tr:nth-of-type(3) > td > table > tr > td")['width']) / 2)
        self.status.magentaLevel = int(int(data_items.select_one("tr:nth-of-type(5) > td > table > tr > td")['width']) / 2)
        self.status.yellowLevel = int(int(data_items.select_one("tr:nth-of-type(7) > td > table > tr > td")['width']) / 2)
        self.status.blackLevel = int(int(data_items.select_one("tr:nth-of-type(9) > td > table > tr > td")['width']) / 2)

        data_items = soup.select_one("body > table > tr > td > table:nth-of-type(5) > tr > td > table")
        self.status.multiPurposeFeederStatus = self._strip(data_items.select_one("tr:nth-of-type(2) > td:nth-of-type(2) > b").string)
        self.status.multiPurposeFeederCapacity = self._strip(data_items.select_one("tr:nth-of-type(2) > td:nth-of-type(3)").string)
        self.status.multiPurposeFeederSize = self._strip(data_items.select_one("tr:nth-of-type(2) > td:nth-of-type(4)").string)

        data_items = soup.select_one("body > table > tr > td > table:nth-of-type(6) > tr > td > table")
        self.status.outputTrayStatus = self._strip(data_items.select_one("tr:nth-of-type(2) > td:nth-of-type(2) > b").string)
        self.status.outputTrayCapacity = self._strip(data_items.select_one("tr:nth-of-type(2) > td:nth-of-type(3)").string)
 
        data_items = soup.select_one("body > table > tr > td > table:nth-of-type(7) > tr > td > table")
        self.status.rearCoverStatus = self._strip(data_items.select_one("tr:nth-of-type(2) > td:nth-of-type(2) > b").string)
        self.status.adfCoverStatus = self._strip(data_items.select_one("tr:nth-of-type(3) > td:nth-of-type(2) > b").string)

        data_items = soup.select_one("body > table > tr > td > table:nth-of-type(8) > tr > td > table")
        self.status.printerType = self._strip(data_items.select_one("tr:nth-of-type(1) > td:nth-of-type(2)").string)
        self.status.printingSpeed = self._strip(data_items.select_one("tr:nth-of-type(2) > td:nth-of-type(2)").get_text(" ", strip=True))
