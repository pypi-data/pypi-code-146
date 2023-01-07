import pandas as pd
import janitor
import pickle
from colorise_terminal.rgb import RGB
from pathlib import Path

parent_path = Path(__file__).parent

colors = pd.read_csv(parent_path / "colors.txt", sep="\t").clean_names()
colors["rgb"] = colors["rgb"].str.extract("\((.*)\)", expand=False).str.split(",").apply(lambda x: [int(y) for y in x])
colors["rgb"] = colors["rgb"].map(lambda x: RGB(*x))
color_dict = colors.set_index("rgb")["xterm_number"].to_dict()
with open(parent_path.parent / "colors_dict.pkl", "wb") as f:
    pickle.dump(color_dict, f)
