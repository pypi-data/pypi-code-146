import threading
import tkinter as tk
from sys import platform

from tempfile import mkstemp

_adwite_light = b"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"
_adwite_dark = b"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"

_adwite_logo_light = b"iVBORw0KGgoAAAANSUhEUgAAAEsAAABLCAYAAAA4TnrqAAAABHNCSVQICAgIfAhkiAAABVZJREFUeJztnG+IVUUYxp9nM4xCif4ahfT/jxFSIWVCJoRhrZRJbSKid6sPWZBERBB9KQi5SyaIECUuVlSQbJHIQmngh/wgGRSRBkVF7OIHKVghicCnD+fc5dxzz733nJl3zjnG/cH9cOfOvPPy7LxzZuads8BZgKQ5kjZV7cdZgaT3Jc1IeqBqX2qNpGYs1IykaUmLq/aplkh6ISFU63NU0mVV+1YrJK3LEKr12V+1f7VB0ooeQrU+u8r2a6jsDvsh6WYAu3NUfVzS66H9SVIrsSRdiEioi3M2eV7SswFdaoNldZQHSRMA7ndouonkhLU/aWozsiTthJtQADAu6R5Lf7KohViSXgWwwcMEAeyWdI2RS107qRRJTwHYZmTuWwCrSJ42stdGpWJJGgbwobHZ/STXGdsEUGEYSroT+ZYIRXlI0lsB7FYjlqQrAYwDOC9QF09KesnaaOlhKGkIwCSApSV09xzJ96yMVSHWHgBrSuxyLckvLQyVGoaStqJcoYBoDXabhaHSxJK0BcDmsvpLMB/RGuwSX0OlhKGkEQDvltFXDw6RXO1jIPjIkrQc1QsFAMslveNjIKhYkm5EmLWUK09Ies21cTCxJM1HtJa6NFQfjmyR9IxLw2BzlqS9AFaGsm/ARpKfFmkQZGRJ2oF6CwVET8i7izQwF0vSKwA2WtsNwDmIBLs6bwPTMJQ0CmC7pc0S+AbRsc4//SqaiSXpQQAfW9krmX0k1/erZBKGkm5HvZYIRVkt6c1+lbzFknQFoiXC+b62KuZpSS/2quAdhpImASzztVMjNpP8IOsHL7EkjQNY62OjpqwheTBd6ByGkt7A/1MoIDrWuTVd6DSy4tSV77GtxZP4jIGNbhxDtKT4s1Uwx9HQDQB+NXHJnb2IHiwt7gJwEsAvhn1cDsBbrM8ALDJxx40fSM6eHki6AMAwgBMkXw7VqeucZXKm7UEz9b0B4CIAiyQ9FqpTJ7FIngLQ8bQoie0kf2x9kbQU7Zv2DaHS+D6L0ipG16HkGkjSuYhGVZrREJ07i0XyAIBThr70YwbAWKqsAWBBRt3Fkh62dsB3u3PAxIt8jJE80foSp/+He9RvSLrK0gFfscoKxQmSk6myrPBLMpSjTiG8xCJ5BMC0kS/d+A2p8JPUALAwR9slklZZOWJxRBN6dDVJ/tv6EmeXi2S1R63uzdddrF3x6E1S9Ek3F0bh6C0WyeMAjhv4kuYoybeTBZLWA7jOwdYySa73VWexSlhYj64z6JynbgIw4mGzEV8dd8ZKLOslxBjJn1NlvgvNefAMRxOxSE4BSM8trnxB8pNkQbzfu8XA9gpJ97o2tswbWoyuk+gMv2vhd+07TUOSU77AUiyLeatJ8q9UmenCEtGrLk4hbSZWfBLhM7o+IvlVskDSIwBCvIy5smjqHrBP37uK9RPJtrxdvK+zHlVJRuNTi9yYiuVxEpE+zAMioULeTFyAgn+MELdoio6unSS/SxbEVwGW2LnUlWFJd+StHEKsIhP9YZLJpAPifVzI8EuTe7I3Fyvey03lqHoanYd5QOT8XFOnerMw7/+MCHVNMk8ojpH8I1kQ79+CvzeYwaN57sqHEqtfKO4j+XmyIN63lRl+afr2HUSsPicRU+gefvNC+JOT6+NTja6EvNrdbXQ1Sf6dLIj3a/cF9CUvI/HpRiZli7WH5NfJgjibHCR15UjXcAwmFslptJ9EfE9yR0bVVja5LnTNaod+HSU5ujrmqYxscl3IzGqHFqu1hNhG8ljyhx7Z5LrQMTUEfytM0tasmy1W7wAGZobk71U7MWDAgAEDBgwYMGDALP8BpTMkAoPuIv4AAAAASUVORK5CYII="
_adwite_logo_dark = b"iVBORw0KGgoAAAANSUhEUgAAAEsAAABLCAYAAAA4TnrqAAAABHNCSVQICAgIfAhkiAAABQNJREFUeJztnF2IVVUUx3+NitSQiJVpiUxFWqlYDZEVaIIaDUZZiERI3SEIfIoeIhBfegi5QyKEECVO0YeQJZFEZFb4kA9+BH2QCX0SEz0MFTOQhCU9rDnTufucM/ecfdba54ycH9yHu2fftdf87977rLPXOhemBzOBx6p2YrrwGjAG3FO1I3WnjQg1BvwKrKzWnfryFP8LFb1OAfOrdKqOPExSqOj1foV+1Y61ZAsVvfaGdmpG6AFzcANwALikS79lE30+NfdogrqJNRd4C+jL2X8VMstOWDkUp25ivYkIUIR1wBngtL47nfRYD1CAPcg/7sMwcKeiL6nURawdwNYSn78I2Adco+NO9iBV8ziwS8nW58C9wFklex1UvWdtBF5StLcQuAl4R9HmJFWK1Y+ECDOV7S5BIvwPle1WJtbViFCXG9m/FfgX+EzTaBVi9SBCrTAeZzUwAnyhZbAKsV4B1gcaawA4CfygYSx06LAT2BR4zGGUZnFIsZ4EtgUcL2IOEoOV3h9DxVlbgJcDjZXFUeC+MgZC7FlrgP0BxulGHxLhH/I1YC3WEuTK12s8Tl6WAxfjeaxjKdYcRCjT+zUPVgF/IlfJQliK9QYBTgI8WQ98O/HKjdXV8AVgg5FtLfZR8OzMQqztwKMGdrWZgQjWl/cD2qHDILBb2aY1J5Fjnb+7ddTcswaoIOOiwFXAjcDBbh21xLoFufLNUrIXmqVIhH94qk4aYi1EhJruWeJ+4BxwLKuDhlgHuHDqD9YAvwBfpv2x7AY/DDxU0kYd2QR87DaWCR2e48IUCmQSLHMbfWfWDuDpUu7ohC3nFWxkcRoJKX6PGnyTBdcDP2p4VIK3kRkQcTswCnyvOMaVKIj1LpJyqoqvgWdj73uRtNpvwDNWg/ruWR+pelGctvO+BcxDvsDNVoP6ijVOytUiELuBb2Lv76Dzpn0rRsdCZa6GVcyuo8DrsfezkFnlMmgxeBmxjiAzLBRjwJDT1gIWpPRdCdyv7UDZI5ojKl7kYwjZwCP6kU09ixawSNOBsmKFWooHgQ+ctrTlF6cnR59ClBXrOFKbbslPpC+/xTk+exsSWKqgcVJqPbvayGlAxAqKZbUHUToRqbtYe5HZG6folW42SstRQ6zCWZKcnAJedNoeAa7zsHUX/vWqk2glLLRn13mS+9RSpAzAlxZSOu6NlljaIcQQ8J3TVjbQvJSSy1FLrBGSe4svh5HT1zibkaRCWdYiRW5eaOYNNWbXKMnldy3lyr5dWnR/1CUVTbE09q028IfTphpYApfhuaQ1xRqn3OzaD3zitD2ATTJkA8Ufe1FP3/uKdQZ43mlbhP6sijNIwTynhVg+JxHuYR6IUJaViQso+GVYFIYUnV17SJZfDyD3ddZsRGrmc2EhVpGN/hidSQeQ+zjL5eeSe7O3EOs4End14yzJMAHE+dmqHk3NYnL+ZoRVMVuepTiEpMrjrKOaasEHyVErbyVWt6V4CHjPaZtL2OXn0nVsq5rSUeS2Iq1QfwT5vYZzTvs25Ga5KuYhk+errA6WT1hkza428JfTthq429CXvGxhii8stFivknysrRej1JUnmcvRsrR7HLgZebYQpOZpe0q/J5Bi/rpwBfAPnYlcwP5Bp/jsSgsT3GxyXUjNaluLFYUQu0j+7kJWNrkuJLaGEE+F7SS9ssX6SVYNxoCfq3aioaGhoaGhoaGhYZL/AL1LyEy624qmAAAAAElFTkSuQmCC"

