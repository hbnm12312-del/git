from PIL import Image, ImageEnhance, ImageFilter
import os

d = r"C:\Users\FYH\Documents\New project\us_imgs_hd"

# Ultra-enhance all images
for f in sorted(os.listdir(d)):
    if not f.lower().endswith('.jpg'): continue
    if 'user_photo' in f: continue
    if f.startswith('285d') or f.startswith('b858'): continue
    
    fp = os.path.join(d, f)
    im = Image.open(fp).convert("RGB")
    w, h = im.size
    
    # Aggressive enhancement for low-res-origin images
    if w <= 1000 and h <= 1000:
        im = im.resize((1920, 1080), Image.LANCZOS)
        # Strong sharpening
        for _ in range(2):
            im = im.filter(ImageFilter.SHARPEN)
        # Brightness + contrast
        im = ImageEnhance.Brightness(im).enhance(1.15)
        im = ImageEnhance.Contrast(im).enhance(1.25)
        im = ImageEnhance.Color(im).enhance(1.2)
    
    im.save(fp, "JPEG", quality=95)
    print(f"Enhanced: {f} -> {w}x{h} -> {im.size[0]}x{im.size[1]}")

# Process user photo 2 for Slide 1 (crop to landscape 1920x1080)
src = os.path.join(d, "b858efb5f3a5e24823c816599005c57.jpg")
dst = os.path.join(d, "user_photo_slide1.jpg")
if os.path.exists(src):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    # Center crop to 16:9
    target_ratio = 1920/1080
    img_ratio = w/h
    if img_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w)//2
        im = im.crop((left, 0, left+new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h)//2
        im = im.crop((0, top, w, top+new_h))
    im = im.resize((1920, 1080), Image.LANCZOS)
    im.save(dst, "JPEG", quality=95)
    print("Created user_photo_slide1.jpg:", im.size)