import sys
import types
import unittest
from unittest.mock import MagicMock, patch

# Mock dependencies before importing main
class FakeFastMCP:
    def __init__(self, *args, **kwargs):
        pass

    def tool(self):
        def decorator(func):
            return func
        return decorator

fastmcp_module = types.ModuleType('fastmcp')
fastmcp_module.FastMCP = FakeFastMCP
sys.modules['fastmcp'] = fastmcp_module

utilities_module = types.ModuleType('fastmcp.utilities')
sys.modules['fastmcp.utilities'] = utilities_module

class FakeImage:
    def __init__(self, data=None, format=None):
        self.data = data
        self.format = format

utilities_types_module = types.ModuleType('fastmcp.utilities.types')
utilities_types_module.Image = FakeImage
sys.modules['fastmcp.utilities.types'] = utilities_types_module

sys.modules['uiautomator2'] = MagicMock()

import main


class TestIsSystemApp(unittest.TestCase):
    def test_is_system_app_true(self):
        assert main.is_system_app('com.android.systemui') is True
        assert main.is_system_app('com.android.systemui.plugin') is True

        assert main.is_system_app('com.android.providers.media') is True
        assert main.is_system_app('com.android.providers.settings') is True

        assert main.is_system_app('com.android.internal.display') is True

        assert main.is_system_app('com.android.cellbroadcastreceiver') is True
        assert main.is_system_app('com.android.phone') is True
        assert main.is_system_app('com.android.bluetooth') is True

        assert main.is_system_app('com.google.android.overlay.modules') is True
        assert main.is_system_app('com.google.mainline.telemetry') is True
        assert main.is_system_app('com.google.android.ext.services') is True

        assert main.is_system_app('com.someapp.auto_generated_rro_vendor') is True
        assert main.is_system_app('com.auto_generated_rro_') is True

        assert main.is_system_app('android') is True

    def test_is_system_app_false(self):
        assert main.is_system_app('com.whatsapp') is False
        assert main.is_system_app('com.facebook.katana') is False
        assert main.is_system_app('org.mozilla.firefox') is False
        assert main.is_system_app('com.google.android.youtube') is False

        assert main.is_system_app('android.something') is False
        assert main.is_system_app('android.auto') is False

        assert main.is_system_app('com.android.settings') is False
        assert main.is_system_app('com.android.vending') is False
        assert main.is_system_app('com.google.android.gms') is False


class TestMobileInit(unittest.TestCase):
    def setUp(self):
        main.device = None

    @patch('main.u2.connect')
    def test_mobile_init_success(self, mock_connect):
        mock_device = MagicMock()
        mock_connect.return_value = mock_device

        result = main.mobile_init()

        self.assertEqual(result, 'Device initialized successfully')
        self.assertEqual(main.device, mock_device)
        mock_connect.assert_called_once()

    @patch('main.u2.connect')
    def test_mobile_init_error(self, mock_connect):
        mock_connect.side_effect = Exception('Connection failed')

        result = main.mobile_init()

        self.assertEqual(result, 'Error initializing device: Connection failed')
        self.assertIsNone(main.device)
        mock_connect.assert_called_once()


class TestIsLaunchableApp(unittest.TestCase):
    def setUp(self):
        main.device = MagicMock()

    @patch('main.is_system_app')
    def test_system_app_is_false(self, mock_is_system_app):
        mock_is_system_app.return_value = True
        self.assertFalse(main.is_launchable_app('com.android.systemui'))
        main.device.shell.assert_not_called()

    @patch('main.is_system_app')
    def test_launchable_app_returns_true(self, mock_is_system_app):
        mock_is_system_app.return_value = False
        mock_response = MagicMock()
        mock_response.output = 'com.example.app/com.example.app.MainActivity'
        main.device.shell.return_value = mock_response

        self.assertTrue(main.is_launchable_app('com.example.app'))
        main.device.shell.assert_called_once()
        self.assertIn('cmd package resolve-activity --brief', main.device.shell.call_args.args[0])
        self.assertIn('com.example.app', main.device.shell.call_args.args[0])

    @patch('main.is_system_app')
    def test_non_launchable_app_returns_false(self, mock_is_system_app):
        mock_is_system_app.return_value = False
        mock_response = MagicMock()
        mock_response.output = 'No activity found'
        main.device.shell.return_value = mock_response

        self.assertFalse(main.is_launchable_app('com.example.hidden'))
        main.device.shell.assert_called_once()
        self.assertIn('com.example.hidden', main.device.shell.call_args.args[0])

    @patch('main.is_system_app')
    def test_shell_exception_returns_false(self, mock_is_system_app):
        mock_is_system_app.return_value = False
        main.device.shell.side_effect = Exception('Device disconnected')

        self.assertFalse(main.is_launchable_app('com.example.app'))
        main.device.shell.assert_called_once()
        self.assertIn('com.example.app', main.device.shell.call_args.args[0])


if __name__ == '__main__':
    unittest.main()
