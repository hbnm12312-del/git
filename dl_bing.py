import requests, re, io, os
from PIL import Image

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
d = r"C:\Users\FYH\Documents\New project\us_imgs_hd"

# Try Bing image search with different regex patterns
queries = {
    "us_capitol": "US Capitol building Washington DC high resolution",
    "statue_of_liberty": "Statue of Liberty New York USA high resolution",
    "mount_rushmore": "Mount Rushmore South Dakota USA high res",
    "times_square": "Times Square New York City night high resolution",
    "new_york_city": "New York City skyline Manhattan high resolution",
}

for name, query in queries.items():
    try:
        encoded = requests.utils.quote(query)
        url = "https://www.bing.com/images/search?q=" + encoded + "&qft=+filterui:imagesize-wallpaper&FORM=IRFLTR"
        r = requests.get(url, headers=headers, timeout=15)
        
        # Try all possible URL patterns
        all_urls = []
        patterns = [
            r'mediaurl="([^"]+)"',
            r'"murl":"([^"]+)"',
            r'imgurl="([^"]+)"',
            r'<a[^>]+href="([^"]+\.jpg[^"]*)"',
        ]
        for pat in patterns:
            found = re.findall(pat, r.text)
            all_urls.extend(found)
        
        if all_urls:
            print(name + ": found " + str(len(all_urls)) + " URLs")
            for img_url in all_urls[:5]:
                print("  " + str(img_url[:100]))
        else:
            print(name + ": no URLs found")
    except Exception as e:
        print(name + ": FAIL - " + str(e)[:60])