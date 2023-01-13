from flask import Flask

import main
import pandas as pd

app = Flask(__name__)




@app.route('/<string:sentences>/')
def getSentences(sentences):
    return main.loadModel(sentences,True)


# @app.route('/', methods=["GET", "POST"])
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
    main.controller(1)
    df = pd.read_csv(main.path)
    main.trainModel(df,True)


app.debug = False
app.run()
