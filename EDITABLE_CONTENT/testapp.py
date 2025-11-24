import dash

app = dash.Dash(__name__)
server = app.server
app.layout = dash.html.Div("Hello, this is a test app for EDITABLE_CONTENT.")

app.run(host='0.0.0.0', port=8080, debug=True)