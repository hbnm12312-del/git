import requests, re, io, os
from PIL import Image
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
d = r"C:\Users\FYH\Desktop"

# Search Bing for the image
query = "LeBron James Anthony Davis 2020 NBA Finals trophy arm"
encoded = requests.utils.quote(query)
url = "https://www.bing.com/images/search?q=" + encoded + "&FORM=HDRSC2"
r = requests.get(url, headers=headers, timeout=15)

# Find image URLs
all_urls = set()
text = r.text
# Pattern 1: mediaurl
for m in re.finditer(r'mediaurl="([^"]+)"', text):
    u = m.group(1)
    if u.startswith("http") and ("jpg" in u.lower() or "jpeg" in u.lower() or "png" in u.lower()):
        all_urls.add(u)

# Pattern 2: imgurl
for m in re.finditer(r'"imgurl":"([^"]+)"', text):
    u = m.group(1).replace("\\/", "/")
    if u.startswith("http"):
        all_urls.add(u)

print("Found", len(all_urls), "URLs")
for u in list(all_urls)[:15]:
    print(u[:120])