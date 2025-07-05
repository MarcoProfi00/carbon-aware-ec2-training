import requests
import subprocess
import json
import server
from operator import attrgetter
#MIO
import paramiko
from Joblib_Estimator_Function import Resume_Training_Ciclo, Play_And_Stop


# Funzione che mi restituisce la carbon intensity della regione passatali come parametro
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


# Mi salva il file 'mapping.json' in 'dictionary'
def apri_file():
    try:
        # Mi salvo il mapping delle region sul dizionario 'dictionary'
        with open('mapping.json', 'r') as f:
            dictionary = json.load(f)
        return dictionary
    except FileNotFoundError:
        return None

# Funzione che mi avvia il server:
def avvio_server(server):
    try:
        subprocess.check_output(['aws', 'ec2', 'start-instances', '--instance-ids', server.get_id_istanza()])
        print("E' stato avviato il server " + server.get_nome_istanza())
    except Exception:
        print("Errore durante l'accesso ai server AWS")

# Funzione che mi dice quale è il server a carbon intesity minore
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

            # Cerco all'interno del dizionario la zona in cui si trova la mia istanza
            regione = output["Reservations"][count]["Instances"][0]["Placement"]["AvailabilityZone"]

            regionEM = ""

            # Faccio il mapping delle region:
            for item in dictionary['Mapping']:
                if item['cloud_region'] == regione[:-1]:  # Cancello l'ultimo carattere della stringa region poichè cambia sempre e non lo conosco (altrimenti non riesco a fare il mapping)
                    regionEM = item['electricity_maps_region']

            # Mi dà la carbon intensity della region desiderata
            carbon_intensity = electricity_map(regionEM)

            # Mi creo il server
            server_aws = server.Server(nome, stato, regione, regionEM, carbon_intensity, id_istanza)

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

def meorizza_ip(server):
    try:
        # Mando il comando da terminale e mi salvo l'output con formato json (dizionario)
        output = json.loads(subprocess.check_output(['aws', 'ec2', 'describe-instances', '--instance-ids', server.get_id_istanza()]))

    except Exception:
        print("Errore durante l'accesso ai server AWS")

    return output["Reservations"][0]["Instances"][0]["PublicIpAddress"]

def stop_server(ip_address):
    try:
        subprocess.check_output(['aws', 'ec2', 'stop-instances', '--instance-ids', ip_address])
        print("E' stato stoppato il server " + ip_address)
    except Exception:
        print("Errore nello stoppare il server, computer locale")

#---------------------------------------------------------------------------#
#MARCO PROFILO
def copy_file_to_ec2(ip_address, server_username, server_key_path,source_path, destination_path):
    try:
        # Creazione della connessione SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Imposta la politica di conferma automatica per l'autenticità dell'host
        ssh.load_host_keys(filename="C:\\Users\\mprof\\.ssh\\known_hosts")

        # Connessione al server remoto
        ssh.connect(ip_address, username=server_username, key_filename=server_key_path)

#        print("Connessione SSH stabilita con successo")

        # Percorso remoto del server EC2 in cui copiare il file
        remote_path = f"{server_username}@{ip_address}:{destination_path}"

        # Comando SCP per copiare il file
        scp_command = ["scp", "-i", server_key_path, source_path, remote_path]

        # Esegui il comando SCP
        subprocess.check_call(scp_command)

        print("Trasferimento avvenuto con successo")

    except paramiko.AuthenticationException as auth_error:
        print("Errore di autenticazione:", str(auth_error))
    except paramiko.SSHException as ssh_error:
        print("Errore SSH:", str(ssh_error))
    except Exception as ex:
        print("Errore generico:", str(ex))
    finally:
        if ssh:
            ssh.close()


def play_first_training_on_ec2_server(ip_address, server_username, server_key_path):
    try:
        # Creazione della connessione SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Imposta la politica di conferma automatica per l'autenticità dell'host
        ssh.load_host_keys(filename="C:\\Users\\mprof\\.ssh\\known_hosts")

        # Connessione al server remoto
        ssh.connect(ip_address, username=server_username, key_filename=server_key_path)

#        print("Connessione SSH stabilita con successo")

        # Comando per continuare il training
        Play_And_Stop.run_first_training()

        print("Training stop sul server: ", ip_address)

    except paramiko.AuthenticationException as auth_error:
        print("Errore di autenticazione:", str(auth_error))
    except paramiko.SSHException as ssh_error:
        print("Errore SSH:", str(ssh_error))
    except Exception as ex:
        print("Errore generico:", str(ex))
    finally:
        if ssh:
            ssh.close()


def continue_training_on_ec2_server(ip_address, server_username, server_key_path):
    try:
        # Creazione della connessione SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Imposta la politica di conferma automatica per l'autenticità dell'host
        ssh.load_host_keys(filename="C:\\Users\\mprof\\.ssh\\known_hosts")

        # Connessione al server remoto
        ssh.connect(ip_address, username=server_username, key_filename=server_key_path)

#        print("Connessione SSH stabilita con successo")

        # Comando per continuare il training
        model = Resume_Training_Ciclo.run_resume_training("training_state.pkl")

        print("Training stop sul server: ", ip_address)

    except paramiko.AuthenticationException as auth_error:
        print("Errore di autenticazione:", str(auth_error))
    except paramiko.SSHException as ssh_error:
        print("Errore SSH:", str(ssh_error))
    except Exception as ex:
        print("Errore generico:", str(ex))
    finally:
        if ssh:
            ssh.close()



def predict(ip_address, server_username, server_key_path,model):
    try:
        # Creazione della connessione SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Imposta la politica di conferma automatica per l'autenticità dell'host
        ssh.load_host_keys(filename="C:\\Users\\mprof\\.ssh\\known_hosts")

        # Connessione al server remoto
        ssh.connect(ip_address, username=server_username, key_filename=server_key_path)

#        print("Connessione SSH stabilita con successo")

        # Comando per continuare il training
        print("Prediction:")
        Resume_Training_Ciclo.predict(model,"training_state.pkl")


        print("Training stop sul server: ", ip_address)

    except paramiko.AuthenticationException as auth_error:
        print("Errore di autenticazione:", str(auth_error))
    except paramiko.SSHException as ssh_error:
        print("Errore SSH:", str(ssh_error))
    except Exception as ex:
        print("Errore generico:", str(ex))
    finally:
        if ssh:
            ssh.close()

def estim():
    estimator_actual= Resume_Training_Ciclo.read_estimator("training_state.pkl")
    return estimator_actual
