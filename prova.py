import time
import funzioni_script_new as f
import server
import copy
import json
import subprocess
from operator import attrgetter
import sys

def server_ci_minore():
    try:
        # Mando il comando da terminale e mi salvo l'output con formato json (dizionario)
        output = json.loads(subprocess.check_output(['aws', 'ec2', 'describe-instances']))

    except Exception:
        print("Errore durante l'accesso ai server AWS")

    # Mi salvo il file 'mapping.json' in dictionary
    dictionary = apri_file()

    servers = []
    count = 0

    while True:
        try:
            # Cerco all'interno del dizionario l'id dell'istanza
            id_istanza = output["Reservations"][count]["Instances"][0]["InstanceId"]

            # Cerco all'interno del dizionario lo stato della mia istanza
            stato = output["Reservations"][count]["Instances"][0]["State"]["Name"]

            # Mi servono solo server in stop per avviare quello a carbon intensity minore
            if stato != "stopped":
                count = count + 1
                continue

            # Cerco all'interno del dizionario il nome della mia istanza
            nome = output["Reservations"][count]["Instances"][0]["Tags"][0]["Value"]

            carbon_intesity = int(input(f" Carbon intensity del server {nome} è: "))

            # Cerco all'interno del dizionario la zona in cui si trova la mia istanza
            regione = output["Reservations"][count]["Instances"][0]["Placement"]["AvailabilityZone"]

            regionEM = ""

            # Faccio il mapping delle region:
            for item in dictionary['Mapping']:
                if item['cloud_region'] == regione[:-1]:  # Cancello l'ultimo carattere della stringa region poichè cambia sempre e non lo conosco (altrimenti non riesco a fare il mapping)
                    regionEM = item['electricity_maps_region']

            # Mi creo il server
            server_aws = server.Server(nome, stato, regione, regionEM, carbon_intesity, id_istanza)

            # Aggiungo il server della lista 'servers'
            servers.insert(count, server_aws)

            count = count + 1

        except IndexError:
            break

        except Exception:
            print("Si è verificato un errore generico")
            break

    # Mi accerto che la lista non sia vuota poichè potrei avere server tutti in esecuzione
    if len(servers) != 0:
        # Ordino i server per carbon intensity
        servers.sort(key=attrgetter('carbon_intensity'))
        return servers[0]
    else:
        print("Non ci sono server in stop")

def apri_file():
    try:
        # Mi salvo il mapping delle region sul dizionario 'dictionary'
        with open('mapping.json', 'r') as f:
            dictionary = json.load(f)
        return dictionary
    except FileNotFoundError:
        return None

# Mi serve un server di partenza
server_vecchio = server.Server("vecchio_server", "running", "Italia", "IT", 100, "i-055198738707f0e90")

while(True):

    # Cerco il server (tra quelli in stop) a carbon intensity minore
    server_nuovo = server_ci_minore()

    # Verifico se il server sia stato caricato correttamente e che abbia carbon intensity minore del vecchio
    if (server_nuovo != None and server_vecchio.carbon_intensity > server_nuovo.carbon_intensity):
        # Avvio il server
        f.avvio_server(server_nuovo)
        # Aggiorno loo stato a running
        server_nuovo.set_stato_istanza("running")

        # Mi salvo l'indirizzo ip del nuovo server (serve per trasferire i dati da vecchia VM a nuova VM)
        # Do il tempo alla VM di avviarsi altrimenti non mi esce l'indirizzo IP
        time.sleep(30)
        try:
            indirizzo_ip = f.meorizza_ip(server_nuovo)
            print(indirizzo_ip)

        except Exception:
            # Se la VM ancora non si è avviata aspetto altri 40 secondi e ripeto l'operazione
            time.sleep(30)
            indirizzo_ip = f.meorizza_ip(server_nuovo)
            print(indirizzo_ip)
        # Qui va messo il codice per trasferire i dati da vecchia VM a nuova VM
        print("Dati trasferiti correttamente")

        # Una volta completato il trasferimento stoppo la vecchia VM
        f.stop_server(server_vecchio)

    else:
        print("Nessun VM avviata")

    # Tengo sempre in esecuzione il mio script con un intervallo di tot secondi
    time.sleep(30)
    server_vecchio = copy.copy(server_nuovo)