import dash

from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv('db/collection_fixed.csv')

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Interactive DataFrame Table", style={'textAlign': 'center', 'color': '#4CAF50'}),
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        filter_action="native",  # Enables filtering on each column
        sort_action="native",    # Enables sorting by column
        sort_mode="multi",       # Allows multi-column sorting
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_header={
            'backgroundColor': '#4CAF50',  # Green background
            'color': 'white',  # White text color
            'fontWeight': 'bold',  # Bold text
            'textAlign': 'center',  # Center align header text
            'fontSize': '16px',  # Font size of header text
            'border': '1px solid #ddd',  # Border around header
        },
        style_cell={
            'padding': '10px',  # Add padding to cells
            'textAlign': 'center',  # Center-align the cell content
            'fontSize': '14px',  # Font size of the cell text
            'border': '1px solid #ddd',  # Border around cells
        },
        style_data_conditional=[
            {
                'if': {'state': 'active'},
                'backgroundColor': '#f4f4f9',  # Highlight active row
                'color': '#000000',
            },
            {
                'if': {'column_id': 'Score', 'filter_query': '{Score} > 90'},
                'backgroundColor': '#c8e6c9',  # Green background for high scores
                'color': '#388e3c',
            },
            {
                'if': {'column_id': 'Score', 'filter_query': '{Score} <= 90'},
                'backgroundColor': '#ffe0b2',  # Orange background for lower scores
                'color': '#f57c00',
            }
        ],
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
