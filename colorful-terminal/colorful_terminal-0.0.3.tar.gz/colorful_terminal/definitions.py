# https://en.wikipedia.org/wiki/ANSI_escape_code
import sys
import os


def Select_Graphic_Rendition(code=0):
    """Sets colors and style of the characters following this code."""
    return f"\033[{code}m"


def SGR_Reset():
    """Resets colors and style of the characters following this code."""
    return f"\033[{0}m"


def Select_RGB_Foreground_Color(r, g, b):
    """"""
    return f"\033[38;2;{r};{g};{b}m"


def Select_RGB_Background_Color(r, g, b):
    """"""
    return f"\033[48;2;{r};{g};{b}m"


def Select_256_Foreground_Color(number):
    """"""
    return f"\033[38;5;{number}m"


def Select_256_Background_Color(number):
    """"""
    return f"\033[48;5;{number}m"


class ForegroundColor:
    BLACK = Select_Graphic_Rendition(30)
    RED = Select_Graphic_Rendition(31)
    GREEN = Select_Graphic_Rendition(32)
    YELLOW = Select_Graphic_Rendition(33)
    BLUE = Select_Graphic_Rendition(34)
    MAGENTA = Select_Graphic_Rendition(35)
    CYAN = Select_Graphic_Rendition(36)
    WHITE = Select_Graphic_Rendition(37)
    RESET = Select_Graphic_Rendition(39)
    # These are fairly well supported, but not part) of the standard.
    BRIGHT_BLACK = Select_Graphic_Rendition(90)
    BRIGHT_RED = Select_Graphic_Rendition(91)
    BRIGHT_GREEN = Select_Graphic_Rendition(92)
    BRIGHT_YELLOW = Select_Graphic_Rendition(93)
    BRIGHT_BLUE = Select_Graphic_Rendition(94)
    BRIGHT_MAGENTA = Select_Graphic_Rendition(95)
    BRIGHT_CYAN = Select_Graphic_Rendition(96)
    BRIGHT_WHITE = Select_Graphic_Rendition(97)

    INTENSE_BLACK = Select_RGB_Foreground_Color(0, 0, 0)
    INTENSE_WHITE = Select_RGB_Foreground_Color(255, 255, 255)

    NEON_RED = Select_RGB_Foreground_Color(255, 0, 0)
    NEON_GREEN = Select_RGB_Foreground_Color(0, 255, 0)
    NEON_BLUE = Select_RGB_Foreground_Color(0, 0, 255)
    NEON_YELLOW = Select_RGB_Foreground_Color(255, 255, 0)
    NEON_MAGENTA = Select_RGB_Foreground_Color(255, 0, 255)
    NEON_CYAN = Select_RGB_Foreground_Color(0, 255, 255)

    def rgb(self, red: int = 0, green: int = 0, blue: int = 0):
        """Choose the color with the rgb channels.

        Args:
            red (int, optional): red channel value (0 to 255, ends included). Defaults to 0.
            green (int, optional): green channel value (0 to 255, ends included). Defaults to 0.
            blue (int, optional): blue channel value (0 to 255, ends included). Defaults to 0.

        Raises:
            ValueError: If any channel is either smaller than 0 or greater than 255.

        Returns:
            str: ANSI Escape Sequences for color manipulation.
        """
        if type(red) == tuple and len(red) == 3:
            red, green, blue = red
        if not 0 <= red <= 255:
            raise ValueError(
                "red needs to be an integer from 0 to 255 including both end points."
            )
        if not 0 <= green <= 255:
            raise ValueError(
                "green needs to be an integer from 0 to 255 including both end points."
            )
        if not 0 <= blue <= 255:
            raise ValueError(
                "blue needs to be an integer from 0 to 255 including both end points."
            )
        return Select_RGB_Foreground_Color(red, green, blue)

    def color_mode_256(self, number):
        """Choose from the 256-color lookup table.

        Args:
            number (_type_): Number of the color. A value from 0 to 255, ends included.

        Raises:
            ValueError: If the number is either smaller than 0 or greater than 255.

        Returns:
            str: ANSI Escape Sequences for color manipulation.
        """
        if 0 > number or number > 255:
            raise ValueError(
                "number of color_mode_256 needs to be between 0 and 255 including both end points."
            )
        return Select_256_Foreground_Color(number)

    def color_mode_256_demo(self, colors_per_line: int = 32, spacing: int = 2):
        """Prints every of the possible colors in the 256-color lookup table. So you don't have to open your browser to know which number you need for which color.

        Args:
            colors_per_line (int, optional): How many colors to display per line. Defaults to 32.
            spacing (int, optional): Spacing between the colors. Defaults to 2.
        """
        print(
            "This is the color_mode_256_demo, the numbers and colors pair corresponding to the 256-color lookup table:"
        )
        for i in range(255):
            colored_print(self.color_mode_256(i) + str(i).rjust(3), end=" " * spacing)
            if (i + 1) % colors_per_line == 0:
                print()
        print()

    def get_rainbow_string(self, string: str):
        """Get a string with a rainbow-like gradient.

        Args:
            string (str): Your string

        Returns:
            str: rainbow-like colored string
        """
        nospace = string.replace(" ", "")
        nospace = nospace.replace("\t", "")
        nospace = nospace.replace("\n", "")
        rgb = []
        for n in range(0, 256, 1):
            rgb.append((255, n, 0))
        for n in range(255, -1, -1):
            rgb.append((n, 255, 0))
        for n in range(0, 256, 1):
            rgb.append((0, 255, n))
        for n in range(255, -1, -1):
            rgb.append((0, n, 255))
        for n in range(0, 256, 1):
            rgb.append((n, 0, 255))

        colors = len(rgb)
        steps = colors // len(nospace)
        if steps != 0:
            needed = []
            for i in range(0, colors, steps):
                needed.append(rgb[i])
            newstring = ""
            counter = 0
            for c in string:
                s = ""
                if not c in ("\t", "\n", " "):
                    s += Fore.rgb(*needed[counter])
                    counter += 1
                s += c
                newstring += s
            return newstring
        else:
            steps = colors / len(nospace)
            while steps < 1:
                steps *= 10
            steps = steps // 1
            newstring = ""
            counter = 0
            everyxcounter = 0
            for c in string:
                s = ""
                if not c in ("\t", "\n", " "):
                    if everyxcounter % steps == 0:
                        s += Fore.rgb(*rgb[counter])
                        counter += 1
                    everyxcounter += 1
                s += c
                newstring += s
            return newstring


