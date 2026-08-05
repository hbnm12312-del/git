import requests, re, io, os
from PIL import Image

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
d = r"C:\Users\FYH\Documents\New project\us_imgs_hd"

# Test with Bing search - find actual image URLs
query = "US Capitol building Washington DC"
encoded = requests.utils.quote(query)
url = "https://www.bing.com/images/search?q=" + encoded + "&FORM=HDRSC2"
r = requests.get(url, headers=headers, timeout=15)

# Save HTML sample to analyze
with open(os.path.join(d, "bing_sample.html"), "w", encoding="utf-8") as f:
    f.write(r.text[:10000])

# Try different patterns
patterns = [
    ("mediaurl", r'mediaurl="([^"]+)"'),
    ("murl", r'"murl":"([^"]+)"'),
    ("imgurl", r'"imgurl":"([^"]+)"'),
    ("thurl", r'"thurl":"([^"]+)"'),
    ("src (img)", r'<img[^>]+src="([^"]+)"'),
    ("src (div)", r'div[^>]+src="([^"]+)"'),
    ("http in text", r'https?://[^"\'<>]+\.(?:jpg|jpeg|png)[^"\'<>]*'),
]

for label, pat in patterns:
    found = re.findall(pat, r.text, re.IGNORECASE)
    if found:
        print(label + ": " + str(len(found)) + " matches")
        for f2 in found[:3]:
            print("  " + str(f2)[:120])
    else:
        print(label + ": 0 matches")