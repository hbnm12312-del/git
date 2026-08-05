import re
fp = r'C:\Users\FYH\Documents\New project\create_ppt_v3.py'
c = open(fp, 'r', encoding='utf-8').read()
rs = {
    "sb(s, 'republican_rally') or sb(s, 'us_capitol')": "bo(s, 'republican_rally,us_capitol')",
    "sb(s, 'us_capitol') or sb(s, 'white_house')": "bo(s, 'us_capitol,white_house', '10000000')",
    "sb(s, 'statue_of_liberty') or sb(s, 'grand_canyon')": "bo(s, 'statue_of_liberty,grand_canyon')",
    "sb(s, 'us_manufacturing') or sb(s, 'new_york_city')": "bo(s, 'us_manufacturing,new_york_city')",
    "sb(s, 'statue_of_liberty') or sb(s, 'liberty_bell')": "bo(s, 'statue_of_liberty,liberty_bell')",
    "sb(s, 'us_china_cooperation') or sb(s, 'times_square')": "bo(s, 'us_china_cooperation,times_square', '10000000')",
    "sb(s, 'us_infrastructure') or sb(s, 'american_healthcare')": "bo(s, 'us_infrastructure,american_healthcare')",
    "sb(s, 'us_education') or sb(s, 'times_square')": "bo(s, 'us_education,times_square')",
    "sb(s, 'mount_rushmore') or sb(s, 'republican_rally')": "bo(s, 'mount_rushmore,republican_rally', '15000000')",
    "sb(s, 'american_flag_eagle') or sb(s, 'white_house')": "bo(s, 'american_flag_eagle,white_house')",
}
for old, new in rs.items():
    n = c.count(old)
    if n > 0:
        c = c.replace(old, new)
        print('Replaced: %s (%d)' % (old[:50], n))
open(fp, 'w', encoding='utf-8').write(c)
print('Done')