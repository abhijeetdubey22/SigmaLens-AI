import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('HAWKVZON_source.pptx') as z:
    xml_data = z.read('ppt/theme/theme1.xml')
    root = ET.fromstring(xml_data)
    ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    clr_scheme = root.find('.//a:clrScheme', ns)
    print(ET.tostring(clr_scheme, encoding='unicode'))
