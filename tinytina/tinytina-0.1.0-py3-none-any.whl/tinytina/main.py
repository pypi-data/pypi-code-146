import beaupy
from ttwlsave.ttwlsave import TTWLSave
from ttwlsave.ttwlprofile import TTWLProfile
from pprint import pprint
import userpaths
import shutil
import os

def	found_ttwl_save() -> list:
	save_folder = userpaths.get_my_documents() + "\\My Games\\Tiny Tina's Wonderlands\\Saved\\SaveGames"
	save = list()
	for dir in os.listdir(save_folder):
		if "profile.sav" in os.listdir(save_folder + "\\" + dir):
			save.append(save_folder + "\\" + dir)
	return save

def	build_save_list(saves: list) -> dict:
	save_infos = dict()
	for save in saves:
		for file in os.listdir(save):
			if os.path.basename(file) != "profile.sav" and os.path.splitext(file)[1] == ".sav":
				save_infos[TTWLSave(save + "\\" + file).get_char_name()] = save + "\\" + file
	return save_infos

def ask_user(type: str, limit: int = None) -> int:
	done: bool = False
	while not done:
		res = beaupy.prompt(f"How much {type} do you want: ")
		try:
			res = int(res)
			if limit and res <= limit:
				done = True
			elif limit:
				beaupy.console.clear()
				beaupy.console.print(f"[red bold]Maximum is {limit}[/red bold]")
			else:
				done = True
		except ValueError:
			beaupy.console.clear()
			beaupy.console.print("[red bold]You must enter a number[/red bold]")
	return res

def main () -> None:
	beaupy.console.clear()
	save_infos = build_save_list(found_ttwl_save())
	items_options = list()
	for key, value in save_infos.items():
		items_options.append(f"{key}")

	beaupy.console.clear()
	beaupy.console.print("Select your save:")
	save_selected = beaupy.select(items_options)
	save = TTWLSave(save_infos[save_selected])

	beaupy.console.clear()
	beaupy.console.print("Select what you want to change:")
	items_options = ["[red bold]Make a backup (recommended)[/red bold]", "Money", "Moon Orbs", "Souls", "Skeleton keys"]
	items_selected = beaupy.select_multiple(items_options)

	if "[red bold]Make a backup (recommended)[/red bold]" in items_selected:
		if os.path.exists(save_infos[save_selected] + ".bak"):
			os.remove(save_infos[save_selected] + ".bak")
		if os.path.exists(os.path.dirname(save_infos[save_selected]) + "\\profile.sav.bak"):
			os.remove(os.path.dirname(save_infos[save_selected]) + "\\profile.sav.bak")
		shutil.copy(
			save_infos[save_selected],
			save_infos[save_selected] + ".bak"
		)
		shutil.copy(
			os.path.dirname(save_infos[save_selected]) + "\\profile.sav",
			os.path.dirname(save_infos[save_selected]) + "\\profile.sav.bak"
		)
	if "Money" in items_selected:
		beaupy.console.clear()
		res = ask_user("money", 2_000_000_000)
		save.set_money(res)
		save.save_to(save_infos[save_selected])
	if "Moon Orbs" in items_selected:
		beaupy.console.clear()
		res = ask_user("moon orbs", 16_000)
		save.set_moon_orbs(res)
		save.save_to(save_infos[save_selected])
	if "Souls" in items_selected:
		beaupy.console.clear()
		res = ask_user("souls")
		save.set_souls(res)
		save.save_to(save_infos[save_selected])
	if "Skeleton keys" in items_selected:
		beaupy.console.clear()
		res = ask_user("skeleton keys")
		profile = TTWLProfile(os.path.dirname(save_infos[save_selected]) + "\\profile.sav")
		profile.set_skeleton_keys(res)
		profile.save_to(os.path.dirname(save_infos[save_selected]) + "\\profile.sav")
	beaupy.console.clear()
	beaupy.console.print("[green]Enjoy ![/green]")

