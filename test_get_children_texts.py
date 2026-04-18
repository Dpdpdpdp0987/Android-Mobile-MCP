import xml.etree.ElementTree as ET

from main import get_children_texts


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
