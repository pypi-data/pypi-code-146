import argparse
import codecs
import sys
import os
import time
import subprocess
from datetime import datetime


clean_up = [
    ".bar",
    ".cor",
    ".lua",
    ".lub",
    ".tab",
    ".log",
    ".gz",
    ".aux",
    ".out",
    ".fdb_latexmk",
    ".fls",
    ".xdv",
    ".dvi",
]


def initilisation(path_to_watch):
    paths = [path_to_watch]
    for root, dirs, files in os.walk(path_to_watch):
        for dir in dirs:
            paths.append(os.path.join(path_to_watch, dir))
    return paths


def get_files(paths):
    files = []
    for path in paths:
        try:
            temp_list = [
                {
                    "name": os.path.join(path, file),
                    "time_modification": os.path.getmtime(os.path.join(path, file)),
                    "path": path,
                }
                for file in os.listdir(path)
                if ".tex" in file
            ]
            files = files + temp_list
        except:
            pass
    return files


def clean_aux(paths):
    for path in paths:
        try:
            for file in os.listdir(path):
                ext = os.path.splitext((file))[1]
                if ext in clean_up:
                    os.remove(os.path.join(path, file))
        except:
            pass


def recompile_all(path_to_watch, latex_engine):
    cmd = f"latexmk -interaction=nonstopmode -{latex_engine}"
    print(cmd)
    subprocess.call(cmd, shell=True)
    subprocess.call(cmd, shell=True)
    clean_aux([path_to_watch])


def watch(path_to_watch, latex_engine):
    print("Démarrage de la surveillance.")
    print(f"Dossier: {path_to_watch}")
    paths = initilisation(path_to_watch)
    before = get_files(paths)
    while 1:
        time.sleep(10)
        after = get_files(paths)
        added = [f for f in after if not f in before]
        if added:
            print("Fichier ajouté ou modifié")
            for file in added:
                if " " in file["path"]:
                    output = paths[0]
                else:
                    output = file["path"]
                print(output)
                cmd = f"latexmk \"{file['name']}\" -interaction=nonstopmode -{latex_engine} -output-directory=\"{os.path.join(file['path'])}\""
                print(cmd)
                subprocess.call(cmd, shell=True)
            before = after
            clean_aux(paths)


def define_latex_engine(args):
    if args.lualatex:
        print("lualatex")
        return "lualatex"
    else:
        print("xelatex")
        return "xelatex"


def main():
    path_to_watch = os.getcwd()
    parser = argparse.ArgumentParser(description="""Basic usage: latexcor""")
    parser.add_argument(
        "--clean",
        action="store_true",
        default=False,
        help="clean all aux files in current directory",
    )
    parser.add_argument(
        "--recompile",
        action="store_true",
        default=False,
        help="recompile all files in current directory",
    )
    parser.add_argument(
        "--xelatex", action="store_true", default=True, help="xelatex default True"
    )
    parser.add_argument(
        "--lualatex", action="store_true", default=False, help="lualatex default False"
    )
    args = parser.parse_args()
    if args.clean:
        print(f"Nettoyage du dossier: {path_to_watch}")
        clean_aux([path_to_watch])
        print("Fait")
    elif args.recompile:
        latex_engine = define_latex_engine(args)
        print("Recompile tout")
        recompile_all(path_to_watch, latex_engine)
        print("Fait")
    else:
        latex_engine = define_latex_engine(args)
        watch(path_to_watch, latex_engine)


if __name__ == "__main__":
    main()
