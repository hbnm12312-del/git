import requests
import os
import re
from urllib.parse import quote

img_dir = r"C:\Users\FYH\Documents\New project\ppt_images"

keywords = [
    ("shanxi_mountains", "Xi'an Shaanxi China landscape mountain"),
    ("terracotta_warriors", "Terracotta Warriors Xi'an China"),
    ("yanan_pagoda", "Yan'an Pagoda Hill Shaanxi China"),
    ("qinling_mountains", "Qinling Mountains Shaanxi China"),
    ("hua_shan", "Mount Hua Shaanxi China"),
    ("xian_city_wall", "Xi'an ancient city wall China"),
    ("red_flag", "red flag communist party China"),
    ("yanan_revolution", "Yan'an revolutionary sacred site Shaanxi China"),
    ("giant_wild_goose_pagoda", "Giant Wild Goose Pagoda Xi'an China"),
    ("hukou_waterfall", "Hukou Waterfall Yellow River Shaanxi China")
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

downloaded = []

for name, query in keywords:
    encoded_query = quote(query)
    url = f"https://www.bing.com/images/search?q={encoded_query}&FORM=HDRSC2&first=1"
    
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            urls = re.findall(r'mediaurl="([^"]+)"', resp.text)
            if not urls:
                urls = re.findall(r'"murl":"([^"]+)"', resp.text)
            if not urls:
                urls = re.findall(r'&quot;murl&quot;:&quot;([^&]+)&quot;', resp.text)
            
            for i, img_url in enumerate(urls[:3]):
                if img_url.startswith('http'):
                    suffix = "" if i == 0 else f"_{i}"
                    fname = os.path.join(img_dir, f"{name}{suffix}.jpg")
                    try:
                        img_resp = requests.get(img_url, headers=headers, timeout=15)
                        if img_resp.status_code == 200 and len(img_resp.content) > 10000:
                            with open(fname, 'wb') as f:
                                f.write(img_resp.content)
                            downloaded.append((os.path.basename(fname), len(img_resp.content)))
                            print(f"OK: {os.path.basename(fname)} ({len(img_resp.content)} bytes)")
                            break
                    except:
                        pass
    except Exception as e:
        print(f"FAIL: {query} - {e}")

print(f"\n=== Downloaded {len(downloaded)} images ===")
for f, s in downloaded:
    print(f"  {f}: {s} bytes")
if not downloaded:
    print("No images downloaded via Bing. Trying alternative sources...")
