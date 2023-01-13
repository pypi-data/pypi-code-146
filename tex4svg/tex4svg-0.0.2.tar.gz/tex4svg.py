# License: GNU GPLv3+, Rodrigo Schwencke, 2023 (Copyleft)

# import sqlite3
import sys
import os.path
import os
import sys
import subprocess

DEFAULT_PACKAGES = ['amsmath', 'tkz-tab', 'amssymb']

def tex2svg(tex:str, mode="inline", packages=DEFAULT_PACKAGES, tmpPath="./img/tex", tmpFilename="tmp.svg")->str:
    assert tmpFilename[tmpFilename.rfind("."):] == ".svg", "Error: Temporary export filename must be end with '.svg'"
    tex = tex.strip()
    mode.strip()
    tmpPath.rstrip("/")
    tmpPath = tmpPath+"/"
    filename = tmpFilename[:tmpFilename.rfind(".")]

    # os.makedirs(os.path.expanduser('~/.tex2svg/'), exist_ok=True)

    if mode == "inline":
        inlineMode = True
    else: # mode == "block"
        inlineMode = False
    # we need to create the result and cache it

    preamble, postamble = get_preamble_postamble(inlineMode, packages)
    texDocument = preamble+tex+postamble

    # with open(os.path.expanduser('~/.tex2svg/tmp.tex'), "w") as f:
    #     f.write(preamble + tex + postamble)
    # os.system("pdflatex -output-directory ~/.tex2svg/ tmp.tex &> /dev/null")
    # os.system("pdfcrop ~/.tex2svg/tmp.pdf ~/.tex2svg/tmp_crop.pdf &> /dev/null")
    # os.system("pdf2svg ~/.tex2svg/tmp_crop.pdf ~/.tex2svg/tmp.svg &> /dev/null")
    
    os.makedirs(tmpPath, exist_ok=True)

    with open(tmpPath+f"{filename}.tex", "w") as f:
        f.write(preamble + tex + postamble)

    os.system(rf"pdflatex -output-directory {tmpPath} {filename}.tex &> /dev/null")
    os.system(rf"pdfcrop {tmpPath}{filename}.pdf {tmpPath}{filename}_crop.pdf &> /dev/null")
    os.system(f"pdf2svg {tmpPath}{filename}_crop.pdf {tmpPath}{filename}.svg &> /dev/null")
    fichierSvg = open(os.path.expanduser(rf"{tmpPath}{filename}.svg"), "r")
    svg = "".join(fichierSvg.readlines())
    
    # svg = subprocess.check_output("svgo --output - --input ~/.tex2svg/tmp.svg", shell=True).decode("utf-8")
    # print(svg)
    # c.execute("INSERT INTO items VALUES(?, ?, ?)", (tex, inline, svg))
    # conn.commit()
    # conn.close()
    return svg

def get_preamble_postamble(inlineMode, packages)->tuple:
    if inlineMode:
        preamble = r"\documentclass{article}"+"\n"
        for package in packages:
            preamble += rf"\usepackage{{{package}}}"+"\n"
        preamble += r"""\begin{document}
\pagestyle{empty}
$$"""
        postamble = r"""$$
\end{document}
"""
    else:
        preamble = r"\documentclass{article}"+"\n"
        for package in packages:
            preamble += rf"\usepackage{{{package}}}"+"\n"
        preamble += r"""\begin{document}
\pagestyle{empty}
\begin{equation*}
"""
        postamble = r"""
\end{equation*}
\end{document}
"""
    return (preamble, postamble)