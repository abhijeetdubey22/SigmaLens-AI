import pptx
from pptx.enum.shapes import MSO_SHAPE_TYPE

prs = pptx.Presentation('HAWKVZON_source.pptx')

for i, slide in enumerate(prs.slides):
    print(f"\n=================== SLIDE {i+1} ===================")
    for shape in slide.shapes:
        info = []
        if shape.name:
            info.append(f"Name: {shape.name}")
        info.append(f"Type: {shape.shape_type}")
        
        # position and dimensions
        l, t, w, h = shape.left.inches, shape.top.inches, shape.width.inches, shape.height.inches
        info.append(f"Box: ({l:.2f}, {t:.2f}, {w:.2f}, {h:.2f})")
        
        # fill
        try:
            if shape.fill.type:
                info.append(f"FillType: {shape.fill.type}")
                if hasattr(shape.fill, 'fore_color'):
                    try:
                        info.append(f"FillRGB: {shape.fill.fore_color.rgb}")
                    except:
                        try:
                            info.append(f"FillThemeClr: {shape.fill.fore_color.theme_color}")
                        except: pass
        except: pass
        
        # line
        try:
            if shape.line and shape.line.color:
                try:
                    info.append(f"LineRGB: {shape.line.color.rgb}")
                except:
                    try:
                        info.append(f"LineThemeClr: {shape.line.color.theme_color}")
                    except: pass
        except: pass
        
        # text
        if shape.has_text_frame:
            txt = shape.text_frame.text.strip().replace('\n', ' // ')
            if txt:
                info.append(f"Text: {txt[:80]}")
        
        print(" | ".join(info))
