import collections
import json
import os
import re

import pyautogui
# import klsframe.workers.desktopWorker as worker

Point = collections.namedtuple("Point", "x y")
Size = collections.namedtuple("Size", "width height")

"""
;button;input;textbox;hyperlink;image;table
inner text;?;Y;Y;Y;N;Y
"""


def calibrate():
    # 1. Select: new gui layout OR edit existing one
    # 2. Select: view current layout OR edit current layout
    #              (tree view)            (list pages)
    # 3. Add a page OR edit an existing page
    # 4. Add / Edit / Remove component
    pass


def safe_coordinates(x, y):
    if x is None or y is None:
        return False
    else:
        return not (x <= 0 or pyautogui.size().width <= x or y <= 0 or pyautogui.size().height <= y)


def screen_center():
    return pyautogui.size().width / 2, pyautogui.size().height / 2


class GUILayout:
    """
    A GUI Layout is a list of pages.
    """

    def __init__(self):
        self.name = ''
        self.screen_size = pyautogui.size()
        self.pages = []

    def __eq__(self, other):
        if other is None or len(self.pages) != len(other.pages):
            return False
        for pg_i, pg_j in zip(self.pages, other.pages):
            if pg_i.name != pg_j.name:
                return False
            if pg_i.components != pg_j.components:
                return False
        return True

    def get(self, comp_name, pg_name=None):
        for pg in self.pages:
            if pg_name is not None and pg_name != pg.name:
                continue
            for k, v in pg.components.items():
                if k == comp_name:
                    return v
        return None

    def new_page(self, page_name):
        _new = GUIPage(page_name)
        self.pages.append(_new)
        return _new

    def add_component(self, page_name, comp_name, x, y):
        for pg in self.pages:
            if pg.name == page_name:
                pg.components[comp_name] = (x, y)
                return
        _new_pg = self.new_page(page_name)
        _new_pg.components[comp_name] = (x, y)
        return

    def to_json(self):
        _res = []
        counter = -1
        for pg in self.pages:
            counter += 1
            _res.append({pg.name: {}})
            for comp, comp_coors in pg.components.items():
                _res[counter][pg.name][comp] = [comp_coors[0], comp_coors[1]]
        return _res

    @staticmethod
    def load(source):
        _gly = GUILayout()
        # TODO: load from a json file/object
        if type(source) is list:
            for src in source:
                _new_pg = _gly.new_page("".join(src.keys()))
                for comp_name, comp_coords in src[_new_pg.name].items():
                    _gly.add_component(_new_pg.name, comp_name, x=comp_coords[0], y=comp_coords[1])
        elif type(source) is str and os.path.isfile(source):
            with open(source, 'r') as file:
                return GUILayout.load(json.load(file))
        elif type(source) is str:
            # TODO: implement JSON string parsing
            pass
        else:
            raise ValueError("Invalid object type for load()")
        return _gly

    def local_save(self, outfile):
        with open(outfile, 'w') as file:
            json.dump(self.to_json(), file, indent=2)

    def verify(self):
        for pg in self.pages:
            for comp, comp_coords in pg.components.items():
                if not safe_coordinates(comp_coords[0], comp_coords[0]):
                    print(f"ERROR. Coordinate verification failed. Coordinates of component '{comp}' are not valid")
                    return 1
        return 0

    # START TABLE FUNCTIONS
    def get_table_row_at(self, tname, rownum):
        pass

    def get_table_row_with(self, tname, filters):
        pass

    def get_table_all_rows(self, tname):
        pass

    # END TABLE FUNCTIONS

    def screen_center(self):
        return self.screen_size.width / 2, self.screen_size.height / 2


class GUIPage:
    def __init__(self, pgname):
        self.name = str(pgname)
        self.transitions = []
        self.components = []
        self.tables = []

    def __repr__(self):
        return self.__dict__


class GUITransition:
    # TODO
    pass


