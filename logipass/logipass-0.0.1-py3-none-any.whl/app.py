""" This file contains the implementations of web application. """
from flask import Flask, render_template, request
from logipass.main import password_gen

app = Flask(__name__, static_folder="static")


@app.route("/", methods=["GET", "POST"])
def my_func():
    """ Executes the password generator function on clicking
    the generate button

    Returns:
        renders template index.html with password
    """
    if request.method == "POST":
        output = password_gen(password_length=12)
        return render_template("index.html", output=output)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)
