import re
html = open(r"C:\Users\FYH\Documents\New project\us_imgs_hd2\bing_result.html", "r", encoding="utf-8").read()
# Try various patterns
patterns = [
    '"murl":"([^"]+)"',
    "mediaurl=\"([^\"]+)\"",
    '"contentUrl":"([^"]+)"',
    '"thumbnailUrl":"([^"]+)"',
    '"url":"([^"]+)"',
    "src=\"([^\"]*\.jpg[^\"]*)\"",
    'src="([^"]+\.jpg)"',
]
for pat in patterns:
    matches = re.findall(pat, html)
    if matches:
        print("Pattern:", pat[:40])
        for m in matches[:3]:
            print("  ", str(m)[:100])
        break
else:
    print("No patterns matched")
    # Search for any jpg URL
    all_jpg = re.findall(r'https?://[^"\'<>]+\.jpg[^"\'<>]*', html)
    print("JPG URLs found:", len(all_jpg))
    for j in all_jpg[:5]:
        print("  ", j[:120])