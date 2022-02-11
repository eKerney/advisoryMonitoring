import streamlit as st
import requests
import json
import pprint
import pandas as pd
import datetime as dt

### DATAMINR API CLASS
# Create Dataminr object, must have client_id and client_secret to obtain key
class DATAMINR(object):

  def __init__(self):
    try:
      self.authURL = 'https://gateway.dataminr.com/auth/2/token'
      client_id = st.secrets.dataminr_id 
      client_secret = st.secrets.dataminr_secret 
      payload=(f'grant_type=api_key&client_id={client_id}&client_secret={client_secret}')
      headers = {'Content-Type': 'application/x-www-form-urlencoded'}
      response = requests.request("POST", self.authURL, headers=headers, data=payload)
      self.__auth = json.loads(response.text)
      print(self.__auth)
    except:
      print(f'COULD NOT AUTHENTICATE TO DATAMINR')

# get all watchlists and set current list id to retrieve alerts
  def getLists(self):
    try:
      self.listsURL = 'https://gateway.dataminr.com/account/2/get_lists'
      payload={}
      headers = {'Authorization': (f'dmauth {self.__auth["dmaToken"]}')}
      response = requests.request("GET", self.listsURL, headers=headers, data=payload)
      self.lists = (json.loads(response.text))['watchlists']['TOPIC']
      print('Dataminr Watchlists')
      # remove user interaction component
      #for i, l in enumerate(self.lists):
      #  print(f'{i} - {l["id"]} - {l["name"]} - {l["properties"]} - {l["type"]}')
      #index = int(input('Select List Index: '))
      self.activeList = self.lists[4]['id']
      print(f'activeList = {self.activeList}')
    except:
      print(f'COULD NOT RETRIEVE LISTS for {self}')

 # get alerts for list specified in getLists() 
  def getAlerts(self, numAlerts, toPrint=False):
    try:
      self.alertsURL = (f'https://gateway.dataminr.com/api/3/alerts?alertversion=14&lists={self.activeList}&num={numAlerts}')
      payload={}
      headers = {'Authorization': (f'dmauth {self.__auth["dmaToken"]}')}
      response = requests.request("GET", self.alertsURL, headers=headers, data=payload)
      self.alerts = json.loads(response.text)
      if toPrint != False:
        pp = pprint.PrettyPrinter(indent=2)
        for i, alert in enumerate(self.alerts['data']['alerts']):
          pp.pprint(alert)
    except:
      print(f'COULD NOT RETRIEVE ALERTS - TRY getLists() first - {self} ')

  def getGDF(self):
    try:
      df = pd.json_normalize(self.alerts['data']['alerts'])
      dfN = df.dropna(subset=['eventLocation.coordinates'])
      dfN['lat'] = dfN.apply(lambda d: (float(d['eventLocation.coordinates'][0])), axis=1)
      dfN['lon'] = dfN.apply(lambda d: (float(d['eventLocation.coordinates'][1])), axis=1)
      self.df = dfN
      self.gdf = gpd.GeoDataFrame(dfN, crs="EPSG:4326",geometry=gpd.points_from_xy(dfN.lon, dfN.lat))
      filter = input(f'Enter alert caption filter terms separated by | or ENTER for NONE: ')
      self.gdfFilter = self.gdf[self.gdf.caption.str.contains(filter, regex=True)]
      return self.gdfFilter.explore(marker_type='marker')
    except:
       print(f'COULD NOT CREATE GDF - TRY getAlerts() first - {self} ')
  
  # eliminating need for geopandas in streamlit, can map directly with df
  def getDF(self):
    try:
      df = pd.json_normalize(self.alerts['data']['alerts'])
      dfN = df.dropna(subset=['eventLocation.coordinates'])
      dfN['lat'] = dfN.apply(lambda d: (d['eventLocation.coordinates'][0]), axis=1)
      dfN['lon'] = dfN.apply(lambda d: (d['eventLocation.coordinates'][1]), axis=1)
      dfN['sliceTime'] = dfN.apply(lambda d: (int(str(d['eventTime'])[0:10])), axis=1)
      dfN['dateTime'] = dfN.apply(lambda d: (dt.datetime.fromtimestamp(d['sliceTime'])), axis=1) 
      #dfN['datTime'] = pd.to_datetime(dfN['sliceTime'])    
      self.df = dfN
      return self.df
    except:
       print(f'COULD NOT CREATE DF - TRY getAlerts() first - {self} ')
  


  
