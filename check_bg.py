import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('HAWKVZON_source.pptx', 'r') as z:
    for name in z.namelist():
        if 'theme1.xml' in name:
            xml_data = z.read(name)
            root = ET.fromstring(xml_data)
            ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            fmt_scheme = root.find('.//a:fmtScheme', ns)
            if fmt_scheme is not None:
                bg_style_lst = fmt_scheme.find('a:bgFillStyleLst', ns)
                if bg_style_lst is not None:
                    print("bgFillStyleLst:")
                    for idx, el in enumerate(bg_style_lst):
                        print(f"  [{idx+1}] tag: {el.tag}")
                        print("     xml:", ET.tostring(el, encoding='unicode'))
