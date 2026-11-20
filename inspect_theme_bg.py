import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('HAWKVZON_source.pptx') as z:
    xml_data = z.read('ppt/theme/theme1.xml')
    root = ET.fromstring(xml_data)
    ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    bg_style_lst = root.find('.//a:bgFillStyleLst', ns)
    print("bgFillStyleLst children count:", len(bg_style_lst))
    for i, c in enumerate(bg_style_lst):
        print(f"Index {i+1}: {c.tag}")
        print(ET.tostring(c, encoding='unicode'))
