fp = r"C:\Users\FYH\Documents\New project\create_ppt_v4.py"
c = open(fp, "r", encoding="utf-8").read()
# Replace SLIDE_IMGS to use only unique images
old_imgs = """SLIDE_IMGS = [
    ["republican_rally", "us_capitol"],
    ["us_capitol", "white_house"],
    ["statue_of_liberty", "grand_canyon"],
    ["us_manufacturing", "new_york_city"],
    ["statue_of_liberty", "liberty_bell"],
    ["us_china_cooperation", "times_square"],
    ["us_infrastructure", "american_healthcare"],
    ["us_education", "times_square"],
    ["mount_rushmore", "republican_rally"],
    ["american_flag_eagle", "white_house"],
]"""
new_imgs = """SLIDE_IMGS = [
    ["republican_rally", "us_capitol"],
    ["us_capitol", "white_house"],
    ["statue_of_liberty", "grand_canyon"],
    ["mount_rushmore", "new_york_city"],
    ["statue_of_liberty", "liberty_bell"],
    ["us_capitol", "times_square"],
    ["times_square", "new_york_city"],
    ["new_york_city", "times_square"],
    ["mount_rushmore", "republican_rally"],
    ["american_flag_eagle", "white_house"],
]"""
c = c.replace(old_imgs, new_imgs)
open(fp, "w", encoding="utf-8").write(c)
print("Updated SLIDE_IMGS")