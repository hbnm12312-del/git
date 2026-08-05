import zipfile, re, os
pp = r"C:\Users\FYH\Documents\New project\Ding_Dongxu_President.pptx"
print("=== Final Verification ===")
sz = os.path.getsize(pp)
print("File size:", sz//1024, "KB")
with zipfile.ZipFile(pp) as z:
    media = sorted(f for f in z.namelist() if f.startswith("ppt/media/"))
    print("Images:", len(media))
    for m in media:
        print(" ", m, z.getinfo(m).file_size//1024, "KB")
    slides = sorted(f for f in z.namelist() if f.startswith("ppt/slides/slide") and f.endswith(".xml"))
    print()
    rels = sorted(f for f in z.namelist() if "slides/_rels" in f)
    print("Slide images:")
    for r in rels:
        xml = z.read(r).decode("utf-8")
        imgs = re.findall(r'Target="(\.\./media/[^"]+)"', xml)
        sn = r.split("/")[-1].replace(".rels","")
        print("  %s: %s" % (sn, ", ".join(imgs)))
    print("\nChinese chars per slide:")
    for sn in slides:
        xml = z.read(sn).decode("utf-8")
        cn = sum(1 for c in xml if 0x4e00 <= ord(c) <= 0x9fff)
        print("  %s: %d" % (sn.split("/")[-1], cn))
print("\nAll OK!")