import typer


def jnb_clean(
    folder: str = typer.Argument(
        "notebooks", help="threshold for device dead runs~(min)"
    ),
    is_debug: bool = typer.Option(False, "--v", help="only show info not run"),
):
    """
    clean notebooks folder, only git clean data, but keep src for reproduce. skip nb file startswith skip
    """
    try:
        import jammy.io as jio
        from jammy.io.path import glob
        from jammy.utils.git import git_rootdir
        from jammy.utils.process import run_simple_command
    except ImportError:
        print("jammy needed to run the func")
        exit(1)

    for in_nb_file in glob(git_rootdir(folder), regex="ipynb$"):
        if ".ipynb_checkpoints" in in_nb_file:
            continue
        names = in_nb_file.split("/")
        nb_file_name = names[-1].split(".")[0]
        if nb_file_name.startswith("_clean_") or nb_file_name.startswith("skip"):
            continue
        out_nb_file = "/".join(names[:-1]) + f"/_clean_{nb_file_name}.ipynb"
        jio.copy(in_nb_file, out_nb_file)
        cmd = f"cat {in_nb_file} | nbstripout > {out_nb_file}"
        if is_debug:
            print(cmd)
        else:
            run_simple_command(cmd)


def main():
    typer.run(jnb_clean)
