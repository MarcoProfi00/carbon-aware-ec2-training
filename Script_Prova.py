import json
import subprocess

import requests

#   output = json.loads(subprocess.check_output(['aws', 'ec2', 'describe-instances']))
#   print(output)
#ok

#   subprocess.check_output(['aws', 'ec2', 'start-instances', '--instance-ids', 'i-0b8bbb79e14f60950'])
#ok

def electricity_map(country_code):

    # Imposta l'URL della richiesta API Electricity Map
    url = 'https://api.co2signal.com/v1/latest'


    # Al posto di '...' inserire la chiave API Electricity Map
    headers = {'auth-token': 'R09WovXmEDQMdFQr81HMDGhlFbZLPwg4'}


    # Effettua la richiesta API con i parametri specificati
    response = requests.get(url, params={'countryCode': country_code}, headers=headers)

    # Ottiene la risposta in formato JSON
    data = response.json()

    return data['data']['carbonIntensity']


def electricity_map1(url, country_code):
    headers = {'auth-token': 'R09WovXmEDQMdFQr81HMDGhlFbZLPwg4'}

    response = requests.get(url, params={'countryCode': country_code}, headers=headers)
    data = response.json()

    return data

url = 'https://api.co2signal.com/v1/latest'
country_code = 'IT'
result = electricity_map(country_code)
print(result)