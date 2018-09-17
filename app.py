import data
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from datetime import date


def today(): return date.today().day


day = today()


class now():
    now = day


type = "BTC"  # Either BTC or ETH
count = 0
bg_colour = '#e7e5e2'
sec_colour = '#38474e'
tick_colour = '#3ed5a0'

x = []
y_btc = []
y_eth = []


def data_type():

    y_btc.append(data.api_data()["btc_price"])
    x.append(data.api_data()["Timestamp"])


layout = go.Layout(title=type + '/ZAR',
                   titlefont={'family': 'MainFont',
                              'size': 36, 'color': sec_colour},
                   xaxis={'title': 'Time', 'tickangle': 45,
                          'color': sec_colour, "showticklabels": False, },
                   yaxis={'title': 'Price', 'color': sec_colour},
                   plot_bgcolor=bg_colour,
                   paper_bgcolor=bg_colour,
                   )


app = dash.Dash(__name__, static_folder='assets')
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.layout = html.Div(children=[
    html.Link(href='/assets/main.css', rel='stylesheet'),
    html.H1(children='Price', id="price"),
    html.H1(children='% Change', id="percent_change"),

    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Interval(
        id='title-time',
        interval=5 * 1000,  # in milliseconds
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
    )
])


@app.callback(Output('ticker', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_output_heading(time):
    today_day = now().now

    if(today_day != today()):
        today_day = today()
        x.clear()
        y.clear()

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


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True, port=5300)
