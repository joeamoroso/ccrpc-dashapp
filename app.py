# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 15:09:10 2021

@author: joe.amoroso

A script to summarize SE Data for the CCRPC regional travel demand model.

Inputs: SE Data CSV files

Outputs: Plotly Dash App 

"""
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import os
# =============================================================================
# Read in SE Data CSVs files
# =============================================================================
def preprocessdata():

    se_2015 = pd.read_csv('Data/2015/LandUse_2015.csv')[['TAZ', 'HH_IncludingGQ', 'HH',
                                                    'Accomodations','College_University',
                                                    'Commercial', 'Industrial',
                                                    'Institutional', 'K12',
                                                    'Retail', 'Special_Commercial',
                                                    'Special_Retail']]
    se_2020 = pd.read_csv('Data/2020/LandUse_2020.csv')[['TAZ', 'HH_IncludingGQ', 'HH',
                                                    'Accomodations','College_University',
                                                    'Commercial', 'Industrial',
                                                    'Institutional', 'K12',
                                                    'Retail', 'Special_Commercial',
                                                    'Special_Retail']]
    se_2030 = pd.read_csv('Data/2030/LandUse_2030.csv')[['TAZ', 'HH_IncludingGQ', 'HH',
                                                    'Accomodations','College_University',
                                                    'Commercial', 'Industrial',
                                                    'Institutional', 'K12',
                                                    'Retail', 'Special_Commercial',
                                                    'Special_Retail']]
    se_2050 = pd.read_csv('Data/2050/LandUse_2050.csv')[['TAZ', 'HH_IncludingGQ', 'HH',
                                                    'Accomodations','College_University',
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
    se_2015['Total Employment'] = se_2015.Accomodations + se_2015.College_University + \
                                  se_2015.Commercial + se_2015.Industrial + \
                                  se_2015.Institutional +se_2015.K12 + se_2015.Retail + \
                                  se_2015.Special_Retail + se_2015.Special_Commercial

    se_2020['Total Employment'] = se_2020.Accomodations + se_2020.College_University + \
                                  se_2020.Commercial + se_2020.Industrial + \
                                  se_2020.Institutional + se_2020.K12 + se_2020.Retail + \
                                  se_2020.Special_Retail + se_2020.Special_Commercial

    se_2030['Total Employment'] = se_2030.Accomodations + se_2030.College_University + \
                                  se_2030.Commercial + se_2030.Industrial + \
                                  se_2030.Institutional+ se_2030.K12 + se_2030.Retail + \
                                  se_2030.Special_Retail + se_2030.Special_Commercial

    se_2050['Total Employment'] = se_2050.Accomodations + se_2050.College_University + \
                                  se_2050.Commercial + se_2050.Industrial + \
                                  se_2050.Institutional + se_2050.K12 + se_2050.Retail + \
                                  se_2050.Special_Retail + se_2050.Special_Commercial

    # add Percent Change from 2015 for 2020-2050 SE data years # 
    # Drop external stations # 
    se_2015 = se_2015.query('TAZ < 961')
    se_2020 = se_2020.query('TAZ < 961')
    se_2030 = se_2030.query('TAZ < 961')
    se_2050 = se_2050.query('TAZ < 961')

    se_2015['HH Percent Change From 2015'] = 0
    se_2020 = se_2020.merge(se_2015[['TAZ', 'HH']], how='left', on='TAZ')
    se_2020['HH Percent Change From 2015'] = np.where(se_2020['HH_y'] > 0, round((se_2020['HH_x'] - se_2020['HH_y']) / se_2020['HH_y'] * 100, 1), 0)
    se_2020['HH Change From 2015'] = se_2020['HH_x'] - se_2020['HH_y']
    se_2030 = se_2030.merge(se_2015[['TAZ', 'HH']], how='left', on='TAZ')
    se_2030['HH Percent Change From 2015'] = np.where(se_2030['HH_y'] > 0,round((se_2030['HH_x'] - se_2030['HH_y']) / se_2030['HH_y'] * 100, 1), 0)
    se_2030['HH Change From 2015'] = se_2030['HH_x'] - se_2030['HH_y']
    se_2050 = se_2050.merge(se_2015[['TAZ', 'HH']], how='left', on='TAZ')
    se_2050['HH Percent Change From 2015'] = np.where(se_2050['HH_y'] > 0,round((se_2050['HH_x'] - se_2050['HH_y']) / se_2050['HH_y'] * 100, 1), 0)
    se_2050['HH Change From 2015'] = se_2050['HH_x'] - se_2050['HH_y']

    se_2015['Total Employment Percent Change From 2015'] = 0
    se_2020 = se_2020.merge(se_2015[['TAZ', 'Total Employment']], how='left', on='TAZ')
    se_2020['Total Employment Percent Change From 2015'] = np.where(se_2020['Total Employment_y'] > 0, round((se_2020['Total Employment_x'] - se_2020['Total Employment_y']) / se_2020['Total Employment_y'] * 100, 1), 0)
    se_2020['Total Employment Change From 2015'] = se_2020['Total Employment_x'] - se_2020['Total Employment_y']
    se_2030 = se_2030.merge(se_2015[['TAZ', 'Total Employment']], how='left', on='TAZ')
    se_2030['Total Employment Percent Change From 2015'] = np.where(se_2030['Total Employment_y'] > 0,round((se_2030['Total Employment_x'] - se_2030['Total Employment_y']) / se_2030['Total Employment_y'] * 100, 1), 0)
    se_2030['Total Employment Change From 2015'] = se_2030['Total Employment_x'] - se_2030['Total Employment_y']
    se_2050 = se_2050.merge(se_2015[['TAZ', 'Total Employment']], how='left', on='TAZ')
    se_2050['Total Employment Percent Change From 2015'] = np.where(se_2050['Total Employment_y'] > 0,round((se_2050['Total Employment_x'] - se_2050['Total Employment_y']) / se_2050['Total Employment_y'] * 100, 1), 0)
    se_2050['Total Employment Change From 2015'] = se_2020['Total Employment_x'] - se_2050['Total Employment_y']

    dat = pd.concat([se_2020, se_2030, se_2050])
    # Make Radio Button list #
    dat.rename(columns={'HH_x': 'Total Households (Excluding GQ)'}, \
               inplace=True)

    dat.to_csv('Data/dat.csv', index=False)

if not os.path.isfile('Data/dat.csv'):
    preprocessdata()

dat = pd.read_csv('Data/dat.csv')

# =============================================================================
# Read in GEOJSON of CCRPC Model 
# =============================================================================
# read json
with open('Data/GIS/CCPRC_TAZ.geojson') as f:
  vt_taz = json.load(f)

with open('Data/GIS/CCPRC_TAZ.geojson') as f:
    centroids = json.load(f)

lats = []
lons = []
labels = []

# Extract Lat/Long and TAZ from GEOJSON # 
for i in centroids['features']:
    cord = i['geometry']['coordinates']
    label = i['properties']['TAZ']
    labels.append(str(label))
    for j in cord:
        for k in j:
            lats.append(k[0][1])
            lons.append(k[0][0])

token = open("Data/.mapbox_token").read()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title ='CCRPC Land Use'

land_use = ["HH Percent Change From 2015", "Total Employment Percent Change From 2015"]

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1(children='CCRPC Land Use Visualizer'))),
    dbc.Row(dbc.Col(html.H3("Land Use Variable:"))),
    dbc.Row(dbc.RadioItems(
        id='radio_button', 
        options=[{'label': k, 'value': k} for k in land_use],
        value=land_use[0],


        labelStyle={'display': 'inline-block'}
    )),
    dbc.Row(
        dbc.Col(dcc.Graph(id="choropleth")))
],
style={"height": "100vh"})

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
        hover_name= 'TAZ',
        hover_data = ['HH Percent Change From 2015','Total Employment Percent Change From 2015',
                      'HH Change From 2015','Total Employment Change From 2015'],
        opacity = 0.6,
        center={"lat": 44.475959, "lon": -73.210382}, zoom=12,
        height =700)

    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_accesstoken=token)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)









