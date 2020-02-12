import requests, json
import io
import time
import datetime
from flask import Flask, render_template, Response, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, create_engine

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG

app = Flask(__name__)
app.debug = True
APIurl = 'http://127.0.0.1:8001/'
numOfPoints = 20


def createPlot(df2plot):
    x = list(df2plot['time'])
    x = [datetime.datetime.strptime('-'.join(i.split('T')).split('.')[0], "%Y-%m-%d-%H:%M:%S") for i in x]
    y = list(df2plot['value'])
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, y)
    axis.tick_params(axis = 'x', rotation = 30)
    xFormat = mdates.DateFormatter('%H:%M:%S')
    axis.xaxis.set_major_locator(plt.MaxNLocator(10))
    axis.xaxis.set_major_formatter(xFormat)
    output = io.BytesIO()
    return fig, output


@app.route("/index/")
def index():
    response = requests.get(APIurl + 'getIDs')
    df = pd.read_json(response.text)
    data = df['hostname'].unique()
    return render_template("index.html",data=data)


@app.route("/index/host-<name>")
def showHostIds(name):
    response = requests.get(APIurl + 'getIDs')
    df = pd.read_json(response.text)
    allIds = df.loc[df['hostname']==name][['hostname','id','metric']]
    idList = allIds['id'].values.tolist()
    return render_template("displayIDs.html",data = allIds.values.tolist(), idList = idList)


@app.route("/index/idvalue-<int:id>")
def viewID(id):
    return render_template("idPlot.html",idList = id)


@app.route("/numberOfDataPoints-<int:id>", methods=['POST'])
def hello(id):
    global numOfPoints
    myvariable = request.form.get("timeDropdown")
    numOfPoints = myvariable
    return redirect("/index/idvalue-{}".format(id))


@app.route("/idvalue-<int:id>.svg")
def plot_png(id):
    response = requests.get(APIurl + 'getData?id={}&nVals={}'.format(id,10))
    data = pd.read_json(response.text)
    fig, output = createPlot(data)

    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


@app.route("/idvalueExpand-<int:id>.svg")
def expand_png(id):
    response = requests.get(APIurl + 'getData?id={}&nVals={}'.format(id,numOfPoints))
    data = pd.read_json(response.text)
    fig, output = createPlot(data)

    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


if __name__ == '__main__':

    import webbrowser
    app.run(port='8002')
