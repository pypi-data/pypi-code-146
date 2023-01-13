try:
    import cefpython3

    def test1():
        from adwite import Application, WebView, RenderType, UI, UIType

        app = Application(app_width=1000, app_height=600, app_title="Adwite Documentation")

        ui = UI(app)
        ui.enable_dark(UIType.ENABLE)

        def new_window(url):
            webview = WebView(Window(app_width=1000, app_height=600, app_title="New Window"),
                              webview_render_engine=RenderType.CEFPYTHON, webview_url=url)
            webview.pack(fill="both", expand=True)

        webview = WebView(app, webview_render_engine=RenderType.CEFPYTHON, webview_url="https://adwite.netlify.app/")
        webview.webview_new_window(new_window)
        webview.pack(fill="both", expand=True)  # 显示

        app.app_run()
except:
    pass
else:
    test1()

try:
    import tkwebview2

    def test2():
        from adwite import Application, WebView, RenderType, UI, UIType

        app = Application(app_width=1000, app_height=600, app_title="Adwite Documentation")

        ui = UI(app)
        ui.enable_dark(UIType.ENABLE)

        webview = WebView(app, webview_render_engine=RenderType.TKWEBVIEW, webview_url="https://adwite.netlify.app/")
        webview.pack(fill="both", expand=True)  # 显示

        app.app_run()
except:
    pass
else:
    from adwite import create_web_thread
    create_web_thread(test2)