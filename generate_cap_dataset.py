import os
import random
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import numpy as np

base_path = 'public/caps/white_cap_base.png'
base_img = Image.open(base_path).convert('RGB')
w, h = base_img.size

os.makedirs('public/caps', exist_ok=True)

# 1. Generate 24 Golden Reference Variations (slight normal factory variances)
for i in range(24):
    im = base_img.copy()
    # Slight rotation (-6 to +6 degrees)
    angle = (i - 12) * 0.5
    im = im.rotate(angle, resample=Image.Resampling.BILINEAR, fillcolor=(240, 235, 225))
    
    # Slight brightness shift (94% to 106%)
    brightness_factor = 0.95 + (i % 7) * 0.02
    enhancer = ImageEnhance.Brightness(im)
    im = enhancer.enhance(brightness_factor)
    
    # Slight contrast variation
    contrast_enhancer = ImageEnhance.Contrast(im)
    im = contrast_enhancer.enhance(0.97 + (i % 5) * 0.015)
    
    im.save(f'public/caps/golden_{i}.png')

print("Generated 24 golden variations of the white cap.")

# 2. Defect 1: Blue Bottle Cap (Wrong Product Mode)
im_blue = base_img.copy()
arr = np.array(im_blue).astype(np.float32)
# Detect cap area (brightness > 160 and within circle radius 110 from center)
center_x, center_y = 155, 170
y, x = np.ogrid[:h, :w]
mask = ((x - center_x)**2 + (y - center_y)**2) <= (115**2)

# Tint the cap blue
arr[mask, 0] = arr[mask, 0] * 0.15 # reduce red
arr[mask, 1] = arr[mask, 1] * 0.55 # medium green
arr[mask, 2] = np.clip(arr[mask, 2] * 1.35, 0, 255) # boost blue
Image.fromarray(arr.astype(np.uint8)).save('public/caps/defect_blue_cap.png')
print("Generated defect_blue_cap.png")

# 3. Defect 2: Red Beverage Cap (Wrong Product Color)
im_red = base_img.copy()
arr_red = np.array(im_red).astype(np.float32)
arr_red[mask, 0] = np.clip(arr_red[mask, 0] * 1.35, 0, 255) # high red
arr_red[mask, 1] = arr_red[mask, 1] * 0.2
arr_red[mask, 2] = arr_red[mask, 2] * 0.2
Image.fromarray(arr_red.astype(np.uint8)).save('public/caps/defect_red_cap.png')
print("Generated defect_red_cap.png")

# 4. Defect 3: Severe Hairline Crack across the white cap
im_crack = base_img.copy()
draw = ImageDraw.Draw(im_crack)
# Draw jagged dark crack across cap
crack_pts = [(100, 140), (130, 155), (150, 170), (180, 165), (210, 190), (225, 205)]
for j in range(len(crack_pts)-1):
    draw.line([crack_pts[j], crack_pts[j+1]], fill=(30, 30, 35), width=3)
# Secondary branch
draw.line([(150, 170), (160, 210), (175, 230)], fill=(30, 30, 35), width=2)
im_crack.save('public/caps/defect_crack.png')
print("Generated defect_crack.png")

# 5. Defect 4: Heavy Oil/Grease Stain on white cap
im_stain = base_img.copy()
draw_stain = ImageDraw.Draw(im_stain)
draw_stain.ellipse([110, 120, 160, 160], fill=(85, 65, 40))
im_stain = im_stain.filter(ImageFilter.GaussianBlur(radius=1.2))
im_stain.save('public/caps/defect_stain.png')
print("Generated defect_stain.png")

# 6. Defect 5: Punctured / Chipped Crown
im_chip = base_img.copy()
draw_chip = ImageDraw.Draw(im_chip)
draw_chip.polygon([(65, 140), (85, 110), (110, 130), (85, 160)], fill=(215, 195, 175))
draw_chip.line([(65, 140), (85, 110), (110, 130)], fill=(40, 30, 20), width=2)
im_chip.save('public/caps/defect_chipped.png')
print("Generated defect_chipped.png")
