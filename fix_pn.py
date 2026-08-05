fp = r"C:\Users\FYH\Documents\New project\create_ppt_v4.py"
c = open(fp, "r", encoding="utf-8").read()
old = "def Pn(sl,x,y,w,h):\n    p=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,x,y,w,h)\n    p.fill.solid();p.fill.fore_color.rgb=DKBG;ap(p,\"70000000\")\n    p.line.color.rgb=RED;p.line.width=Pt(1.5)"
new = "def Pn(sl,x,y,w,h,bg=None,al=None):\n    p=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,x,y,w,h)\n    g=bg if bg else DKBG; a=al if al else \"70000000\"\n    p.fill.solid();p.fill.fore_color.rgb=g;ap(p,a)\n    p.line.color.rgb=RED;p.line.width=Pt(1.5)"
c = c.replace(old, new)
open(fp, "w", encoding="utf-8").write(c)
print("Fixed")