class BackroundColor:
    BLACK = Select_Graphic_Rendition(40)
    RED = Select_Graphic_Rendition(41)
    GREEN = Select_Graphic_Rendition(42)
    YELLOW = Select_Graphic_Rendition(43)
    BLUE = Select_Graphic_Rendition(44)
    MAGENTA = Select_Graphic_Rendition(45)
    CYAN = Select_Graphic_Rendition(46)
    WHITE = Select_Graphic_Rendition(47)
    RESET = Select_Graphic_Rendition(49)
    # These are fairly well supported, but not part) of the standard.
    BRIGHT_BLACK = Select_Graphic_Rendition(100)
    BRIGHT_RED = Select_Graphic_Rendition(101)
    BRIGHT_GREEN = Select_Graphic_Rendition(102)
    BRIGHT_YELLOW = Select_Graphic_Rendition(103)
    BRIGHT_BLUE = Select_Graphic_Rendition(104)
    BRIGHT_MAGENTA = Select_Graphic_Rendition(105)
    BRIGHT_CYAN = Select_Graphic_Rendition(106)
    BRIGHT_WHITE = Select_Graphic_Rendition(107)

    INTENSE_BLACK = Select_RGB_Background_Color(0, 0, 0)
    INTENSE_WHITE = Select_RGB_Background_Color(255, 255, 255)

    NEON_RED = Select_RGB_Background_Color(255, 0, 0)
    NEON_GREEN = Select_RGB_Background_Color(0, 255, 0)
    NEON_BLUE = Select_RGB_Background_Color(0, 0, 255)
    NEON_YELLOW = Select_RGB_Background_Color(255, 255, 0)
    NEON_MAGENTA = Select_RGB_Background_Color(255, 0, 255)
    NEON_CYAN = Select_RGB_Background_Color(0, 255, 255)

    def rgb(self, red: int = 0, green: int = 0, blue: int = 0):
        """Choose the color with the rgb channels.

        Args:
            red (int, optional): red channel value (0 to 255, ends included). Defaults to 0.
            green (int, optional): green channel value (0 to 255, ends included). Defaults to 0.
            blue (int, optional): blue channel value (0 to 255, ends included). Defaults to 0.

        Raises:
            ValueError: If any channel is either smaller than 0 or greater than 255.

        Returns:
            str: ANSI Escape Sequences for color manipulation.
        """
        if type(red) == tuple and len(red) == 3:
            red, green, blue = red
        if not 0 <= red <= 255:
            raise ValueError(
                "red needs to be an integer from 0 to 255 including both end points."
            )
        if not 0 <= green <= 255:
            raise ValueError(
                "green needs to be an integer from 0 to 255 including both end points."
            )
        if not 0 <= blue <= 255:
            raise ValueError(
                "blue needs to be an integer from 0 to 255 including both end points."
            )
        return Select_RGB_Background_Color(red, green, blue)

    def color_mode_256(self, number):
        """Choose from the 256-color lookup table.

        Args:
            number (_type_): Number of the color. A value from 0 to 255, ends included.

        Raises:
            ValueError: If the number is either smaller than 0 or greater than 255.

        Returns:
            str: ANSI Escape Sequences for color manipulation.
        """
        if 0 > number or number > 255:
            raise ValueError(
                "number of color_mode_256 needs to be between 0 and 255 including both end points."
            )
        return Select_256_Background_Color(number)

    def color_mode_256_demo(self, colors_per_line: int = 32, spacing: int = 2):
        """Prints every of the possible colors in the 256-color lookup table. So you don't have to open your browser to know which number you need for which color.

        Args:
            colors_per_line (int, optional): How many colors to display per line. Defaults to 32.
            spacing (int, optional): Spacing between the colors. Defaults to 2.
        """
        print(
            "This is the color_mode_256_demo, the numbers and colors pair corresponding to the 256-color lookup table:"
        )
        for i in range(255):
            colored_print(self.color_mode_256(i) + str(i).rjust(3), end=" " * spacing)
            if (i + 1) % colors_per_line == 0:
                print()
        print()

    def get_rainbow_string(self, string: str):
        """Get a string with a rainbow-like gradient.

        Args:
            string (str): Your string

        Returns:
            str: rainbow-like colored string
        """
        rgb = []
        for n in range(0, 256, 1):
            rgb.append((255, n, 0))
        for n in range(255, -1, -1):
            rgb.append((n, 255, 0))
        for n in range(0, 256, 1):
            rgb.append((0, 255, n))
        for n in range(255, -1, -1):
            rgb.append((0, n, 255))
        for n in range(0, 256, 1):
            rgb.append((n, 0, 255))

        colors = len(rgb)
        steps = colors // len(string)
        if steps != 0:
            needed = []
            for i in range(0, colors, steps):
                needed.append(rgb[i])
            newstring = ""
            counter = 0
            for c in string:
                s = ""
                if not c in ("\t", "\n", " "):
                    s += Back.rgb(*needed[counter])
                    counter += 1
                s += c
                newstring += s
            return newstring
        else:
            steps = colors / len(string)
            while steps < 1:
                steps *= 10
            steps = steps // 1
            newstring = ""
            counter = 0
            everyxcounter = 0
            for c in string:
                s = ""
                if not c in ("\t", "\n", " "):
                    if everyxcounter % steps == 0:
                        s += Back.rgb(*rgb[counter])
                        counter += 1
                    everyxcounter += 1
                s += c
                newstring += s
            return newstring


class Styling:
    RESET_ALL = Select_Graphic_Rendition(0)
    BOLD = Select_Graphic_Rendition(1)
    DIM = Select_Graphic_Rendition(2)
    ITALIC = Select_Graphic_Rendition(3)
    UNDERLINED = Select_Graphic_Rendition(4)
    CORSSED_OUT = Select_Graphic_Rendition(9)
    NORMAL = Select_Graphic_Rendition(22)
    DOUBLY_UNDERLINED = NOT_BOLD = Select_Graphic_Rendition(21)
    NOT_UNDERLINED = Select_Graphic_Rendition(24)
    NOT_CORSSED_OUT = Select_Graphic_Rendition(29)
    OVERLINED = Select_Graphic_Rendition(53)
    NOT_OVERLINED = Select_Graphic_Rendition(55)
    SUPERSCRIPT = Select_Graphic_Rendition(73)
    SUBSCRIPT = Select_Graphic_Rendition(74)
    NEITHER_SUPERSCRIPT_NOR_SUBSCRIPT = Select_Graphic_Rendition(75)

    def underline_rgb(self, red: int = 0, green: int = 0, blue: int = 0):
        """Will underline with the specified color.

        Args:
            red (int, optional): red channel (0 to 255, ends included). Defaults to 0.
            green (int, optional): green channel (0 to 255, ends included). Defaults to 0.
            blue (int, optional): blue channel (0 to 255, ends included). Defaults to 0.

        Raises:
            ValueError: If any channel is either smaller than 0 or greater than 255.

        Returns:
            str: ANSI Escape Sequences for string manipulation.
        """
        if type(red) == tuple and len(red) == 3:
            red, green, blue = red
        if not 0 <= red <= 255:
            raise ValueError(
                "red needs to be an integer from 0 to 255 including both end points."
            )
        if not 0 <= green <= 255:
            raise ValueError(
                "green needs to be an integer from 0 to 255 including both end points."
            )
        if not 0 <= blue <= 255:
            raise ValueError(
                "blue needs to be an integer from 0 to 255 including both end points."
            )
        return Select_Graphic_Rendition(f"58;2;{red};{green};{blue}")


class TerminalActions:
    Cursor_Up = "\033[A"
    """Moves the cursor 1 cell in the given direction. If the cursor is already at the edge of the screen, this has no effect."""

    Cursor_Down = "\033[B"
    """Moves the cursor 1 cell in the given direction. If the cursor is already at the edge of the screen, this has no effect."""

    Cursor_Forward = "\033[C"
    """Moves the cursor 1 cell in the given direction. If the cursor is already at the edge of the screen, this has no effect."""

    Cursor_Back = "\033[D"
    """Moves the cursor 1 cell in the given direction. If the cursor is already at the edge of the screen, this has no effect."""

    Cursor_Next_Line = "\033[E"
    """Moves cursor to beginning of the line 1 line down. (not ANSI.SYS)"""

    Cursor_Previous_Line = "\033[F"
    """Moves cursor to beginning of the line 1 line up. (not ANSI.SYS)"""

    Scroll_Up = "\033[S"
    """Scroll whole page up by 1 line. New lines are added at the bottom. (not ANSI.SYS)"""

    Scroll_Down = "\033[T"
    """Scroll whole page down by 1 line. New lines are added at the top. (not ANSI.SYS)"""

    def Cursor_Horizontal_Absolute(self, n=1) -> str:
        """Moves the cursor to column n (default 1). (not ANSI.SYS)"""
        return f"\033[{n}G"

    def Cursor_Position(self, n=1, m=1) -> str:
        """Moves the cursor to row n, column m. The values are 1-based, and default to 1 (top left corner) if omitted. A sequence such as CSI ;5H is a synonym for CSI 1;5H as well as CSI 17;H is the same as CSI 17H and CSI 17;1H"""
        return f"\033[{n};{m}H"

    def Erase_in_Display(self, n=0) -> str:
        """Clears part of the screen. If n is 0 (or missing), clear from cursor to end of screen. If n is 1, clear from cursor to beginning of the screen. If n is 2, clear entire screen (and moves cursor to upper left on DOS ANSI.SYS). If n is 3, clear entire screen and delete all lines saved in the scrollback buffer (this feature was added for xterm and is supported by other terminal applications)."""
        return f"\033[{n}J"

    def Erase_in_Line(self, n=0) -> str:
        """Erases part of the line. If n is 0 (or missing), clear from cursor to the end of the line. If n is 1, clear from cursor to beginning of the line. If n is 2, clear entire line. Cursor position does not change."""
        return f"\033[{n}K"

    def Horizontal_Vertical_Position(self, n, m) -> str:
        """Same as CUP, but counts as a format effector function (like CR or LF) rather than an editor function (like CUD or CNL). This can lead to different handling in certain terminal modes."""
        return f"\033[{n};{m}f"

    def SGR_Reset(self) -> str:
        """Resets colors and style of the characters following this code."""
        return f"\033[{0}m"

    def Save_Current_Cursor_Position(self) -> str:
        """Saves the cursor position/state in SCO console mode. In vertical split screen mode, instead used to set (as CSI n ; n s) or reset left and right margins."""
        return f"\033[s"

    def Restore_Saved_Cursor_Position(self) -> str:
        """Restores the cursor position/state in SCO console mode."""
        return f"\033[u"

    def Show_Cursor(self) -> str:
        """Shows the cursor, from the VT220."""
        return f"\033[?25h"

    def Hide_Cursor(self) -> str:
        """Hides the cursor."""
        return f"\033[?25l"

    def Undo_Line(self):
        """Goes one line up and clears the line."""
        colored_print(TermAct.Cursor_Previous_Line + TermAct.Erase_in_Line(), end="")

    def Clear_Current_Line(self):
        """Clears everything in current line."""
        colored_print(self.Cursor_Horizontal_Absolute() + self.Erase_in_Line(), end="")

    def clear_Terminal(self):
        """Clears your terminal with either cls or clear"""
        os.system("cls" if os.name == "nt" else "clear")

    def clear_Console(self):
        """Alias for clear_Terminal"""
        self.clear_Terminal()


