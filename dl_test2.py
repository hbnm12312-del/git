import requests, re, os
d = r"C:\Users\FYH\Documents\New project\us_imgs_hd2"
os.makedirs(d, exist_ok=True)
headers = {"User-Agent": "Mozilla/5.0"}
try:
    r = requests.get("https://www.bing.com/images/search?q=Grand+Canyon+landscape+huge&FORM=HDRSC2", headers=headers, timeout=10)
    print("Got HTML, length:", len(r.text))
    # Save HTML to analyze
    with open(os.path.join(d, "bing_result.html"), "w", encoding="utf-8") as f:
        f.write(r.text[:5000])
    print("Saved HTML sample")
except Exception as e:
    print("Error:", str(e)[:80])