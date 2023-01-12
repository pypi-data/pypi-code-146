#!/usr/bin/env python3

import logging
import os
import pathlib
import shutil
import PyPDF2


def load_pdf(fpath) -> PyPDF2.PdfFileReader:
    with open(fpath, "rb") as f:
        pdf = PyPDF2.PdfFileReader(f)
    return pdf


def add_path_suffix(fpath: str, suffix="_backup") -> pathlib.Path:
    fpath = pathlib.Path(fpath)
    root, fname = os.path.split(fpath)
    fname_new = os.path.splitext(fname)[0] + suffix + os.path.splitext(fpath)[-1]
    fpath_new = os.path.join(root, fname_new)
    return pathlib.Path(fpath_new)


def files_are_identical(fpath_1, fpath_2):
    files = []
    for fpath in [fpath_1, fpath_2]:
        with open(fpath, "rb") as f:
            files.append(f.read())
    assert len(files) == 2
    if files[0] == files[1]:
        return True
    return False


def get_metadata(fpath) -> dict:
    metadata = {}
    try:
        with open(fpath, "rb") as f:
            pdf = PyPDF2.PdfFileReader(f)
            metadata = pdf.getDocumentInfo()
    except Exception as e:
        print(e)
    return metadata


def remove_metadata_from_file(fpath_src, fpath_dst=None):
    fpath_src = pathlib.Path(fpath_src)
    if fpath_dst is None:
        fpath_dst = fpath_src
    else:
        fpath_dst = pathlib.Path(fpath_dst)

    metadata_old: dict = get_metadata(fpath_src)
    metatdata_new = {k: "no_data" for k, v in metadata_old.items()}

    logging.debug(f"Processing file {fpath_src}")
    with open(fpath_dst, "wb") as f:
        writer = PyPDF2.PdfWriter()
        writer.appendPagesFromReader(PyPDF2.PdfReader(fpath_src))
        writer.addMetadata(metatdata_new)
        writer.write(fpath_dst)
    print(f"Removed metadata from {fpath_src}")


def remove_metadata_from_all(fdir_root, recursive=False, backup=True, fdir_backup=None):
    # Paths setup
    fdir_root = pathlib.Path(fdir_root)
    fpaths_pdf = get_all_pdf_paths(fdir_root, recursive=recursive)
    if recursive:
        fpaths_pdf = [f for f in fpaths_pdf if not f.lower().startswith(fdir_backup.lower())]

    for fpath_src in fpaths_pdf:
        fpath_dst = add_path_suffix(fpath_src, suffix="_no_metadata")
        remove_metadata_from_file(fpath_src, fpath_dst)
    print("Done")


def get_all_pdf_paths(fdir_root, recursive=False):
    fpaths = []
    if recursive:
        for root, dirs, files in os.walk(fdir_root):
            fpaths.extend([os.path.join(root, f) for f in files if f.lower().endswith(".pdf")])
    else:
        fpaths = [os.path.join(fdir_root, f) for f in os.listdir(fdir_root) if f.lower().endswith(".pdf")]
    return fpaths


def merge_all_pdfs(fdir_root: str, fpath_dst: str, recursive: bool = False):
    fpaths = get_all_pdf_paths(fdir_root=fdir_root, recursive=recursive)
    merger = PyPDF2.PdfMerger()
    for f in fpaths:
        merger.append(f)
    try:
        merger.write(fpath_dst)
    except Exception as e:
        print(e)
    finally:
        merger.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s]\t%(message)s")

    fdir_src = "/home/findux/Desktop/Next/print/spec/nometadata/"
    merge_all_pdfs(fdir_src, "/home/findux/Desktop/spectral_package.pdf")