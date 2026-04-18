import pytest
from main import is_system_app

def test_is_system_app_true():
    # Matches system UI patterns
    assert is_system_app("com.android.systemui") is True
    assert is_system_app("com.android.systemui.plugin") is True

    # Matches provider patterns
    assert is_system_app("com.android.providers.media") is True
    assert is_system_app("com.android.providers.settings") is True

    # Matches internal patterns
    assert is_system_app("com.android.internal.display") is True

    # Matches cellbroadcast, phone, bluetooth
    assert is_system_app("com.android.cellbroadcastreceiver") is True
    assert is_system_app("com.android.phone") is True
    assert is_system_app("com.android.bluetooth") is True

    # Matches google patterns
    assert is_system_app("com.google.android.overlay.modules") is True
    assert is_system_app("com.google.mainline.telemetry") is True
    assert is_system_app("com.google.android.ext.services") is True

    # Matches auto_generated_rro_ anywhere
    assert is_system_app("com.someapp.auto_generated_rro_vendor") is True
    assert is_system_app("com.auto_generated_rro_") is True

    # Exact 'android' match
    assert is_system_app("android") is True

def test_is_system_app_false():
    # Regular apps
    assert is_system_app("com.whatsapp") is False
    assert is_system_app("com.facebook.katana") is False
    assert is_system_app("org.mozilla.firefox") is False
    assert is_system_app("com.google.android.youtube") is False

    # Prefix matches that shouldn't trigger exact matches
    assert is_system_app("android.something") is False
    assert is_system_app("android.auto") is False

    # Similar but not quite matching prefixes
    assert is_system_app("com.android.settings") is False # not in exclude list specifically
    assert is_system_app("com.android.vending") is False
    assert is_system_app("com.google.android.gms") is False
