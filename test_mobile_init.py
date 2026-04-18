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


if __name__ == '__main__':
    unittest.main()