_, _adwite_light_temp = mkstemp()
_, _adwite_dark_temp = mkstemp()

_, _adwite_logo_light_temp = mkstemp()
_, _adwite_logo_dark_temp = mkstemp()

with open(_adwite_light_temp, "wb") as _adwite_light_file:
    from base64 import b64decode

    _adwite_light_file.write(b64decode(_adwite_light))

with open(_adwite_dark_temp, "wb") as _adwite_dark_file:
    from base64 import b64decode

    _adwite_dark_file.write(b64decode(_adwite_dark))

with open(_adwite_logo_light_temp, "wb") as _adwite_logo_light_file:
    from base64 import b64decode

    _adwite_logo_light_file.write(b64decode(_adwite_logo_light))

with open(_adwite_logo_dark_temp, "wb") as _adwite_logo_dark_file:
    from base64 import b64decode

    _adwite_logo_dark_file.write(b64decode(_adwite_logo_dark))

adwite_light_icon = (_adwite_light_temp).replace("\\", "//")
adwite_dark_icon = (_adwite_dark_temp).replace("\\", "//")

adwite_logo_light_icon = (_adwite_logo_light_temp).replace("\\", "//")
adwite_logo_dark_icon = (_adwite_logo_dark_temp).replace("\\", "//")


def create_web_thread(main):
    from tkwebview2.tkwebview2 import Thread, ThreadStart, ApartmentState
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()

