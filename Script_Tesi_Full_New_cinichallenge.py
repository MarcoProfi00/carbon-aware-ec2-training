# FUNZIONA IMPLEMENTARE CON CICLO
# QUI USO IL PACKAGE JOBLIB_ESTIMATOR_FUNCTION
import time
import funzioni_script_new as f
import server
from Joblib_Estimator_Function import Play_And_Stop

# Variabili d'istanza per la funzione di trasferimento file
username = "ubuntu"
path_key = r'C:\Users\mprof\.ssh\key.pem'
source_path = r'C:\Users\mprof\Desktop\UNIVERSITA\Tesi\EC2_CI\training_state.pkl'
dest_path = "/home/ubuntu/training_state.pkl"

# Mi serve un server di partenza
server_vecchio = server.Server("vecchio_server", "running", "Italia", "IT", 5000, "i-055198738707f0e90")

# Cerco il server (tra quelli in stop) a carbon intensity minore -- MARCO PROFILO --
server_nuovo = f.server_ci_minore()
# Verifico se il server sia stato caricato correttamente e che abbia carbon intensity minore del vecchio
if (server_nuovo != None and server_vecchio.carbon_intensity >= server_nuovo.carbon_intensity):
    # Avvio il server
    f.avvio_server(server_nuovo)
    # Aggiorno lo stato a running
    server_nuovo.set_stato_istanza("running")

    # Mi salvo l'indirizzo IP del nuovo server (serve per trasferire i dati da vecchia VM a nuova VM)
    # Do il tempo alla VM di avviarsi altrimenti non mi esce l'indirizzo IP
    print("Attendi 30 secondi per permettere l'avvio della VM EC2")
    time.sleep(30)
    try:
        indirizzo_ip = f.meorizza_ip(server_nuovo)
        print(indirizzo_ip)

    except Exception:
        # Se la VM ancora non si è avviata aspetto altri 40 secondi e ripeto l'operazione
        time.sleep(30)
        print("La VM non si è ancora avviata attendi altri 30 secondi")
        indirizzo_ip = f.meorizza_ip(server_nuovo)
        print(indirizzo_ip)
print("Inizio training su VM " + server_nuovo.get_nome_istanza())
f.play_first_training_on_ec2_server(indirizzo_ip,username,path_key)
estim_total = 30
estim_act = 0

while True:
    # Cerco il server (tra quelli in stop) a carbon intensity minore -- MARCO PROFILO --
    server_nuovo = f.server_ci_minore()

    # Verifico se il server sia stato caricato correttamente e che abbia carbon intensity minore del vecchio
    if (server_nuovo != None and server_vecchio.carbon_intensity >= server_nuovo.carbon_intensity):
        # Avvio il server
        f.avvio_server(server_nuovo)
        # Aggiorno lo stato a running
        server_nuovo.set_stato_istanza("running")

        # Mi salvo l'indirizzo IP del nuovo server (serve per trasferire i dati da vecchia VM a nuova VM)
        # Do il tempo alla VM di avviarsi altrimenti non mi esce l'indirizzo IP
        print("Attendi 30 secondi per permettere l'avvio della VM EC2")
        time.sleep(30)
        try:
            indirizzo_ip = f.meorizza_ip(server_nuovo)
            print(indirizzo_ip)

        except Exception:
            # Se la VM ancora non si è avviata aspetto altri 40 secondi e ripeto l'operazione
            time.sleep(30)
            print("La VM non si è ancora avviata attendi altri 30 secondi")
            indirizzo_ip = f.meorizza_ip(server_nuovo)
            print(indirizzo_ip)

        print("Attendi 10 secondi per iniziare la copia del file")
        time.sleep(10)
        # Copio il file dello stato della prima fase di training sul nuovo server
        f.copy_file_to_ec2(indirizzo_ip, username, path_key, source_path, dest_path)

        # Una volta completato il trasferimento stoppo la vecchia VM (NON FUNZIONA)
        f.stop_server(indirizzo_ip)

        # Continuazione training
        print("Ricomincio il training su VM " + server_nuovo.get_nome_istanza())
        time.sleep(30)
        model = f.continue_training_on_ec2_server(indirizzo_ip, username, path_key)
        estim_act = f.estim()
        # print(estim_act)
        if (estim_act == estim_total):
            f.predict(indirizzo_ip, username, path_key, model)
            break

    else:
        print("Nessun VM avviata")
