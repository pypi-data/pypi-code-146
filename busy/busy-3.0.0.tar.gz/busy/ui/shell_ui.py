from ..ui import UI


class ShellUI(UI):

    def confirmed(self, parsed, itemlist, verb):
        print('\n'.join([str(i[1]) for i in itemlist]))
        confirmed = input(f'{verb}? (Y/n) ').startswith('Y')
        if not confirmed:
            print("Not confirmed")
        return confirmed
