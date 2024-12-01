import dash

from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

df_safe = pd.read_csv('db/collection_fixed.csv')

df = df_safe[['name', 'set_code', 'foil', 'rarity', 'quantity', 'language']]

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div([
    html.H1("Does rack have this card", style={'textAlign': 'center', 'color': '#4CAF50'}),

    html.Div([
        dcc.Input(
            id='input-text',
            type='text',
            placeholder='Enter the card you want to find',
            className='input-text',
            debounce=False,
            value=''
        ),
        dcc.Dropdown(
            id='drop-down',
            options=[],
            searchable=False,
            placeholder='Select an option...',
            className='drop-down'
        )],
        className='row'
    ),

    html.Div([
        html.Div(
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in df.columns],
                data=df.to_dict('records'),
                # filter_action="native",  # Enables filtering on each column
                sort_action="native",  # Enables sorting by column
                sort_mode="multi",  # Allows multi-column sorting
                style_table={"width": "100%"},
                row_selectable='single',
                page_size=10,
                style_cell={
                    "textAlign": "left",
                    "padding": "10px",
                    "border": "1px solid #ddd",
                },
                style_header={
                    "backgroundColor": "#f4f4f4",
                    "fontWeight": "bold",
                    "border": "1px solid #ddd",
                },
                style_data_conditional=[
                    {
                        'if': {
                            'state': 'active'
                        },
                        'backgroundColor': '#c0c0c0',  # Slightly darker grey for active cell
                        'color': 'black',
                        'border': '1px solid black'
                    }
                ]
            ),
            className='table-container'
        ),
        html.Div(
            html.Img(
                src="https://via.placeholder.com/800x400",
                className='image'
            ),
            className='image-container'
        )],
        className='row'
    ),

    # html.Div(id='results')
    # Future; I'd like this area to populate with a little table of the relevant data points that or just populate
    # with the photo of card, with sub text about if its in deck/not, the printing, quantity,  for each printing

    # IDEA table, where rows can be selected (maybe 70% width) If only one row, auto select selected row will
    # populate the right side of screen with a photo of the card, and other info as needed (maybe 30% width) will be
    # based on scryfall api call
], className='big-container')


@app.callback(
    Output('drop-down', 'options'),
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


# Callback to handle selected row styling
@app.callback(
    Output('table', 'style_data_conditional'),
    Input('table', 'selected_rows')
)
def highlight_selected_rows(selected_rows):
    # Create base style for active cells
    if selected_rows is None:
        selected_rows = []

    active_cell_style = {
        'if': {
            'state': 'active'
        },
        'backgroundColor': '#c0c0c0',  # Slightly darker grey for active cell
        'color': 'black',
        'border': '1px solid black'
    }

    # Create styles for selected rows
    selected_rows_styles = [
        {
            'if': {
                'row_index': row_index
            },
            'backgroundColor': '#d0d0d0',  # Light grey for selected row
        }
        for row_index in selected_rows
    ]

    # Return the combined styles for active cell and selected rows
    return [active_cell_style] + selected_rows_styles


if __name__ == '__main__':
    app.run_server(debug=True)
