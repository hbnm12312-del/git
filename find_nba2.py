import requests, io, os
from PIL import Image
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
d = r"C:\Users\FYH\Desktop"

# Try known URLs for this iconic NBA 2020 photo
# These are known Getty/NBA associated image domains
urls_to_try = [
    # Try NBA official CDN with various known patterns
    "https://cdn.nba.com/teams/uploads/sites/1610612747/2020/10/lakers-champions-2020.jpg",
    "https://library.sportingnews.com/styles/facebook_1200x630/s3/2020-10/nba-lakers-lebron-james-trophy-10122020.jpg",
    # Try known Getty watermark-free URLs
    "https://www.nba.com/lakers/sites/lakers/files/styles/story_main_image/public/leBron_James_Anthony_Davis_Trophy_2020.jpg",
]

# Also try searching via a simpler Bing query
import urllib.parse
query = "LeBron James Anthony Davis trophy 2020 Lakers champions HD"
encoded = urllib.parse.quote(query)
try:
    r = requests.get("https://www.bing.com/images/search?q=" + encoded, headers=headers, timeout=10)
    import re
    urls = re.findall(r'mediaurl="([^"]+)"', r.text)
    for u in urls:
        if ("lebron" in u.lower() or "lakers" in u.lower() or "james" in u.lower() or "trophy" in u.lower()):
            if "jpg" in u.lower() or "jpeg" in u.lower():
                urls_to_try.append(u)
                break
except:
    pass

# Try downloading each URL
for i, url in enumerate(urls_to_try):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if len(r.content) > 20000:
            im = Image.open(io.BytesIO(r.content))
            fp = os.path.join(d, f"nba_photo_{i}.jpg")
            im.save(fp, "JPEG", quality=92)
            print(f"OK #{i}: {im.size[0]}x{im.size[1]} {len(r.content)//1024}KB - {url[:80]}")
        else:
            print(f"Small #{i}: {len(r.content)} bytes")
    except Exception as e:
        print(f"FAIL #{i}: {str(e)[:40]}")