import aiohttp
import pytest

from dell_printer_parser.const import STATUS_URL, INFORMATION_URL, PRINT_VOLUME_URL

LOCAL_TEST_IP = "192.168.0.20"

@pytest.mark.skip(reason="only works locally")
async def test_endpoint_status():
    """Test a status endpoint"""
    await _test_endpoint(STATUS_URL)

@pytest.mark.skip(reason="only works locally")
async def test_endpoint_information():
    """Test a status endpoint"""
    await _test_endpoint(INFORMATION_URL)

@pytest.mark.skip(reason="only works locally")
async def test_endpoint_print_volume():
    """Test a status endpoint"""
    await _test_endpoint(PRINT_VOLUME_URL)

async def _test_endpoint(url: str):
    """Test a given endpoint is returning data"""
    async with aiohttp.ClientSession() as session:
        server_url = "http://" + LOCAL_TEST_IP + url
        async with session.get(server_url) as response:
            assert response.status == 200

            body = await response.text()
            assert body is not None