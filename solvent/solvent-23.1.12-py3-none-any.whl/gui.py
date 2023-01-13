import itertools
import random

import caffeine
import flet
import pomace
from flet import Page, Text

from solvent.scripts import Script


def main(page: Page):
    page.title = "Solvent"
    page.scroll = "adaptive"
    text = Text("Hello")
    page.add(text)

    scripts = {}
    for cls in Script.__subclasses__():
        script = cls()  # type: ignore
        scripts[script.name] = script

    text.value = "Running all scripts"
    names = [k for k, v in scripts.items() if not v.SKIP]
    random.shuffle(names)

    pomace.utils.locate_models()
    pomace.freeze()

    caffeine.on(display=True)

    for count in itertools.count(start=1):
        text.value += f"\nStarting loop {count}"
        page.update()
        for name in names:
            scripts[name].loop(5 * 60)


flet.app(target=main)
