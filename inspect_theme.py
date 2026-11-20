import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile('HAWKVZON_source.pptx', 'r') as z:
    for name in z.namelist():
        if 'theme' in name and name.endswith('.xml'):
            print("Found theme file:", name)
            xml_data = z.read(name)
            root = ET.fromstring(xml_data)
            ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            clr_scheme = root.find('.//a:clrScheme', ns)
            if clr_scheme is not None:
                print("Color Scheme Name:", clr_scheme.attrib.get('name'))
                for elem in clr_scheme:
                    tag = elem.tag.split('}')[-1]
                    child = list(elem)[0] if len(elem) > 0 else None
                    if child is not None:
                        val = child.attrib.get('val') or child.attrib.get('lastClr')
                        print(f"  {tag}: {child.tag.split('}')[-1]} = {val}")
            
            font_scheme = root.find('.//a:fontScheme', ns)
            if font_scheme is not None:
                print("\nFont Scheme Name:", font_scheme.attrib.get('name'))
                major = font_scheme.find('a:majorFont/a:latin', ns)
                minor = font_scheme.find('a:minorFont/a:latin', ns)
                if major is not None:
                    print(f"  Major Font (Headings): {major.attrib.get('typeface')}")
                if minor is not None:
                    print(f"  Minor Font (Body): {minor.attrib.get('typeface')}")

        if 'slideMaster' in name and name.endswith('.xml'):
            print("\nFound Slide Master:", name)
            xml_data = z.read(name)
            root = ET.fromstring(xml_data)
            ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
                  'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            bg = root.find('.//p:bg', ns)
            if bg is not None:
                print("Slide Master Background:", ET.tostring(bg, encoding='unicode'))
