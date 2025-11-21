#!/usr/bin/env python
# coding: utf-8

# In[1]:


#4.Visualization. 
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import pymongo

myclient = pymongo.MongoClient("")  #put atlas db url
iotdb = myclient['add232iotdb']  # database name
temp_data = iotdb["humidity"]  # collection name
data_pnt = 15

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1('NoSQL Practices', style={'color': 'blue'}),
        html.H2('Demonstration for KIC students'),
        html.Div(
            [
                html.H1('Temperature Graph'),
                dcc.Graph(id="temp_graph"),
                html.H1('Humidity Graph'),
                dcc.Graph(id="humidity_graph"),
            ]
        ),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  
            n_intervals=0
        )
    ]
)


@callback(
    [Output('temp_graph', 'figure'), Output('humidity_graph', 'figure')],Input('interval-component', 'n_intervals'))
def update_temp_fig(n):
    try:
        
        data = list(temp_data.find())
        if len(data) > data_pnt:
            data = data[-data_pnt:]  

        
        filtered_data = [
            record for record in data 
            if 'time' in record and 'temperature' in record and 'humidity' in record #connect with mongodb data
        ]

       
        if filtered_data:
           
            data_frame = pd.DataFrame(filtered_data)

            data_frame.rename(columns={'time': 'time', 'temperature': 'temp', 'humidity': 'humidity'}, inplace=True)
            
            temp_fig = px.line(data_frame, x="time", y="temp", title='Temperature over Time')
            humidity_fig = px.line(data_frame, x="time", y="humidity", title='Humidity over Time')
        else:
            temp_fig = px.line(title='No valid data available')
            humidity_fig = px.line(title='No valid data available')

    except Exception as e:
        temp_fig = px.line(title='Error retrieving temperature data')
        humidity_fig = px.line(title='Error retrieving humidity data')
        print(f"Error: {e}")

    return temp_fig, humidity_fig


if __name__ == '__main__':
    app.run(debug=True)

 
 


# In[ ]:




