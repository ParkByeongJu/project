import matplotlib.font_manager as fm

def font():
    font_path = 'C:\\Windows\\Fonts\\Malgun.ttf'
    font_name = fm.FontProperties(fname=font_path).get_name()
    return font_name