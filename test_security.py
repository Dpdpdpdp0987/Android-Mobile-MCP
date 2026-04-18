import unittest
from unittest.mock import MagicMock
import main

class TestSecurity(unittest.TestCase):
    def test_is_launchable_app_command_injection(self):
        # Mock the device
        main.device = MagicMock()
        mock_response = MagicMock()
        mock_response.output = "/"
        main.device.shell.return_value = mock_response

        # Malicious payload
        malicious_package = "com.example; rm -rf /"

        # Run function
        result = main.is_launchable_app(malicious_package)

        # Verify shell command was safely quoted
        main.device.shell.assert_called_once_with(
            "cmd package resolve-activity --brief 'com.example; rm -rf /'"
        )
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()