import streamlit as st
import requests
import json
import pprint
import pandas as pd
import datetime as dt

@st.cache
def getFlights():
    url = 'https://services5.arcgis.com/DzCDf9ACTMZgB0Wd/ArcGIS/rest/services/Insights_Data_UAS_Tracks_SuperBowl_View_STAGE/FeatureServer/0/query?where=1%3D1&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false&outFields=&returnHiddenFields=false&returnGeometry=true&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&f=pgeojson&token=zhZtzo6BWd543jQv4coY9u38P1bArhAdRSwlzmZjvStqeLTl-ql8qzXXD7v3MX7aq8FA-s10Rx3rjToiE-LpvpZjktN7nBkgouwKqynubR0rLCxE2rou8plavILyUHEVKLKx5C7O9RlXJ6A7kd4Oz3eKdOiQJtDeVryw8Vhm3pLXE6LfJdyTr5xevg5lTPf4jqlWQNW3do03Oy-NJh8q4POIsPrBMuphq2vED7Q5iXx9uXTwIC0YBW4Rw-Mw9SPV_X0jb__7S6zaIi56K5Pcwg..'
    response = requests.request("GET", url)
    data = json.loads(response.text)
    df = pd.json_normalize(data['features'])
    df['lon'] = df.apply(lambda d: (d['geometry.coordinates'][0]), axis=1)
    df['lat'] = df.apply(lambda d: (d['geometry.coordinates'][1]), axis=1)
    return df