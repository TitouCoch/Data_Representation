
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 09:17:16 2022

@author: tcocheril001
"""

import geopy as geo
import pyodbc
import pandas as pd
from pyproj import Proj, transform

conn=pyodbc.connect('DSN=nodenot_bd4')
cursor = conn.cursor()


#indice de gravité
sql ="SELECT *, nb_morts*10+nb_blesses_graves*10+nb_blesses_legers AS indice_gravite FROM MAccident;"
df1=pd.read_sql(sql,conn)

#accidents qui correspondent aux parametre
luminosite =input("luminosite: ")
meteo =input("meteo: ")
sql3="SELECT MLieu.x,MLieu.y FROM MAccident JOIN MLieu ON MLieu.lieu_id=MAccident.lieu_id JOIN MLuminosite ON MAccident.lum_id=MLuminosite.code JOIN MIntemperie ON MIntemperie.code=MAccident.intemp_id WHERE MLuminosite.type_luminosite=? AND MIntemperie.libelle=?"
param = (f'{luminosite}%',f'{meteo}%')
df2=pd.read_sql(sql3,conn,params=param)

#entree = input("saisir le rayon: ")


def to_latlon(x,y):
    inProj = Proj(init='epsg:27561')
    outProj = Proj(init='epsg:4326')
    x = 658600
    y = 324153
    lon, lat = transform(inProj, outProj, x, y)
    return(lon,lat)

def DansRayon(x,y,x1,y1,rayon):
        a=(x,y)
        b=(x1,y1)
        if geo.distance(a,b).meters <=rayon:
            return(True)


        
        
