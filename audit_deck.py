import pptx

prs = pptx.Presentation('SigmaLens_Tech4Bharat_Dark_Submission.pptx')
conditions = [
    ('Applied AI System', 'Applied AI System classification'),
    ('Commodity Hardware', 'Commodity Hardware (webcams / entry-level Android)'),
    ('Android', 'Entry-level Android phones support'),
    ('Offline', '100% Offline edge execution'),
    ('Connectivity', 'Intermittent connectivity resilience'),
    ('Voice', 'Voice-first audio tones & Text-to-Speech'),
    ('Vernacular', 'Vernacular Hindi/regional prompts for low literacy'),
    ('JanAI Café', 'Assisted path through JanAI Café'),
    ('Consent', 'Explicit consent & data sovereignty'),
    ('Data Sovereignty', 'Zero factory photos leave premises'),
    ('Technical Dimension', 'Technical Dimension evaluation criteria'),
    ('Entrepreneurial Dimension', 'Entrepreneurial Dimension evaluation criteria'),
    ('Simulated', 'Disclosed simulated conveyor & PLC digital twin'),
    ('Madan Padaki', 'Rural MSME problem inventory grounding'),
    ('Cpk', 'Cpk Process Capability Index (Target: >= 1.33)'),
    ('Sign-Off', 'Owner/Supervisor sign-off boundary on ISO cert')
]

print("=== VERIFICATION OF ALL CHALLENGE CONDITIONS IN DECK ===")
all_passed = True
for kw, desc in conditions:
    found_slides = []
    for i, slide in enumerate(prs.slides):
        for s in slide.shapes:
            if s.has_text_frame and kw.lower() in s.text_frame.text.lower():
                found_slides.append(i + 1)
                break
    status = f"PASSED -> Slides {found_slides}" if found_slides else "FAILED -> MISSING!"
    if not found_slides:
        all_passed = False
    print(f"[{'OK' if found_slides else 'FAIL'}] {desc:55s} : {status}")

print("\n" + ("="*70))
if all_passed:
    print(">>> SUCCESS: 100% OF ALL CHALLENGE CONDITIONS ARE FILLED IN THE DECK! <<<")
else:
    print(">>> WARNING: Some conditions are missing! <<<")
print("="*70)