class GUIComponent:
    """
    comp_name: "boton borrar"
    comp_type: "button"
    start: (x1, y1)
    end: (x2, y2)
    screenArea
    regex: "borrar"
    """

    def __init__(self, title, compclass: str, regex=None):
        _allowed_classes = ['button', 'input', 'textbox', 'table', 'hyperlink', 'image']
        # Check component type
        if str(compclass.lower()) in _allowed_classes:
            self.comp_type = str(compclass.lower())
            self.title = title
            self.regex = regex
            # self.start = None
            # self.end = None
            # self.screen_area = None
            self.screen_area = ScreenArea()
        else:
            raise TypeError(f"Invalid type ({type}) for GUIComponent")

    def calibrate(self):
        self.screen_area = ScreenArea()

    def get_inner_text(self):
        return self.title

    def validate(self, value):
        if self.regex is None or re.fullmatch(self.regex, value) is not None:
            return True
        else:
            return False

    def get_point(self, position='center'):
        _allowed_positions = ['top-left-corner', 'top-right-corner', 'bottom-right-corner', 'bottom-left-corner',
                              'left-side', 'right-side', 'top-side', 'bottom-side',
                              'left-border', 'top-border', 'right-border', 'bottom-border',
                              'top-left-side', 'top-right-side', 'bottom-right-side', 'bottom-left-side', 'center']
        if position not in _allowed_positions:
            raise ValueError(f"Unexpected value for parameter 'position'. Allowed: {', '.join(_allowed_positions)}")
        return eval(f"self.screen_area.{opt.replace('-', '_')}")
        # w = worker.Worker()
        # w.click_at(eval(f"self.screen_area.{opt.replace('-', '_')}"), button=button, clicks=clicks)


class GUIButton(GUIComponent):
    def __init__(self, title, regex=None):
        super().__init__(compclass='button', title=title, regex=regex)


class GUIInput(GUIComponent):
    def __init__(self, title, regex=None):
        super().__init__(compclass='input', title=title, regex=regex)


class GUITextBox(GUIComponent):
    def __init__(self, title, regex=None):
        super().__init__(compclass='textbox', title=title, regex=regex)


class GUIHyperLink(GUIComponent):
    def __init__(self, title, regex=None):
        super().__init__(compclass='hyperlink', title=title, regex=regex)


class GUIImageBox(GUIComponent):
    def __init__(self, title, regex=None):
        super().__init__(compclass='image', title=title, regex=regex)


class GUITable(GUIComponent):
    def __init__(self, title):
        super().__init__(title=title, compclass='table')
        self.first_row_Y = 0.0
        self.row_height = 0.0
        self.table_size = 0  # Num of rows
        self.next_page_button = GUIButton(title='nextPage')
        self.prev_page_button = GUIButton(title='prevPage')
        self.columns = []

    def get_row_at(self, index):
        # TODO: Fix this shit. GuiLayour CANNOT use WORKER.
        # IT only hold coordinates values, but it cannot click, nor move
        pass
        # if index == 0:
        #     return self.headers()
        # elif 0 < index <= self.table_size:
        #     # TODO
        #     offset = (index - 1) * self.row_height
        #     row = {}
        #     for col in self.columns:
        #         # A human will just read the columns, but the app need to copy the text to get it
        #         # Thus those clicks do not count for Worker.stats
        #         w = worker.Worker()
        #         content = w.copy_text(x=col.left_border(), y=self.first_row_Y + offset)
        #         if self.validate(content):
        #             row[col.col_name] = content
        #         else:
        #             raise ValueError(f"Unexpected value ({content}) for column '{col.col_name}'")
        #     return row
        # else:
        #     raise IndexError(f"Index {index} out of bounds [0, {self.table_size}]")

    def get_row_where(self, **kwargs):
        pass

    def headers(self):
        return [col.col_name for col in self.columns]


class GUITableColumn:
    def __init__(self):
        self.col_name = ''
        self.left_border_x = -1.0
        self.right_border_x = -1.0
        self.regex = None


