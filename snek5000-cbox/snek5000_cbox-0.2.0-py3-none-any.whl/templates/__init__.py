import jinja2

loader = jinja2.ChoiceLoader(
    [
        jinja2.PackageLoader("snek5000_cbox", "templates"),
        jinja2.PackageLoader("snek5000", "resources"),
    ]
)

env = jinja2.Environment(
    loader=loader,
    undefined=jinja2.StrictUndefined,
)

box = env.get_template("box.j2")
makefile_usr = env.get_template("makefile_usr.inc.j2")
size = env.get_template("SIZE_cbox.j2")
