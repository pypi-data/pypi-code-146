#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs


class Usage:

    def __init__(self):
        colors = Configs.colour
        color = colors()

        self.bold = color['bold']
        self.red = color['red']
        self.cyan = color['cyan']
        self.yellow = color['yellow']
        self.endc = color['endc']

    def help_short(self):
        """ Prints the short menu. """
        args = (
            f'Usage: {Configs.prog_name} [{self.yellow}OPTIONS{self.endc}] [{self.cyan}COMMAND{self.endc}] <packages>\n'
            f'\n  slpkg [{self.cyan}COMMAND{self.endc}] [update, upgrade, check-updates, configs]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [clean-logs, clean-tmp]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-b, build, -i, install, -d, download, -r, remove] <packages>\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-f, find, -w, view, -s, search, -e, dependees] <packages>\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-t, tracking] <packages>\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [--yes, --jobs, --resolve-off, --reinstall]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [--skip-installed, --full-reverse, --search]\n'
            "  \nIf you need more information please try 'slpkg --help'.")

        print(args)
        raise SystemExit()

    def help(self, status: int):
        """ Prints the main menu. """
        args = (
            f'{self.bold}USAGE:{self.endc} {Configs.prog_name} [{self.yellow}OPTIONS{self.endc}] '
            f'[{self.cyan}COMMAND{self.endc}] <packages>\n'
            f'\n{self.bold}DESCRIPTION:{self.endc} Packaging tool that interacts with the SBo repository.\n'
            f'\n{self.bold}COMMANDS:{self.endc}\n'
            f'  {self.red}update{self.endc}                        Update the package lists.\n'
            f'  {self.cyan}upgrade{self.endc}                       Upgrade all the packages.\n'
            f'  {self.cyan}check-updates{self.endc}                 Check for news on ChangeLog.txt.\n'
            f'  {self.cyan}configs{self.endc}                       Edit the configuration file.\n'
            f'  {self.cyan}clean-logs{self.endc}                    Clean dependencies log tracking.\n'
            f'  {self.cyan}clean-tmp{self.endc}                     Delete all the downloaded sources.\n'
            f'  {self.cyan}-b, build{self.endc} <packages>          Build only the packages.\n'
            f'  {self.cyan}-i, install{self.endc} <packages>        Build and install the packages.\n'
            f'  {self.cyan}-d, download{self.endc} <packages>       Download only the scripts and sources.\n'
            f'  {self.cyan}-r, remove{self.endc} <packages>         Remove installed packages.\n'
            f'  {self.cyan}-f, find{self.endc} <packages>           Find installed packages.\n'
            f'  {self.cyan}-w, view{self.endc} <packages>           View packages from the repository.\n'
            f'  {self.cyan}-s, search{self.endc} <packages>         Search and print packages from the repository.\n'
            f'  {self.cyan}-e, dependees{self.endc} <packages>      Show which packages depend.\n'
            f'  {self.cyan}-t, tracking{self.endc} <packages>       Tracking the packages dependencies.\n'
            f'\n{self.bold}OPTIONS:{self.endc}\n'
            f'  {self.yellow}--yes{self.endc}                         Answer Yes to all questions.\n'
            f'  {self.yellow}--jobs{self.endc}                        Set it for multicore systems.\n'
            f'  {self.yellow}--resolve-off{self.endc}                 Turns off dependency resolving.\n'
            f'  {self.yellow}--reinstall{self.endc}                   Upgrade packages of the same version.\n'
            f'  {self.yellow}--skip-installed{self.endc}              Skip installed packages.\n'
            f'  {self.yellow}--full-reverse{self.endc}                Full reverse dependency.\n'
            f'  {self.yellow}--search{self.endc}                      Search packages from the repository.\n'
            '\n  -h, --help                    Show this message and exit.\n'
            '  -v, --version                 Print version and exit.\n'
            '\nEdit the configuration file in the /etc/slpkg/slpkg.toml \n'
            "or run 'slpkg configs'.\n"
            'If you need more information try to use slpkg manpage.')

        print(args)
        raise SystemExit(status)

    def error_for_options(self, flags):
        """ Error messages for flags. """
        print(f'Usage: {Configs.prog_name} [{self.yellow}OPTIONS{self.endc}] '
              f'[{self.cyan}COMMAND{self.endc}] <packages>')
        print("Try 'slpkg --help' for help.\n")
        if flags:
            raise SystemExit(f"{self.red}Error:{self.endc} Got an unexpected extra option, "
                             f"please use: \n{self.yellow}'{', '.join(flags)}'{self.endc}")

        raise SystemExit(f"{self.red}Error:{self.endc} Got an unexpected extra option.")

