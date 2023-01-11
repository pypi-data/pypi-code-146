import os
import platform
from shutil import copytree

from pick import pick

proj_dir_windows = "X:"
proj_dir_macos = "/Volumes/ams-fileserver/"

go_folder = "GO"
mv_folder = "MV"
deal_folder = "9999_Offertes_Gegevens"


def get_latest_proj():
    projectcodes = []

    dir = proj_dir_windows if platform.system() == "Windows" else proj_dir_macos

    for x in os.scandir(dir):
        if x.is_dir():
            try:
                code = int(x.name[0:4])
            except Exception:
                continue
            else:
                if code != 9999:
                    projectcodes.append(code)

    return max(projectcodes) + 1


def get_deal_info(dealnumber):
    dir = proj_dir_windows if platform.system() == "Windows" else proj_dir_macos
    deal_dir = os.path.join(dir, deal_folder)
    deal = None
    deals = [f for f in os.listdir(deal_dir) if f"_{dealnumber}_" in f]

    if len(deals) > 1:
        ret = pick(deals, "pick a deal")
        deal = deals[ret[1]]
    elif len(deals) == 1:
        deal = deals[0]
    else:
        print(f'no deal found in {deal_folder}')

    if deal is not None:
        return deal


def create_project_on_fileserver(project, internal=False, deal=None):

    dir = proj_dir_windows if platform.system() == "Windows" else proj_dir_macos
    project_dir = f"{dir}/{project}"

    print(project_dir)
    print(f"{project_dir} already exists") if os.path.isdir(
        project_dir
    ) else os.makedirs(project_dir)
    project_go = os.path.join(project_dir, go_folder)
    print(f"{project_go} already exists") if os.path.isdir(
        project_go) else os.makedirs(project_go)
    project_mv = os.path.join(project_dir, mv_folder)
    print(f"{project_mv} already exists") if os.path.isdir(
        project_mv) else os.makedirs(project_mv)

    if deal is not None:
        deal_dir = os.path.join(dir, deal_folder, deal)
        deal_go = os.path.join(deal_dir, "GO")
        deal_mv = os.path.join(deal_dir, "MV")

        if os.path.isdir(deal_go):
            copytree(deal_go, project_go, dirs_exist_ok=True)

        if os.path.isdir(deal_mv):
            copytree(deal_mv, project_mv, dirs_exist_ok=True)
        else:
            print("probber on MV proj")

    if internal:
        maps = os.path.join(project_dir, "Maps")
        print(f"{maps} already exists") if os.path.isdir(maps) else os.makedirs(maps)
        scenes = os.path.join(project_dir, "Scenes")
        print(f"{scenes} already exists") if os.path.isdir(
            scenes) else os.makedirs(scenes)
