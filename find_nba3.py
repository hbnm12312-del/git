import requests, io, os, re
from PIL import Image
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
d = r"C:\Users\FYH\Desktop"

# Try DuckDuckGo image search (less restrictive)
query = "LeBron James Anthony Davis 2020 NBA Finals trophy HD"
encoded = requests.utils.quote(query)
try:
    r = requests.get("https://lite.duckduckgo.com/lite/?q=" + encoded, headers=headers, timeout=10)
    print("DuckDuckGo:", r.status_code, len(r.text))
except:
    print("DuckDuckGo: FAIL")

# Try Getty Images directly  
try:
    r = requests.get("https://www.gettyimages.com/photos/lebron-james-anthony-davis-2020-finals?license=rf", headers=headers, timeout=10)
    print("Getty:", r.status_code, len(r.text))
except:
    print("Getty: FAIL")

# Try Zimbio
try:
    r = requests.get("https://www.zimbio.com/search?q=LeBron+James+2020+NBA+Finals+trophy", headers=headers, timeout=10)
    print("Zimbio:", r.status_code, len(r.text))
except:
    print("Zimbio: FAIL")