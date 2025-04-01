import dash
from dash import html

app = dash.Dash(__name__)
server = app.server  # needed for deployment

app.layout = html.Div(children=[
    html.H1('FIFA Dashboard (Placeholder)', style={'textAlign': 'center'}),
    html.P('Your full Dash app will go here.')
])

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=10000)