Fore = ForegroundColor()
Back = BackroundColor()
Style = Styling()
TermAct = TerminalActions()


def colored_print(*args, end="\n", sep=" "):
    if args == ():
        args = ""
    _args = []
    for a in args:
        if isinstance(a, str):
            _args.append(a)
        else:
            _args.append(str(a))
    string = sep.join(_args) + SGR_Reset()
    string += end
    out = sys.stdout
    out.write(string)
    sys.stdout.flush()


def foreground_demo():
    """See what you can do with Fore. Calling this will print the demo."""
    filling = 20

    BLACK = Fore.BLACK + "Fore.BLACK".ljust(filling)
    BRIGHT_BLACK = Fore.BRIGHT_BLACK + "Fore.BRIGHT_BLACK".ljust(filling)
    INTENSE_BLACK = Fore.INTENSE_BLACK + "Fore.INTENSE_BLACK".ljust(filling)

    WHITE = Fore.WHITE + "Fore.WHITE".ljust(filling)
    BRIGHT_WHITE = Fore.BRIGHT_WHITE + "Fore.BRIGHT_WHITE".ljust(filling)
    INTENSE_WHITE = Fore.INTENSE_WHITE + "Fore.INTENSE_WHITE".ljust(filling)

    RED = Fore.RED + "Fore.RED".ljust(filling)
    BRIGHT_RED = Fore.BRIGHT_RED + "Fore.BRIGHT_RED".ljust(filling)
    NEON_RED = Fore.NEON_RED + "Fore.NEON_RED".ljust(filling)

    GREEN = Fore.GREEN + "Fore.GREEN".ljust(filling)
    BRIGHT_GREEN = Fore.BRIGHT_GREEN + "Fore.BRIGHT_GREEN".ljust(filling)
    NEON_GREEN = Fore.NEON_GREEN + "Fore.NEON_GREEN".ljust(filling)

    BLUE = Fore.BLUE + "Fore.BLUE".ljust(filling)
    BRIGHT_BLUE = Fore.BRIGHT_BLUE + "Fore.BRIGHT_BLUE".ljust(filling)
    NEON_BLUE = Fore.NEON_BLUE + "Fore.NEON_BLUE".ljust(filling)

    YELLOW = Fore.YELLOW + "Fore.YELLOW".ljust(filling)
    BRIGHT_YELLOW = Fore.BRIGHT_YELLOW + "Fore.BRIGHT_YELLOW".ljust(filling)
    NEON_YELLOW = Fore.NEON_YELLOW + "Fore.NEON_YELLOW".ljust(filling)

    MAGENTA = Fore.MAGENTA + "Fore.MAGENTA".ljust(filling)
    BRIGHT_MAGENTA = Fore.BRIGHT_MAGENTA + "Fore.BRIGHT_MAGENTA".ljust(filling)
    NEON_MAGENTA = Fore.NEON_MAGENTA + "Fore.NEON_MAGENTA".ljust(filling)

    CYAN = Fore.CYAN + "Fore.CYAN".ljust(filling)
    BRIGHT_CYAN = Fore.BRIGHT_CYAN + "Fore.BRIGHT_CYAN".ljust(filling)
    NEON_CYAN = Fore.NEON_CYAN + "Fore.NEON_CYAN".ljust(filling)

    print("Fore allows you to change the color of the letters.")
    colored_print(BLACK + WHITE + RED + GREEN + BLUE + YELLOW + MAGENTA + CYAN)
    colored_print(
        BRIGHT_BLACK
        + BRIGHT_WHITE
        + BRIGHT_RED
        + BRIGHT_GREEN
        + BRIGHT_BLUE
        + BRIGHT_YELLOW
        + BRIGHT_MAGENTA
        + BRIGHT_CYAN
    )
    colored_print(
        INTENSE_BLACK
        + INTENSE_WHITE
        + NEON_RED
        + NEON_GREEN
        + NEON_BLUE
        + NEON_YELLOW
        + NEON_MAGENTA
        + NEON_CYAN
    )
    print()


