import time
import funzioni_script_new as f
import server
import copy

# Mi serve un server di partenza
server_vecchio = server.Server("vecchio_server", "running", "Italia", "IT", 5000, "i-055198738707f0e90")

while(True):

    # Cerco il server (tra quelli in stop) a carbon intensity minore
    server_nuovo = f.server_ci_minore()

    # Verifico se il server sia stato caricato correttamente e che abbia carbon intensity minore del vecchio
    if (server_nuovo != None and server_vecchio.carbon_intensity >= server_nuovo.carbon_intensity):
        # Avvio il server
        f.avvio_server(server_nuovo)
        # Aggiorno lo stato a running
        server_nuovo.set_stato_istanza("running")

        # Mi salvo l'indirizzo IP del nuovo server (serve per trasferire i dati da vecchia VM a nuova VM)
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
    # Aggiorno il vecchio server con quello in esecuzione
    server_vecchio = copy.copy(server_nuovo)