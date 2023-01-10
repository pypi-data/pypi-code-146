import wezel


def all(parent): 

    parent.action(HelloWorld, text="Hello World")


class HelloWorld(wezel.Action):

    def run(self, app):
        app.dialog.information("Hello World!", title = 'My first pipeline!')


