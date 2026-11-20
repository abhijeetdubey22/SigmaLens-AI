import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('HAWKVZON_source.pptx') as z:
    for f in ['data1.xml', 'data2.xml', 'data3.xml']:
        xml_data = z.read(f'ppt/diagrams/{f}')
        root = ET.fromstring(xml_data)
        texts = []
        for t in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
            if t.text and t.text.strip():
                texts.append(t.text.strip())
        print(f"\n--- {f} TEXTS ({len(texts)}) ---")
        for t in texts:
            print("  *", t)
