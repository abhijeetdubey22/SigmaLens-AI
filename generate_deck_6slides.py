import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_6slide_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Clean executive color palette
    BG_DARK = RGBColor(10, 15, 29)          # #0A0F1D
    CARD_BG = RGBColor(18, 26, 48)          # #121A30
    CARD_BORDER = RGBColor(35, 52, 90)      # #23345A
    ACCENT_CYAN = RGBColor(0, 229, 255)     # #00E5FF
    ACCENT_BLUE = RGBColor(56, 139, 253)    # #388BFD
    ACCENT_GREEN = RGBColor(16, 185, 129)   # #10B981
    ACCENT_AMBER = RGBColor(245, 158, 11)   # #F59E0B
    ACCENT_RED = RGBColor(239, 68, 68)      # #EF4444
    TEXT_LIGHT = RGBColor(241, 245, 249)    # #F1F5F9
    TEXT_MUTED = RGBColor(148, 163, 184)    # #94A3B8
    TEXT_DIM = RGBColor(100, 116, 139)      # #64748B

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, category, title, slide_num):
        # Category Badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.0), Inches(0.35))
        tf = cat_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN
        p.font.name = "Segoe UI"

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(10.5), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT
        p_t.font.name = "Segoe UI"

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(11.5), Inches(0.4), Inches(1.0), Inches(0.4))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"{slide_num:02d} / 06"
        p_n.font.size = Pt(12)
        p_n.font.bold = True
        p_n.font.color.rgb = TEXT_MUTED
        p_n.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 1: TITLE & WHAT WE DO
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    top_glow = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(1.8), Inches(0.06))
    top_glow.fill.solid()
    top_glow.fill.fore_color.rgb = ACCENT_CYAN
    top_glow.line.fill.background()

    b1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(8), Inches(0.4))
    tf1 = b1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "TECHFORGE 2026 HACKATHON  |  AI & MACHINE LEARNING"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = ACCENT_CYAN
    p1.font.name = "Segoe UI"

    t1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.5), Inches(1.6))
    tf_main = t1.text_frame
    tf_main.word_wrap = True
    p_main = tf_main.paragraphs[0]
    p_main.text = "SIGMALENS"
    p_main.font.size = Pt(48)
    p_main.font.bold = True
    p_main.font.color.rgb = TEXT_LIGHT
    p_main.font.name = "Segoe UI"

    p_sub = tf_main.add_paragraph()
    p_sub.text = "Smart Camera Quality Inspection for Small Factories"
    p_sub.font.size = Pt(23)
    p_sub.font.bold = True
    p_sub.font.color.rgb = ACCENT_BLUE
    p_sub.font.name = "Segoe UI"

    desc_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.4), Inches(10.5), Inches(1.0))
    tf_d = desc_box.text_frame
    tf_d.word_wrap = True
    p_d = tf_d.paragraphs[0]
    p_d.text = (
        "Catches factory defects in under 30 milliseconds using normal webcams or phones. "
        "No defect photos required for training — it learns what a good product looks like "
        "from just 20 standard samples directly in the web browser."
    )
    p_d.font.size = Pt(16)
    p_d.font.color.rgb = TEXT_MUTED
    p_d.font.name = "Segoe UI"

    stat_data = [
        ("0 Defect Photos", "Learns from 20 good parts only", ACCENT_GREEN),
        ("28 Milliseconds", "Super fast check directly on edge", ACCENT_CYAN),
        ("96% Cost Reduction", "Replaces $25,000 legacy machines", ACCENT_AMBER)
    ]
    for i, (title, sub, color) in enumerate(stat_data):
        cx = Inches(0.8 + i * 3.9)
        cy = Inches(4.7)
        cw = Inches(3.7)
        ch = Inches(1.4)
        c = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER
        c.line.width = Pt(1)

        stb = s1.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.2), cw - Inches(0.4), ch - Inches(0.4))
        stf = stb.text_frame
        stf.word_wrap = True
        sp1 = stf.paragraphs[0]
        sp1.text = title
        sp1.font.size = Pt(20)
        sp1.font.bold = True
        sp1.font.color.rgb = color
        sp1.font.name = "Segoe UI"

        sp2 = stf.add_paragraph()
        sp2.text = sub
        sp2.font.size = Pt(11.5)
        sp2.font.color.rgb = TEXT_MUTED
        sp2.font.name = "Segoe UI"

    team_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.5), Inches(0.5))
    tf_team = team_box.text_frame
    p_team = tf_team.paragraphs[0]
    p_team.text = "Team Strawhead: Abhijeet Dubey, Shiva Pandey & Keval Shinde  |  Applied AI Edge Platform"
    p_team.font.size = Pt(11)
    p_team.font.color.rgb = TEXT_DIM
    p_team.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 2: THE PROBLEM IN SMALL FACTORIES
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Real-World Problem", "Why Quality Checks Fail in Small Factories Today", 2)

    pains = [
        (
            "1. Too Expensive",
            "₹20 Lakh ($25,000)",
            "Factory inspection machines from big brands are way too expensive for small businesses.",
            [
                "Requires costly special hardware and sensors",
                "Completely out of budget for 80% of small factories",
                "High yearly maintenance and licensing fees"
            ],
            ACCENT_RED
        ),
        (
            "2. No Defect Photos",
            "Zero Defect Data",
            "Normal AI models need thousands of photos of broken items to learn what to catch.",
            [
                "Factories don't keep photos of defective parts",
                "Different types of defects can happen anytime",
                "Stopping production to label data is not practical"
            ],
            ACCENT_AMBER
        ),
        (
            "3. Human Eye Fatigue",
            "8% - 15% Slip Through",
            "Over 80% of small factories use manual workers staring at parts for 8 hours.",
            [
                "Eyes get tired after just 30 minutes of checking",
                "Hairline cracks and solder shorts get missed",
                "Leads to customer complaints, returns, and lost money"
            ],
            ACCENT_CYAN
        )
    ]

    for i, (title, stat, lead, bullets, col_accent) in enumerate(pains):
        cx = Inches(0.8 + i * 3.9)
        cy = Inches(1.5)
        cw = Inches(3.7)
        ch = Inches(5.3)
        c = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER
        c.line.width = Pt(1)

        bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx + Inches(0.2), cy + Inches(0.2), Inches(0.8), Inches(0.05))
        bar.fill.solid()
        bar.fill.fore_color.rgb = col_accent
        bar.line.fill.background()

        tb = s2.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.35), cw - Inches(0.5), ch - Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_LIGHT
        p1.font.name = "Segoe UI"

        p_stat = tf.add_paragraph()
        p_stat.text = stat
        p_stat.font.size = Pt(24)
        p_stat.font.bold = True
        p_stat.font.color.rgb = col_accent
        p_stat.font.name = "Segoe UI"
        p_stat.space_after = Pt(10)

        p_lead = tf.add_paragraph()
        p_lead.text = lead
        p_lead.font.size = Pt(11.5)
        p_lead.font.color.rgb = TEXT_MUTED
        p_lead.font.name = "Segoe UI"
        p_lead.space_after = Pt(14)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = "•  " + b
            pb.font.size = Pt(11)
            pb.font.color.rgb = TEXT_LIGHT
            pb.font.name = "Segoe UI"
            pb.space_after = Pt(8)

    # ==========================================
    # SLIDE 3: HOW IT WORKS (SIMPLE & CLEAR)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Our Simple Solution", "How SigmaLens Works: Learn 'Normal' in 2 Minutes", 3)

    # 4 Simple Step Cards
    steps = [
        ("Step 1: Snap 20 Good Parts",
         "The operator takes 20 photos of standard good products. The system learns the colors, edges, and normal appearance in 2 seconds. No defect photos needed at all.",
         ACCENT_GREEN),
        ("Step 2: Auto-Fix Light & Tilt",
         "Room lights change and parts may sit tilted on the table. SigmaLens automatically balances the lighting and straightens the item (up to 30°) before checking.",
         ACCENT_CYAN),
        ("Step 3: Instant 28ms Check",
         "When a live piece comes under the camera, the system compares it to the good baseline. It computes differences in 28 milliseconds directly in the browser.",
         ACCENT_BLUE),
        ("Step 4: Red Heatmap & Alarm",
         "If anything is broken, missing, or scratched, a red heat overlay points out the exact spot (e.g. 'DEFECT Center-Left') and sounds a buzzer to reject it.",
         ACCENT_AMBER)
    ]

    for i, (stitle, sdesc, scol) in enumerate(steps):
        col_idx = i % 2
        row_idx = i // 2
        cx = Inches(0.8 + col_idx * 5.95)
        cy = Inches(1.5 + row_idx * 2.7)
        cw = Inches(5.7)
        ch = Inches(2.45)

        c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER
        c.line.width = Pt(1)

        tb = s3.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.2), cw - Inches(0.6), ch - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = stitle
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = scol
        p1.font.name = "Segoe UI"
        p1.space_after = Pt(8)

        p2 = tf.add_paragraph()
        p2.text = sdesc
        p2.font.size = Pt(12)
        p2.font.color.rgb = TEXT_LIGHT
        p2.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 4: TEST RESULTS & PROVEN ACCURACY
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Proven Real-World Accuracy", "Tested on 4 Real Products with 98.5% Accuracy", 4)

    # 4 Top Stats
    top_metrics = [
        ("28.9 ms", "Average Inspection Speed", ACCENT_CYAN),
        ("98.5%", "Defect Catch Rate (Recall)", ACCENT_GREEN),
        ("1.1%", "Low False Alarm Rate", ACCENT_AMBER),
        ("Zero Fees", "Runs 100% in Browser / Offline", ACCENT_BLUE)
    ]
    for i, (val, label, col) in enumerate(top_metrics):
        cx = Inches(0.8 + i * 2.95)
        cy = Inches(1.5)
        cw = Inches(2.75)
        ch = Inches(1.2)
        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER
        c.line.width = Pt(1)

        tb = s4.shapes.add_textbox(cx + Inches(0.15), cy + Inches(0.15), cw - Inches(0.3), ch - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.font.name = "Segoe UI"

        p2 = tf.add_paragraph()
        p2.text = label
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_MUTED
        p2.font.name = "Segoe UI"

    # 4 Product Cards
    card_prods = [
        ("SMT Circuit Board", "Spots missing capacitors, solder bridges, burnt resistors, and scratches.", "31 ms  •  98.7% Catch Rate"),
        ("Machined Steel Gear", "Spots broken teeth, rust spots, grease stains, and rough burr edges.", "28 ms  •  97.9% Catch Rate"),
        ("Pharma Medicine Pack", "Spots empty pill cavities, crushed tablets, and foil punctures.", "29 ms  •  99.1% Catch Rate"),
        ("Bottle Cap & Seal", "Spots torn tamper rings, crooked caps, crown dents, and plastic flash.", "26 ms  •  98.2% Catch Rate")
    ]
    for i, (pname, pdesc, pstats) in enumerate(card_prods):
        col_idx = i % 2
        row_idx = i // 2
        cx = Inches(0.8 + col_idx * 5.95)
        cy = Inches(3.0 + row_idx * 1.95)
        cw = Inches(5.7)
        ch = Inches(1.75)

        c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER
        c.line.width = Pt(1)

        tb = s4.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.15), cw - Inches(0.5), ch - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = pname
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_LIGHT
        p1.font.name = "Segoe UI"

        p2 = tf.add_paragraph()
        p2.text = pdesc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED
        p2.font.name = "Segoe UI"
        p2.space_after = Pt(4)

        p3 = tf.add_paragraph()
        p3.text = pstats
        p3.font.size = Pt(11.5)
        p3.font.bold = True
        p3.font.color.rgb = ACCENT_CYAN
        p3.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 5: FACTORY AUTOMATION & CONVEYOR
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Factory Ready Ecosystem", "Works with Real Conveyor Belts and Factory Computers", 5)

    eco = [
        (
            "Conveyor Belt Sorter",
            "Auto Sorts 15 - 60 Parts / Minute",
            "Works with moving conveyor belts. An optical sensor detects parts, the camera inspects them, and an air kicker automatically pushes bad parts into a scrap box.",
            ACCENT_CYAN
        ),
        (
            "Connects to Factory PLCs",
            "Standard Modbus & 3-Color Lights",
            "Talks to standard factory control systems. Controls green/red tower lights and sends live pass/fail numbers to factory monitors without custom wiring.",
            ACCENT_BLUE
        ),
        (
            "Early Machine Warning",
            "Stops Defects Before They Happen",
            "Watches the numbers continuously. If parts slowly drift over 4 units, it warns the supervisor that tooling is wearing out before bad parts get made.",
            ACCENT_AMBER
        ),
        (
            "1-Click Quality Certificate",
            "Official ISO 9001 Reports",
            "Creates ready-to-print batch quality certificates with supervisor signature lines and downloadable CSV spreadsheet logs for customer audits.",
            ACCENT_GREEN
        )
    ]

    for i, (title, tag, body, col) in enumerate(eco):
        col_idx = i % 2
        row_idx = i // 2
        cx = Inches(0.8 + col_idx * 5.95)
        cy = Inches(1.5 + row_idx * 2.7)
        cw = Inches(5.7)
        ch = Inches(2.45)

        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch)
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER
        c.line.width = Pt(1)

        tb = s5.shapes.add_textbox(cx + Inches(0.3), cy + Inches(0.2), cw - Inches(0.6), ch - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_LIGHT
        p1.font.name = "Segoe UI"

        p_tag = tf.add_paragraph()
        p_tag.text = tag
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = col
        p_tag.font.name = "Segoe UI"
        p_tag.space_after = Pt(8)

        p_body = tf.add_paragraph()
        p_body.text = body
        p_body.font.size = Pt(11.5)
        p_body.font.color.rgb = TEXT_MUTED
        p_body.font.name = "Segoe UI"

    # ==========================================
    # SLIDE 6: BUSINESS IMPACT & CONCLUSION
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Business Value & Next Steps", "Affordable for Any Factory: 2.5 Months Payback", 6)

    # Left: Comparison
    cx1 = Inches(0.8)
    cy1 = Inches(1.5)
    cw1 = Inches(6.8)
    ch1 = Inches(4.3)

    c1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx1, cy1, cw1, ch1)
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = CARD_BORDER
    c1.line.width = Pt(1)

    tb1 = s6.shapes.add_textbox(cx1 + Inches(0.3), cy1 + Inches(0.25), cw1 - Inches(0.6), ch1 - Inches(0.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p_comp_title = tf1.paragraphs[0]
    p_comp_title.text = "How SigmaLens Compares to Big Brand Systems"
    p_comp_title.font.size = Pt(16)
    p_comp_title.font.bold = True
    p_comp_title.font.color.rgb = ACCENT_CYAN
    p_comp_title.font.name = "Segoe UI"
    p_comp_title.space_after = Pt(10)

    simples = [
        ("System Cost", "₹20 Lakhs ($25,000) expensive machine", "Under ₹10,000 ($120) webcam or phone"),
        ("Defect Data", "Needs hundreds of broken piece photos", "Zero defect photos (just 20 good units)"),
        ("Setup Time", "Takes 4 to 6 weeks of engineer setup", "Takes under 2 minutes to learn"),
        ("Escape Rate", "8% to 15% slip through with humans", "Under 1.5% defect escape rate")
    ]

    for m, old, new in simples:
        pm = tf1.add_paragraph()
        pm.text = f"• {m}:"
        pm.font.size = Pt(11.5)
        pm.font.bold = True
        pm.font.color.rgb = TEXT_LIGHT
        pm.font.name = "Segoe UI"

        pl = tf1.add_paragraph()
        pl.text = f"   Old Way: {old}"
        pl.font.size = Pt(10.5)
        pl.font.color.rgb = ACCENT_RED
        pl.font.name = "Segoe UI"

        ps = tf1.add_paragraph()
        ps.text = f"   SigmaLens: {new}"
        ps.font.size = Pt(10.5)
        ps.font.color.rgb = ACCENT_GREEN
        ps.font.name = "Segoe UI"
        ps.space_after = Pt(4)

    # Right: The ROI Box
    cx2 = Inches(7.9)
    cw2 = Inches(4.6)
    c2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx2, cy1, cw2, ch1)
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = CARD_BORDER
    c2.line.width = Pt(1)

    tb2 = s6.shapes.add_textbox(cx2 + Inches(0.3), cy1 + Inches(0.25), cw2 - Inches(0.6), ch1 - Inches(0.5))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p_roi_title = tf2.paragraphs[0]
    p_roi_title.text = "Clear Financial Return"
    p_roi_title.font.size = Pt(16)
    p_roi_title.font.bold = True
    p_roi_title.font.color.rgb = ACCENT_AMBER
    p_roi_title.font.name = "Segoe UI"
    p_roi_title.space_after = Pt(6)

    p_case = tf2.add_paragraph()
    p_case.text = "For a factory making 5,000 units per day:"
    p_case.font.size = Pt(11)
    p_case.font.color.rgb = TEXT_MUTED
    p_case.font.name = "Segoe UI"
    p_case.space_after = Pt(12)

    roi_items = [
        ("₹14.6 Lakh / Year", "Money saved by stopping bad shipments"),
        ("2.5 Months", "Time to recover the entire investment"),
        ("Zero Cloud Fees", "Works completely offline in the plant")
    ]
    for val, lbl in roi_items:
        pv = tf2.add_paragraph()
        pv.text = val
        pv.font.size = Pt(21)
        pv.font.bold = True
        pv.font.color.rgb = ACCENT_CYAN
        pv.font.name = "Segoe UI"

        pl = tf2.add_paragraph()
        pl.text = lbl
        pl.font.size = Pt(11)
        pl.font.color.rgb = TEXT_LIGHT
        pl.font.name = "Segoe UI"
        pl.space_after = Pt(8)

    # Bottom Callout / Next Steps Bar
    bx = Inches(0.8)
    by = Inches(6.0)
    bw = Inches(11.7)
    bh = Inches(1.0)
    cb = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, bh)
    cb.fill.solid()
    cb.fill.fore_color.rgb = CARD_BG
    cb.line.color.rgb = CARD_BORDER
    cb.line.width = Pt(1)

    tbb = s6.shapes.add_textbox(bx + Inches(0.3), by + Inches(0.12), bw - Inches(0.6), bh - Inches(0.24))
    tfb = tbb.text_frame
    tfb.word_wrap = True

    p_cl = tfb.paragraphs[0]
    p_cl.text = "Summary: Ready to deploy on Raspberry Pi & smart cameras. Open source at github.com/abhijeetdubey22/SigmaLens-AI"
    p_cl.font.size = Pt(11.5)
    p_cl.font.bold = True
    p_cl.font.color.rgb = ACCENT_CYAN
    p_cl.font.name = "Segoe UI"

    p_sub_cl = tfb.add_paragraph()
    p_sub_cl.text = "Team Strawhead: Abhijeet Dubey, Shiva Pandey & Keval Shinde  |  Thank you!"
    p_sub_cl.font.size = Pt(11)
    p_sub_cl.font.color.rgb = TEXT_MUTED
    p_sub_cl.font.name = "Segoe UI"

    prs.save(output_path)
    print(f"6-slide presentation created successfully at: {output_path}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "SigmaLens_6Slides_Presentation.pptx"
    create_6slide_presentation(out_file)
