import os
import os.path as osp
import shutil
from pathlib import Path

import typer
from loguru import logger
from pyfzf.pyfzf import FzfPrompt


def cp_jam_template(
    is_debug: bool = typer.Option(
        False, "--v", help="only show content not direct copy"
    )
):
    """
    select and copy jam template files into pwd, files saved in `jamexp/template_data`
    """
    jamexp_path = Path(__file__).parent.parent
    jam_template_path = osp.join(jamexp_path, "template_data")
    whole_template = {
        item: osp.join(jam_template_path, item)
        for item in os.listdir(jam_template_path)
    }
    try:
        fzf = FzfPrompt()
        select = fzf.prompt(whole_template.keys(), "-m")
    except Exception as error:  # pylint: disable=broad-except
        raise RuntimeError(  # pylint: disable=raise-missing-from
            "FZF error: {}".format(error)
        )
    if is_debug:
        for item in select:
            logger.info(item)
            logger.info(f"cp {whole_template[item]} {osp.join(os.getcwd(), item)}")
            with open(whole_template[item], "r", encoding="utf8") as fp:
                for _ in range(5):
                    print(fp.readline())
    else:
        for item in select:
            shutil.copy(whole_template[item], osp.join(os.getcwd(), item))


def cp_template():
    typer.run(cp_jam_template)


if __name__ == "__main__":
    cp_jam_template(is_debug=True)
