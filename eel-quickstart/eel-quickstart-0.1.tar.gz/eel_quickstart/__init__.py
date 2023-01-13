def create_main(n1="web"):
    with open("./main.py", "w+") as mainpy:
        mainpy.write(
            f"""import eel
eel.init('{n1}')
eel.start('index.html')"""
        )
        mainpy.close()

def create_web(n1="web"):
    from os import mkdir
    mkdir(f"./{n1}")
    with open(f"./{n1}/index.html", "w+") as indexhtml:
        indexhtml.write(
            """
<h1>Hello Eel</h1>
            """
        )
        indexhtml.close()
