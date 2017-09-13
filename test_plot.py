import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from coinmarketcap import Market

def write_prices(timescale):

    coinmarketcap = Market()
    currencies = ['ARDOR','basic-attention-token','IOTA','LISK','NEM']
    delta_price = list()
    colors = list()
    all_col = ['r','g']

    for icurr in currencies:

        val = float(coinmarketcap.ticker(icurr, limit=3, convert='USD')[0][timescale])
        delta_price.append(val)
        colors.append(all_col[int(val>0)]) 

    return delta_price, colors

app = dash.Dash()

df = pd.read_csv('output/prices.csv')
available_indicators = ['percent_change_1h','percent_change_24h','percent_change_7d']
currencies = list(df.columns.values)[1:]

app.layout = html.Div([
    html.Div([

        html.Div([
            
            dcc.Graph(id='abc',
            figure={
            
            'layout': {
                'title': 'Percent change'
                }
            }),
            
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=available_indicators[0]
            ),
        ],
        style={'width': '30%', 'display': 'inline-block'}),
    ]),
])

@app.callback(
    dash.dependencies.Output('abc', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value')])

def update_graph(xaxis_column_name):

    prices, colors = write_prices(xaxis_column_name)

    return {
            'layout': {
                'title': 'Percent change',
                'height':'300',
                'margin': {'l': 80, 'r': 80, 't': 50, 'b': 40},
                'yaxis': {'title': 'Change [in %]'},
            },
                
            'xaxis': dict(
                title='Change [in %]',
            ),

            'data': [go.Bar(
                x=currencies,
                y=prices,
                width=0.4,
        
                marker=dict(
                    color='rgba(75, 125, 0, 0.6)',
                    line=dict(
                        color='rgba(50, 100, 0, 0.6)',
                        width=3
                    )
                )
            )]
    }
#fig = go.Figure(data=data, layout=layout)
app.css.append_css({'external_url': 'style.css'})

if __name__ == '__main__':
    app.run_server(debug=True)