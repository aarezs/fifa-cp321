import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
from io import StringIO

# Create the dataset
data = """Year,Host Country,Winner,Runner-Up
1930,Uruguay,Uruguay,Argentina
1934,Italy,Italy,Czechoslovakia
1938,France,Italy,Hungary
1950,Brazil,Uruguay,Brazil
1954,Switzerland,Germany,Hungary
1958,Sweden,Brazil,Sweden
1962,Chile,Brazil,Czechoslovakia
1966,England,England,Germany
1970,Mexico,Brazil,Italy
1974,Germany,Germany,Netherlands
1978,Argentina,Argentina,Netherlands
1982,Spain,Italy,Germany
1986,Mexico,Argentina,Germany
1990,Italy,Germany,Argentina
1994,United States,Brazil,Italy
1998,France,France,Brazil
2002,Japan,Brazil,Germany
2006,Germany,Italy,France
2010,South Africa,Spain,Netherlands
2014,Brazil,Germany,Argentina
2018,Russia,France,Croatia
2022,Qatar,Argentina,France
"""

df = pd.read_csv(StringIO(data))
df['Winner'] = df['Winner'].replace({'West Germany': 'Germany'})
df['Runner-Up'] = df['Runner-Up'].replace({'West Germany': 'Germany'})
wins_df = df.groupby('Winner').size().reset_index(name='Wins')

# App setup
app = dash.Dash(__name__)
server = app.server

winner_list = np.sort(df['Winner'].unique())
year_list = np.sort(df['Year'].unique())

dropdown_style = {
    'backgroundColor': '#1e1e1e',
    'color': 'white',
    'border': '1px solid #555'
}

app.layout = html.Div(style={'backgroundColor': '#1e1e1e', 'color': 'white'}, children=[
    html.H1("FIFA World Cup Finals Dashboard", style={'textAlign': 'center'}),

    html.Div([
        dcc.Graph(
            id='choropleth-map',
            figure=px.choropleth(
                wins_df,
                locations="Winner",
                locationmode='country names',
                color="Wins",
                hover_name="Winner",
                color_continuous_scale=px.colors.sequential.Plasma,
                title="World Cup Wins by Country"
            ).update_layout(
                paper_bgcolor='#1e1e1e',
                plot_bgcolor='#1e1e1e',
                font_color='white'
            )
        )
    ], style={'padding': '20px'}),

    html.Div([
        html.H3("Select a Country"),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': c, 'value': c} for c in winner_list],
            placeholder="Select a country",
            style=dropdown_style
        ),
        html.Div(id='country-wins-output', style={'paddingTop': '10px'})
    ], style={'padding': '20px'}),

    html.Div([
        html.H3("Select a Year"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(y), 'value': y} for y in year_list],
            placeholder="Select a year",
            style=dropdown_style
        ),
        html.Div(id='year-result-output', style={'paddingTop': '10px'})
    ], style={'padding': '20px'})
])

@app.callback(Output('country-wins-output', 'children'),
              [Input('country-dropdown', 'value')])
def update_country_wins(selected_country):
    if selected_country is None:
        return ""
    wins = wins_df[wins_df['Winner'] == selected_country]['Wins'].values[0]
    return f"{selected_country} has won the World Cup {wins} time(s)."

@app.callback(Output('year-result-output', 'children'),
              [Input('year-dropdown', 'value')])
def update_year_result(selected_year):
    if selected_year is None:
        return ""
    row = df[df['Year'] == selected_year]
    if not row.empty:
        return f"In {selected_year}, the winner was {row['Winner'].values[0]} and the runner-up was {row['Runner-Up'].values[0]}."
    return "Year not found."

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=10000)
