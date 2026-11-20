import json

with open('hawkvzon_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for s in data:
    idx = s['slide_index']
    print(f"\n=================== SLIDE {idx} ===================")
    # Find titles / main headings
    titles = []
    subtitles = []
    body_items = []
    shapes_summary = []
    
    for sh in s['shapes']:
        text_content = ""
        if 'paragraphs' in sh:
            text_content = " ".join(p['text'].strip() for p in sh['paragraphs'] if p['text'].strip())
        
        fill = sh.get('fill_rgb') or sh.get('fill_theme')
        line = sh.get('line_rgb') or sh.get('line_theme')
        
        if text_content:
            if 'Title' in sh['name'] or (sh.get('paragraphs') and any(p.get('font_size') and p['font_size'] >= 24 for p in sh['paragraphs'])):
                titles.append(f"[{sh['name']}] (fill={fill}, line={line}): {text_content[:80]}")
            elif any(p.get('font_size') and p['font_size'] >= 16 for p in sh.get('paragraphs', [])):
                subtitles.append(f"[{sh['name']}] (fill={fill}, line={line}): {text_content[:80]}")
            else:
                body_items.append(f"[{sh['name']}] (fill={fill}, line={line}): {text_content[:60]}")
        elif fill or line or 'AUTO_SHAPE' in sh['type'] or 'TABLE' in sh['type']:
            shapes_summary.append(f"Shape: {sh['name']} {sh['type']} fill={fill} line={line} box=({sh['left']},{sh['top']},{sh['width']},{sh['height']})")
            
        if 'table' in sh:
            print("  Table rows:", len(sh['table']), "columns:", len(sh['table'][0]) if sh['table'] else 0)
            for row in sh['table']:
                print("    | " + " | ".join(row[:4]) + " |")

    if titles:
        print("  TITLES:")
        for t in titles: print("    ", t)
    if subtitles:
        print("  SUBTITLES:")
        for sub in subtitles: print("    ", sub)
    if body_items:
        print("  BODY (sample 3):")
        for b in body_items[:3]: print("    ", b)
    if shapes_summary:
        print("  SHAPES/CONTAINERS:")
        for sh_s in shapes_summary[:5]: print("    ", sh_s)
