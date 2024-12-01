import dash
import pandas as pd
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from scryfall import get_sf_card, get_card_image

df = pd.read_csv('db/collection_fixed.csv')

available_binders = ['rares', 'commanders', 'artifacts', 'foreign', 'non basic lands', 'fancy basic lands',
                     'multicolored', 'white', 'blue', 'black', 'red', 'green']

df['available'] = (df['binder'].isin(available_binders))
df = df.sort_values(by='name')

visible_columns = ['name', 'set_code', 'foil', 'rarity', 'quantity', 'binder', 'available', 'language']

# Initialize Dash app
app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# App layout


app.layout = html.Div([
    html.H1("Rack Collection Search", style={'textAlign': 'center', 'color': '#4CAF50'}),

    # 1ST ROW:  DATA ENTRY
    html.Div([

        # TEXT ENTRY
        dcc.Input(
            id='input-text',
            type='text',
            placeholder='Enter the card you want to find',
            className='input-text',
            debounce=False,
            value=''
        )
        # ,

        # html.H3('matching names dropdown:', style={'color': 'darkgrey'})  ,

        # DROPDOWN ENTRY
        # dcc.Dropdown(
        #    id='drop-down',
        #    options=[],
        #    searchable=False,
        #    placeholder='Select an option...',
        #    className='drop-down'
        # )
    ],
        className='row'
    ),

    # 2ND ROW: TABLE AND IMAGE
    html.Div([

        # TABLE CONTAINER
        html.Div(

            # DASH TABLE
            dash_table.DataTable(
                id='table',
                columns=[{'name': col, 'id': col} for col in visible_columns],
                data=df.to_dict('records'),
                # filter_action="native",  # Enables filtering on each column
                sort_action="native",  # Enables sorting by column
                sort_mode="multi",  # Allows multi-column sorting
                style_table={"width": "100%"},
                row_selectable='single',
                cell_selectable=False,
                page_size=18,
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

        # IMAGE CONTAINER
        html.Div(

            # IMAGE
            html.Img(
                id='img',
                src='',  # '"https://via.placeholder.com/800x400",
                className='image',
                style={}
            ),
            className='image-container'
        )],
        className='row'
    ),

], className='big-container')


# ----------------------------------------------------------------------------------
# CALLBACKS


# DROP-DOWN SUGGESTION UPDATES
@app.callback(
    # Output('drop-down', 'options'),
    Output('table', 'data'),
    Output('table', 'selected_rows'),
    Input('input-text', 'value')
)
def update_suggestions(input_text):
    if input_text is None or input_text == '':
        return (  # [{'label': name, 'value': name} for name in df['name'].unique()],
            df.to_dict('records'), [])

    # Find the closest matches (filter based on input text)
    matched_options = [name for name in df['name'].unique() if input_text.lower() in name.lower()]
    data_out = df[df['name'].isin(matched_options)].copy().to_dict('records')

    # Return the options and set the dropdown value to None initially
    return (  # [{'label': match, 'value': match} for match in matched_options],
        data_out, [])


# Callback to update the image on the right based on selected row
@app.callback(
    Output('img', 'src'),
    Output('img', 'style'),
    Input('table', 'selected_rows'),
    Input('table', 'data')
)
def grab_selected_image(selected_rows, data):
    if not selected_rows:
        return '', {}
    target_row = data[selected_rows[0]]
    card_id = target_row['scryfall_id']
    new_style = {'width': '488px', 'height': '680px', 'border': '2x solid black'}
    return get_card_image(card_id, 'normal'), new_style


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