def create_ie_thread(main):
    from tkwebview2.tkwebview2 import Thread, ThreadStart, ApartmentState
    t = Thread(ThreadStart(main))
    t.ApartmentState = ApartmentState.STA
    t.Start()
    t.Join()


class RenderType:
    CEFPYTHON = 1
    TKWEBVIEW = 2
    TKINTERIE = 3
    TKHTMLVIEW = 4


class Base(object):
    def __init__(self, _class, *args, **kwargs):
        self._widget = _class(*args, **kwargs)

    def widget(self, object=None) -> tk.Widget:
        if object is None:
            return self._widget
        else:
            self._widget = object


class Winfo(object):
    def winfo_screen_width(self):
        return self._widget.winfo_screenwidth()

    def winfo_screen_height(self):
        return self._widget.winfo_screenheight()

    def winfo_width(self):
        return self._widget.winfo_width()

    def winfo_height(self):
        return self._widget.winfo_height()


class Pack():
    def pack(self, *args, **kwargs):
        self._widget.pack(*args, **kwargs)


class Layout(Pack):
    pass


class Widget(Base, Winfo, Layout):
    isadw = True

    def parent(self, parent):
        if parent is None:
            if hasattr(parent, "isadw"):
                return parent.widget()
            else:
                return parent
        else:
            return None

    def widget_attr(self, attr_name, attr_value):
        eval(f"self._widget.config({attr_name}={attr_value})")

    def widget_bell(self, off=False):
        self._widget.bell(off)

    def widget_destroy(self):
        self._widget.destroy()

    def widget_id(self):
        return self._widget.winfo_id()

    def widget_win32_parent_id(self):
        from ctypes import windll
        return windll.user32.GetParent(self.widget_id())


