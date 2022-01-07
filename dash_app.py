import math

import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import pandas as pd
import dash_table
from dash import callback_context
import json

PAGE_SIZE = 1

df = pd.read_json('https://isod.ee.pw.edu.pl/isod-portal/wapi?q=dissertations_offers&orgunit=ISEP&fromrow=10&maxrows=4&active=true&format=json&lang=en&datefrom=23.02.2010', orient="records")

df = pd.DataFrame(df['list'].to_list(), columns=list(df['list'][1].keys()))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

component_buttons_lst = []
for button in ['First', 'Previous', 'Next', 'Last']:
    component_buttons_lst.append(html.Button(button, id=button, n_clicks=0))

current_page = 0


def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe
        ]) for i in range(current_page*PAGE_SIZE, current_page*PAGE_SIZE+PAGE_SIZE)]
    )


app.layout = html.Div(children=[
    html.H4(children='Paging table in Dash'),
    html.Div(id='table', children=generate_table(df)),
    html.Div(id='paging-component', children=component_buttons_lst)
])


@app.callback(
    Output('table', 'children'),
    Input('First', 'n_clicks'),
    Input('Previous', 'n_clicks'),
    Input('Next', 'n_clicks'),
    Input('Last', 'n_clicks')
)
def update_table(first, prev, next, last):
    ctx = dash.callback_context
    btn_name = ctx.triggered[0]['prop_id'].split('.')[0]
    global current_page
    if btn_name == 'First' and first > 0:
        current_page = 0
    elif btn_name == 'Previous' and prev > 0:
        if current_page > 0:
            current_page -= 1
    elif btn_name == 'Next' and next > 0:
        if current_page*PAGE_SIZE+PAGE_SIZE < len(df):
            current_page += 1
    elif btn_name == 'Last' and last > 0:
        current_page = math.floor(len(df)/PAGE_SIZE) - 1
    return generate_table(df)


if __name__ == '__main__':
    app.run_server(debug=True)
