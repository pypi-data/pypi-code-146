from typing import List


class Menu:
    """
    Display a list of choices until the user chooses quit

    Example usage::

        from simple_menu.items import FunctionItem
        from simple_menu.items import MenuItem
        from simple_menu import Menu

        m = Menu(prompt="Main Menu")
        m.items.append(FunctionItem(label="Item 1", function=lambda: print("Item 2")))

        m2 = Menu(parent=m, prompt="Sub Menu 1")
        m2.items.append(FunctionItem(label="Item 2", function=lambda: print("Item 2")))
        m.items.append(MenuItem(label="Sub Menu 1", menu=m2))

        m.run()

    Attributes:

        prompt(str): The prompt before the item list (default: "Menu")
        prompt_quit(str): The prompt to quit the application (default: "Quit")
        prompt_go_back(str): The prompt to exit the sub-menu (default: "Go Back")
        parent(Menu|None): The parent menu this menu belongs to
    """

    def __init__(
        self,
        prompt="Menu",
        prompt_quit="Quit",
        prompt_go_back="Go Back",
        parent: "Menu|None" = None,
    ):
        from .items import BaseItem

        self.prompt = prompt
        self.prompt_quit = prompt_quit
        self.prompt_go_back = prompt_go_back
        self.items: List[BaseItem] = []
        self.parent = parent

    def run(self):

        while True:

            print()
            print(self.prompt)

            index = 0

            for index, item in enumerate(self.items, start=1):
                print(f"{index}: {item.label}")

            if self.parent:
                index += 1
                print(f"{index}: {self.prompt_go_back}")

            index += 1
            print(f"{index}: {self.prompt_quit}")

            try:
                choice = int(input("> ").strip()) - 1

                if 0 <= choice < len(self.items):
                    self.items[choice].exec()
                    continue

                elif self.parent and choice == len(self.items):
                    break

                exit(0)

            except Exception as e:
                print(f"Error: {e}")
                continue
