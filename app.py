import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from dash.dependencies import Input, Output

import data

'''
TODO: 
-Create venv
-Add an hourly reset feature and increment x axis in 30 seconds intervals. (Make sure graph is reset not just list)
-Add custom HTML: favicon, title, etc. Might be weird cause Dash has its own HTML thing going on
-Is it necessary to return layout in every period?
-Clean code
-Deploy using flask , docker , nginx on EC2. Should probably load own instance of flask into app.
'''


type = "BTC"
count = 0

def get_time():
    hour = str(dt.datetime.now().hour)
    minute = str(dt.datetime.now().minute)

    if int(minute) < 10:
        minute = "0"+minute

    return hour+":"+minute
    
bg_colour = '#e7e5e2'
sec_colour = '#38474e'
tick_colour = '#3ed5a0'

interval = 30 * 1000  # In milliseconds

x = []
y_btc = []


def data_type():

    y_btc.append(data.api_data()["btc_price"])
    x.append(((len(y_btc)-1)/2))


layout = go.Layout(title=type + '/ZAR',
                   titlefont={'family': 'MainFont',
                              'size': 36, 'color': sec_colour},
                   xaxis={'title': 'Time (Minutes)', 'tickangle': 45,
                          'color': sec_colour, "showticklabels": True, },
                   yaxis={'title': 'Price', 'color': sec_colour},
                   plot_bgcolor=bg_colour,
                   paper_bgcolor=bg_colour,
                   )


app = dash.Dash(__name__, static_folder='assets')
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

server = app.server


app.layout = html.Div(children=[

    html.Link(href='/assets/main.css', rel='stylesheet'),
    html.H1(children='Price', id="price"),
    html.H1(children='% Change', id="percent_change"),

    html.H2(children=get_time(), id="time"),
    dcc.Interval(
        id='interval-component',
        interval=interval,
        n_intervals=0
    ),
    dcc.Interval(
        id='title-time',
        interval=interval,
        n_intervals=1
    ),

    dcc.Graph(
        id='ticker',
        figure={
            'data': [
            ],
            'layout': [
                layout
            ]
        }
    ),
])


@app.callback(Output('ticker', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_output_heading(time):

    print(len(y_btc))

    if(len(y_btc) >= 120):  # Resets graph hourly
        x.clear()
        y_btc.clear()

        trace_btc = go.Scatter(
            x=[],
            y=[],
        )

    data_type()

    trace_btc = go.Scatter(
        x=x,
        y=y_btc,

        name='Price',
        line=dict(
            color=tick_colour,
            width=2,
        ),
    ),

    return{
        'data': trace_btc,
        'layout': layout,
    }


@app.callback(Output('price', 'children'),
              [Input('title-time', 'n_intervals')])
def updatePrice(time):
    latest_price = "R" + str(y_btc[-1])
    return latest_price


@app.callback(Output('percent_change', 'children'),
              [Input('title-time', 'n_intervals')])
def updateChange(time):
    change = round((((y_btc[-1] / y_btc[0]) - 1) * 100), 2)
    change = str(change) + "%"
    return change

@app.callback(Output('time', 'children'),
              [Input('title-time', 'n_intervals')])
def updateTime(time):
    time = get_time()
    return time


if __name__ == '__main__':
    app.run_server(debug=True, port=5300)
