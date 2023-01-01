from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import yfinance as yf
import json

app = Flask(__name__)


# Define the root route
@app.route('/')
def index():

    return render_template('index.html')


@app.route('/ticker')
def stock():
    return render_template('stock.html')


@app.route('/callback/<endpoint>')
def cb(endpoint):
    if endpoint == "getStock":
        return gm(request.args.get('data'))
    elif endpoint == "getInfo":
        stock = request.args.get('data')
        df1 = pd.read_csv(f"./static/nifty_500_data/AWL.csv")
        max = df1['Close'].max()
        min = df1['Close'].min()
        info = {"a52high": max, "a52low": min,
                "shortName": "ntggg", "symbol": "hell"}
        return json.dumps(info)
    else:
        return "Bad endpoint", 400

# Return the JSON data for the Plotly graph


def gm(stock):
    # Create a line graph
    df = pd.read_csv("./static/ACC.csv")
    df = df.reset_index()
    max = (df['Open'].max())
    min = (df['Open'].min())
    range = max - min
    margin = range * 0.05
    max = max + margin
    min = min - margin
    fig = px.area(df, x='Date', y="Open",
                  hover_data=("Open", "Close", "Volume"),
                  range_y=(min, max), template="seaborn")

    # Create a JSON representation of the graph
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


if __name__ == "__main__":
    app.run(debug=True)