def background_demo():
    """See what you can do with Back. Calling this will print the demo."""
    filling = 20

    BLACK = Back.BLACK + "Back.BLACK".ljust(filling)
    BRIGHT_BLACK = Back.BRIGHT_BLACK + "Back.BRIGHT_BLACK".ljust(filling)
    INTENSE_BLACK = Back.INTENSE_BLACK + "Back.INTENSE_BLACK".ljust(filling)

    WHITE = Back.WHITE + "Back.WHITE".ljust(filling)
    BRIGHT_WHITE = Back.BRIGHT_WHITE + "Back.BRIGHT_WHITE".ljust(filling)
    INTENSE_WHITE = Back.INTENSE_WHITE + "Back.INTENSE_WHITE".ljust(filling)

    RED = Back.RED + "Back.RED".ljust(filling)
    BRIGHT_RED = Back.BRIGHT_RED + "Back.BRIGHT_RED".ljust(filling)
    NEON_RED = Back.NEON_RED + "Back.NEON_RED".ljust(filling)

    GREEN = Back.GREEN + "Back.GREEN".ljust(filling)
    BRIGHT_GREEN = Back.BRIGHT_GREEN + "Back.BRIGHT_GREEN".ljust(filling)
    NEON_GREEN = Back.NEON_GREEN + "Back.NEON_GREEN".ljust(filling)

    BLUE = Back.BLUE + "Back.BLUE".ljust(filling)
    BRIGHT_BLUE = Back.BRIGHT_BLUE + "Back.BRIGHT_BLUE".ljust(filling)
    NEON_BLUE = Back.NEON_BLUE + "Back.NEON_BLUE".ljust(filling)

    YELLOW = Back.YELLOW + "Back.YELLOW".ljust(filling)
    BRIGHT_YELLOW = Back.BRIGHT_YELLOW + "Back.BRIGHT_YELLOW".ljust(filling)
    NEON_YELLOW = Back.NEON_YELLOW + "Back.NEON_YELLOW".ljust(filling)

    MAGENTA = Back.MAGENTA + "Back.MAGENTA".ljust(filling)
    BRIGHT_MAGENTA = Back.BRIGHT_MAGENTA + "Back.BRIGHT_MAGENTA".ljust(filling)
    NEON_MAGENTA = Back.NEON_MAGENTA + "Back.NEON_MAGENTA".ljust(filling)

    CYAN = Back.CYAN + "Back.CYAN".ljust(filling)
    BRIGHT_CYAN = Back.BRIGHT_CYAN + "Back.BRIGHT_CYAN".ljust(filling)
    NEON_CYAN = Back.NEON_CYAN + "Back.NEON_CYAN".ljust(filling)

    print("Back allows you to change the color of the background.")
    colored_print(BLACK + WHITE + RED + GREEN + BLUE + YELLOW + MAGENTA + CYAN)
    colored_print(
        BRIGHT_BLACK
        + BRIGHT_WHITE
        + BRIGHT_RED
        + BRIGHT_GREEN
        + BRIGHT_BLUE
        + BRIGHT_YELLOW
        + BRIGHT_MAGENTA
        + BRIGHT_CYAN
    )
    colored_print(
        INTENSE_BLACK
        + INTENSE_WHITE
        + NEON_RED
        + NEON_GREEN
        + NEON_BLUE
        + NEON_YELLOW
        + NEON_MAGENTA
        + NEON_CYAN
    )
    print()


