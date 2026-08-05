import requests, re, os
d = r"C:\Users\FYH\Documents\New project\us_imgs_hd2"
os.makedirs(d, exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0"}
try:
    r = requests.get("https://www.bing.com/images/search?q=US+Capitol+Washington+DC&FORM=HDRSC2", headers=headers, timeout=10)
    print("Bing OK:", r.status_code, len(r.text))
    # Find image URLs
    urls = re.findall(r"mediaurl=\"([^\"]+)\"", r.text)
    if not urls:
        urls = re.findall(r'"murl":"([^"]+)"', r.text)
    print("Found", len(urls), "image URLs")
    if len(urls) > 0:
        from PIL import Image
        import io
        for i, url in enumerate(urls[:2]):
            try:
                ir = requests.get(url, headers=headers, timeout=10)
                if len(ir.content) > 10000:
                    im = Image.open(io.BytesIO(ir.content))
                    print("  URL", i+1, ":", im.size[0], "x", im.size[1], len(ir.content)//1024, "KB")
            except Exception as e2:
                print("  URL", i+1, "failed:", str(e2)[:50])
except Exception as e:
    print("Bing failed:", str(e)[:80])