import win32com.client
import os

ppt_app = win32com.client.Dispatch("PowerPoint.Application")
# ppt_app.Visible = True # or False

deck_path = os.path.abspath("HAWKVZON_source.pptx")
out_dir = os.path.abspath("hawkvzon_slides")
os.makedirs(out_dir, exist_ok=True)

presentation = ppt_app.Presentations.Open(deck_path, WithWindow=False)
try:
    for i, slide in enumerate(presentation.Slides):
        out_path = os.path.join(out_dir, f"slide_{i+1}.png")
        slide.Export(out_path, "PNG", 1920, 1080)
        print(f"Exported slide {i+1} to {out_path}")
finally:
    presentation.Close()
    ppt_app.Quit()
print("Done exporting slides!")
