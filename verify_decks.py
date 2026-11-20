import pptx

def verify(filename):
    prs = pptx.Presentation(filename)
    print(f"\n=== Verification of {filename} ===")
    print(f"Total Slides: {len(prs.slides)}")
    print(f"Dimensions: {prs.slide_width.inches} x {prs.slide_height.inches} inches")
    for i, slide in enumerate(prs.slides):
        texts = []
        for s in slide.shapes:
            if s.has_text_frame and s.text_frame.text.strip():
                texts.append(s.text_frame.text.strip().replace('\n', ' // '))
        title = texts[1] if len(texts) > 1 else (texts[0] if texts else "None")
        print(f"  Slide {i+1} [{len(slide.shapes)} shapes]: {title[:65]}")

verify('SigmaLens_Tech4Bharat_Presentation.pptx')
verify('SigmaLens_6Slides_Presentation.pptx')
