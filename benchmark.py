import time
import xml.etree.ElementTree as ET

def get_children_texts_original(element):
    child_texts = []
    """Check if element has any focusable children"""
    for child in list(element.iter())[1:]:
        child_text = child.get('text', '').strip()
        if child_text and child_text not in child_texts:
            child_texts.append(child_text)
    return child_texts

def get_children_texts_optimized(element):
    child_texts = []
    seen = set()
    """Check if element has any focusable children"""
    for child in list(element.iter())[1:]:
        child_text = child.get('text', '').strip()
        if child_text and child_text not in seen:
            seen.add(child_text)
            child_texts.append(child_text)
    return child_texts

# Generate a large XML structure
root = ET.Element("root")
# Add a lot of children with some repeated texts
for i in range(10000):
    child = ET.SubElement(root, "child")
    child.set("text", f"Text {i % 1000}") # 1000 unique strings

# Benchmark Original
start = time.perf_counter()
res1 = get_children_texts_original(root)
end = time.perf_counter()
print(f"Original: {end - start:.6f} seconds")

# Benchmark Optimized
start = time.perf_counter()
res2 = get_children_texts_optimized(root)
end = time.perf_counter()
print(f"Optimized: {end - start:.6f} seconds")

assert res1 == res2, "Results do not match!"
