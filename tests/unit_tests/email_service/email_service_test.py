import smtplib
import sys
import unittest
from unittest.mock import patch
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from email_service.send_email import send_email

class EmailServiceTest(unittest.IsolatedAsyncioTestCase):

    @patch('email_service.send_email.smtplib.SMTP_SSL', autospec=True)
    async def test_send_email(self, mock_smtp):
        context = mock_smtp.return_value.__enter__.return_value
        
        await send_email("subject", "content")

        mock_smtp.assert_called()
        context.login.assert_called()
        context.send_message.assert_called()
        
    @patch('email_service.send_email.smtplib.SMTP_SSL', autospec=True)
    async def test_send_email_fail(self, mock_smtp):
        context = mock_smtp.return_value.__enter__.return_value
        context.send_message.side_effect = smtplib.SMTPException('Failed to send email')
        
        res = await send_email("Test", "Content")
        
        self.assertFalse(res)
        self.assertEqual(context.send_message.call_count, 3)
        self.assertEqual(context.login.call_count, 3)
        
        
    @patch('email_service.send_email.smtplib.SMTP_SSL', autospec=True)
    async def test_send_email_login_fail(self, mock_smtp):
        context = mock_smtp.return_value.__enter__.return_value
        context.login.side_effect = smtplib.SMTPAuthenticationError(535, 'Invalid Credentials')
        
        res = await send_email("Test", "Content")
        
        self.assertFalse(res)
        self.assertEqual(context.login.call_count, 3)
        self.assertEqual(context.send_message.call_count, 0)

    @patch('email_service.send_email.smtplib.SMTP_SSL', autospec=True)
    async def test_smtp_connection_failure(self, mock_smtp):
        mock_smtp.side_effect = smtplib.SMTPException('Connection Failed')
        context = mock_smtp.return_value.__enter__.return_value
        
        res = await send_email("Test", "Content")
        
        self.assertFalse(res)
        self.assertEqual(context.login.call_count, 0)
        self.assertEqual(context.send_message.call_count, 0)
            
if __name__ == '__main__':
    unittest.main()