class ScreenArea:
    def __init__(self, startp=None, endp=None):
        self.start = None
        self.end = None
        # Check coordinates
        if startp is not None and endp is not None:
            self.set_coordinates('start', startp)
            self.set_coordinates('end', endp)
        elif (startp is None) ^ (endp is None):
            raise AttributeError("The parameter 'startp' and 'endp' must be used together")

    def set_coordinates(self, position, point):
        # Check coordinates
        if not isinstance(point, (Point, tuple)):
            raise TypeError("Invalid type for parameter 'point'. Must be coordinates tuples (x, y)")
        if position == 'start':
            if self.end is None:
                self.start = point
            elif point[0] >= self.end.x or point[1] >= self.end.y or point <= (0, 0):
                raise ValueError("Invalid coordinates. Start is bigger than end")
            else:
                self.start = point
        elif position == 'end':
            if self.start is None:
                self.end = point
            elif point[0] <= self.start.x or point[1] <= self.start.y or point <= (0, 0):
                raise ValueError("Invalid coordinates. End is smaller than start")
            else:
                self.end = point
        else:
            raise ValueError(f"Unknown position '{position}'. Valid: start|end")

    @staticmethod
    def select_screen_area(verbose=False):
        import klsframe.IplusD.loggers as logger
        while True:
            try:
                print(f"[INFO] Select a screen area. Click the top-left border, then the bottom-right one.")
                user_input = logger.record_mouse(clicks=2, verbose=verbose)
                sa = ScreenArea()
                sa.set_coordinates('start', user_input[0]['position'])
                sa.set_coordinates('end', user_input[1]['position'])
                return sa
            except (ValueError, TypeError) as e:
                sa = None
                print(e)

    # ----| C E N T E R |----
    @property
    def center(self) -> Point:
        return Point(self.center_x, self.center_y)

    @property
    def center_x(self) -> int:
        return self.start.x + self.width / 2

    @property
    def center_y(self) -> int:
        return self.start.y + self.height / 2

    @property
    def width(self) -> int:
        return self.end.x - self.start.x

    @property
    def height(self) -> int:
        return self.end.y - self.start.y

    @property
    def size(self) -> Size:
        return Size(self.width, self.height)

    # ----| S I D E S |----
    @property
    def top_left_side(self):
        return Point(self.start.x + self.width * 0.25, self.start.y + self.height * 0.25)

    @property
    def top_right_side(self):
        return Point(self.end.x - self.width * 0.25, self.start.y + self.height * 0.25)

    @property
    def bottom_left_side(self):
        return Point(self.start.x + self.width * 0.25, self.end.y - self.height * 0.25)

    @property
    def bottom_right_side(self):
        return Point(self.end.x - self.width * 0.25, self.end.y - self.height * 0.25)

    @property
    def left_side(self):
        return Point(self.start.x + self.width * 0.25, self.center_y)

    @property
    def right_side(self):
        return Point(self.end.x - self.width * 0.25, self.center_y)

    @property
    def top_side(self):
        return Point(self.center_x, self.start.y + self.height * 0.25)

    @property
    def bottom_side(self):
        return Point(self.center_x, self.end.y - self.height * 0.25)

    # ----| B O R D E R S |----
    def left_border(self):
        return Point(self.start.x, self.center_y)

    def right_border(self):
        return Point(self.end.x, self.center_y)

    def top_border(self):
        return Point(self.center_x, self.start.y)

    def bottom_border(self):
        return Point(self.center_x, self.end.y)

    # ----| C O R N E R S |----
    def corners(self, reverse=False) -> tuple:
        """

        :return: a 4-position tuple (top-left, top-right, bottom-right, bottom-left)
                indicating the corner points of the area
        """
        if isinstance(reverse, bool) and reverse:
            return (self.top_left_corner, self.bottom_left_corner,
                    self.bottom_right_corner, self.top_right_corner)

        elif isinstance(reverse, bool):
            return (self.top_left_corner, self.top_right_corner,
                    self.bottom_right_corner, self.bottom_left_corner)
        else:
            raise TypeError("Invalid type for parameter 'reverse'. Expected: bool")

    @property
    def top_left_corner(self) -> Point:
        return Point(self.start.x, self.start.y)

    @property
    def top_right_corner(self) -> Point:
        return Point(self.end.x, self.start.y)

    @property
    def bottom_left_corner(self) -> Point:
        return Point(self.start.x, self.end.y)

    @property
    def bottom_right_corner(self) -> Point:
        return Point(self.end.x, self.end.y)

    def draw_border(self, rounds=1, drawtime=5.0, reverse=False):
        tmp = pyautogui.PAUSE  # Disable pause to meet the specified drawtime
        pyautogui.PAUSE = 0
        if drawtime > 1.0:
            _duration = drawtime / 5.0
        else:
            raise ValueError("The drawing time must be greater than 0")
        _rectangle = self.corners(reverse=reverse)
        for i in range(0, rounds):
            for j in range(0, 5):
                point = _rectangle[j % 4]
                # TODO: implement the moves with kls-worker
                pyautogui.moveTo(x=point[0], y=point[1], duration=_duration)
        pyautogui.PAUSE = tmp

    def select(self):
        # TODO: develop select (hold ctrl + drag)
        pass


if __name__ == '__main__':
    sa1 = ScreenArea.select_screen_area(verbose=True)
    # sa1.draw_border(rounds=2, reverse=True, drawtime=0.5)
    opt = 'top-left-corner'
    print(eval(f"self.{opt.replace('-', '_')}"))
