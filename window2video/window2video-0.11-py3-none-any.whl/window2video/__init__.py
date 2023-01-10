from shutil import copyfile
from time import time, sleep
import keyboard
from ctypes_screenshots import screencapture_window, list_windows
from get_video_len import get_video_len_and_frames
from list_files_with_timestats import get_folder_file_complete_path_limit_subdirs
from make_even_odd import make_even_ceil
import os
from plyer import notification
from a_cv_imwrite_imread_plus import save_cv_image
import pandas as pd
import sys
import subprocess

goon = True


def start_recorder_in_console():
    subprocess.run(
        f"start cmd /k {sys.executable} -i {os.path.normpath(__file__)}", shell=True
    )


def start_recorder(hwnd, outputfolder, exit_keys="ctrl+alt+k"):
    outputfolder = os.path.normpath(outputfolder)
    subprocess.run(
        f"start cmd /k {sys.executable} -i {os.path.normpath(__file__)} {hwnd} {outputfolder} {exit_keys}",
        shell=True,
    )


def stop_video():
    global goon
    goon = False


def write_with_ffmpeg(foldername, allwrittenpics=None):
    if not isinstance(foldername, list):
        foldername = [foldername]
    outputfolder = os.path.join(foldername[0], "video")
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)
    allfi = get_folder_file_complete_path_limit_subdirs(
        foldername, maxsubdirs=0, withdate=True
    )
    df = pd.DataFrame(allfi)
    if isinstance(allwrittenpics, list):
        df = df.loc[df.path.isin(allwrittenpics)]
    df = df.sort_values(by="path").reset_index(drop=True)
    df["timestamppython"] = df.file.str.split(r"[_\.]").str[-2].astype("Int64")
    df.timestamppython = df.timestamppython.apply(lambda x: next(make_even_ceil(x)))
    df["timedifference"] = df.timestamppython.diff()
    df["timedifference"] = df["timedifference"].shift(-1)
    df = df.dropna().reset_index(drop=True)
    df.timedifference = df.timedifference.astype(int)
    fname = 0
    allframescreated = []
    counterf = 0
    for key, item in df.iterrows():
        counterf += 1
        for fi in range(item.timedifference):
            randval = counterf % 4 == 0

            counterf += 1
            if not randval:
                continue
            newpath = os.path.join(outputfolder, str(fname).zfill(9) + ".png")
            oldpath = item.path
            print(newpath, end="\r")
            fname += 1
            copyfile(oldpath, newpath)
            allframescreated.append(newpath)
    oldwd = os.getcwd()
    os.chdir(outputfolder)
    os.system(
        f"""ffmpeg -y -i %09d.png -codec:v libx264 -preset slow -filter:v fps=29.97 out.mp4"""
    )

    os.chdir(oldwd)
    for f in allframescreated:
        try:
            os.remove(f)
        except Exception as fe:
            print(fe)
            continue


def start_recording(foldernames: list, allhwnds: list) -> list:
    global goon
    message = [
        f"title: {x.title} pid: {x.pid} hwnd: {x.hwnd}"
        for x in list_windows()
        if x.hwnd == allhwnds[0]
    ][0]
    wholecounter = -1
    allwrittenpics_ = []
    lastgoodpic = None
    lasterrordisplayed = time()
    while goon:

        for _ in zip(
            [(i, screencapture_window(x)) for i, x in zip(foldernames, allhwnds)]
        ):
            wholecounter += 1
            for ini, wi in enumerate(_):
                loop_time = time()
                wibild = wi[1]
                fpath = wi[0]
                savepath = os.path.normpath(
                    os.path.join(
                        fpath,
                        str(wholecounter).zfill(9)
                        + "_"
                        + str(time())[:13].replace(".", "")
                        + ".png",
                    )
                )
                pictowrite = next(wibild)
                try:
                    save_cv_image(savepath, pictowrite)
                    lastgoodpic = pictowrite.copy()
                except Exception as fe:
                    save_cv_image(savepath, lastgoodpic)
                    if time() - lasterrordisplayed > 5:
                        notification.notify(
                            title="Error writing file! Is the window minimized?", message=message, timeout=0
                        )
                        lasterrordisplayed = time()
                    sleep(0.7)

                allwrittenpics_.append(savepath)
                print("FPS {}            ".format(1 / (time() - loop_time)), end="\r")
                sleep(0.001)
    goon = True
    return allwrittenpics_


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            allhwnds = [int(sys.argv[1])]
            foldernames = [str(sys.argv[2]).strip()]

            exit_keys = str(sys.argv[3]).strip()

        except Exception as fe:
            for w in list_windows():
                if w.status == "visible":
                    print(w)
            print(fe)
            print("args: hwnd outputfolder exitkeys")
            print(sys.argv)

    else:
        for w in list_windows():
            if w.status == "visible":
                print(w)
        allhwnds = None
        while True:
            try:
                allhwnds = [int(input("hwnd: "))]
                break
            except Exception:
                print("Wrong input!")
        foldernames = None
        while True:
            try:
                foldernames = [str(input("output folder: ")).strip()]
                break
            except Exception:
                print("Wrong input!")
        exit_keys = str(input("Stop recording keys (default: ctrl+alt+k): ")).strip()
        if exit_keys == "":
            exit_keys = "ctrl+alt+k"

    keyboard.add_hotkey(exit_keys, stop_video)
    starttime = time()
    allwrittenpics = start_recording(foldernames, allhwnds)
    endtime = time()
    write_with_ffmpeg(foldernames, allwrittenpics=allwrittenpics)
    print("Converted video: ")
    print(get_video_len_and_frames(os.path.join(foldernames[0], r"video\out.mp4")))
    print("Real duration:")
    print(endtime - starttime)
