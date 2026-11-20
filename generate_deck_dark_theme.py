import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_10slide_dark_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Premium Executive Dark Slate / Charcoal Palette
    BG_DARK = RGBColor(15, 23, 42)            # #0F172A - Deep Slate Charcoal
    CARD_BG = RGBColor(30, 41, 59)            # #1E293B - Elevated Dark Slate Card
    CARD_BORDER = RGBColor(51, 65, 85)        # #334155 - Crisp Dark Border
    TEXT_TITLE = RGBColor(248, 250, 252)      # #F8FAFC - Luminous Crisp White/Silver
    TEXT_BODY = RGBColor(226, 232, 240)       # #E2E8F0 - High-Contrast Soft Slate Body
    TEXT_MUTED = RGBColor(148, 163, 184)      # #94A3B8 - Secondary Muted Text
    ACCENT_GOLD = RGBColor(251, 191, 36)      # #FBBF24 - Tech Amber Gold
    ACCENT_GREEN = RGBColor(52, 211, 153)     # #34D399 - Industrial Success Green
    ACCENT_RED = RGBColor(248, 113, 113)      # #F87171 - Defect / Reject Red
    DIVIDER_LINE = RGBColor(71, 85, 105)      # #475569 - Subtle Section Divider

    FONT_FAMILY = "Trebuchet MS"

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
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
        p_t.font.color.rgb = TEXT_TITLE
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
        line.fill.fore_color.rgb = DIVIDER_LINE
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

    # Event Sub-badge
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
    t1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.7), Inches(1.6))
    tf1 = t1.text_frame
    tf1.word_wrap = True
    p_main = tf1.paragraphs[0]
    p_main.text = "SIGMALENS"
    p_main.font.size = Pt(46)
    p_main.font.bold = True
    p_main.font.color.rgb = TEXT_TITLE
    p_main.font.name = FONT_FAMILY

    p_sub = tf1.add_paragraph()
    p_sub.text = "Vision on Commodity Hardware: Applied AI Defect Inspection for MSMEs"
    p_sub.font.size = Pt(21)
    p_sub.font.bold = True
    p_sub.font.color.rgb = ACCENT_GOLD
    p_sub.font.name = FONT_FAMILY

    desc_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.25), Inches(11.7), Inches(0.85))
    tf_d = desc_box.text_frame
    tf_d.word_wrap = True
    p_d = tf_d.paragraphs[0]
    p_d.text = (
        "Grounded in Madan Padaki's Rural MSME Inventory for components, packaging & textiles. "
        "Eliminates 10–15% defect escapes using unsupervised 3-Sigma SPC. "
        "Runs 100% offline on ₹1,500 USB webcams and entry-level Android phones with zero cloud fees."
    )
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = TEXT_BODY
    p_d.font.name = FONT_FAMILY

    kpis = [
        ("0 Defect Photos", "Learns normal from 20 good units via 3-Sigma SPC", ACCENT_GREEN),
        ("28.9ms Latency", "Offline inference on entry-level Android & webcams", ACCENT_GOLD),
        ("Voice & Vernacular", "Dual audio tones + Hindi TTS for low-literacy workers", RGBColor(56, 189, 248))
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
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_BODY
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(4)

    f_box = s1.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.7), Inches(0.4))
    tf_f = f_box.text_frame
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = "Team Strawhead: Abhijeet Dubey (CTO / Founder), Shiva Pandey (COO) & Keval Shinde (AI/ML Lead)  •  Applied AI Edge Platform"
    p_f.font.size = Pt(11)
    p_f.font.bold = True
    p_f.font.color.rgb = ACCENT_GOLD
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
         [
             "• Turnkey AOI (Keyence, Cognex) costs ₹20L+ ($25,000) per line.",
             "• Completely unaffordable for small components, packaging & textile units.",
             "• Demands dedicated machine vision engineers that MSMEs cannot hire."
         ],
         ACCENT_RED),
        ("2. Defect Data Scarcity",
         "Zero Labeled Defect Image Banks",
         [
             "• Supervised AI models (YOLO, ResNet) require 5,000+ labeled defect photos.",
             "• Small factories produce good units and have no photo albums of broken items.",
             "• Non-expert operators lack the time, tools, and expertise to label bounding boxes."
         ],
         ACCENT_GOLD),
        ("3. Human Eye Fatigue (10–15% Escapes)",
         "Informal Visual Inspection Bottleneck",
         [
             "• Line inspection is done manually; severe eye fatigue sets in within 30 minutes.",
             "• 10–15% of defects escape unnoticed into customer and OEM shipments.",
             "• Results in rejected consignments, return freight, and 5–12% debit-note penalties."
         ],
         RGBColor(56, 189, 248))
    ]

    for i, (num_head, title_sub, bullets, bar_color) in enumerate(prob_cards):
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
        p2.font.color.rgb = TEXT_TITLE
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(4)
        p2.space_after = Pt(10)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = TEXT_BODY
            p_b.font.name = FONT_FAMILY
            p_b.space_before = Pt(4)

    # ==========================================
    # SLIDE 3: THE SOLUTION — HOW SIGMALENS WORKS
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Applied AI Innovation — Vision on Commodity Hardware", "How SigmaLens Works: Learn 'Normal' in Under 2 Minutes on Edge Devices", 3, 10)

    steps = [
        ("Step 1: Snap 20 Good Units",
         [
             "• Operator captures 20 normal samples in 2 mins.",
             "• Learns CIELAB color moments & Sobel gradients.",
             "• ZERO defect training photos required."
         ],
         ACCENT_GREEN),
        ("Step 2: Auto-Fix Light & Tilt",
         [
             "• CIELAB L* neutralizes 150–900 lux lighting swings.",
             "• Central moments auto-deskew tilt up to ±30°.",
             "• No custom light domes or fixturing needed."
         ],
         RGBColor(56, 189, 248)),
        ("Step 3: Sub-30ms Commodity Edge Scoring",
         [
             "• Vectorized Mahalanobis distance vs μ + 3σ boundary.",
             "• Runs 100% offline on phones & webcams.",
             "• Sub-30ms latency (34+ FPS real-time speed)."
         ],
         ACCENT_GOLD),
        ("Step 4: Voice-First Vernacular & Alarm",
         [
             "• High-contrast Turbo colormap frames defects.",
             "• Vernacular Hindi/regional TTS voice prompts.",
             "• Dual audio buzzer instantly alerts operators."
         ],
         ACCENT_RED)
    ]

    for i, (stitle, bullets, scolor) in enumerate(steps):
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
        p2.font.color.rgb = TEXT_TITLE
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(4)
        p2.space_after = Pt(10)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = TEXT_BODY
            p_b.font.name = FONT_FAMILY
            p_b.space_before = Pt(4)

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
        ("SMT Circuit Board", "31.2 ms", "98.7% Recall", ["• Missing Capacitors & Resistors", "• Solder Bridges & Trace Shorts", "• Copper Track Scratches"], RGBColor(56, 189, 248)),
        ("Machined Steel Gear", "28.4 ms", "97.9% Recall", ["• Fractured & Chipped Teeth", "• Internal Bore Gouges", "• Surface Rust Pitting & Burrs"], ACCENT_GREEN),
        ("Pharma Blister Pack", "29.8 ms", "99.1% Recall", ["• Empty Pill Pockets", "• Crushed & Chipped Tablets", "• Punctured Foil Seals"], ACCENT_GOLD),
        ("Bottle Cap & Tamper Seal", "26.5 ms", "98.2% Recall", ["• Severed Tamper Rings", "• Cross-Thread Misalignments", "• Crown Dents & Seal Gaps"], ACCENT_RED)
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
        p1.font.color.rgb = TEXT_TITLE
        p1.font.name = FONT_FAMILY

        p2 = tf.add_paragraph()
        p2.text = f"Speed: {speed}  •  Recall: {acc}"
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = col
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(6)
        p2.space_after = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = "Target Defects Detected:"
        p3.font.size = Pt(11)
        p3.font.bold = True
        p3.font.color.rgb = TEXT_TITLE
        p3.font.name = FONT_FAMILY
        p3.space_after = Pt(4)

        for d in defects:
            p_d = tf.add_paragraph()
            p_d.text = d
            p_d.font.size = Pt(10.5)
            p_d.font.color.rgb = TEXT_BODY
            p_d.font.name = FONT_FAMILY
            p_d.space_before = Pt(3)

    # ==========================================
    # SLIDE 5: TECHNICAL ARCHITECTURE
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Technical Dimension — Robust Edge-First Architecture", "100% Client-Side Edge Execution Resilient to Intermittent Connectivity", 5, 10)

    arch_blocks = [
        ("1. Commodity Video Ingestion & Motion Trigger",
         [
             "• Captures live video from $15 USB webcams & entry-level Android RTSP streams.",
             "• Optical motion-energy trigger (<2.5% motion) auto-starts inspection when settled."
         ],
         Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3), RGBColor(56, 189, 248)),
        ("2. CIELAB Normalization & Deskew",
         [
             "• Equalizes CIELAB L* luminance to neutralize 150–900 lux factory lighting swings.",
             "• Central moment deskew auto-straightens rotated parts up to ±30°."
         ],
         Inches(6.933), Inches(1.8), Inches(5.6), Inches(2.3), ACCENT_GREEN),
        ("3. Offline 3-Sigma Anomaly Engine",
         [
             "• Vectorized Mahalanobis distance across color moments & Sobel gradient tensors.",
             "• Runs 100% offline with zero cloud server dependencies or data egress costs."
         ],
         Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.3), ACCENT_GOLD),
        ("4. Edge Analytics & Disclosed Simulated PLC",
         [
             "• Evaluates Nelson Rule #2 (4-point tool wear drift) for predictive quality.",
             "• Modbus TCP signals to simulated ejectors, WhatsApp alerts & ISO 9001 cert logs."
         ],
         Inches(6.933), Inches(4.5), Inches(5.6), Inches(2.3), TEXT_TITLE)
    ]

    for title, bullets, x, y, w, h, col in arch_blocks:
        add_card(s5, x, y, w, h, border_color=CARD_BORDER, top_accent_color=col)
        tb = s5.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), w - Inches(0.5), h - Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.font.name = FONT_FAMILY

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = TEXT_BODY
            p_b.font.name = FONT_FAMILY
            p_b.space_before = Pt(4)

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
         "Replaces 5-sample manual guesswork with 100% digital check at line speed (<30ms).",
         RGBColor(56, 189, 248)),
        ("2. Statistical Cpk Proof",
         "Mathematical proof of Process Capability (Cpk ≥ 1.33) verifies manufacturing stability.",
         ACCENT_GREEN),
        ("3. Visual Defect Evidence",
         "Stores Turbo heatmap snapshots with exact quadrant coordinates (DEFECT Center-Left).",
         ACCENT_GOLD),
        ("4. Tamper-Evident Logs",
         "Sequential RFC 4180 CSV/JSON audit logs with timestamps and operator credentials.",
         TEXT_TITLE),
        ("5. Dock-to-Stock Clearance",
         "Eliminates 3–5 day buyer receiving hold times, ending invoice debit notes.",
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
        p2.font.color.rgb = TEXT_BODY
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
         [
             "• No Fabricated Data: 1:1 stillness trigger ensures only physical parts enter audit logs.",
             "• Data Sovereignty & Consent: 100% on-device edge execution; zero factory images leave the unit.",
             "• Complete Defect Telemetry: Logs serial ID, millisecond timestamp, 3-Sigma score & quadrant."
         ],
         RGBColor(56, 189, 248)),
        ("BOUNDARY 2: Unit Owner Sign-Off & JanAI Café Assisted Path",
         "Verifiable ISO 9001:2015 Conformance Certification",
         [
             "• Mandatory Sign-Off: Edge cryptographic audit with Unit Owner signature block.",
             "• JanAI Café Path: Bring encrypted logs to local JanAI Café for QR verification & cert printing.",
             "• Verifiable Conformance: Certifies batch size, yield %, defect Pareto, and Cpk index."
         ],
         ACCENT_GOLD)
    ]

    for i, (b_title, b_sub, bullets, b_col) in enumerate(bounds):
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
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = b_col
        p1.font.name = FONT_FAMILY

        p2 = tf.add_paragraph()
        p2.text = b_sub
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_TITLE
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(4)
        p2.space_after = Pt(8)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = TEXT_BODY
            p_b.font.name = FONT_FAMILY
            p_b.space_before = Pt(4)

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
        cell.fill.fore_color.rgb = RGBColor(40, 53, 76) if j < 3 else ACCENT_GOLD
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEXT_TITLE if j < 3 else BG_DARK
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
            cell.fill.fore_color.rgb = CARD_BG if (r_idx % 2 == 0) else RGBColor(22, 30, 46)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.name = FONT_FAMILY
            if c_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_TITLE
            elif c_idx == 3:
                p.font.bold = True
                p.font.color.rgb = ACCENT_GREEN
            else:
                p.font.color.rgb = TEXT_BODY

    # ==========================================
    # SLIDE 9: MASS ENTREPRENEURSHIP & ROI
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Entrepreneurial Dimension — Mass Entrepreneurship & Job Creation", "Mass Entrepreneurship ROI: Transforming 63M MSMEs into Certified Suppliers", 9, 10)

    roi_cards = [
        ("₹3.8L – ₹6.5L", "Annual Direct Savings Per Line",
         [
             "• Eliminates 85%+ of consignment rejections.",
             "• Avoids 5–12% debit-note penalties and return freight costs.",
             "• Prevents scrap and wasted raw material across production lines."
         ],
         ACCENT_GREEN),
        ("< 30 Days", "Capital Payback Period",
         [
             "• Deploys for only ₹1,500 ($18) on commodity hardware.",
             "• Pays for itself in the very first prevented batch recall.",
             "• Zero recurring cloud computing fees or subscription burden."
         ],
         ACCENT_GOLD),
        ("Class A Vendor", "Tier-1 Supply Chain Access",
         [
             "• Transforms small unorganized job-shops into certified suppliers.",
             "• Unlocks direct contracts with enterprise OEMs (Tata, Maruti).",
             "• Elevates local job creation and wage stability in rural MSME clusters."
         ],
         RGBColor(56, 189, 248))
    ]

    for i, (stat, title, bullets, col) in enumerate(roi_cards):
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
        p2.font.color.rgb = TEXT_TITLE
        p2.font.name = FONT_FAMILY
        p2.space_before = Pt(6)
        p2.space_after = Pt(10)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = TEXT_BODY
            p_b.font.name = FONT_FAMILY
            p_b.space_before = Pt(4)

    # ==========================================
    # SLIDE 10: TEAM & ROADMAP
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Execution & Team — Committed Bharat Entrepreneurs", "Team Strawhead & 6-Month MSME Cluster Deployment Roadmap", 10, 10)

    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.0), border_color=CARD_BORDER, top_accent_color=ACCENT_GOLD)
    t_box = s10.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(5.1), Inches(4.5))
    tf_team = t_box.text_frame
    tf_team.word_wrap = True

    p_t1 = tf_team.paragraphs[0]
    p_t1.text = "FOUNDING TEAM"
    p_t1.font.size = Pt(13)
    p_t1.font.bold = True
    p_t1.font.color.rgb = ACCENT_GREEN
    p_t1.font.name = FONT_FAMILY

    team_members = [
        ("Abhijeet Dubey — CTO / Founder",
         "Lead architect of the SigmaLens edge machine vision & 3-Sigma SPC inference engine. Google Startup Build-a-thon finalist."),
        ("Shiva Pandey — COO / Co-Founder",
         "Operations, industrial partnerships & MSME cluster rollouts across Indian manufacturing hubs."),
        ("Keval Shinde — AI/ML & Edge Deployment Lead",
         "Real-time client-side optimization, defect benchmarking & Android hardware camera integration.")
    ]

    for m_name, m_bio in team_members:
        p_name = tf_team.add_paragraph()
        p_name.text = m_name
        p_name.font.size = Pt(14)
        p_name.font.bold = True
        p_name.font.color.rgb = TEXT_TITLE
        p_name.font.name = FONT_FAMILY
        p_name.space_before = Pt(6)

        p_bio = tf_team.add_paragraph()
        p_bio.text = m_bio
        p_bio.font.size = Pt(10.5)
        p_bio.font.color.rgb = TEXT_BODY
        p_bio.font.name = FONT_FAMILY
        p_bio.space_before = Pt(2)

    add_card(s10, Inches(6.933), Inches(1.7), Inches(5.6), Inches(5.0), border_color=CARD_BORDER, top_accent_color=ACCENT_GREEN)
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
        ("Months 1–2: MSME Cluster Field Trials", "Deploy test rigs across 5 packaging and machining job-shops in Peenya & Coimbatore."),
        ("Months 3–4: JanAI Café & PLC Bridges", "Integrate JanAI Café certificate embossing service, Modbus TCP relays, and automated Tally sync."),
        ("Months 5–6: Buyer Cloud Portal", "Launch verified buyer dashboard for enterprise OEMs to inspect batch Cpk and approve consignments.")
    ]

    for r_title, r_desc in roadmap_items:
        p_head = tf_road.add_paragraph()
        p_head.text = r_title
        p_head.font.size = Pt(14)
        p_head.font.bold = True
        p_head.font.color.rgb = TEXT_TITLE
        p_head.font.name = FONT_FAMILY
        p_head.space_before = Pt(8)

        p_desc_txt = tf_road.add_paragraph()
        p_desc_txt.text = r_desc
        p_desc_txt.font.size = Pt(11)
        p_desc_txt.font.color.rgb = TEXT_BODY
        p_desc_txt.font.name = FONT_FAMILY
        p_desc_txt.space_before = Pt(2)

    try:
        prs.save(output_path)
        print(f"Dark Slate Presentation saved successfully to: {output_path}")
        return True
    except PermissionError:
        print(f"[NOTE] '{output_path}' is currently open in PowerPoint.")
        print("Please close PowerPoint to overwrite it, or save your manual edits directly in PowerPoint!")
        return False

if __name__ == "__main__":
    out_file = "SigmaLens_Tech4Bharat_Dark_Submission.pptx"
    success = build_10slide_dark_presentation(out_file)
    if not success:
        temp_file = "SigmaLens_Tech4Bharat_Dark_Submission_Updated.pptx"
        build_10slide_dark_presentation(temp_file)
        print(f"Also saved clean updated version to: {temp_file}")
