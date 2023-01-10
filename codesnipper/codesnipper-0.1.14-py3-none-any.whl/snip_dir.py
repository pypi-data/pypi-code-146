import os
import shutil
from snipper.snipper_main import censor_file
from pathlib import Path
import time
import fnmatch
import tempfile
# from line_profiler_pycharm import profile

# @profile
def snip_dir(source_dir,  # Sources
             dest_dir=None,  # Will write to this directory
             output_dir=None, # Where snippets are going to be stored
             references=None, # Reference database
             exclude=None, clean_destination_dir=True,
             run_files=True,  # Run #!o tags and #!i tags
             cut_files=True,   # censor files.
             license_head=None,
             censor_files=True,
             verbose=True,
             ):

    print("Snipper fixing", source_dir)
    if dest_dir == None:
        dest_dir = tempfile.mkdtemp()
        print("[snipper]", "no destination dir was specified so using nonsense destination:", dest_dir)

    if references == None:
        references = dict(aux=None, bibtex=None,  commands=[])

    if exclude == None:
        exclude = []

    exclude += ["*__pycache__*"]  # Just...no.
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    source_dir = os.path.abspath(source_dir)
    dest_dir = os.path.abspath(dest_dir)
    if output_dir == None:
        output_dir = os.path.dirname(source_dir) + "/output"

    output_dir = os.path.abspath(output_dir)
    if os.path.samefile( source_dir, dest_dir):
        raise Exception("Source and destination is the same")

    if clean_destination_dir:
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir)
    out = dest_dir
    hw = {'base': source_dir}
    if verbose:
        print(f"[snipper]: {hw['base']} -> {out}")
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    shutil.copytree(source_dir, dest_dir)
    time.sleep(0.02)

    ls = list(Path(dest_dir).glob('**/*'))
    acceptable = []
    for l in ls:
        split = os.path.normpath(os.path.relpath(l, dest_dir))
        m = [fnmatch.fnmatch(split, ex) for ex in exclude]
        acceptable.append( (l, not any(m) ))

    n = 0
    cutouts = {}
    for f, accept in acceptable:
        if os.path.isdir(f) or str(f).endswith("_grade.py"):
            continue
        # if os.path.isdir(f) or not str(f).endswith(".py") or str(f).endswith("_grade.py"):
        #     continue
        # if accept and str(f).endswith(".rst"):
        #     nrem, cut = censor_file(f, run_files=run_files, run_out_dirs=output_dir, cut_files=cut_files,
        #                             # solution_list=solution_list,
        #                             base_path=dest_dir,
        #                             references=references,
        #                             license_head=license_head,
        #                             censor_files=censor_files,
        #                             **kwargs)

            # print("rst file")
        if accept and (str(f).endswith(".py") or str(f).endswith(".rst")):
            # if f.endswith("rst"):
            #     pass
            solution_list = []
            kwargs = {}
            if verbose:
                print("Snipper processing", f)
            nrem, cut = censor_file(f, run_files=run_files, run_out_dirs=output_dir, cut_files=cut_files,
                               # solution_list=solution_list,
                               base_path=dest_dir,
                               references=references,
                               license_head=license_head,
                               censor_files=censor_files,
                               **kwargs)
            if nrem > 0 and verbose:
                print(f"{nrem}> {f}")
            cutouts[str(f)] = cut
            n += nrem

    for rm_file, accept in acceptable:
        rm_file = os.path.abspath(rm_file)
        if not accept:
            if os.path.isfile(rm_file):
                os.remove(rm_file)
            else:
                if os.path.isdir(rm_file+"/"):
                    shutil.rmtree(rm_file)
    print("[snipper]", "done")
    return n, cutouts
