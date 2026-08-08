#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unified batch image downloader — replaces dl_bing.py, dl_pexels.py,
download_images.py, download_us_imgs.py, download_hd_images.py, etc.

Usage:
    python image_downloader.py                    # use built-in keyword list
    python image_downloader.py --keywords kw.json # custom keyword JSON
    python image_downloader.py --dir ./out        # custom output dir
    python image_downloader.py --enhance          # auto-enhance after download
"""
import argparse, json, os, re, sys, time
from urllib.parse import quote

import requests

# -----------------------------------------------------------------------
# Default keyword list — (save_name, bing_search_query)
# -----------------------------------------------------------------------
DEFAULT_KEYWORDS = [
    ("us_capitol",          "US Capitol building Washington DC"),
    ("american_flag_eagle", "American flag bald eagle patriotic"),
    ("grand_canyon",        "Grand Canyon national park USA landscape"),
    ("statue_of_liberty",   "Statue of Liberty New York"),
    ("mount_rushmore",      "Mount Rushmore presidents South Dakota"),
    ("white_house",         "White House Washington DC"),
    ("us_manufacturing",    "American factory manufacturing industry"),
    ("new_york_city",       "New York City skyline Manhattan"),
    ("republican_rally",    "Republican party rally crowd people flag"),
    ("us_infrastructure",   "American highway bridge construction infrastructure"),
    ("us_china_cooperation","USA China cooperation handshake global trade"),
    ("american_healthcare", "American hospital healthcare medical center"),
    ("us_education",        "American school university students education graduation"),
    ("liberty_bell",        "Liberty Bell Philadelphia Pennsylvania USA"),
    ("times_square",        "Times Square New York City USA night view"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# -----------------------------------------------------------------------
def _extract_image_urls(html):
    """Try several regex patterns to pull image URLs from Bing results."""
    patterns = [
        r'mediaurl="([^"]+)"',
        r'"murl":"([^"]+)"',
        r'&quot;murl&quot;:&quot;([^&]+)&quot;',
    ]
    urls = []
    for pat in patterns:
        found = re.findall(pat, html)
        urls.extend(found)
    return urls


def download_one(name, query, out_dir, min_bytes=10000, timeout=15):
    """Download the first usable image for (name, query) into out_dir."""
    encoded = quote(query)
    search_url = (
        "https://www.bing.com/images/search?q=" + encoded +
        "&FORM=HDRSC2&first=1"
    )

    try:
        resp = requests.get(search_url, headers=HEADERS, timeout=timeout)
    except Exception as exc:
        print(f"  [FAIL] {name}: search request error — {exc}")
        return None

    if resp.status_code != 200:
        print(f"  [FAIL] {name}: HTTP {resp.status_code}")
        return None

    urls = _extract_image_urls(resp.text)
    if not urls:
        print(f"  [SKIP] {name}: no image URLs found in search results")
        return None

    for idx, img_url in enumerate(urls[:5]):
        if not img_url.startswith("http"):
            continue
        try:
            img_resp = requests.get(img_url, headers=HEADERS, timeout=timeout)
            if img_resp.status_code == 200 and len(img_resp.content) >= min_bytes:
                suffix = "" if idx == 0 else f"_{idx}"
                fname = os.path.join(out_dir, f"{name}{suffix}.jpg")
                with open(fname, "wb") as fh:
                    fh.write(img_resp.content)
                size_kb = len(img_resp.content) // 1024
                print(f"  [OK]   {name} -> {os.path.basename(fname)} ({size_kb} KB)")
                return fname
        except Exception:
            continue

    print(f"  [SKIP] {name}: all image URLs failed to download")
    return None


def download_batch(keywords, out_dir, min_bytes=10000, delay=0.5):
    """Download all keywords, return list of (name, path)."""
    os.makedirs(out_dir, exist_ok=True)
    downloaded = []
    total = len(keywords)

    for idx, (name, query) in enumerate(keywords, 1):
        print(f"[{idx}/{total}] Searching: {name}")
        path = download_one(name, query, out_dir, min_bytes)
        if path:
            downloaded.append((name, path))
        time.sleep(delay)

    return downloaded


def enhance_images(img_dir, min_dim=1920):
    """Resize small images and sharpen. Requires Pillow."""
    try:
        from PIL import Image, ImageEnhance, ImageFilter
    except ImportError:
        print("[WARN] Pillow not installed; skipping enhancement.")
        return

    for fname in sorted(os.listdir(img_dir)):
        if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        fp = os.path.join(img_dir, fname)
        try:
            im = Image.open(fp).convert("RGB")
            w, h = im.size
            if w < min_dim or h < (min_dim * 9 // 16):
                im = im.resize((min_dim, min_dim * 9 // 16), Image.LANCZOS)
                im = im.filter(ImageFilter.SHARPEN)
                enh = ImageEnhance.Contrast(im)
                im = enh.enhance(1.15)
                im.save(fp, "JPEG", quality=92)
                print(f"  Enhanced: {fname} -> {im.size[0]}x{im.size[1]}")
        except Exception as exc:
            print(f"  [WARN] {fname}: enhancement failed — {exc}")


# -----------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Batch download images from Bing image search."
    )
    parser.add_argument(
        "--dir", default=None,
        help="Output directory (default: ./downloaded_images)"
    )
    parser.add_argument(
        "--keywords", default=None,
        help="Path to JSON file with [[name, query], ...] list"
    )
    parser.add_argument(
        "--enhance", action="store_true",
        help="Auto-enhance images after download (requires Pillow)"
    )
    parser.add_argument(
        "--min-bytes", type=int, default=10000,
        help="Minimum file size to accept (default: 10000)"
    )
    args = parser.parse_args()

    out_dir = args.dir or os.path.join(os.getcwd(), "downloaded_images")

    if args.keywords:
        with open(args.keywords, "r", encoding="utf-8") as fh:
            keywords = json.load(fh)
    else:
        keywords = DEFAULT_KEYWORDS

    print(f"Target directory: {out_dir}")
    print(f"Keywords to process: {len(keywords)}\n")

    downloaded = download_batch(keywords, out_dir, min_bytes=args.min_bytes)

    print(f"\n=== Downloaded {len(downloaded)}/{len(keywords)} images ===")
    for name, path in downloaded:
        sz = os.path.getsize(path) // 1024
        print(f"  {name}: {os.path.basename(path)} ({sz} KB)")

    if args.enhance and downloaded:
        print("\nEnhancing images...")
        enhance_images(out_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
