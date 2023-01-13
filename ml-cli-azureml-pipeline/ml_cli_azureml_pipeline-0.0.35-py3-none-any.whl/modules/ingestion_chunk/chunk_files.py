import sys
import time
from pathlib import Path
import shutil
import numpy
import multiprocessing as mp
import gc


def move_files(source_dir, chunk, dest_dir, chunk_name, sub_directory: str = None):
    for file_path in chunk:
        try:
            file_pathlib = Path(file_path)
            filename = file_pathlib.stem + file_pathlib.suffix
            if sub_directory is None or sub_directory == "":
                dest_path = Path(dest_dir) / chunk_name / filename
            else:
                dest_path = Path(dest_dir) / chunk_name / sub_directory / filename
            scr_dir = str(Path(source_dir) / filename)
            if Path(scr_dir).is_file():
                shutil.copy(scr_dir, str(dest_path))
            else:
                print("a new file appear, won't be copied")
        except Exception as ex:
            print("Exception thrown. x does not exist." + str(file_path) + " " + str(ex))


def chunk_files(raw_dataset, dest_dir: str,
                number_chunk: int, multithread=True, chunk_index_to_copy=None, sub_directory: str = None):
    with raw_dataset.mount() as mount_context:
        all_documents_flatten_dir = mount_context.mount_point
        files_list = [str(p) for p in Path(all_documents_flatten_dir).iterdir() if p.is_file()]
    files_list.sort()
    number_files = len(files_list)
    print("number file is : " + str(number_files))
    chunks = numpy.array_split(numpy.array(files_list), number_chunk)
    for index, chunk in enumerate(chunks):
        if chunk_index_to_copy is not None and index not in chunk_index_to_copy:
            continue
        chunk_name = "chunk" + str(index)
        if sub_directory is None or sub_directory == "":
            dir_path = Path(str(Path(dest_dir) / chunk_name))
        else:
            dir_path = Path(str(Path(dest_dir) / chunk_name / sub_directory))
        dir_path.mkdir(parents=True, exist_ok=True)
        start = time.time()

        if multithread:
            number_sub_chunk = int(len(chunk) / 5000)
            if number_sub_chunk == 0:
                number_sub_chunk = 1
            sub_chunks = numpy.array_split(numpy.array(chunk), number_sub_chunk)
            for sub_chunk in sub_chunks:
                with raw_dataset.mount() as mount_context:
                    all_documents_flatten_dir = mount_context.mount_point
                    number_cpus = mp.cpu_count()
                    print('Number cores found: ' + str(number_cpus))
                    pool = mp.Pool(number_cpus)
                    csv_files_chuncks = numpy.array_split(sub_chunk, number_cpus)
                    try:
                        pool.starmap(move_files, [(all_documents_flatten_dir, row, dest_dir, chunk_name, sub_directory) for row in
                                                  csv_files_chuncks])
                    except Exception:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise
                    finally:
                        pool.close()
                        gc.collect()
        else:
            move_files(all_documents_flatten_dir, chunk, dest_dir, chunk_name)
            gc.collect()

        end = time.time() - start
        print("Time move chunk " + str(index) + " " + str(end))
