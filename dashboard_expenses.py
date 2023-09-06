from dash import dash, html, dcc, Input, Output
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import date
import plotly.express as px

#Read the data
df=pd.read_csv(r"D:\00_BACKUP_BY_DRIVE\Bank_expense_analysis\expenses.csv")

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div([
    html.H1('Descriptive Analyses of Expenses', style={'textAlign': 'center', 'color': '#503D36','childrennt-size': 40}),
    html.Div([

        html.Div([
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=df["date"].min(),
                max_date_allowed=df["date"].max(),
                start_date=df["date"].min(),
                end_date=df["date"].max()),
            html.Div([
                html.Div([
                    html.H2('Select Year:', style={'margin-right': '2em'})
                    ]),
                dcc.Dropdown(
                    id='year-drop-down',
                    options=df['year'].unique(),
                    #value="2022",
                    multi=False,
                    placeholder='Select a year',
                    style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}
                    )], style={'display':'flex'})
            ]),
            
            dcc.Dropdown(
                id='month-drop-down',
                options=df['month'].unique(),
                value=df["month"].unique(),
                multi=False,
                placeholder='Select month(s)'
            ),
            dcc.Dropdown(
                id='day-drop-down',
                options=df['day'].unique(),
                value=df["day"].unique(),
                multi=False,
                placeholder='Select day(s)'
            ),
        ],style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='label-drop-down',
                options=np.sort(df['label'].unique()),
                value="Grocery",
                
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='crossfilter-yaxis-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            ),
            html.Br(),
            dcc.Slider(
                df['year'].min(),
                df['year'].max(),
                step=None,
                id='slider',
                value=df['year'].max(),
                marks={str(year): str(year) for year in df['year'].unique()}
            )], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
            html.Div([], id="graph")
            ], style={'padding': '10px 5px'})




@app.callback(Output(component_id="graph", component_property="children"),
             Input(component_id="year-drop-down", component_property="value"),
             Input(component_id="label-drop-down", component_property="value"))
def get_pie_chart(year, label):
    chart_df = df.loc[(df["debit_credit"]=="Debit") & (df["year"] ==year) & (df["label"] == label)].groupby(["day"])[["amount"]].sum()
    fig= px.pie(data_frame=chart_df, values="amount")
    return dcc.Graph(figure=fig)


if __name__ == '__main__':
    app.run_server()