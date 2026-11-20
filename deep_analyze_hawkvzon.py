import pptx
from pptx.enum.shapes import MSO_SHAPE_TYPE
import re
import json

prs = pptx.Presentation('HAWKVZON_source.pptx')

slides_data = []

for i, slide in enumerate(prs.slides):
    slide_info = {
        'slide_index': i + 1,
        'shapes': []
    }
    
    # Check background XML
    s_xml = slide._element.xml
    slide_info['xml_snippet'] = s_xml[:500]
    
    for s in slide.shapes:
        sh_data = {
            'name': s.name,
            'type': str(s.shape_type),
            'left': round(s.left.inches, 2) if s.left else 0,
            'top': round(s.top.inches, 2) if s.top else 0,
            'width': round(s.width.inches, 2) if s.width else 0,
            'height': round(s.height.inches, 2) if s.height else 0,
        }
        
        # Check fill
        if hasattr(s, 'fill'):
            try:
                sh_data['fill_type'] = str(s.fill.type)
                if s.fill.fore_color:
                    try:
                        sh_data['fill_rgb'] = str(s.fill.fore_color.rgb)
                    except:
                        try:
                            sh_data['fill_theme'] = str(s.fill.fore_color.theme_color)
                        except: pass
            except: pass
            
        # Check line
        if hasattr(s, 'line'):
            try:
                if s.line.color:
                    try:
                        sh_data['line_rgb'] = str(s.line.color.rgb)
                    except:
                        try:
                            sh_data['line_theme'] = str(s.line.color.theme_color)
                        except: pass
            except: pass
            
        # Check text paragraphs & runs
        if s.has_text_frame:
            sh_data['paragraphs'] = []
            for p in s.text_frame.paragraphs:
                p_data = {
                    'text': p.text,
                    'font_size': p.font.size.pt if p.font.size else None,
                    'font_bold': p.font.bold,
                    'font_name': p.font.name,
                    'align': str(p.alignment),
                    'runs': []
                }
                for r in p.runs:
                    r_color = None
                    try:
                        if r.font.color and r.font.color.rgb:
                            r_color = str(r.font.color.rgb)
                        elif r.font.color and r.font.color.theme_color:
                            r_color = f"theme:{r.font.color.theme_color}"
                    except: pass
                    p_data['runs'].append({
                        'text': r.text,
                        'font_name': r.font.name,
                        'font_size': r.font.size.pt if r.font.size else None,
                        'bold': r.font.bold,
                        'color': r_color
                    })
                sh_data['paragraphs'].append(p_data)
        
        # Check table
        if s.has_table:
            sh_data['table'] = []
            for row in s.table.rows:
                r_cells = []
                for cell in row.cells:
                    r_cells.append(cell.text.strip().replace('\n', ' '))
                sh_data['table'].append(r_cells)
                
        slide_info['shapes'].append(sh_data)
    slides_data.append(slide_info)

with open('hawkvzon_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(slides_data, f, indent=2)

print("Saved detailed analysis to hawkvzon_analysis.json!")
