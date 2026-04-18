import sys
import types
import pytest
from unittest.mock import MagicMock

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


@pytest.fixture(autouse=True)
def reset_device():
    main.device = None
    yield
    main.device = None


def test_system_app_is_false(monkeypatch):
    main.device = MagicMock()
    monkeypatch.setattr(main, 'is_system_app', lambda package: True)

    assert main.is_launchable_app('com.android.systemui') is False
    main.device.shell.assert_not_called()


def test_launchable_app_returns_true(monkeypatch):
    main.device = MagicMock()
    monkeypatch.setattr(main, 'is_system_app', lambda package: False)

    mock_response = MagicMock()
    mock_response.output = 'com.example.app/com.example.app.MainActivity'
    main.device.shell.return_value = mock_response

    assert main.is_launchable_app('com.example.app') is True
    main.device.shell.assert_called_once()
    assert 'cmd package resolve-activity --brief' in main.device.shell.call_args.args[0]
    assert 'com.example.app' in main.device.shell.call_args.args[0]


def test_non_launchable_app_returns_false(monkeypatch):
    main.device = MagicMock()
    monkeypatch.setattr(main, 'is_system_app', lambda package: False)

    mock_response = MagicMock()
    mock_response.output = 'No activity found'
    main.device.shell.return_value = mock_response

    assert main.is_launchable_app('com.example.hidden') is False
    main.device.shell.assert_called_once()
    assert 'com.example.hidden' in main.device.shell.call_args.args[0]


def test_shell_exception_returns_false(monkeypatch):
    main.device = MagicMock()
    monkeypatch.setattr(main, 'is_system_app', lambda package: False)
    main.device.shell.side_effect = Exception('Device disconnected')

    assert main.is_launchable_app('com.example.app') is False
    main.device.shell.assert_called_once()
    assert 'com.example.app' in main.device.shell.call_args.args[0]
