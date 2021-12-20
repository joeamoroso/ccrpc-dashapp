# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 15:09:10 2021

@author: joe.amoroso

A script to summarize SE Data for the CCRPC regional travel demand model.

Inputs: SE Data CSV files

Outputs: Plotly HTML map

"""
import pandas as pd
import json
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
# =============================================================================
# Read in SE Data CSVs files
# =============================================================================


se_2015 = pd.read_csv('Data/2015/LandUse_2015.csv')[['TAZ', 'HH_IncludingGQ', 
                                                'Commercial', 'Industrial',
                                                'Institutional', 'K12',
                                                'Retail', 'Special_Commercial',
                                                'Special_Retail']]
se_2020 = pd.read_csv('Data/2020/LandUse_2020.csv')[['TAZ', 'HH_IncludingGQ', 
                                                'Commercial', 'Industrial',
                                                'Institutional', 'K12',
                                                'Retail', 'Special_Commercial',
                                                'Special_Retail']]
se_2030 = pd.read_csv('Data/2030/LandUse_2030.csv')[['TAZ', 'HH_IncludingGQ', 
                                                'Commercial', 'Industrial',
                                                'Institutional', 'K12',
                                                'Retail', 'Special_Commercial',
                                                'Special_Retail']]
se_2050 = pd.read_csv('Data/2050/LandUse_2050.csv')[['TAZ', 'HH_IncludingGQ', 
                                                'Commercial', 'Industrial',
                                                'Institutional', 'K12',
                                                'Retail', 'Special_Commercial',
                                                'Special_Retail']]
# Add Years # 
se_2015['Year'] = 2015
se_2020['Year'] = 2020
se_2030['Year'] = 2030
se_2050['Year'] = 2050

# Add Total Employment # 
se_2015['Total Employment'] = se_2015.Commercial + se_2015.Industrial + \
                              se_2015.Institutional + se_2015.Retail + \
                              se_2015.Special_Retail + se_2015.Special_Commercial

se_2020['Total Employment'] = se_2020.Commercial + se_2020.Industrial + \
                              se_2020.Institutional + se_2020.Retail + \
                              se_2020.Special_Retail + se_2020.Special_Commercial

se_2030['Total Employment'] = se_2030.Commercial + se_2030.Industrial + \
                              se_2030.Institutional + se_2030.Retail + \
                              se_2030.Special_Retail + se_2030.Special_Commercial

se_2050['Total Employment'] = se_2050.Commercial + se_2050.Industrial + \
                              se_2050.Institutional + se_2050.Retail + \
                              se_2050.Special_Retail + se_2050.Special_Commercial

dat = pd.concat([se_2015, se_2020, se_2030, se_2050])

# Drop external stations # 
dat = dat.query('TAZ < 961')


# Make Radio Button list #
dat.rename(columns={'HH_IncludingGQ': 'Total Households (Including GQ)'}, \
           inplace=True)

# =============================================================================
# Read in GEOJSON of CCRPC Model 
# =============================================================================
# read json
with open('Data/GIS/CCPRC_TAZ.geojson') as f:
  vt_taz = json.load(f)
  

token = open("Data/.mapbox_token").read()


app = dash.Dash(__name__)
server = app.server
app.title('CCPRC Land Use')

land_use = ["Total Households (Including GQ)", "Total Employment"]

app.layout = html.Div([
    html.H1(children='CCPRC Land Use'),
    html.P("Land Use Variable:"),
    dcc.RadioItems(
        id='radio_button', 
        options=[{'label': k, 'value': k} for k in land_use],
        value=land_use[0]
    ,
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="choropleth"),
])

@app.callback(
    Output("choropleth", "figure"), 
    [Input("radio_button", "value")])
def display_choropleth(value):
    fig = px.choropleth_mapbox(
        dat, geojson=vt_taz, color=value,
        locations="TAZ", featureidkey="properties.TAZ",
        animation_frame='Year',
        color_continuous_scale='Oranges',
        mapbox_style='open-street-map',
        opacity = 0.7,
        center={"lat": 44.4, "lon": -73.2}, zoom=10)
    
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_accesstoken=token)
    

    return fig

if __name__ == '__main__':
    app.run_server()









