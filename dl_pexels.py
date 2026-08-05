import requests, io, os, re
from PIL import Image

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
d = r"C:\Users\FYH\Documents\New project\us_imgs_hd"

# Search Pexels for specific images
searches = {
    "republican_rally": "republican+convention+crowd+usa",
    "us_capitol": "us+capitol+building+washington+dc",
    "statue_of_liberty": "statue+of+liberty+new+york+usa",
    "mount_rushmore": "mount+rushmore+south+dakota",
    "times_square": "times+square+new+york+night",
    "new_york_city": "new+york+city+skyline+manhattan",
    "american_flag_eagle": "american+flag+usa+eagle+patriotic",
    "grand_canyon": "grand+canyon+arizona+sunset",
    "white_house": "white+house+washington+dc",
    "liberty_bell": "liberty+bell+philadelphia",
}

for name, query in searches.items():
    search_url = "https://www.pexels.com/search/" + query + "/"
    try:
        r = requests.get(search_url, headers=headers, timeout=15)
        # Find image URLs in pexels HTML
        img_urls = []
        # Try multiple patterns
        for pat in [r'data-src="([^"]+\.jpg[^"]*)"', r'<img[^>]+src="([^"]+\.jpg[^"]*)"']:
            found = re.findall(pat, r.text)
            img_urls.extend(found)
        
        if img_urls:
            # Try to download the first high-res image
            for img_url in img_urls:
                if "pexels.com" in img_url or img_url.startswith("http"):
                    try:
                        ir = requests.get(img_url, headers=headers, timeout=10)
                        if len(ir.content) > 20000:
                            im = Image.open(io.BytesIO(ir.content))
                            fp = os.path.join(d, name + ".jpg")
                            # Resize to 1920x1080 if needed
                            if im.size[0] < 1920 or im.size[1] < 1080:
                                im = im.resize((1920, 1080), Image.LANCZOS)
                            im.save(fp, "JPEG", quality=92)
                            print("OK: " + name + " -> " + str(im.size) + " " + str(len(ir.content)//1024) + "KB")
                            break
                    except:
                        pass
        else:
            print("NO IMAGES: " + name)
    except Exception as e:
        print("FAIL: " + name + " - " + str(e)[:50])