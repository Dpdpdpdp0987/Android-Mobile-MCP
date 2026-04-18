import xml.etree.ElementTree as ET

from main import get_children_texts, is_system_app


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
    assert is_system_app("com.android.settings") is False
    assert is_system_app("com.android.vending") is False
    assert is_system_app("com.google.android.gms") is False


def test_get_children_texts_happy_path():
    root = ET.Element("root")
    child1 = ET.SubElement(root, "node")
    child1.set("text", "First Text")
    child2 = ET.SubElement(root, "node")
    child2.set("text", "Second Text")

    result = get_children_texts(root)
    assert result == ["First Text", "Second Text"]


def test_get_children_texts_no_children():
    root = ET.Element("root")
    root.set("text", "Root Text")

    result = get_children_texts(root)
    assert result == []


def test_get_children_texts_no_text_attribute():
    root = ET.Element("root")
    ET.SubElement(root, "node")
    child2 = ET.SubElement(root, "node")
    child2.set("text", "")

    result = get_children_texts(root)
    assert result == []


def test_get_children_texts_whitespace_stripping():
    root = ET.Element("root")
    child1 = ET.SubElement(root, "node")
    child1.set("text", "  Padded Text  ")
    child2 = ET.SubElement(root, "node")
    child2.set("text", "\tTabbed Text\n")

    result = get_children_texts(root)
    assert result == ["Padded Text", "Tabbed Text"]


def test_get_children_texts_deduplication():
    root = ET.Element("root")
    child1 = ET.SubElement(root, "node")
    child1.set("text", "Duplicate Text")
    child2 = ET.SubElement(root, "node")
    child2.set("text", "Duplicate Text")
    child3 = ET.SubElement(root, "node")
    child3.set("text", "  Duplicate Text  ")

    result = get_children_texts(root)
    assert result == ["Duplicate Text"]


def test_get_children_texts_skips_root():
    root = ET.Element("root")
    root.set("text", "Root Text")
    child1 = ET.SubElement(root, "node")
    child1.set("text", "Child Text")

    result = get_children_texts(root)
    assert result == ["Child Text"]
    assert "Root Text" not in result


def test_get_children_texts_nested_children():
    root = ET.Element("root")
    child1 = ET.SubElement(root, "node")
    child1.set("text", "Child 1")
    grandchild = ET.SubElement(child1, "node")
    grandchild.set("text", "Grandchild 1")

    result = get_children_texts(root)
    assert result == ["Child 1", "Grandchild 1"]
