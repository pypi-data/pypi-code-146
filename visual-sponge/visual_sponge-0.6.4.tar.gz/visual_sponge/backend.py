#pylint: disable = too-many-statements
import os, time, signal, traceback, webbrowser
from multiprocessing import Process
from pathlib import Path
from tempfile import TemporaryDirectory

from flask import Flask, render_template, send_from_directory, request, jsonify

from . import MACROS, Xponge, Model, Initialize, Configure
from .commands import *
from .commands import __all__ as all_commands
from .utils.ffmpeg import ff



Initialize()
Xponge.source("__main__")

def open_webbrowser(url):
    time.sleep(1)
    webbrowser.open(url, 1)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def run(run_files):
    app = Flask(MACROS.PACKAGE,
                template_folder=os.path.join(os.path.dirname(__file__), "templates"),
                static_folder=os.path.join(os.path.dirname(__file__), "static"))

    app.template_filter('localization')(MACROS.localization)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(os.path.dirname(__file__), "static"),
                                   'favicon.ico',
                                   mimetype='image/vnd.microsft.icon')

    @app.route('/')
    def index():
        argfiles = {}
        if run_files:
            argfiles["ini_mfile"] = run_files.pop()
        append = False
        argfiles["ini_tfile"] = []
        while run_files:
            argfiles["ini_tfile"].append(f"'{run_files.pop()}'{', append=True' if append else ''}")
            append=True
        return render_template("index.html",
                                translation=render_template("translation.js"),
                                myCodeMirrorCommands=render_template("myCodeMirrorCommands.js",
                                                                     commands=all_commands),
                                Configure=Configure,
                                **argfiles)

    @app.route("/cmd", methods=['POST'])
    def cmd():
        MACROS.CMD = None
        MACROS.TEXT = ""
        MACROS.TEMP = None
        value = request.form["value"]
        if not value:
            return jsonify({"text":""})
        try:
            try:
                exec(f"MACROS.TEMP = {value}", globals())
                if MACROS.TEMP is not None:
                    MACROS.TEXT += f"{MACROS.TEMP}"
                Xponge.source("__main__")
            except SyntaxError:
                exec(value, globals())
                Xponge.source("__main__")
            return jsonify({"text":MACROS.TEXT, "cmd":MACROS.CMD})
        except:
            return jsonify({"text":f"{traceback.format_exc()}"})

    @app.route("/get_png", methods=["POST"])
    def get_png():
        f = request.files["file"]
        suffix = request.form["suffix"]
        fname = Path(request.form["fname"])
        ofname = fname.with_suffix(suffix)
        if suffix == ".png":
            f.save(fname)
        else:
            with TemporaryDirectory() as tmpDir:
                ifname = Path(tmpDir) / fname.name
                f.save(Path(tmpDir) / fname.name)
                ff.options(f"-i {ifname} {ofname}")
        return MACROS.localization("MovieOrPrintScreenFinishedHint") + str(ofname.absolute())

    @app.route("/get_webm", methods=["POST"])
    def get_webm():
        f = request.files["file"]
        suffix = request.form["suffix"]
        fname = Path(request.form["fname"])
        ofname = fname.with_suffix(suffix)
        if suffix == ".webm":
            f.save(fname)
        else:
            with TemporaryDirectory() as tmpDir:
                ifname = Path(tmpDir) / fname.name
                f.save(Path(tmpDir) / fname.name)
                ofoptions = ""
                if suffix == ".mp4":
                    ofoptions += '-vf "pad=ceil(iw/2)*2:ceil(ih/2)*2"'
                ff.options(f"-i {ifname} {ofoptions} {ofname}")
        return MACROS.localization("MovieOrPrintScreenFinishedHint") + str(ofname.absolute())

    @app.route("/file", methods=["POST"])
    def file():
        folder = request.form["folder"]
        special = request.form["special"]
        if special == "HOME":
            folder = Path.home()
        elif special == "PARENT":
            folder = Path(folder).absolute().parent
        else:
            folder = Path(folder).absolute()

        try:
            files = list(folder.iterdir())
            hint = ""
        except PermissionError:
            files = []
            hint = MACROS.localization(" is not accissible (permission denied)")
        except FileNotFoundError:
            files = []
            hint = MACROS.localization(" is not accissible (invalid directory)")
        return render_template("open_file.html", folder=folder, files=files, hint=hint)

    @app.route("/setting", methods=["POST"])
    def setting():
        return render_template("setting.html", title=request.form.get("title", ""),
                                               head=request.form.get("head", ""),
                                               main=request.form.get("main", ""),
                                               foot=request.form.get("foot", ""),
                                               heights=request.form.get("heights", ""),
                                               title_style=request.form.get("title_style", ""),
                                               head_style=request.form.get("head_style", ""),
                                               main_style=request.form.get("main_style", ""),
                                               foot_style=request.form.get("foot_style", ""))

    @app.route("/getNumFrames", methods=["POST"])
    def getNumFrames():
        mid = int(request.form["mid"])
        return jsonify(len(Model.models[mid].u.trajectory))

    @app.route("/setFrame", methods=["POST"])
    def setFrame():
        mid = int(request.form["mid"])
        frame = int(request.form["frame"])
        traj = Model.models[mid].u.trajectory[frame]
        box = traj.dimensions.tolist() if traj.dimensions is not None else None
        return jsonify({"position": traj.positions.tolist(),
                        "box": box})

    @app.route("/exit", methods=["POST"])
    def exit():
        os.kill(os.getpid(), signal.SIGINT)
        return ""


    MACROS.APP = app
    Process(target=open_webbrowser, args=(f"http://127.0.0.1:{MACROS.PORT}",)).run()
    app.run(port=MACROS.PORT)
