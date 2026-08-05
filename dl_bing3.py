import requests, re, io, os, json
from PIL import Image

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
d = r"C:\Users\FYH\Documents\New project\us_imgs_hd"

# Read the Bing sample and find URL pattern
html = open(os.path.join(d, "bing_sample.html"), "r", encoding="utf-8").read()

# Look for murl in the raw text
idx = html.find("murl")
if idx >= 0:
    print("Found 'murl' at position", idx)
    print("Context:", html[max(0,idx-20):idx+80])
    
# Let me try: search for the pattern "murl":"URL" in different ways
# The quotes in HTML might be unicode quotes
all_matches = []
for i, c in enumerate(html):
    if html[i:i+6] == '"murl"':
        # Find the URL after it
        start = html.find('"', i+8)
        if start >= 0:
            end = html.find('"', start+1)
            if end >= 0:
                url = html[start+1:end]
                if url.startswith("http"):
                    all_matches.append(url)

print("\nFound", len(all_matches), "murl URLs")
for u in all_matches[:3]:
    print(" ", u[:120])