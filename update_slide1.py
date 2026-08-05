fp = r"C:\Users\FYH\Documents\New project\create_ppt_v4.py"
c = open(fp, "r", encoding="utf-8").read()
# Add user photo to slide 1 - insert after T["s1_name_en"] line
old = 'Tb(s, Emu(800000), Emu(1900000), Emu(int(SW-1600000)), Emu(400000), T["s1_name_en"], 40, True, WHITE, PP_ALIGN.CENTER)'
new = old + '\n# User photo on title slide\nup_path = os.path.join(IMG, "user_photo_slide1.jpg")\nif os.path.exists(up_path):\n    try:\n        circ = Emu(1200000)\n        cx = int(SW/2 - circ/2)\n        s.shapes.add_picture(up_path, cx, Emu(2950000), circ, circ)\n        border = s.shapes.add_shape(MSO_SHAPE.OVAL, cx, Emu(2950000), circ, circ)\n        border.fill.background(); border.line.color.rgb = GOLD; border.line.width = Pt(3)\n    except:\n        pass'
c = c.replace(old, new)
# Fix the BG call for slide 1 to use the right opacity
# Also move the career text down to make room for photo
c = c.replace('Tb(s, Emu(800000), Emu(2500000), Emu(int(SW-1600000)), Emu(350000), T["s1_slogan"], 18, True, GOLD, PP_ALIGN.CENTER)',
    'Tb(s, Emu(800000), Emu(2500000), Emu(int(SW-1600000)), Emu(350000), T["s1_slogan"], 18, True, GOLD, PP_ALIGN.CENTER)')
open(fp, "w", encoding="utf-8").write(c)
print("Added user photo to slide 1")