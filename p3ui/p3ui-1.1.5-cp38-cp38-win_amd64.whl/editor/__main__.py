import argparse
import importlib

from p3ui import *
from .editor_template import EditorTemplate
from .editor import Editor


async def main(module_name):
    window = Window(
        title='Template Editor',
        position=(50, 50),
        size=(1080, 960),
        idle_timeout=600.
    )
    padding = 50
#    size = window.monitor.mode.width - 2 * padding, window.monitor.mode.height - 2 * padding
    window.position = (padding, padding)
#    window.size = size

    editor = Editor(window)
    window.user_interface.content = editor.root_node
    editor.load_module(module_name)

    await window.closed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='template editor')
    parser.add_argument('module', type=str, help='target module for created templates')
    args = parser.parse_args()
    run(main(args.module))