def style_demo():
    """See what you can do with Style. Calling this will print the demo."""
    BOLD = Style.BOLD + "Style.BOLD" + "    " + Style.RESET_ALL
    CORSSED_OUT = Style.CORSSED_OUT + "Style.CORSSED_OUT" + "    " + Style.RESET_ALL
    DIM = Style.DIM + "Style.DIM" + "    " + Style.RESET_ALL
    UNDERLINED = Style.UNDERLINED + "Style.UNDERLINED" + "    " + Style.RESET_ALL
    DOUBLY_UNDERLINED = (
        Style.DOUBLY_UNDERLINED + "Style.DOUBLY_UNDERLINED" + "    " + Style.RESET_ALL
    )
    ITALIC = Style.ITALIC + "Style.ITALIC" + "    " + Style.RESET_ALL
    OVERLINED = Style.OVERLINED + "Style.OVERLINED" + "    " + Style.RESET_ALL
    SUPERSCRIPT = Style.SUPERSCRIPT + "Style.SUPERSCRIPT" + "    " + Style.RESET_ALL
    SUBSCRIPT = Style.SUBSCRIPT + "Style.SUBSCRIPT" + "    " + Style.RESET_ALL

    print(
        "With Style you can edit the style of your string, if the output allows it. (I use VSCode and cannot print Style.OVERLINED, Style.SUPERSCRIPT and Style.SUBSCRIPT)"
    )
    colored_print(
        BOLD
        + CORSSED_OUT
        + DIM
        + UNDERLINED
        + DOUBLY_UNDERLINED
        + ITALIC
        + OVERLINED
        + SUPERSCRIPT
        + SUBSCRIPT
    )
    print()


def rgb_demo(size: float = 15):
    """Be fascinated by the color selection through the three color channels red, green and blue (0 to 255, ends included). Calling this will print the demo.
    The output contains three squares with one of the channels on each axis. Size determines the size of the squares.
    """
    if not 0 < size <= 255:
        raise ValueError("size needs to be between 0 (excluded) and 255 (included)")
    print(
        "With the rgb methods of Fore and Back you are not bound to specific colors. Just choose from the range of 0 to 255 for the red, green and blue channel."
    )
    for n in range(255, -1, -int(255 / size)):
        for m in range(0, 256, int(255 / size)):
            colored_print(Back.rgb(n, m, 0) + "  ", end="")
        print("  ", end="")
        for m in range(0, 256, int(255 / size)):
            colored_print(Back.rgb(0, n, m) + "  ", end="")
        print("  ", end="")
        for m in range(0, 256, int(255 / size)):
            colored_print(Back.rgb(m, 0, n) + "  ", end="")
        print()
    print()


def rainbow_demo():
    """RAINBOW STRINGS!. Calling this will print the demo."""
    for n in range(0, 256, 15):
        colored_print(Back.rgb(255, n, 0) + "  ", end="")
    for n in range(255, -1, -15):
        colored_print(Back.rgb(n, 255, 0) + "  ", end="")
    for n in range(0, 256, 15):
        colored_print(Back.rgb(0, 255, n) + "  ", end="")
    for n in range(255, -1, -15):
        colored_print(Back.rgb(0, n, 255) + "  ", end="")
    for n in range(0, 256, 15):
        colored_print(Back.rgb(n, 0, 255) + "  ", end="")
    print()
    print()


