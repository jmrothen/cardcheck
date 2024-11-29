import dash


from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv('db/collection_fixed.csv')

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Does rack have this card", style={'textAlign': 'center', 'color': '#4CAF50'}),

    dcc.Input(
        id='input-text',
        type='text',
        placeholder='Enter the card you want to find',
        debounce=False,
        value=''
    ),
    html.Hr(),
    dcc.Dropdown(
        id='drop-down',
        options=[],
        searchable=False,
        placeholder='Select an option...'
    ),
    html.Hr(),
    html.Div(id='results')
    # Future; I'd like this area to populate with a little table of the relevant data points that or just populate
    # with the photo of card, with sub text about if its in deck/not, the printing, quantity,  for each printing



    # IDEA table, where rows can be selected (maybe 70% width) If only one row, auto select selected row will
    # populate the right side of screen with a photo of the card, and other info as needed (maybe 30% width) will be
    # based on scryfall api call
])


@app.callback(
    Output('drop-down','options'),
    Input('input-text', 'value')
)
def update_suggestions(input_text):
    if input_text is None or input_text == '':
        return [{'label': name, 'value': name} for name in df['name'].unique()]

    # Find the closest matches (filter based on input text)
    matched_options = [name for name in df['name'].unique() if input_text.lower() in name.lower()]

    # Return the options and set the dropdown value to None initially
    return [{'label': match, 'value': match} for match in matched_options]


# Callback to display the selected item after selection
@app.callback(
    Output('results', 'children'),
    Input('drop-down', 'value')
)
def display_selected_item(selected_value):
    if selected_value:
        return f"Ye"
    return "No"


if __name__ == '__main__':
    app.run_server(debug=True)


