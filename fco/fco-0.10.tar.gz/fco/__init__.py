import os, shutil


def flatcopy(rdir, output, sep="#"):
    if not os.path.exists(output):
        os.makedirs(output)
    for sdirs, dirs, files in os.walk(rdir):
        [
            shutil.copyfile(
                g := os.path.join(sdirs, k),
                os.path.join(output, g.replace(os.sep, sep).replace(":", "")),
            )
            for k in files
        ]
