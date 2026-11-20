import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_10slide_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Exact HAWKVZON extracted color palette
    BG_LIGHT = RGBColor(235, 235, 235)       # #EBEBEB - Corporate Light Gray
    CARD_BG = RGBColor(255, 255, 255)        # #FFFFFF - Pure Crisp White
    CARD_BORDER = RGBColor(196, 199, 197)    # #C4C7C5 - Neutral Clean Gray
    TEXT_NAVY = RGBColor(0, 32, 96)          # #002060 - Deep Corporate Navy Blue
    ACCENT_GOLD = RGBColor(255, 192, 0)      # #FFC000 - Tech Amber Gold
    ACCENT_GREEN = RGBColor(84, 160, 33)     # #54A021 - Industrial Success Green
    TEXT_CHARCOAL = RGBColor(44, 60, 67)     # #2C3C43 - Slate Body Text
    TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B - Muted Subtitle / Labels
    ACCENT_RED = RGBColor(196, 47, 26)       # #C42F1A - Defect / Reject Red

    FONT_FAMILY = "Trebuchet MS"

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()
        return bg

    def add_header(slide, category, title, slide_num, total_slides=10):
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(8.5), Inches(0.3))
        tf = cat_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GREEN
        p.font.name = FONT_FAMILY

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(10.5), Inches(0.6))
        tf_t = title_box.text_frame
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_NAVY
        p_t.font.name = FONT_FAMILY

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(11.2), Inches(0.4), Inches(1.3), Inches(0.35))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p_n = tf_n.paragraphs[0]
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.text = f"{slide_num:02d} / {total_slides:02d}"
        p_n.font.size = Pt(12)
        p_n.font.bold = True
        p_n.font.color.rgb = TEXT_MUTED
        p_n.font.name = FONT_FAMILY

        # Underline Divider
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.28), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = TEXT_NAVY
        line.line.fill.background()

    def add_card(slide, left, top, width, height, border_color=CARD_BORDER, top_accent_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        
        if top_accent_color:
            accent_bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(0.08))
            accent_bar.fill.solid()
            accent_bar.fill.fore_color.rgb = top_accent_color
            accent_bar.line.fill.background()
            
        return card

    # ==========================================
    # SLIDE 1: TITLE & WHAT WE DO
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    top_band = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.65), Inches(2.2), Inches(0.06))
    top_band.fill.solid()
    top_band.fill.fore_color.rgb = ACCENT_GOLD
    top_band.line.fill.background()

    # Event Sub-badge (Official Tech4Bharat Details)
    b_ev = s1.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.55))
    tf_ev = b_ev.text_frame
    tf_ev.margin_left = tf_ev.margin_top = tf_ev.margin_right = tf_ev.margin_bottom = 0
    p_ev = tf_ev.paragraphs[0]
    p_ev.text = "TECH4BHARAT 2026  |  THEME 4.2: DEFECT INSPECTION (APPLIED AI SYSTEM)"
    p_ev.font.size = Pt(11)
    p_ev.font.bold = True
    p_ev.font.color.rgb = ACCENT_GREEN
    p_ev.font.name = FONT_FAMILY

    p_ev_sub = tf_ev.add_paragraph()
    p_ev_sub.text = "Global Accelerator Vision Summit 2026 • JanAI Mass Entrepreneurship Challenge • KAVM & RV College of Engineering"
    p_ev_sub.font.size = Pt(9.5)
    p_ev_sub.font.bold = True
    p_ev_sub.font.color.rgb = TEXT_MUTED
    p_ev_sub.font.name = FONT_FAMILY

    # Main Project Title
    t1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.7), Inches(1.7))
    tf1 = t1.text_frame
    tf1.word_wrap = True
    p_main = tf1.paragraphs[0]
    p_main.text = "SIGMALENS"
    p_main.font.size = Pt(46)
    p_main.font.bold = True
    p_main.font.color.rgb = TEXT_NAVY
    p_main.font.name = FONT_FAMILY

    p_sub = tf1.add_paragraph()
    p_sub.text = "Vision on Commodity Hardware: Applied AI Defect Inspection for MSMEs"
    p_sub.font.size = Pt(21)
    p_sub.font.bold = True
    p_sub.font.color.rgb = ACCENT_GOLD
    p_sub.font.name = FONT_FAMILY

    # Project Description & Hackathon Alignment
    desc_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.2), Inches(11.7), Inches(1.0))
    tf_d = desc_box.text_frame
    tf_d.word_wrap = True
    p_d = tf_d.paragraphs[0]
    p_d.text = (
        "Grounding: Based on Madan Padaki's Rural MSME Inventory. Built for micro-units in components, packaging, and textiles. "
        "Runs 100% offline on entry-level Android phones and ₹1,500 USB webcams with zero cloud fees. "
        "Eliminates the 10–15% defect escape rate by learning normal tolerance from 20 good units with zero defect photos needed."
    )
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = TEXT_CHARCOAL
    p_d.font.name = FONT_FAMILY

    kpis = [
        ("0 Defect Photos", "Learns from 20 good parts only using 3-Sigma SPC", ACCENT_GREEN),
        ("28.9ms on Commodity Hardware", "Sub-50ms offline inference on entry-level Android & webcams", TEXT_NAVY),
        ("Voice-First & Vernacular", "Dual audio tones + Hindi/regional TTS for low-literacy workers", ACCENT_GOLD)
    ]
    for i, (head, sub, color) in enumerate(kpis):
        cx = Inches(0.8 + i * 3.95)
        cy = Inches(4.35)
        cw = Inches(3.8)
        ch = Inches(1.5)
        add_card(s1, cx, cy, cw, ch, border_color=CARD_BORDER, top_accent_color=color)

        tb = s1.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.2), cw - Inches(0.4), ch - Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = head
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = color
        p1.font.name = FONT_FAMILY

        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_CHARCOAL
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(4)

    f_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.7), Inches(0.4))
    tf_f = f_box.text_frame
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = "Team Strawhead: Abhijeet Dubey (CTO / Founder), Shiva Pandey (COO) & Keval Shinde (AI/ML Lead)  •  Applied AI Edge Platform"
    p_f.font.size = Pt(11)
    p_f.font.bold = True
    p_f.font.color.rgb = TEXT_NAVY
    p_f.font.name = FONT_FAMILY

    # ==========================================
    # SLIDE 2: THE REAL-WORLD PROBLEM
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Real-World Crisis — Madan Padaki's Rural MSME Inventory", "Theme 4.2: Why Quality Checks Fail in Small Manufacturing Units Today", 2, 10)

    prob_cards = [
        ("1. High CapEx Barrier (₹20 Lakhs)",
         "Legacy Machine Vision Unaffordable",
         "Turnkey Automated Optical Inspection (AOI) from Keyence or Cognex costs upwards of ₹20,00,000 ($25,000) per line. Small units in components, packaging, and textiles cannot afford this capital investment or hire specialized vision engineers.",
         ACCENT_RED),
        ("2. Defect Data Scarcity",
         "Zero Labeled Defect Image Banks",
         "Standard supervised AI models (YOLO, ResNet) require thousands of labeled defect photos. Small factories produce good units, have no photo albums of broken items, and non-expert operators lack the time or tools to label bounding boxes.",
         ACCENT_GOLD),
        ("3. Human Eye Fatigue (10–15% Escapes)",
         "Informal Visual Inspection Bottleneck",
         "Inspection is done by whoever is free on the line. Human eye fatigue sets in within 30 minutes, allowing 10–15% of defects to escape to buyers. This leads to rejected consignments, return freight, and punitive 5–12% debit-note haircuts.",
         TEXT_NAVY)
    ]

    for i, (num_head, title_sub, desc, bar_color) in enumerate(prob_cards):
        cx = Inches(0.8 + i * 3.95)
        cy = Inches(1.65)
        cw = Inches(3.8)
        ch = Inches(5.1)
        add_card(s2, cx, cy, cw, ch, border_color=CARD_BORDER, top_accent_color=bar_color)

        tb = s2.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.3), cw - Inches(0.5), ch - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = num_head
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = bar_color
        p1.font.name = FONT_FAMILY

        p2 = tf.add_paragraph()
        p2.text = title_sub
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_NAVY
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(6)
        p2.space_after = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(11.5)
        p3.font.color.rgb = TEXT_CHARCOAL
        p3.font.name = FONT_FAMILY

    # ==========================================
    # SLIDE 3: THE SOLUTION — HOW SIGMALENS WORKS
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Applied AI Innovation — Vision on Commodity Hardware", "How SigmaLens Works: Learn 'Normal' in Under 2 Minutes on Edge Devices", 3, 10)

    steps = [
        ("Step 1: Snap 20 Good Units",
         "Operator captures 20 normal samples. Learns spatial CIELAB color moments (μ, σ) and Sobel gradient stability maps with ZERO defect images required.",
         ACCENT_GREEN),
        ("Step 2: Auto-Fix Light & Tilt",
         "CIELAB L* equalization neutralizes shop-floor lighting swings (150–900 lux). Spatial central moments auto-deskew rotated parts up to ±30°.",
         TEXT_NAVY),
        ("Step 3: Sub-30ms Commodity Edge Scoring",
         "Vectorized Mahalanobis distance evaluates live video frames against the 3-Sigma boundary (μ + 3σ) directly on entry-level Android phones and webcams.",
         ACCENT_GOLD),
        ("Step 4: Voice-First Vernacular & Alarm",
         "High-contrast Turbo colormap pinpoints defect quadrants (e.g. DEFECT Center-Left). Vernacular Hindi/regional TTS voice & audio buzzer alert operators.",
         ACCENT_RED)
    ]

    for i, (stitle, sdesc, scolor) in enumerate(steps):
        cx = Inches(0.8 + i * 2.95)
        cy = Inches(1.8)
        cw = Inches(2.75)
        ch = Inches(4.8)
        add_card(s3, cx, cy, cw, ch, border_color=CARD_BORDER, top_accent_color=scolor)

        tb = s3.shapes.add_textbox(cx + Inches(0.2), cy + Inches(0.3), cw - Inches(0.4), ch - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = f"PHASE {i+1}"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = scolor
        p1.font.name = FONT_FAMILY

        p2 = tf.add_paragraph()
        p2.text = stitle
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_NAVY
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(6)
        p2.space_after = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = sdesc
        p3.font.size = Pt(11.5)
        p3.font.color.rgb = TEXT_CHARCOAL
        p3.font.name = FONT_FAMILY

        if i < 3:
            ar = s3.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, cx + Inches(2.78), cy + Inches(2.1), Inches(0.14), Inches(0.24))
            ar.fill.solid()
            ar.fill.fore_color.rgb = ACCENT_GOLD
            ar.line.fill.background()

    # ==========================================
    # SLIDE 4: PROVEN BENCHMARKS ACROSS 4 SECTORS
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Applied AI Performance — Measured Shop-Floor Benchmarks", "Tested on 4 Real Industrial Sectors with 98.5% Accuracy & Sub-30ms Latency", 4, 10)

    recipes = [
        ("SMT Circuit Board", "31.2 ms", "98.7% Recall", "Missing Capacitors, Solder Bridges, Blown Resistors, Copper Scratches", TEXT_NAVY),
        ("Machined Steel Gear", "28.4 ms", "97.9% Recall", "Fractured Teeth, Bore Gouges, Surface Rust Pitting, Edge Burrs", ACCENT_GREEN),
        ("Pharma Blister Pack", "29.8 ms", "99.1% Recall", "Empty Pill Pockets, Crushed Tablets, Punctured Foil Seals", ACCENT_GOLD),
        ("Bottle Cap & Tamper Seal", "26.5 ms", "98.2% Recall", "Severed Tamper Rings, Cross-Thread Misalignment, Crown Dents", ACCENT_RED)
    ]

    for i, (name, speed, acc, defects, col) in enumerate(recipes):
        col_x = Inches(0.8 + i * 2.95)
        col_y = Inches(1.65)
        cw = Inches(2.75)
        ch = Inches(5.1)
        add_card(s4, col_x, col_y, cw, ch, border_color=CARD_BORDER, top_accent_color=col)

        tb = s4.shapes.add_textbox(col_x + Inches(0.2), col_y + Inches(0.25), cw - Inches(0.4), ch - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = name
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_NAVY
        p1.font.name = FONT_FAMILY

        p2 = tf.add_paragraph()
        p2.text = f"Speed: {speed}\nRecall: {acc}"
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(8)
        p2.space_after = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = "Target Defects Detected:\n" + defects
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_CHARCOAL
        p3.font.name = FONT_FAMILY

    # ==========================================
    # SLIDE 5: TECHNICAL ARCHITECTURE
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Technical Dimension — Robust Edge-First Architecture", "100% Client-Side Edge Execution Resilient to Intermittent Connectivity", 5, 10)

    arch_blocks = [
        ("1. Commodity Video Ingestion & Motion Trigger",
         "Captures live video from $15 USB webcams or entry-level Android RTSP streams. Optical motion-energy trigger automatically initiates inspection when movement settles (<2.5%).",
         Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3), TEXT_NAVY),
        ("2. CIELAB Normalization & Deskew",
         "Converts RGB to CIELAB perceptual space. Equalizes L* luminance to neutralize 150–900 lux factory lighting swings. Spatial moment deskew straightens parts within ±30°.",
         Inches(6.933), Inches(1.8), Inches(5.6), Inches(2.3), ACCENT_GREEN),
        ("3. Offline 3-Sigma Anomaly Engine",
         "Computes vectorized Mahalanobis distance across color moments and Sobel gradient tensors against μ + 3σ threshold. Runs 100% offline with zero cloud server dependencies.",
         Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3), ACCENT_GOLD),
        ("4. Edge Analytics & Disclosed Simulated PLC",
         "Evaluates Nelson Rule #2 (4-point tool wear drift). Sends Modbus TCP signals to simulated pneumatic ejectors, triggers WhatsApp alerts, and compiles tamper-evident ISO 9001 logs.",
         Inches(6.933), Inches(4.5), Inches(5.6), Inches(2.3), TEXT_NAVY)
    ]

    for title, desc, x, y, w, h, col in arch_blocks:
        add_card(s5, x, y, w, h, border_color=CARD_BORDER, top_accent_color=col)
        tb = s5.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), w - Inches(0.5), h - Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.font.name = FONT_FAMILY

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = TEXT_CHARCOAL
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(6)

    ar1 = s5.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.45), Inches(2.85), Inches(0.4), Inches(0.22))
    ar1.fill.solid()
    ar1.fill.fore_color.rgb = ACCENT_GOLD
    ar1.line.fill.background()

    ar2 = s5.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(9.5), Inches(4.15), Inches(0.22), Inches(0.3))
    ar2.fill.solid()
    ar2.fill.fore_color.rgb = ACCENT_GOLD
    ar2.line.fill.background()

    ar3 = s5.shapes.add_shape(MSO_SHAPE.LEFT_ARROW, Inches(6.45), Inches(5.55), Inches(0.4), Inches(0.22))
    ar3.fill.solid()
    ar3.fill.fore_color.rgb = ACCENT_GOLD
    ar3.line.fill.background()

    # ==========================================
    # SLIDE 6: "FOLLOWING THE MONEY" — BUYER TRUST
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Following The Money — Buyer Revenue & Trust Architecture", "What It Takes for Large Tier-1 Buyers to Trust Small Unit Quality Records", 6, 10)

    pillars = [
        ("1. 100% In-Line Inspection",
         "Replaces manual 5-sample guesswork with 100% digital verification at line speed (<30ms).",
         TEXT_NAVY),
        ("2. Statistical Cpk Proof",
         "Mathematical proof of Process Capability (Target: Cpk ≥ 1.33) proves the manufacturing process is stable.",
         ACCENT_GREEN),
        ("3. Visual Defect Evidence",
         "Stores Turbo heatmap snapshots with exact quadrant coordinates (e.g. DEFECT Center-Left 88, 200).",
         ACCENT_GOLD),
        ("4. Tamper-Evident Logs",
         "Sequential RFC 4180 CSV/JSON export with unit timestamps, anomaly scores, and operator credentials.",
         TEXT_NAVY),
        ("5. Dock-to-Stock Clearance",
         "Eliminates 3–5 day buyer receiving hold times, ending invoice debit notes and unlocking direct OEM contracts.",
         ACCENT_GREEN)
    ]

    for i, (p_title, p_desc, p_col) in enumerate(pillars):
        px = Inches(0.8 + i * 2.36)
        py = Inches(1.8)
        pw = Inches(2.25)
        ph = Inches(4.9)
        add_card(s6, px, py, pw, ph, border_color=CARD_BORDER, top_accent_color=p_col)

        tb = s6.shapes.add_textbox(px + Inches(0.18), py + Inches(0.25), pw - Inches(0.36), ph - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = p_title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = p_col
        p1.font.name = FONT_FAMILY

        p2 = tf.add_paragraph()
        p2.text = p_desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_CHARCOAL
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(8)

    # ==========================================
    # SLIDE 7: OPERATIONAL BOUNDARIES & GOVERNANCE
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Governance & Hackathon Boundaries — Ethical & Verifiable AI", "Actual Inspection Audit, Owner Sign-Off & JanAI Café Assisted Path", 7, 10)

    bounds = [
        ("BOUNDARY 1: Records Reflect What Was Actually Inspected",
         "Hardware-Synchronized Inspection & Explicit Consent",
         "• No Fabricated Data: Optical stillness trigger (<2.5% motion) guarantees 1:1 hardware capture—only physically inspected parts enter the audit log.\n"
         "• Data Sovereignty & Explicit Consent: 100% on-device edge execution. Zero factory video or proprietary CAD images leave the premises, protecting MSME IP.\n"
         "• Complete Defect Telemetry: Logs serial ID, millisecond timestamp, 3-Sigma score, pass/fail verdict, and defect quadrant coordinate.",
         TEXT_NAVY),
        ("BOUNDARY 2: Unit Owner Sign-Off & JanAI Café Assisted Path",
         "Verifiable ISO 9001:2015 Conformance Certification",
         "• Dual Digital Sign-Off: Each shift report features cryptographic verification from the SigmaLens Edge Engine and a mandatory physical/digital signature block for the Unit Owner.\n"
         "• JanAI Café Assisted Path: Micro-enterprises without IT systems or printers bring encrypted batch logs to local JanAI Cafés for official QR verification and embossed certificate printing.\n"
         "• Verifiable Quality Conformance: Certifies batch size, pass yield %, defect Pareto breakdown, and computed Cpk Process Capability Index.",
         ACCENT_GOLD)
    ]

    for i, (b_title, b_sub, b_body, b_col) in enumerate(bounds):
        bx = Inches(0.8 + i * 5.95)
        by = Inches(1.7)
        bw = Inches(5.8)
        bh = Inches(5.0)
        add_card(s7, bx, by, bw, bh, border_color=CARD_BORDER, top_accent_color=b_col)

        tb = s7.shapes.add_textbox(bx + Inches(0.3), by + Inches(0.3), bw - Inches(0.6), bh - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = b_title
        p1.font.size = Pt(13.5)
        p1.font.bold = True
        p1.font.color.rgb = b_col
        p1.font.name = FONT_FAMILY

        p2 = tf.add_paragraph()
        p2.text = b_sub
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_NAVY
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(6)
        p2.space_after = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = b_body
        p3.font.size = Pt(11.5)
        p3.font.color.rgb = TEXT_CHARCOAL
        p3.font.name = FONT_FAMILY

    # ==========================================
    # SLIDE 8: COMPETITIVE MOAT (TABLE)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Entrepreneurial Dimension — Competitive Moat & Market Fit", "Why SigmaLens Wins Against Incumbents, Supervised AI (YOLO) & Manual Eye", 8, 10)

    table_shape = s8.shapes.add_table(6, 4, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.0))
    table = table_shape.table

    table.columns[0].width = Inches(2.5)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(3.0)
    table.columns[3].width = Inches(3.233)

    headers_text = ["Key Capability", "Manual Inspection", "Legacy Industrial AOI (Keyence)", "SigmaLens (Our Moat)"]
    for j, h in enumerate(headers_text):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TEXT_NAVY if j < 3 else ACCENT_GOLD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = CARD_BG if j < 3 else TEXT_NAVY
        p.font.name = FONT_FAMILY

    table_data = [
        ("Capital Investment", "₹0 (Labor costs only)", "₹20,00,000+ ($25,000) per line", "₹1,500 ($18) commodity USB webcam / phone"),
        ("Defect Data Requirement", "None (Human memory)", "Complex rule programming", "0 Defect Photos (20 good units only)"),
        ("Offline & Connectivity", "100% Offline", "Requires server network", "100% Offline Edge (Resilient to intermittent web)"),
        ("Language & Accessibility", "Dependent on line worker", "Complex English interface", "Voice-First Vernacular (Hindi/regional audio)"),
        ("Compliance & Traceability", "Missing or handwritten paper", "Proprietary server silos", "Verifiable ISO 9001 Batch Certificate + JanAI Café")
    ]

    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if (r_idx % 2 == 0) else RGBColor(245, 245, 245)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.name = FONT_FAMILY
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_NAVY
            elif c_idx == 3:
                p.font.bold = True
                p.font.color.rgb = ACCENT_GREEN
            else:
                p.font.color.rgb = TEXT_CHARCOAL

    # ==========================================
    # SLIDE 9: MASS ENTREPRENEURSHIP & ROI
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Entrepreneurial Dimension — Mass Entrepreneurship & Job Creation", "Mass Entrepreneurship ROI: Transforming 63M MSMEs into Certified Suppliers", 9, 10)

    roi_cards = [
        ("₹3.8L – ₹6.5L", "Annual Direct Savings Per Line",
         "Eliminates 85%+ of consignment rejections, avoiding punitive buyer debit notes (5–12% invoice haircuts) and return freight.",
         ACCENT_GREEN),
        ("< 30 Days", "Capital Payback Period",
         "At a deployment cost of only ₹1,500 ($18) on commodity hardware, the system pays for itself within the very first prevented batch recall.",
         ACCENT_GOLD),
        ("Class A Vendor", "Tier-1 Supply Chain Access",
         "Transforms small unorganized job-shops into certified OEM suppliers for Tata, Maruti, and Unilever through verifiable quality records.",
         TEXT_NAVY)
    ]

    for i, (stat, title, desc, col) in enumerate(roi_cards):
        rx = Inches(0.8 + i * 3.95)
        ry = Inches(1.7)
        rw = Inches(3.8)
        rh = Inches(4.9)
        add_card(s9, rx, ry, rw, rh, border_color=CARD_BORDER, top_accent_color=col)

        tb = s9.shapes.add_textbox(rx + Inches(0.25), ry + Inches(0.3), rw - Inches(0.5), rh - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = stat
        p1.font.size = Pt(28)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.font.name = FONT_FAMILY

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_NAVY
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(8)
        p2.space_after = Pt(12)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(12)
        p3.font.color.rgb = TEXT_CHARCOAL
        p3.font.name = FONT_FAMILY

    # ==========================================
    # SLIDE 10: TEAM & ROADMAP
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Execution & Team — Committed Bharat Entrepreneurs", "Team Strawhead & 6-Month MSME Cluster Deployment Roadmap", 10, 10)

    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0), border_color=CARD_BORDER, top_accent_color=TEXT_NAVY)
    t_box = s10.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(5.1), Inches(4.5))
    tf_team = t_box.text_frame
    tf_team.word_wrap = True

    p_t1 = tf_team.paragraphs[0]
    p_t1.text = "FOUNDING TEAM"
    p_t1.font.size = Pt(13)
    p_t1.font.bold = True
    p_t1.font.color.rgb = ACCENT_GREEN
    p_t1.font.name = FONT_FAMILY

    p_t2 = tf_team.add_paragraph()
    p_t2.text = "Abhijeet Dubey — CTO / Founder"
    p_t2.font.size = Pt(15)
    p_t2.font.bold = True
    p_t2.font.color.rgb = TEXT_NAVY
    p_t2.font.name = FONT_FAMILY
    p_t2.space_before = Pt(4)

    p_t3 = tf_team.add_paragraph()
    p_t3.text = "Core architect of the SigmaLens edge machine vision and 3-Sigma statistical inference engine. Selected for Google Startup Build-a-thon."
    p_t3.font.size = Pt(10.5)
    p_t3.font.color.rgb = TEXT_CHARCOAL
    p_t3.font.name = FONT_FAMILY
    p_t3.space_before = Pt(1)
    p_t3.space_after = Pt(6)

    p_t4 = tf_team.add_paragraph()
    p_t4.text = "Shiva Pandey — COO / Co-Founder"
    p_t4.font.size = Pt(15)
    p_t4.font.bold = True
    p_t4.font.color.rgb = TEXT_NAVY
    p_t4.font.name = FONT_FAMILY

    p_t5 = tf_team.add_paragraph()
    p_t5.text = "Operations, institutional strategy, and industrial partnerships lead. Drives MSME cluster relationships across manufacturing hubs."
    p_t5.font.size = Pt(10.5)
    p_t5.font.color.rgb = TEXT_CHARCOAL
    p_t5.font.name = FONT_FAMILY
    p_t5.space_before = Pt(1)
    p_t5.space_after = Pt(6)

    p_t6 = tf_team.add_paragraph()
    p_t6.text = "Keval Shinde — AI/ML & Edge Deployment Lead"
    p_t6.font.size = Pt(15)
    p_t6.font.bold = True
    p_t6.font.color.rgb = TEXT_NAVY
    p_t6.font.name = FONT_FAMILY

    p_t7 = tf_team.add_paragraph()
    p_t7.text = "Computer vision engineering, real-time client-side optimization, defect dataset benchmarking, and edge hardware camera integration."
    p_t7.font.size = Pt(10.5)
    p_t7.font.color.rgb = TEXT_CHARCOAL
    p_t7.font.name = FONT_FAMILY
    p_t7.space_before = Pt(1)

    add_card(s10, Inches(6.933), Inches(1.7), Inches(5.6), Inches(5.0), border_color=CARD_BORDER, top_accent_color=ACCENT_GOLD)
    r_box = s10.shapes.add_textbox(Inches(7.183), Inches(1.95), Inches(5.1), Inches(4.5))
    tf_road = r_box.text_frame
    tf_road.word_wrap = True

    p_r1 = tf_road.paragraphs[0]
    p_r1.text = "6-MONTH EXECUTION ROADMAP"
    p_r1.font.size = Pt(13)
    p_r1.font.bold = True
    p_r1.font.color.rgb = ACCENT_GOLD
    p_r1.font.name = FONT_FAMILY

    roadmap_items = [
        ("Months 1–2: MSME Cluster Field Trials", "Deploy on-premise test rigs across 5 packaging and machining job-shops in Peenya & Coimbatore."),
        ("Months 3–4: JanAI Café Integration & PLC Bridges", "Integrate JanAI Café certificate embossing service, Modbus TCP relays, and automated Tally sync."),
        ("Months 5–6: Buyer Cloud Portal", "Launch verified buyer dashboard allowing enterprise OEMs to inspect batch Cpk and approve consignments prior to dispatch.")
    ]

    for r_title, r_desc in roadmap_items:
        p_head = tf_road.add_paragraph()
        p_head.text = r_title
        p_head.font.size = Pt(14)
        p_head.font.bold = True
        p_head.font.color.rgb = TEXT_NAVY
        p_head.font.name = FONT_FAMILY
        p_head.space_before = Pt(8)

        p_desc_txt = tf_road.add_paragraph()
        p_desc_txt.text = r_desc
        p_desc_txt.font.size = Pt(11)
        p_desc_txt.font.color.rgb = TEXT_CHARCOAL
        p_desc_txt.font.name = FONT_FAMILY
        p_desc_txt.space_before = Pt(2)

    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out_file = "SigmaLens_Tech4Bharat_Presentation.pptx"
    build_10slide_presentation(out_file)