class WebView(Widget):
    def __init__(self, parent=None, webview_render_engine=1, webview_url=None):
        self.webview_render_engine = webview_render_engine
        if webview_render_engine == RenderType.CEFPYTHON:
            from adwite.cefweb import Browser
            super().__init__(Browser, master=self.parent(parent), url=webview_url)
            self._webview_cef3_run()
        elif webview_render_engine == RenderType.TKWEBVIEW:
            from tkwebview2.tkwebview2 import have_runtime, install_runtime, WebView2
            if not have_runtime():
                install_runtime()
            super().__init__(WebView2, parent=self.parent(parent), width=10000, height=10000, url=webview_url)
        elif webview_render_engine == RenderType.TKINTERIE:
            from tkinterie.tkinterIE import WebView
            super().__init__(WebView, parent=self.parent(parent), width=10000, height=10000, url=webview_url)
        elif webview_render_engine == RenderType.TKHTMLVIEW:
            from tkhtmlview import HTMLScrolledText
            super().__init__(HTMLScrolledText, master=self.parent(parent), html=webview_url)

    def webview_run(self, web_add_func):
        if self.webview_render_engine == RenderType.CEFPYTHON:
            self._webview_cef3_run()

    def _webview_cef3_run(self):
        from adwite.cefweb import maincefloop
        maincefloop()

    def webview_get_url(self):
        if self.webview_render_engine == RenderType.CEFPYTHON:
            return self._webview_cef3_get_url()
        elif self.webview_render_engine == RenderType.TKWEBVIEW:
            return self._webview_web_get_url()

    def _webview_cef3_get_url(self):
        return self._widget.geturl()

    def _webview_web_get_url(self):
        return self._widget.get_url()

    def webview_new_window(self, func):
        if self.webview_render_engine == RenderType.CEFPYTHON:
            self._webview_cef3_new_window(func)
        elif self.webview_render_engine == RenderType.TKWEBVIEW:
            self._webview_web_new_window(func)

    def _webview_web_new_window(self, func):
        self._widget.event_new_window(func)

    def _webview_cef3_new_window(self, func):
        self._widget.NewWindow = func

    def webview_load_url(self, url=""):
        if self.webview_render_engine == RenderType.CEFPYTHON:
            self._webview_cef3_load_url(url)
        elif self.webview_render_engine == RenderType.TKWEBVIEW:
            self._webview_web_load_url(url)
        elif self.webview_render_engine == RenderType.TKINTERIE:
            self._webview_ie_load_url(url)

    def webview_load_html(self, html_string=""):
        if self.webview_render_engine == RenderType.TKWEBVIEW:
            self._webview_web_load_html(html)
        elif self.webview_render_engine == RenderType.TKHTMLVIEW:
            self._webview_html_load_html(html)

    def _webview_cef3_load_url(self, url=""):
        self._widget.loadurl(url)

    def _webview_web_load_url(self, url=""):
        self._widget.load_url(url)

    def _webview_ie_load_url(self, url=""):
        self._widget.navigate(url)

    def _webview_web_load_html(self, html=""):
        self._widget.load_html(html)

    def _webview_html_load_html(self, html=""):
        self._widget.set_html(html)

    def webview_refresh(self):
        if self.webview_render_engine == RenderType.CEFPYTHON:
            self._webview_cef3_refresh()
        elif self.webview_render_engine == RenderType.TKWEBVIEW:
            self._webview_web_refresh()
        elif self.webview_render_engine == RenderType.TKINTERIE:
            self._webview_ie_refresh()

    def _webview_cef3_refresh(self):
        self._widget.reload()

    def _webview_web_refresh(self):
        self._widget.reload()

    def _webview_ie_refresh(self):
        self._widget.refresh()

    def webview_ie_go_home(self):
        self._widget.gohome()

    def webview_ie_go_back(self):
        self._widget.goback()


class DrawEngine(Widget):
    def __init__(self, parent=None):
        super().__init__(tk.Canvas, master=self.parent(parent))


