import sys, os
sys.path.append(r'C:\Users\FYH\AppData\Local\Programs\Python\Python313\Lib\site-packages')
from pptx import Presentation
p = r'C:\Users\FYH\Desktop\班长竞选_房振平.pptx'
prs = Presentation(p)
print(f'Success! {len(prs.slides)} slides')
