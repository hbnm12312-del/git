
# -*- coding: utf-8 -*-
import requests, os, re, time, urllib.request, urllib.parse

img_dir = r"C:\Users\FYH\Documents\New project\us_imgs"
os.makedirs(img_dir, exist_ok=True)

# ???????? - ????Wikimedia/??CDN
sources = [
    # (filename, bing_search, fallback_wikimedia_url)
    ("us_capitol.jpg", "US Capitol building Washington DC high resolution wallpaper",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/US_Capitol_east_side.JPG/1280px-US_Capitol_east_side.JPG"),
    ("american_flag_eagle.jpg", "American flag bald eagle patriotic wallpaper high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Bald_eagle_about_to_fish_in_the_Pacific_Northwest.jpg/1280px-Bald_eagle_about_to_fish_in_the_Pacific_Northwest.jpg"),
    ("grand_canyon.jpg", "Grand Canyon national park Arizona USA high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Grand_Canyon_View.jpg/1280px-Grand_Canyon_View.jpg"),
    ("statue_of_liberty.jpg", "Statue of Liberty New York high resolution wallpaper",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Statue_of_Liberty_2023.jpg/1280px-Statue_of_Liberty_2023.jpg"),
    ("mount_rushmore.jpg", "Mount Rushmore South Dakota USA high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Mount_Rushmore_detail_view.jpg/1280px-Mount_Rushmore_detail_view.jpg"),
    ("white_house.jpg", "White House Washington DC night high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/White_House_2022.jpg/1280px-White_House_2022.jpg"),
    ("us_manufacturing.jpg", "American factory manufacturing industry workers high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Ford_Rouge_Plant_2006.jpg/1280px-Ford_Rouge_Plant_2006.jpg"),
    ("new_york_city.jpg", "New York City skyline Manhattan high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/New_york_times_square_terabass.jpg/1280px-New_york_times_square_terabass.jpg"),
    ("republican_rally.jpg", "Republican convention rally crowd American flag high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/2016_Republican_National_Convention_10.jpg/1280px-2016_Republican_National_Convention_10.jpg"),
    ("us_infrastructure.jpg", "American highway bridge construction infrastructure high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/MacArthur_Maze_Bridge.jpg/1280px-MacArthur_Maze_Bridge.jpg"),
    ("american_healthcare.jpg", "American hospital healthcare medical center high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Massachusetts_General_Hospital_2024.jpg/1280px-Massachusetts_General_Hospital_2024.jpg"),
    ("us_education.jpg", "American university campus students graduation high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Harvard_Yard_2021.jpg/1280px-Harvard_Yard_2021.jpg"),
    ("liberty_bell.jpg", "Liberty Bell Philadelphia Pennsylvania high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Liberty_Bell_2008.jpg/1280px-Liberty_Bell_2008.jpg"),
    ("times_square.jpg", "Times Square New York City night high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/New_york_times_square_terabass.jpg/1280px-New_york_times_square_terabass.jpg"),
    ("us_china_flag.jpg", "USA China flags together diplomatic high resolution",
     "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/US_and_Chinese_flags.jpg/1280px-US_and_Chinese_flags.jpg"),
]

downloaded = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

for fname, query, fallback_url in sources:
    fp = os.path.join(img_dir, fname)
    
    # Strategy 1: Try Bing for larger size
    try:
        encoded = urllib.parse.quote(query)
        url = "https://www.bing.com/images/search?q=" + encoded + "&qft=+filterui:imagesize-large&FORM=IRFLTR"
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            urls = re.findall(r'mediaurl="([^"]+)"', resp.text)
            if not urls:
                urls = re.findall(r'"murl":"([^"]+)"', resp.text)
            for img_url in urls[:5]:
                if img_url.startswith("http"):
                    try:
                        img_resp = requests.get(img_url, headers=headers, timeout=15)
                        if len(img_resp.content) > 50000:
                            with open(fp, "wb") as f:
                                f.write(img_resp.content)
                            sz = len(img_resp.content)
                            downloaded.append((fname, sz, "Bing"))
                            print(f"Bing OK: {fname} ({sz} bytes)")
                            break
                    except:
                        pass
    except:
        pass
    
    # Strategy 2: Fallback to Wikimedia
    if not os.path.exists(fp) or os.path.getsize(fp) < 50000:
        try:
            urllib.request.urlretrieve(fallback_url, fp)
            sz = os.path.getsize(fp)
            if sz > 50000:
                downloaded.append((fname, sz, "Wiki"))
                print(f"Wiki OK: {fname} ({sz} bytes)")
            else:
                print(f"Wiki SMALL: {fname} ({sz} bytes)")
        except Exception as e:
            print(f"FAIL: {fname} - {e}")
    
    time.sleep(0.3)

print(f"\n=== Downloaded/Updated {len(downloaded)} images ===")
for f, s, src in downloaded:
    print(f"  [{src}] {f}: {s} bytes")

# Convert to JPEG for PPT
from PIL import Image
for f in os.listdir(img_dir):
    if f.lower().endswith(('.png', '.webp', '.tif', '.bmp')):
        fp = os.path.join(img_dir, f)
        try:
            im = Image.open(fp).convert("RGB")
            new_fp = os.path.join(img_dir, os.path.splitext(f)[0] + ".jpg")
            im.save(new_fp, "JPEG", quality=95)
            os.remove(fp)
            print(f"Converted: {f} -> {os.path.basename(new_fp)}")
        except:
            pass

print("\n=== Final image sizes ===")
for f in sorted(os.listdir(img_dir)):
    fp = os.path.join(img_dir, f)
    sz = os.path.getsize(fp)
    try:
        im = Image.open(fp)
        print(f"  {f}: {im.size[0]}x{im.size[1]} px, {sz//1024} KB")
    except:
        print(f"  {f}: {sz//1024} KB (unreadable)")
