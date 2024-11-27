#!/bin/python

import requests
import yaml
import time
import configparser
from influxdb_client import InfluxDBClient, WriteOptions

#############################
###   Liste des données   ###
#############################
# lat : latitude (deg)
# lon : longitude (deg)
# geo_id_insee : INSEE ID
# t : température sous abris (kelvin)
# td : température du point de rosée (kelvin)
# tx : température max sous abris (kelvin)
# tn : température min sous abris (kelvin)
# u : humidité relative (%)
# ux : humidité relative max (%)
# un : humidité relative min (%)
# dd : direction du vent à 10m (deg)
# ff : vitesse du vent (m/s)
# dxy : direction du vent moyen sur 10mn (deg)
# fxy : vitesse du vent moyen sur 10mn (m/s)
# dxi : direction du vent maxi instantané (deg)
# fxi : vitesse du vent maxi instantané (deg)
# rr1 : hauteur de précipitation (mm)
# t_10 : température à -10cm (kelvin)
# t_20 : température à -20cm (kelvin)
# t_50 : température à -50cm (kelvin)
# t_100 : température à -100cm (kelvin)
# vv : visibilité (%)
# etat_sol : ground state code ???
# sss : epaisseur de neige (m)
# n : nébulosité totale (%)
# insolh : durée d'insolation (minutes)
# ray_glo01 : radiations totales (J/m2)
# pres : pression de l'air (Pa)
# pmer : pression de l'air au niveau de la mer (Pa)
########################
#
# Lister les stations
# curl -m10  -X 'GET' 'https://public-api.meteofrance.fr/public/DPObs/v1/liste-stations' -H 'accept: */*' -H "apikey: <api_key>"
#
########################


### Variables ###

def get_data(ApiKey,StationID):
    Query = {'accept':'*/*','apikey': ApiKey}
    response = requests.get("https://public-api.meteofrance.fr/public/DPObs/v1/station/horaire?id_station=%s&format=json" %StationID, headers=Query)
    return response.json()

def kelvin_to_celcius(TempKelvin):
    if TempKelvin is not None:
        TempCelcius = round(float(TempKelvin or 0) - 273.15, 3)
        return TempCelcius
    else:
        return TempKelvin

### Main ###
# config loading
Config = configparser.ConfigParser()
Config.read('config.ini')
MeteoApi=Config.get('meteofrance', 'api')
InfluxUrl=Config.get('influx2', 'url')
InfluxToken=Config.get('influx2', 'token')
InfluxOrg=Config.get('influx2', 'org')

# stations loading
with open('stations.yml', 'r') as file:
    StationList = yaml.safe_load(file)

# set influxDB connexion
Client = InfluxDBClient(
        url=InfluxUrl,
        token=InfluxToken,
        org=InfluxOrg
)
Write_api = Client.write_api(write_options=WriteOptions(flush_interval=300, max_retry_time=100))

for Station in StationList:
    AllData = get_data(MeteoApi,Station["id"])
    DataFormated = {
        'lat':AllData[0]['lat'],
        'lon':AllData[0]['lon'],
        'reference_time':AllData[0]['reference_time'],
        'insert_time':AllData[0]['insert_time'],
        't':kelvin_to_celcius(AllData[0]['t']),
        'td':kelvin_to_celcius(AllData[0]['td']),
        'tx':kelvin_to_celcius(AllData[0]['tx']),
        'tn':kelvin_to_celcius(AllData[0]['tn']),
        'u':AllData[0]['u'],
        'ux':AllData[0]['ux'],
        'un':AllData[0]['un'],
        'dd':AllData[0]['dd'],
        'ff':AllData[0]['ff'],
        'dxy':AllData[0]['dxy'],
        'fxy':AllData[0]['fxy'],
        'dxi':AllData[0]['dxi'],
        'fxi':AllData[0]['fxi'],
        'rr1':AllData[0]['rr1'],
        't_10':kelvin_to_celcius(AllData[0]['t_10']),
        't_20':kelvin_to_celcius(AllData[0]['t_20']),
        't_50':kelvin_to_celcius(AllData[0]['t_50']),
        't_100':kelvin_to_celcius(AllData[0]['t_100']),
        'vv':AllData[0]['vv'],
        'sss':AllData[0]['sss'],
        'n':AllData[0]['n'],
        'insolh':AllData[0]['insolh'],
        'pres':AllData[0]['pres'],
        'pmer':AllData[0]['pmer']
        }
    JsonBodyWeather = [{
        "measurement": "Weather",
        "tags": Station,
        "fields": DataFormated
    }]
    #print(JsonBodyWeather)
    Write_api.write("Weather", InfluxOrg, JsonBodyWeather)

time.sleep(1)