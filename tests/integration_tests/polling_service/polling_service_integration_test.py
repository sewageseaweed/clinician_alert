import aiohttp
import sys
import unittest
from aiolimiter import AsyncLimiter
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from unittest.mock import patch
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from polling_service.polling_service import get_clinician
from data.clinician_zone_status import clinician_status_map

OUT_CLINICIAN_ID = 7
IN_CLINICIAN_ID = 1

class PollingServiceIntegrationTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        clinician_status_map[IN_CLINICIAN_ID] = {"in-zone": True, "error": False}
    
    async def test_out_of_zone_clinician_7(self):
        limiter = AsyncLimiter(max_rate=1, time_period=1)
        async with aiohttp.ClientSession() as client_session:
            with patch('email_service.send_email.smtplib.SMTP_SSL', autospec=True) as mock_smtp:
                try:
                    await get_clinician(client_session, limiter, OUT_CLINICIAN_ID)
                    mock_smtp.assert_called_once()
                    context = mock_smtp.return_value.__enter__.return_value
                    context.login.assert_called()
                    context.send_message.assert_called()
                    self.assertFalse(clinician_status_map[OUT_CLINICIAN_ID]["in-zone"])
                except Exception as _:
                    context = mock_smtp.return_value.__enter__.return_value
                    context.login.assert_called()
                    context.send_message.assert_called()

    async def test_api_response(self):
        limiter = AsyncLimiter(max_rate=1, time_period=1)
        async with aiohttp.ClientSession() as client_session:
            with patch('email_service.send_email.smtplib.SMTP_SSL', autospec=True) as mock_smtp:
                try:
                    res = await get_clinician(client_session, limiter, IN_CLINICIAN_ID)
                    if res:
                        self.assertTrue(clinician_status_map[IN_CLINICIAN_ID]["in-zone"])
                except Exception as _:
                    context = mock_smtp.return_value.__enter__.return_value
                    context.login.assert_called()
                    context.send_message.assert_called()
        
if __name__ == '__main__':
    load_dotenv(find_dotenv())
    unittest.main()