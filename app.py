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
        # JSON file
        f = open(f'./static/db/companyInfo/{stock}.json', "r")
        # Reading from file
        data = json.loads(f.read())
        # print(type(data),data['sector']['0'])
        max = data['fiftyTwoWeekHigh']['0']
        min = data['fiftyTwoWeekLow']['0']
        symbol = stock
        logo = data['logo_url']['0']
        info = {"a52high": max, "a52low": min,
                "shortName": data['longName']['0'] , "symbol": symbol,"logo":logo,"about":data['longBusinessSummary']['0'],
                "fullTimeEmployees":data['fullTimeEmployees']['0'],
                "city":data['city']['0'],
                "website":data['website']['0'],
                "phone":data['phone']['0'],"sector":data['sector']['0'],
                }
        tableinfo=['grossProfits','totalCash','totalDebt','totalRevenue','totalCashPerShare','revenuePerShare','bookValue','priceToBook','marketCap','averageVolume']
        for i in tableinfo:
            info[i]=data[i]['0']
        return json.dumps(info)

    elif endpoint == "fetchListOfStocks":
        df = pd.read_csv("./static/db/list_500.csv")
        companyName=(df['Company Name']).to_list()
        symbol = (df['Symbol']).to_list()
        listOf500 = {"symbol":symbol,
        "companyName":companyName
        }
        return json.dumps(listOf500)

    else:
        return "Bad endpoint", 400

# Return the JSON data for the Plotly graph


def gm(stock):
    # Create a line graph
    df = pd.read_csv(f"./static/nifty_500_data/{stock}.csv")
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

@app.route('/fetchListOfStocks')
def fetchListOfStocks():
    df = pd.read_csv("./static/db/list_500.csv")
    info=df.Industry+"("+df.Symbol+")"
    symbol = df.Symbol
    listOf500 = {"info":1,
    "info2":2,
    # "symbol":symbol
    }
    return json.dumps(listOf500)

if __name__ == "__main__":
    app.run(debug=True)
