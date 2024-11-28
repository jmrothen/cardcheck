import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Enter some text:"),
    dcc.Input(id='text-input', type='text', placeholder='Type here', style={'marginRight': '10px'}),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-text')
])


# Define callback to update the output text
@app.callback(
    Output('output-text', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('text-input', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        return f'You entered: {value}'
    return ""


if __name__ == '__main__':
    app.run_server(debug=True)
