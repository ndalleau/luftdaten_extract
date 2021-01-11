#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 21:05:19 2021

@author: nicolas
"""

import requests
import json


#Variables géographiques ##########

lat1,lon1 = 45.4091427,5.43537 #Point Nord Ouest
lat2,lon2 = 45.3111788,5.690073 #Point Sud Est
domaine=[lat1,lon1,lat2,lon2]


lat,lon = 45.6671647,6.373437
distance = 5
circle = [lat,lon,distance]


countries = "FR"

###################################

sensors = "SDS011,BME280"

url1 = "https://data.sensor.community/airrohr/v1/filter/"

type={sensors} #comma-separated list of sensor types, e.g. sensors = SDS011,BME280
area={lat,lon,distance} #all sensors within a max radius e.g. 52.5200,13.4050,10 (Berlin)
#box={lat1,lon1,lat2,lon2} #all sensors in a 'box' with the given coordinates e.g. 52.1,13.0,53.5,13.5
country={countries} #comma-separated list of country codes. Example BE,DE,NL

"https://data.sensor.community/airrohr/v1/filter/box=47,2,44,8&type=SDS011,BME280"

def extractbox(box=domaine,sensor="SDS011"):
    "https://data.sensor.community/airrohr/v1/filter/box=52.1,13.0,53.5,13.5"
    urlRequest = "{url}box={lat1},{lon1},{lat2},{lon2}&type={sensor}".format(url=url1, lat1= box[0],lon1 = box[1], lat2 = box[2],lon2 = box[3],sensor = sensor)
    print(urlRequest)
    resp = requests.get(urlRequest)
    data = resp.json()
    return data

def extractcercle(cercle=circle,sensor="SDS011"):
    "https://data.sensor.community/airrohr/v1/filter/area=52.5200,13.4050,10"
    urlRequest = "{url}area={lat},{lon},{r}&type={sensor}".format(url=url1, lat= lat,lon = lon, r = distance,sensor = sensor)
    print(urlRequest)
    resp = requests.get(urlRequest)
    data = resp.json()
    return data