class Application(Widget):
    def __init__(self, app_width=None, app_height=None, app_taskbar_icon=True, app_icon=adwite_logo_dark_icon,
                 app_title=None):
        super().__init__(tk.Tk)
        self.app_size(app_width, app_height)
        self.app_taskbar_icon(app_taskbar_icon)
        self.app_icon(app_icon)
        self.app_title(app_title)

    def app_create_webview(self, *args, **kwargs):
        _webview = WebView(*args, **kwargs)
        _webview.pack(fill="both", expand=True)
        return _webview

    def app_frameless(self, boolean: bool = True):
        self._widget.overrideredirect(boolean)
        if platform == "win32":
            self._app_win32_application(self.widget_win32_parent_id())

    def app_caption(self):
        if platform == "win32":
            self._app_win32_caption(self.widget_win32_parent_id())

    def app_caption_move(self, widget):
        if platform == "win32":
            self._app_win32_caption_move(widget.widget_win32_parent_id())

    def _app_win32_caption_move(self, hwnd):
        def move():
            from ctypes import windll
            WM_SYSCOMMAND = 274
            SC_MOVE = 61456
            HTCAPTION = 2
            windll.user32.ReleaseCapture()
            windll.user32.SendMessageA(hwnd, WM_SYSCOMMAND, SC_MOVE + HTCAPTION, 0)

        self._widget.bind("<B1-Motion>", lambda _: move())

    def _app_win32_caption(self, hwnd):
        def titlebar():
            from ctypes import windll
            GWL_EXSTYLE = -16
            WS_CAPTION = 12582912
            SWP_NOSIZE = 1
            SWP_NOMOVE = 2
            SWP_NOZORDER = 4
            SWP_DRAWFRAME = 32
            hWnd = hwnd
            windll.user32.SetWindowLongW(hWnd, GWL_EXSTYLE,
                                         windll.user32.GetWindowLongW(hWnd, GWL_EXSTYLE) & ~WS_CAPTION)
            windll.user32.SetWindowPos(hWnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_DRAWFRAME)
            windll.user32.UpdateWindow(hWnd)

        self._widget.after(10, lambda: titlebar())

    def _app_win32_application(self, hwnd):
        from ctypes import windll
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    def app_center(self):
        x = self.winfo_screen_width() / 2 - self.winfo_width() / 2
        y = self.winfo_screen_height() / 2 - self.winfo_height() / 2
        self.app_pos(round(x), round(y))

    def app_taskbar_icon(self, enable, *args):
        if enable:
            if platform == "win32":
                self._app_win32_taskbar_icon(*args)

    def _app_win32_taskbar_icon(self, app_id="adwite.development.appid"):
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)

    def app_icon(self, file=None):
        if file is not None:
            self.default_icon = file
            self._widget.iconphoto(False, tk.PhotoImage(file=file))

    def app_pos(self, x, y):
        self._widget.geometry(f"+{x}+{y}")

    def app_run(self):
        self._widget.mainloop()

    def app_size(self, width, height):
        if width is not None or height is not None:
            self._widget.geometry(f"{width}x{height}")

    def app_title(self, text: str):
        if text is not None:
            self._widget.title(text)


class Window(Application):
    def __init__(self, app_width=None, app_height=None, app_taskbar_icon=True, app_icon=adwite_logo_dark_icon,
                 app_title=None):
        Widget.__init__(self, tk.Toplevel)
        self.app_size(app_width, app_height)
        self.app_taskbar_icon(app_taskbar_icon)
        self.app_icon(app_icon)
        self.app_title(app_title)


class UI(object):
    def __init__(self, app: Application):
        self._app = app

    def enable_dark(self, named):
        if platform == "win32":
            self._enable_win32_dark(named, self._app.widget_win32_parent_id())
            if named == UIType.ENABLE:
                self._app.widget_attr("bg", "'#000000'")

    def _enable_win32_dark(self, named, hwnd):
        from ctypes import windll, wintypes, byref, c_int, sizeof
        value = c_int(named)
        windll.dwmapi.DwmSetWindowAttribute(
            hwnd,  # 窗柄 输入值
            20,  # 类型 DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            byref(value),  # 数值 启用
            sizeof(value)  # 大小 数值大小
        )
        if self._app.default_icon == adwite_logo_light_icon and named == 0:
            self._app.app_icon(adwite_logo_dark_icon)
        elif self._app.default_icon == adwite_logo_dark_icon and named == 1:
            self._app.app_icon(adwite_logo_light_icon)
        if self._app.default_icon == adwite_light_icon and named == 0:
            self._app.app_icon(adwite_dark_icon)
        elif self._app.default_icon == adwite_dark_icon and named == 1:
            self._app.app_icon(adwite_light_icon)

    def enable_mica(self, named):
        if platform == "win32":
            self._enable_win32_mica(named, self._app.widget_win32_parent_id())

    def _enable_win32_mica(self, named, hwnd):
        from win32mica import ApplyMica
        ApplyMica(hwnd, named)


class UIType:
    ENABLE = 1
    DISABLE = 0


def main():
    app = Application(app_width=1000, app_height=600, app_title="Adwite Documentation")

    ui = UI(app)
    ui.enable_dark(UIType.ENABLE)

    webview = WebView(app, webview_render_engine=RenderType.TKWEBVIEW, webview_url="https://adwite.netlify.app/")
    webview.pack(fill="both", expand=True)  # 显示

    app.app_run()

if __name__ == '__main__':
    create_web_thread(main)