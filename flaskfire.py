from flask import Flask
from flask import render_template
from flask import request
from PIL import Image

from backend import simulate

from numpy import interp

import pandas as pd

from PIL import ImageDraw

import time

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
@app.route("/<name>")
def index(name=None):
    return render_template('fire_predictor_website.html', name=name)

@app.route("/predict",methods = ["POST", "GET"])
def predict_the_fire(name=None):
    output = request.form.to_dict()
    year = output["year"]
    real_year = int(year)-2022
    simulate(real_year)
    return render_template('fire_predictor_website.html', year = year)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port = 8080, debug=True)

