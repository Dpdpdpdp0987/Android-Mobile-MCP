import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock dependencies before importing main
sys.modules['uiautomator2'] = MagicMock()
fastmcp_mock = MagicMock()
sys.modules['fastmcp'] = fastmcp_mock
sys.modules['fastmcp.utilities'] = MagicMock()
sys.modules['fastmcp.utilities.types'] = MagicMock()

import main

class TestIsLaunchableApp(unittest.TestCase):
    @patch('main.is_system_app')
    @patch('main.device')
    def test_system_app_is_false(self, mock_device, mock_is_system_app):
        mock_is_system_app.return_value = True
        self.assertFalse(main.is_launchable_app('com.android.systemui'))
        mock_device.shell.assert_not_called()

    @patch('main.is_system_app')
    @patch('main.device')
    def test_launchable_app_returns_true(self, mock_device, mock_is_system_app):
        mock_is_system_app.return_value = False
        mock_response = MagicMock()
        mock_response.output = "com.example.app/com.example.app.MainActivity"
        mock_device.shell.return_value = mock_response

        self.assertTrue(main.is_launchable_app('com.example.app'))
        mock_device.shell.assert_called_once_with("cmd package resolve-activity --brief com.example.app")

    @patch('main.is_system_app')
    @patch('main.device')
    def test_non_launchable_app_returns_false(self, mock_device, mock_is_system_app):
        mock_is_system_app.return_value = False
        mock_response = MagicMock()
        mock_response.output = "No activity found"
        mock_device.shell.return_value = mock_response

        self.assertFalse(main.is_launchable_app('com.example.hidden'))
        mock_device.shell.assert_called_once_with("cmd package resolve-activity --brief com.example.hidden")

    @patch('main.is_system_app')
    @patch('main.device')
    def test_shell_exception_returns_false(self, mock_device, mock_is_system_app):
        mock_is_system_app.return_value = False
        mock_device.shell.side_effect = Exception("Device disconnected")

        self.assertFalse(main.is_launchable_app('com.example.app'))
        mock_device.shell.assert_called_once_with("cmd package resolve-activity --brief com.example.app")

if __name__ == '__main__':
    unittest.main()