def termact_demo(horses: int = 5, lenght: int = 100):
    from random import randint
    from time import sleep

    print(TermAct.Hide_Cursor(), end="")
    posis = {f"Horse-{i+1}": 0 for i in range(horses)}
    positioning = {f"Horse-{i+1}": 0 for i in range(horses)}
    horses_list = []
    horses_len = max([len(f"Horse-{n+1}") for n in range(horses)])
    space_len = lenght - horses_len
    s = " " * space_len
    s2 = " " * (space_len - 17)
    print(f"TermAct Horse Race!{s2}Finish Line")
    for i in range(horses):
        st = f"Horse-{i+1}{s}|"
        horses_list.append(f"Horse-{i+1}")
        print(st)
    finished = []

    def run_horses_run():
        steps = [randint(1, 5) for _ in range(horses)]
        for i in range(horses):
            posis[f"Horse-{i+1}"] = posis[f"Horse-{i+1}"] + steps[i]
            if posis[f"Horse-{i+1}"] > (lenght + 1):
                posis[f"Horse-{i+1}"] = lenght + 1

            if posis[f"Horse-{i+1}"] > (space_len):
                if f"Horse-{i+1}" not in finished:
                    finished.append(f"Horse-{i+1}")
                    positioning[f"Horse-{i+1}"] = len(finished)
        spaces = [" " * s for s in posis.values()]
        strings = [f"{spaces[i]}Horse-{i+1}" for i in range(horses)]
        if any([len(s) > space_len for s in strings]):
            newstrings = []
            for s in strings:
                ns = ""
                for i, c in enumerate(s):
                    if i == lenght and c == " ":
                        ns += "|"
                    else:
                        ns += c
                newstrings.append(ns)
            strings = newstrings
        for i, (h, v) in enumerate(positioning.items()):
            prestr = " " * (lenght - posis[h] + horses_len + 3)
            if v == 1:
                strings[i] += (
                    prestr + f"{Fore.rgb(255,215,0)}Finished in 1st place!!! Winner!!!"
                )
            elif v == 2:
                strings[i] += prestr + f"{Fore.rgb(211,211,211)}Finished in 2nd place!"
            elif v == 3:
                strings[i] += prestr + f"{Fore.rgb(191,137,112)}Finished in 3rd place!"
            elif v > 3:
                strings[i] += (
                    prestr + f"{Fore.rgb(100,100,100)}Finished in {v}th place."
                )

        print(TermAct.Cursor_Up * horses, end="")
        for i in strings:
            colored_print(i)
        sleep(0.3)

    while not all([n >= (lenght + 1) for n in posis.values()]):
        run_horses_run()
    run_horses_run()
    print(TermAct.Show_Cursor(), end="")
    print(
        """
With TermAct you can hide you cursor or move the cursor in any direction.
If you want to erase printed rows, call TermAct.Undo_Line. Perfect to update the progress of multiple tasks in multiple rows.
Sadly it is hard to demonstrate all of it.
    """
    )


def demo_print():
    """Complete demo print: Will call all the demos (foreground_demo, background_demo, style_demo, rgb_demo, rainbow_demo).
    See which visual manipulations you can perform.
    """
    print(
        """
Similar to colorama you can import and use Fore, Back, Style in your string as well as TermAct.
But you should use colored_print instead of print to automatically reset your modifications. 
Else you need to either individually change stuff back to the normal state with Fore/Back.RESET or (much simpler) use Style.RESET_ALL to get back to your normal prints.

This module allows a wider range of colors ... if your output can display it. 
    """
    )

    foreground_demo()
    background_demo()
    style_demo()
    rgb_demo(25)
    rainbow_demo()
    colored_print(
        Fore.get_rainbow_string(
            "Fore.get_rainbow_string and Back.get_rainbow_string allow you to conveniently print rainbow colored strings!"
        )
    )
    colored_print(Fore.get_rainbow_string("This is a rainbow string!"))
    colored_print(Back.get_rainbow_string("This is also a rainbow string!"))
    print()
    termact_demo()


if __name__ == "__main__":

    demo_print()
