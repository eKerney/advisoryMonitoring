
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk 
from dataminr import *
from droneData import *
pd.options.mode.chained_assignment = None  # default='warn'

### MAIN APP FLOW
# page config
st.set_page_config(layout="wide")
st.markdown(""" <style>#MainMenu {visibility: hidden;}footer {visibility: hidden;}</style> """, unsafe_allow_html=True)
# sliders and widgets

drones =  pdk.Layer('ScatterplotLayer', data=getFlights(),get_position='[lon, lat]', 
    get_fill_color=[100,100,100], 
    get_radius=70, auto_highlight=True,opacity=0.4, stroked=True, )

def changeStatus():
    st.write(f'<h1 style="text-align:center;margin-top:-70px;">DATAMINR SUPERBOWL ALERTS</h1>', unsafe_allow_html=True)
    st.write(f'<h5 style="text-align:center;margin-top:-10px;">Selected Alert: {alert}</h5>', unsafe_allow_html=True)
    global viewState 
    viewState = pdk.ViewState(latitude=match['lat'].iloc[0], longitude=match['lon'].iloc[0], bearing=33, pitch=40, zoom=13,)
    st.session_state.active = True
    st.pydeck_chart(pdk.Deck(
     map_style='road',
     initial_view_state=viewState,
     layers=[scatter, drones],
     tooltip=TOOLTIP_TEXT
 ))

dataminr = DATAMINR()
dataminr.getLists()
dataminr.getAlerts(30)
data = dataminr.getDF()

dfMap = data[['lat', 'lon', 'alertId', 'eventTime','caption','relatedTerms','eventLocation.name','headerLabel','dateTime']]
dfMap2 = data[['lat', 'lon']]
# hex =  pdk.Layer('HexagonLayer', data=getFlights(),get_position='[lon, lat]', get_fill_color=[200, 30, 0],
#              extruded=True, elevation_scale=50, auto_highlight=True, opacity=0.2, coverage=1, elevation_range=[10, 1000])

scatter =  pdk.Layer('ScatterplotLayer', data=dfMap,get_position='[lon, lat]', 
    get_fill_color=['headerLabel == "Urgent" ? 250 : 250', 'headerLabel == "Urgent" ? 0 : 150', 0], 
    get_radius='headerLabel == "Urgent" ? 600 : 300', pickable=True, auto_highlight=True,opacity=0.5, stroked=True, )

TOOLTIP_TEXT = {"html": "{caption} <br /> {eventLocation.name} <br /> Status: {headerLabel}<br /> UNIX Timestamp: {eventTime} <br /> DateTime: {dateTime}<br /> alertId: {alertId}"}
#   get_fill_color=[200, 'headerLabel == "Urgent" ? 0 : 200', 0, 160],
#dateTimes = dt.datetime.fromtimestamp(1644516042)

dataList = data[['caption']]
#st.sidebar.write(dataList)
alert = st.sidebar.selectbox('CHOOSE ALERT', dataList, on_change=changeStatus)

match = data[data.caption.str.startswith(alert)]
keyList = ['caption','dateTime','eventLocation.name','alertType.name','post.link','alertId','lat', 'lon', 'relatedTerms',]


for k in keyList:
    st.sidebar.write(k, ': ', match[k].iloc[0])

# One of ‘light’, ‘dark’, ‘road’, ‘satellite’,

if 'active' not in st.session_state:
    st.write(f'<h1 style="text-align:center;margin-top:-70px;">DATAMINR SUPERBOWL ALERTS</h1>', unsafe_allow_html=True)
    st.write(f'<h5 style="text-align:center;margin-top:-10px;">Selected Alert: {alert}</h5>', unsafe_allow_html=True)
    viewState = pdk.ViewState(latitude=33.98, longitude=-118.37, bearing=33, pitch=40, zoom=10,)
    st.session_state.active = False
    st.pydeck_chart(pdk.Deck(
        map_style='road',
        initial_view_state=viewState,
        layers=[scatter, drones],
        tooltip=TOOLTIP_TEXT
    ))
    #st.write(deckMap)

st.write('---')
st.write('Raw Data')
st.write(data)


