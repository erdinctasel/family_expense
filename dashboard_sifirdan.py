from dash import dash, html, dcc, Input, Output, dash_table
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import date
import plotly.express as px

#Read the data
df=pd.read_csv(r"D:\00_BACKUP_BY_DRIVE\Bank_expense_analysis\expenses.csv")

# Create a dash application
app= dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add a html.Div and core input text component
# Finally, add graph component.

app.layout = html.Div([
    html.H1('Descriptive Analysis of Expenses in the Netherlands',style={'textAlign':'center'}),
    html.Div([
        html.Div([
            dcc.Dropdown(id='year-drop-down',options=df["year"].unique(), value=2022,
                         multi=False,placeholder='Select a Year', style={'width':'100%','padding':'3px', 'text-align-last' : 'center'}),
            dcc.Dropdown(id='label-drop-down',options=df["label"].unique(), value=["Grocery", "Turk market"],
                         multi=True,placeholder='Select a Label',style={'width':'100%','padding':'3px', 'text-align-last' : 'center'}),
            dcc.Dropdown(id='month-drop-down',options=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
                         multi=False,placeholder='Select a Month',style={'width':'100%','padding':'3px', 'text-align-last' : 'center'}),
            dcc.Dropdown(id='day-drop-down',options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                         multi=False,placeholder='Select a Day',style={'width':'100%','padding':'3px', 'text-align-last' : 'center'}),

        ], style={'display': 'flex','width':'100%'}),

        #dash_table.DataTable(data=df.to_dict('records'), page_size=10,column_selectable=True),
        
        html.Div([
            
            html.Div([],id='plot-1'),  
            html.Div([],id='plot-2')
                      
        ], style={'display': 'flex','textAlign':'center'}),
     

    ]),  

])

@app.callback([Output(component_id="plot-1",component_property="children"),
               Output(component_id="plot-2",component_property="children")],
              [Input(component_id="year-drop-down",component_property="value"),
               Input(component_id="label-drop-down",component_property="value")])

def get_graph(year,label):
    label_txt = ""
    for i in range(0,len(label)):
        if i < (len(label)-1):
            label_txt = label_txt + label[i] + "|"
            print(label_txt)
        else:
            label_txt += label[i]
        print(label[i])
        print(label_txt)
    
    print(label)
    df_query=df.loc[(df["debit_credit"]=="Debit") & (df["year"]==year) & (df["label"].str.contains(label_txt,case=False))].groupby(["month"])[["month","amount"]].sum("amount")
    bar_data=df_query.reset_index().sort_values(by="amount",ascending=False)
    print(bar_data)
    
    bar_fig= px.bar(bar_data,x="month",y="amount", title=label_txt + " Expenses in "+ str(year))

    chart_df = df.loc[(df["debit_credit"]=="Debit") & (df["year"] == year) & (df["label"].str.contains(label_txt,case=False))].groupby(["day"])[["amount"]].sum()
    pie_fig = px.pie(chart_df.reset_index(),values= "amount", names="day", title= label_txt + " Expenses according to days in "+ str(year))
    
    

    return [dcc.Graph(figure=bar_fig),dcc.Graph(figure=pie_fig)]

if __name__ == '__main__':
    app.run_server()