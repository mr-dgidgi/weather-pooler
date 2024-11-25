#!/bin/python

import requests
import yaml
import configparser
from influxdb_client import InfluxDBClient, WriteOptions

#############################
###   Liste des données   ###
#############################
# lat : latitude
# lon : longitude
# geo_id_insee : INSEE ID
# t : température sous abris (celcius)
# td : température du point de rosée (celcius)
# tx : température max sous abris (celcius)
# tn : température min sous abris (celcius)
# u : humidité relative (%)
# ux : humidité relative max (%)
# un : humidité relative min (%)
# dd : direction du vent à 10m (360°)
# ff : vitesse du vent (m/s)
# dxy : direction du vent moyen sur 10mn (360°)
# fxy : vitesse du vent moyen sur 10mn (m/s)
# dxi : direction du vent maxi instantané (360°)
# fxi : vitesse du vent maxi instantané (360°)
# rr1 : hauteur de précipitation (mm)
# t_10 : température à -10cm (celcius)
# t_20 : température à -20cm (celcius)
# t_50 : température à -50cm (celcius)
# t_100 : température à -100cm (celcius)
# vv : visibilité (%)
# etat_sol : ???
# sss : ???
# n : nébulosité totale (octas)
# insolh : durée d'insolation (minutes)
# ray_glo01
# pres : pression de l'air (hPa)
# pmer : pression de la mer (hPa)
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
    JsonBodyWeather = [{
        "measurement": "Weather",
        "tags": Station,
        "fields": AllData[0]
    }]
    print(JsonBodyWeather)

#Write_api.write("Weather", InfluxOrg, JsonBodyWeather)