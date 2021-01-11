#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 10:02:09 2020

@author: nicolas

Module pour extraire des données des fichiers textes des stations Luftdaten

"""

import pandas as pd



urlAPI = 'https://archive.sensor.community/' #url de l api de luftdaten fichier texte


class Airrohr():
    "Objet capteur Luftadten, doit être décrit à minima avec le numéro PM10 apparaissant sur la carte"
    def __init__(self,
                 sensor_id = 7737,  #numero de la mesure PM sur la carte du site
                 sensor_type_name = 'sds011'):
        self.sensor_id = sensor_id
        self.sensor_type_name = sensor_type_name
        
    def extractCsv(self,date = '2020-01-01'):
        """Fonction pour extraire le csv d une station luftdaten pour date = AAAA-MM-JJ sous forme de dataframe
        https://archive.sensor.community/2020-01-29/2020-01-29_hpm_sensor_30727.csv"""
        url = "{urlAPI}{date}/{date}_{sensor_type_name}_sensor_{sensor_id}.csv".format(urlAPI=urlAPI,date=date,sensor_type_name=self.sensor_type_name,sensor_id=self.sensor_id)
        print('\n')
        print("Extraction du fichier: ")
        print(url)
        print('\n')
        try:
            df = pd.read_csv(url,sep=';',index_col='timestamp',parse_dates=True)
            df = df.rename(columns={"lat": "latitude", "lon": "longitude", "P1":"PM10", "P2":"PM2.5", "P0":"PM1"})
            df = df.drop(columns=['durP1','ratioP1','durP2','ratioP2'])
            return df
        except:
            print('Attention: Le fichier n existe pas sur le serveur')
            
    

    


        




        
    
        
        

