# weather-pooler
a pooler to request Meteo France API and save observation data to InfluxDB

# Info

## Mandatory : 
* an API Key from Meteo France (it's free) [Données d'observation](https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesObservation)
* An influxdb server
* A server with python
* the following pithon modules : 
  * influxdb-client
  * configparser
  * requests
  * yaml

## List of stations
This script can be use for multiples weatherstations. All the stations are set in ```station.yml```

| variable                      | meaning                                                |
|-------------------------------|--------------------------------------------------------|
| id                            | The ID of the station **                               |
| name                          | The name of the station **                             |
| department                    | French department where the station is located         |
| region                        | French state where the station is located              |

** These data can be retrieved with the meteo france API