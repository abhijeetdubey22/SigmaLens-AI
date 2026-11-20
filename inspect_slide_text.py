import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('HAWKVZON_source.pptx') as z:
    for slide_num in [2, 3, 7]:
        xml_name = f'ppt/slides/slide{slide_num}.xml'
        xml_data = z.read(xml_name)
        root = ET.fromstring(xml_data)
        ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
              'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
        # Find all text in this slide
        texts = []
        for t in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
            if t.text and t.text.strip():
                texts.append(t.text.strip())
        print(f"\n--- SLIDE {slide_num} TEXTS ({len(texts)}) ---")
        print(" // ".join(texts[:30]))
