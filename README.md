# 🌍 Carbon-Aware EC2 Training – Tesi Triennale

Sistema intelligente per la selezione automatica di istanze EC2 AWS a **bassa intensità di carbonio**, con trasferimento dello stato di training e prosecuzione remota. Progetto sviluppato come **tesi triennale in Ingegneria dell’Informazione** al Politecnico di Torino.

---

## ⚙️ Funzionamento

Il sistema:

1. Verifica la carbon intensity delle regioni associate alle istanze EC2 (tramite API ElectricityMap)
2. Seleziona l’istanza **ferma (stopped)** con minore impatto ambientale
3. Avvia l’istanza selezionata e ne ottiene l’indirizzo IP
4. Copia lo stato del training locale nella nuova macchina EC2
5. Ferma l’istanza vecchia e **prosegue il training sulla nuova EC2** a minore impatto
6. Tutto in automatico via script Python + AWS CLI

---

## 🛠️ Preparazione

### 🔐 1. Configurare AWS CLI

- Avviare **Learner Lab**
- Copiare i dettagli AWS dal portale e configurare il terminale:
  ```bash
  aws configure


### 🔐 2. Chiave API ElectricityMap

- Inserire la propria API Key nello script funzioni_script_new.py per usare i dati in tempo reale sulla carbon intensity.


### 🔐 3. SSH Key

- Scaricare la chiave .pem da AWS
- Posizionarla in: C:\Users\user\.ssh\key.pem

### 🔐 4. Avvio Script Completo
- python script_tesi_full_new.py