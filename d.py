from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = px.data.iris()

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("Analysis of Iris data using scatter matrix"),
        dcc.Dropdown(
            id="dropdown",
            options=["sepal_length", "sepal_width", "petal_length", "petal_width"],
            value=["sepal_length", "sepal_width"],
            multi=True,
        ),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(
    Output("graph", "figure"),
    Input("dropdown", "value"),
)
def update_charts(dims):
    fig = px.scatter_matrix(df, dimensions=dims, color="species")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)