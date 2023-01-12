import math

from fipper.types import (
    InlineKeyboardButton
)


class ToolBot(object):
    def HelpXd(
        self,
        page_number,
        allmodules,
        prefix
    ):
        rows = 4
        column = 2
        help_modules = []
        for mod in allmodules:
            if not mod.startswith("_"):
                help_modules.append(mod)
        help_modules = sorted(help_modules)
        modules = [
            InlineKeyboardButton(
                text="{}".format(
                    x.replace("_", " ").title(),
                ),
                callback_data="pluginlist-{}|{}".format(x, page_number),
            )
            for x in help_modules
        ]
        twins = list(zip(modules[::column], modules[1::column]))
        if len(modules) % column == 1:
            twins.append((modules[-1],))
        num_pages = math.ceil(len(twins) / rows)
        mod_page = page_number % num_pages
        if len(twins) > rows:
            twins = twins[
                mod_page * rows: rows * (mod_page + 1)
            ] + [
                (
                    InlineKeyboardButton(
                        text="❮❮",
                        callback_data="{}-prev({})".format(
                            prefix, mod_page
                        ),
                    ),
                    InlineKeyboardButton(
                        text="❯❯",
                        callback_data="{}-next({})".format(
                            prefix, mod_page
                        ),
                    ),
                )
            ]
        return twins
    
    
    async def PluginXd(
        self,
        cmd_help,
        modules: str
    ):
        try:
            module_data = []
            module_data.clear()
    
            for x, y in zip(
                cmd_help.get(modules)[1].keys(),
                cmd_help.get(modules)[1].values()
            ):
                module_data.append(
                    f"<b>CMD:</b> <code>{x}</code>\n<b>INFO:</b> <code>{y}</code>\n\n"
                )
            return module_data
        except Exception:
            return None
