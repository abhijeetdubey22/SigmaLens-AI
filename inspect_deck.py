import pptx
import re
import os

prs = pptx.Presentation('HAWKVZON_source.pptx')

print(f"Total Slides: {len(prs.slides)}")
print(f"Slide Size: {prs.slide_width.inches} x {prs.slide_height.inches} inches")

# Analyze theme colors in slide master
master = prs.slide_master
print("Slide Master:", master)
try:
    theme = master.part.element
    theme_xml = theme.xml
    theme_colors = re.findall(r'<a:srgbClr val="([0-9A-Fa-f]{6})"/>', theme_xml)
    print("Theme srgb colors in master:", set(theme_colors))
except Exception as e:
    print("Error getting theme xml:", e)

all_srgb = set()
all_scheme = set()
fonts = set()

for i, slide in enumerate(prs.slides):
    s_xml = slide._element.xml
    srgb = set(re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', s_xml))
    scheme = set(re.findall(r'schemeClr val="([^"]+)"', s_xml))
    all_srgb.update(srgb)
    all_scheme.update(scheme)
    
    # check fonts
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.name:
                        fonts.add(r.font.name)
                    if r.font.color and hasattr(r.font.color, 'rgb') and r.font.color.rgb:
                        all_srgb.add(str(r.font.color.rgb))
        # check background or shape fills
        if hasattr(shape, 'fill'):
            try:
                if shape.fill.type and shape.fill.fore_color and hasattr(shape.fill.fore_color, 'rgb'):
                    all_srgb.add(str(shape.fill.fore_color.rgb))
            except:
                pass

print("\n--- ALL SRGB COLORS IN DECK ---")
for c in sorted(all_srgb):
    print(f"#{c}")

print("\n--- SCHEME COLOR REFERENCES ---")
for s in sorted(all_scheme):
    print(s)

print("\n--- FONTS USED ---")
for f in sorted(fonts):
    print(f)
