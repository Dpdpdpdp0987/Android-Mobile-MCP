import sys
import unittest
from unittest.mock import MagicMock, patch

# Provide a fake mcp.tool decorator that returns the function unchanged
class FakeFastMCP:
    def __init__(self, *args, **kwargs):
        pass
    def tool(self):
        def decorator(func):
            return func
        return decorator

class FakeFastMCPModule:
    FastMCP = FakeFastMCP

# Mock dependencies before importing main
sys.modules['uiautomator2'] = MagicMock()
sys.modules['fastmcp'] = FakeFastMCPModule()
sys.modules['fastmcp.utilities'] = MagicMock()
sys.modules['fastmcp.utilities.types'] = MagicMock()

import main

class TestMobileInit(unittest.TestCase):
    def setUp(self):
        # Reset device state before each test
        main.device = None

    @patch('main.u2.connect')
    def test_mobile_init_success(self, mock_connect):
        # Arrange
        mock_device = MagicMock()
        mock_connect.return_value = mock_device

        # Act
        result = main.mobile_init()

        # Assert
        self.assertEqual(result, "Device initialized successfully")
        self.assertEqual(main.device, mock_device)
        mock_connect.assert_called_once()

    @patch('main.u2.connect')
    def test_mobile_init_error(self, mock_connect):
        # Arrange
        mock_connect.side_effect = Exception("Connection failed")

        # Act
        result = main.mobile_init()

        # Assert
        self.assertEqual(result, "Error initializing device: Connection failed")
        self.assertIsNone(main.device)
        mock_connect.assert_called_once()

if __name__ == '__main__':
    unittest.main()
