import wezel

def dicom(parent): 

    wezel.actions.folder.all(parent.menu('File'))
    wezel.actions.edit.all(parent.menu('Edit'))
    wezel.actions.view.all(parent.menu('View'))
    wezel.actions.filter.all(parent.menu('Filter'))
    wezel.actions.segment.all(parent.menu('Segment'))
    wezel.actions.transform.all(parent.menu('Transform'))
    wezel.actions.about.all(parent.menu('About'))

def test(parent):

    wezel.actions.folder.all(parent.menu('File'))
    wezel.actions.edit.all(parent.menu('Edit'))
    wezel.actions.view.all(parent.menu('View'))
    wezel.actions.about.all(parent.menu('About'))
    wezel.actions.test.all(parent.menu('Test'))

def about(parent): 

    wezel.actions.about.all(parent.menu('About'))

def hello_world(parent):

    subMenu = parent.menu('Hello')
    subMenu.action(wezel.actions.demo.HelloWorld, text="Hello World")
    subMenu.action(wezel.actions.demo.HelloWorld, text="Hello World (again)")

    subSubMenu = subMenu.menu('Submenu')
    subSubMenu.action(wezel.actions.demo.HelloWorld, text="Hello World (And again)")
    subSubMenu.action(wezel.actions.demo.HelloWorld, text="Hello World (And again!)")

    wezel.actions.about.all(parent.menu('About'))

def tricks(parent): 

    wezel.actions.folder.all(parent.menu('File'))
    wezel.actions.edit.all(parent.menu('Edit'))

    view = parent.menu('View')
    view.action(wezel.actions.demo.ToggleApp, text='Toggle application')
    view.action(wezel.actions.view.Image, text='Display image')
    view.action(wezel.actions.view.Series, text='Display series')
    view.action(wezel.actions.view.Region, text='Draw region')
    view.separator()
    view.action(wezel.actions.view.CloseWindows, text='Close windows')
    view.action(wezel.actions.view.TileWindows, text='Tile windows')

    tutorial = parent.menu('Tutorial')
    tutorial.action(wezel.actions.demo.HelloWorld, text="Hello World")

    subMenu = tutorial.menu('Submenus')
    subMenu.action(wezel.actions.demo.HelloWorld, text="Hello World (Again)")
    subMenu.action(wezel.actions.demo.HelloWorld, text="Hello World (And again)")

    subSubMenu = subMenu.menu('Subsubmenus')
    subSubMenu.action(wezel.actions.demo.HelloWorld, text="Hello World (And again again)")
    subSubMenu.action(wezel.actions.demo.HelloWorld, text="Hello World (And again again again)")

    wezel.actions.about.all(parent.menu('About'))
