import webbrowser
import wezel


def all(parent):

    parent.action(About, text='Wezel', icon=wezel.icons.question_mark) 


class About(wezel.Action):

    def run(self, app):
        webbrowser.open("weasel.pro")
