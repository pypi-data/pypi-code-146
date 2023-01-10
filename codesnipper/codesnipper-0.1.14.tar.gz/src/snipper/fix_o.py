import functools
import os
from snipper.legacy import block_process
from snipper.block_parsing import indent


def run_o(lines, file, output):
    def block_fun(lines, start_extra, end_extra, art, output, **kwargs):
        id = indent(lines[0])
        outf = output + ("_" + art if art is not None else "") + ".txt"
        l2 = []
        l2 += [id + "import sys", id + f"sys.stdout = open('{outf}', 'w')"]
        l2 += lines
        l2 += [indent(lines[-1]) + "sys.stdout = sys.__stdout__"]
        return l2, None
    try:
        lines2, didfind, extra, _ = block_process(lines, tag="#!o", block_fun=functools.partial(block_fun, output=output) )
    except Exception as e:
        print("Bad file: ", file)
        print("I was cutting the #!o tag")
        print("\n".join( lines) )
        raise(e)

    if didfind:
        fp, ex = os.path.splitext(file)
        file_run = fp + "_RUN_OUTPUT_CAPTURE" +ex
        if os.path.exists(file_run):
            print("file found mumble...")
        else:
            with open(file_run, 'w', encoding="utf-8") as f:
                f.write("\n".join(lines2) )
            cmd = "python " + file_run
            import subprocess
            s = subprocess.check_output(cmd, shell=True)
            os.remove(file_run)