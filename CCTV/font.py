import matplotlib.font_manager as fm

def font():
    font_path = 'C:\\Users\\bj490\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NanumGothic.ttf'
    font_name = fm.FontProperties(fname=font_path).get_name()
    return font_name
print(font())