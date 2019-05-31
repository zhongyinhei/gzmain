import aircv as ac
import sys
# pyautogui.screenshot(IMGSRC)
imgobj = r'\bljdgz.jpg'
file=sys.path[0]
IMGSRC=file+'\screenshot.jpg'
imsrc = ac.imread(IMGSRC)
imobj = ac.imread(file + imgobj)
match_result = ac.find_template(imsrc, imobj,
                                0.7)
print(match_result)