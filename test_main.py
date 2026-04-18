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


def test_is_system_app_true():
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


def test_is_system_app_false():
    assert main.is_system_app('com.whatsapp') is False
    assert main.is_system_app('com.facebook.katana') is False
    assert main.is_system_app('org.mozilla.firefox') is False
    assert main.is_system_app('com.google.android.youtube') is False

    assert main.is_system_app('android.something') is False
    assert main.is_system_app('android.auto') is False

    assert main.is_system_app('com.android.settings') is False
    assert main.is_system_app('com.android.vending') is False
    assert main.is_system_app('com.google.android.gms') is False


def test_mobile_init_success(monkeypatch):
    mock_device = MagicMock()
    monkeypatch.setattr(main.u2, 'connect', lambda: mock_device)

    result = main.mobile_init()

    assert result == 'Device initialized successfully'
    assert main.device == mock_device


def test_mobile_init_error(monkeypatch):
    def raise_error():
        raise Exception('Connection failed')

    monkeypatch.setattr(main.u2, 'connect', raise_error)

    result = main.mobile_init()

    assert result == 'Error initializing device: Connection failed'
    assert main.device is None


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
