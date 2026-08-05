# -*- coding: utf-8 -*-
import requests, os, re, time
from urllib.parse import quote

img_dir = r"C:\Users\FYH\Documents\New project\us_imgs"
os.makedirs(img_dir, exist_ok=True)

keywords = [
    ("us_capitol", "US Capitol building Washington DC"),
    ("american_flag_eagle", "American flag bald eagle patriotic"),
    ("grand_canyon", "Grand Canyon national park USA landscape"),
    ("statue_of_liberty", "Statue of Liberty New York"),
    ("mount_rushmore", "Mount Rushmore presidents South Dakota"),
    ("white_house", "White House Washington DC"),
    ("us_manufacturing", "American factory manufacturing industry"),
    ("new_york_city", "New York City skyline Manhattan"),
    ("republican_rally", "Republican party rally crowd people flag"),
    ("us_infrastructure", "American highway bridge construction infrastructure"),
    ("us_china_cooperation", "USA China cooperation handshake global trade"),
    ("american_healthcare", "American hospital healthcare medical center"),
    ("us_education", "American school university students education graduation"),
    ("liberty_bell", "Liberty Bell Philadelphia Pennsylvania USA"),
    ("times_square", "Times Square New York City USA night view"),
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

downloaded = []

for name, query in keywords:
    encoded_query = quote(query)
    url = "https://www.bing.com/images/search?q=" + encoded_query + "&FORM=HDRSC2&first=1"
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            urls = re.findall(r'mediaurl="([^"]+)"', resp.text)
            if not urls:
                urls = re.findall(r'"murl":"([^"]+)"', resp.text)
            if not urls:
                urls = re.findall(r'&quot;murl&quot;:&quot;([^&]+)&quot;', resp.text)
            
            for i, img_url in enumerate(urls[:4]):
                if img_url.startswith("http"):
                    suffix = "" if i == 0 else "_{}".format(i)
                    fname = os.path.join(img_dir, "{}{}.jpg".format(name, suffix))
                    try:
                        img_resp = requests.get(img_url, headers=headers, timeout=15)
                        if img_resp.status_code == 200 and len(img_resp.content) > 10000:
                            with open(fname, "wb") as f:
                                f.write(img_resp.content)
                            downloaded.append((os.path.basename(fname), len(img_resp.content)))
                            print("OK: {} ({} bytes)".format(os.path.basename(fname), len(img_resp.content)))
                            break
                    except:
                        pass
    except Exception as e:
        print("FAIL: {} - {}".format(query, e))
    time.sleep(0.5)

print("\n=== Downloaded {} images ===".format(len(downloaded)))
for f, s in downloaded:
    print("  {}: {} bytes".format(f, s))
if not downloaded:
    print("No images downloaded via Bing. Trying alternative sources...")
    import urllib.request
    fallback = {
        "us_capitol": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/US_Capitol_west_side.JPG/800px-US_Capitol_west_side.JPG",
        "american_flag_eagle": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Bald_Eagle_Portrait.jpg/800px-Bald_Eagle_Portrait.jpg",
        "statue_of_liberty": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Statue_of_Liberty_7.jpg/800px-Statue_of_Liberty_7.jpg",
    }
    for name, f_url in fallback.items():
        fname = os.path.join(img_dir, "{}.jpg".format(name))
        try:
            urllib.request.urlretrieve(f_url, fname)
            sz = os.path.getsize(fname)
            downloaded.append((os.path.basename(fname), sz))
            print("Fallback OK: {} ({} bytes)".format(os.path.basename(fname), sz))
        except Exception as e2:
            print("Fallback FAIL: {} - {}".format(name, e2))
    print("\n=== Final: Downloaded {} images ===".format(len(downloaded)))
    for f, s in downloaded:
        print("  {}: {} bytes".format(f, s))
