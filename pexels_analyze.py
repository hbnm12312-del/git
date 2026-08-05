import requests
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
r = requests.get("https://www.pexels.com/search/us+capitol/", headers=headers, timeout=15)
# Save first 2000 chars for analysis
sample = r.text[:2000]
print(sample.replace(">", ">\n"))