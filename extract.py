#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 22:43:38 2021

@author: nicolas
"""

import api
import airrohr
import folium
import os

from pandas import DataFrame
import matplotlib.pyplot as plt
import seaborn as sns

 
#Variables ################################################
# Modifiez ici la date et/ou le sensor (SDS011 pour avoir les mesures PM10 et PM2.5 des sds011)
date = "2021-01-09"
sensor = "SDS011"
###########################################################

#Constantes ###############################################
lat1,lon1 = 45.2433608,5.614488 #Point Nord Ouest
lat2,lon2 = 45.0899558,5.895916 #Point Sud Est
box1 = [lat1,lon1,lat2,lon2]

metro = [45.2496378,5.598292,45.0760708,5.90253]
voironnais = [45.3889537,5.45502,45.3015058,5.691215]
ra = [46.4848047,3.214603,44.5976102,6.9796573]
###########################################################

os.makedirs(date,exist_ok=True) #repertoire dans lequel sont sockées les infos, graphs, cartes etc...
os.chdir(date)

def doublon(liste):
    new_list = [] 
    for i in liste : 
        if i not in new_list: 
            new_list.append(i)
    return new_list


def extractJ(box=[45.3889537,5.45502,45.3015058,5.691215],sensor="SDS011",date="2021-01-05"):
    "Fonction pour extraire les résultats dans une box pour une date sous forme de dataframe"
    e = api.extractbox(box,sensor)
    sensors = doublon([i['sensor'] for i in e])
    l = [airrohr.Airrohr(sensor_id= i['id'], sensor_type_name= i['sensor_type']['name'].lower()) for i in sensors]    
    df = DataFrame()    
    for i in l:
        try:
            res = i.extractCsv(date=date)
            res[['PM10','PM2.5']].plot(title=i.sensor_id)
            print(res.describe())
            df = df.append(res)
        except:
            pass
    return df

def graphs(polluant):
    "Fonction pour tracer les graphiques"
    pivot=dfM.pivot_table(values=polluant,index='timestamp',columns='location')
    f, ax = plt.subplots(figsize=(18, 6))
    sns.heatmap(pivot, annot=False, fmt="d", linewidths=.5, ax=ax,cmap="YlGnBu")
    f.savefig(polluant+'_pivot.png')
    f, ax = plt.subplots(figsize=(18, 6))
    sns.boxplot(x="location", y=polluant,data=dfM)
    f.savefig(polluant+'_boxplot.png')
    

#Debut du programme
    
df = extractJ(box=ra, sensor=sensor,date=date)
stats = df.groupby('location')[['PM2.5','PM10']].describe()
stats.to_html('stats.html') #export des stats
dfM = df.groupby('sensor_id').resample('H').mean()
dfM=dfM.drop(labels='sensor_id',axis=1)
dfM=dfM.reset_index(level=['sensor_id','timestamp'])


#Tracé des graphs
graphs('PM10')
graphs('PM2.5')


#Carte moyenne journaliere
dfM_J = df.groupby('sensor_id').resample('D').mean()
res=dfM_J.to_dict(orient='records')

print("Creation carte PM10: \n")
m = folium.Map(location=[(lat1+lat2)/2,(lon1+lon2)/2])
for js in res:
    folium.CircleMarker(location=[js['latitude'],js['longitude']], popup=str(js['location'])+": "+str(int(js['PM10'])),radius = js['PM10']).add_to(m)
m.save('PM10'+'.html')

print("Creation carte PM2.5: \n")
m25 = folium.Map(location=[(lat1+lat2)/2,(lon1+lon2)/2])
for js in res:
    folium.CircleMarker(location=[js['latitude'],js['longitude']], popup=str(js['location'])+": "+str(int(js['PM2.5'])),radius = js['PM2.5']).add_to(m25)
m.save('PM25'+'.html')
 