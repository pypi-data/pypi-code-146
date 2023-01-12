#!/usr/bin/env python3

import cv2
import logging
from pathlib import Path
from comfun import utils


def cvt_imgs(fdir_root, input_exts: tuple = (".webp",), out_ext=".jpg", recursive=True) -> None:
    """
    Creates a "out_ext" copy of each image that has an extesion in "input_exts"
    :param fdir_root: Root folder.
    :param input_exts: Tuple of extensions to be converted.
    :param out_ext:
    :param recursive:
    :return:
    """
    fpaths_webp = utils.get_all_fpaths_by_extension(fdir_root, exts=input_exts, recursive=recursive)
    for fpath in fpaths_webp:
        new_path = str(Path(fpath).parent / (Path(fpath).stem + out_ext))
        try:
            cv2.imwrite(new_path, cv2.imread(fpath))
        except Exception as e:
            print(f"[ ERROR ]  Writing {new_path} failed: {e}")
        else:
            logging.info(f"[  OK  ] created {new_path} from {fpath}")


if __name__ == "__main__":
    fpath = "/media/findux/DATA/Wallpaper/"
    cvt_imgs(fdir_root=fpath, input_exts=(".webp", ".avif"))
