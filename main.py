import data
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

type = "ETH"  # Either BTC or ETH

bg_colour = '#e7e5e2'
sec_colour = '#38474e'
tick_colour = '#3ed5a0'

x = []
y = []


def data_type(value=type):
    ticker_data = data.prices()

    if(type == "ETH"):
        y.append(ticker_data.ETH)
    if(type == "BTC"):
        y.append(ticker_data.BTC)


layout = go.Layout(title=type + '/ZAR',
                   titlefont={'family': 'MainFont',
                              'size': 36, 'color': sec_colour},
                   xaxis={'title': 'Time', 'tickangle': 45,
                          'color': sec_colour},
                   yaxis={'title': 'Revenue', 'color': sec_colour},
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
        interval=2 * 1000,  # in milliseconds
        n_intervals=0
    ),
    dcc.Interval(
        id='title-time',
        interval=2 * 1000,  # in milliseconds
        n_intervals=1
    ),

    dcc.Graph(
        id='ticker',
        figure={
            'data': [
            ],
            'layout': [
            ]
        }
    )
])


@app.callback(Output('ticker', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_output_heading(time):
    data_type()
    x.append(time)

    trace2 = go.Scatter(

        x=x,
        y=y,
        name='Money',
        line=dict(
            color=tick_colour,
            width=2,
        )),

    return{
        'data': trace2,
        'layout': layout
    }


@app.callback(Output('price', 'children'),
              [Input('title-time', 'n_intervals')])
def updatePrice(time):
    latest_price = "R" + str(y[-1])
    return latest_price


@app.callback(Output('percent_change', 'children'),
              [Input('title-time', 'n_intervals')])
def updateChange(time):
    change = round((((y[-1] / y[0]) - 1) * 100), 2)
    change = str(change) + "%"
    return change


if __name__ == '__main__':
    app.run_server(debug=True, port=5300)
