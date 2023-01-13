from flask import Flask, request, render_template

import main
from flask_cors import CORS
app = Flask(__name__)
# CORS(app)


@app.route('/<string:sentences>/')
def getSentences(sentences):
    return main.loadModel(sentences)


@app.route('/', methods=["GET", "POST"])
#
# def gfg():
#     if request.method == "POST":
#        # getting input with name = fname in HTML form
#        sentences = request.form.get("sentences")
#        responses = main.loadModel(sentences)
#        return responses
#     return render_template("form.html")


@app.route('/train/')
def train():
    main.trainModel()


app.debug = False
app.run()
