from PIL import Image

def getCmd(color):
    if color == "(255, 128, 0)":
        return "print"
    elif color == "(191, 0, 0)":
        return '(f"'
    elif color == "(0, 0, 191)":
        return '")'
    elif color == "(16, 16, 16)":
        return "\n"
    elif color == "(128, 255, 128)":
        return "input"
    elif color == "(32, 32, 32)":
        return " "

    elif color[3:] == " 1, 64)" or color[4:] == " 1, 64)":
        letters = "abcdefghijklmnopqrstuvwxyz"
                  #12345678901234567890123456
                  #         1         2
        return letters[int(color[1:color.index(",")]) - 1]

    elif color[3:] == " 2, 64)" or color[4:] == " 2, 64)":
        letters = "abcdefghijklmnopqrstuvwxyz".upper()
        return letters[int(color[1:color.index(",")]) - 1]

    elif color[3:] == " 3, 64)" or color[4:] == " 3, 64)":
        letters = '!"#¤%&/()=?`<>@£$€{[]}\\~^*,.-_:;' + "'"
                  #12345678901234567890123456789012      3
                  #         1         2         3
        return letters[int(color[1:color.index(",")]) - 1]
    
    elif color[3:] == " 4, 64)" or color[4:] == " 4, 64)":
        return color[1:color.index(",")]

    elif color == "(0, 222, 255)":
        return "if "
    elif color == "(255, 33, 0)":
        return "else:"
    elif color == "(255, 222, 0)":
        return "elif "
    elif color == "(255, 222, 33)":
        return "for "
    elif color == "(255, 222, 222)":
        return "def "

    elif color == "(70, 70, 70)":
        return "    " #return indent / tab
    else:
        return ""

class ColpytConvert:
    """The Colpyt Converter (added: v0.0.1)"""
    def __init__(self, file):
        self.codeim = Image.open(file)
        self.code = ""
        imsizex,imsizey = self.codeim.size
        for i in range(imsizey):
            for j in range(imsizex):
                self.code += getCmd(str(self.codeim.load()[j,i]))
    def get(self):
        """Returns The Converted Code"""
        return self.code
    def export(self, filename="pycode"):
        """Saves The Converted Code To A File"""
        codefile = open(f"{filename}.py","w")
        codefile.write(self.code)
        codefile.close()