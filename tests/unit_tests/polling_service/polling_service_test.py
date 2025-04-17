import sys
import unittest
from aiolimiter import AsyncLimiter
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from unittest.mock import AsyncMock, patch
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from polling_service.polling_service import get_clinician
from data.clinician_zone_status import clinician_status_map

CLINICIAN_ID = 1

class PollingServiceTest(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        clinician_status_map[1] = {
        'in-zone': True,
        'error': False
    }
    
    @patch('aiohttp.ClientSession')
    async def test_successful_polling(self, mock_session):
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "features": [
                {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-122.3631693841, 37.5804219281]
                    }
                },
                {
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-122.3561525345, 37.5873025984],
                            [-122.3595428467, 37.5885948602],
                            [-122.3616886139, 37.5899211055],
                            [-122.3638343812, 37.5912813326],
                            [-122.3688554764, 37.5875746554],
                            [-122.3716449738, 37.5832556334],
                            [-122.367181778, 37.5780860808],
                            [-122.3595428467, 37.5750930179],
                            [-122.3482131959, 37.5847520158],
                            [-122.3503589631, 37.5869965331],
                            [-122.3561525345, 37.5873025984]
                        ]]
                    }
                }
            ]
        }
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        limiter = AsyncLimiter(max_rate = 96, time_period = 1)
        await get_clinician(mock_session, limiter, CLINICIAN_ID)
        
        self.assertTrue(clinician_status_map[CLINICIAN_ID]["in-zone"])
        mock_session.get.assert_called_once()

    @patch('aiohttp.ClientSession')
    async def test_out_of_zone_alert(self, mock_session):
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "features": [
                {"geometry": {"type": "Point", "coordinates": [-121.9433529854, 37.3198692754]}},
                {"geometry": {"type": "Polygon", "coordinates": [[
                    [-121.9346809388, 37.3363162561],
                    [-121.9624900818, 37.3361797698],
                    [-121.9652366639, 37.3046448047],
                    [-121.937084198, 37.3049178915],
                    [-121.9377708436, 37.3176153316],
                    [-121.9515037537, 37.3167962067],
                    [-121.9521903992, 37.3260791003],
                    [-121.937084198, 37.3264886133],
                    [-121.9346809388, 37.3363162561]]]}}
            ]
        }
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        limiter = AsyncLimiter(max_rate = 96, time_period = 1)

        with patch('email_service.send_email.smtplib.SMTP_SSL', autospec=True) as mock_smtp:
            await get_clinician(mock_session, limiter, CLINICIAN_ID)
            mock_smtp.assert_called_once()
            context = mock_smtp.return_value.__enter__.return_value
            context.login.assert_called()
            context.send_message.assert_called()
            self.assertFalse(clinician_status_map[CLINICIAN_ID]["in-zone"])
            
    @patch('aiohttp.ClientSession')
    async def test_api_server_error(self, mock_session):
        mock_response = AsyncMock()
        mock_response.json.return_value = {"error": "Internal server error"}
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        limiter = AsyncLimiter(max_rate = 96, time_period = 1)
        
        with patch('email_service.send_email.smtplib.SMTP_SSL', autospec=True) as mock_smtp:
            await get_clinician(mock_session, limiter, CLINICIAN_ID)
            mock_smtp.assert_called_once()
            context = mock_smtp.return_value.__enter__.return_value
            context.login.assert_called()
            context.send_message.assert_called()
            self.assertTrue(clinician_status_map[CLINICIAN_ID]["error"])

    @patch('aiohttp.ClientSession')
    async def test_missing_features_error(self, mock_session):
        mock_response = AsyncMock()
        mock_response.json.return_value = {} 
        mock_session.get.return_value.__aenter__.return_value = mock_response
        
        limiter = AsyncLimiter(max_rate = 96, time_period = 1)
        
        with patch('email_service.send_email.smtplib.SMTP_SSL', autospec=True) as mock_smtp:
            await get_clinician(mock_session, limiter, CLINICIAN_ID)
            mock_smtp.assert_called_once()
            context = mock_smtp.return_value.__enter__.return_value
            context.login.assert_called()
            context.send_message.assert_called()
            self.assertTrue(clinician_status_map[CLINICIAN_ID]["error"])


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    unittest.main()