import sys
sys.path.insert(0, "..")
import time
from opcua import ua, uamethod, Server, Client, Node
from datetime import datetime
import csv
import keyboard

#Declaration de variable globale
ENDPOINT = "opc.tcp://10.10.10.10:4840/" #IP fixe du server et prot fixe 4840 
CERTIFICATE = 'D:\\certificate\\digitaltwincert.der'
PRIVATE_KEY = 'D:\\certificate\\key2.pem'
SEUIL_AEROTHERME = 35 #en degree Celcius


def update_data_server(aquired_current, ambiant_temperature, mixing_cycle_flowrate, chaud_flowrate, froid_flowrate, out_aerotherme, out_heat_exchanger, temp_out_froid, temp_in_froid, temp_out_chaud, temp_in_chaud, aerotherme_aquis, process_value):
    """
    ATTENTION : Apres chaque deploiement vérifier/changer le nodeID
    """
    """
    IMPORTANT : S'assurer que le serveur est DEMARREE et que les variables sont DISPO avant d'appeller cette fonction
    """ 
    client = Client(ENDPOINT)
    # securication de la communication
    str = "Basic256Sha256,SignAndEncrypt,"+CERTIFICATE+","+PRIVATE_KEY
    client.set_security_string(str)

    client.application_uri = "urn:DigitalTwinv1"
    client.secure_channel_timeout = 10000
    client.session_timeout = 10000
    
    try:
        # Connection sur le serveur
        client.connect()
        

        # Ecriture de chaque valeur à l'instant t = 1,0005 S
        OUTHEATEXCHANGER = float(out_heat_exchanger)
        OUTAEROTHERME = float(out_aerotherme)
        FROIDFLOWRATE = float(froid_flowrate)
        CHAUDFLOWRATE = float(chaud_flowrate)
        MIXINGCYCLEFLOWRATE = float(mixing_cycle_flowrate)
        AMBIENTTEMPERATURE = float(ambiant_temperature)
        CURRENT = float(aquired_current)
        TEMPINCHAUD = float(temp_in_chaud)
        TEMPINFROID = float(temp_in_froid)
        TEMPOUTCHAUD = float(temp_out_chaud)
        TEMPOUTFROID = float(temp_out_froid)
        PROCESS_VALUE = float(process_value)

        #Simulation d'ajout de donnee sur OPC UA Server chaque variables
        node_id_OutHeatExchanger = "ns=2;i=11"
        node_id_OutAerotherme = "ns=2;i=12"
        node_id_FroidFlowrate = "ns=2;i=13"
        node_id_ChaudFlowrate = "ns=2;i=14"
        node_id_MixingCycleFlowrate = "ns=2;i=15"
        node_id_AmbiantTemperature = "ns=2;i=16"
        node_id_Current = "ns=2;i=17"
        node_id_TempInChaud = "ns=2;i=18"
        node_id_TempInFroid = "ns=2;i=19"
        node_id_TempOutChaud = "ns=2;i=20"
        node_id_TempOutFroid = "ns=2;i=21"
        node_id_SetPointInChaudAquis = "ns=2;i=22"
        node_id_ProcessValue = "ns=2;i=24"

        #Ecrire des nouvelles valeurs tous les t=1,0005s
        client.get_node(node_id_OutHeatExchanger).set_value(OUTHEATEXCHANGER)
        client.get_node(node_id_OutAerotherme).set_value(OUTAEROTHERME)
        client.get_node(node_id_FroidFlowrate).set_value(FROIDFLOWRATE)
        client.get_node(node_id_ChaudFlowrate).set_value(CHAUDFLOWRATE)
        client.get_node(node_id_MixingCycleFlowrate).set_value(MIXINGCYCLEFLOWRATE)
        client.get_node(node_id_AmbiantTemperature).set_value(AMBIENTTEMPERATURE)
        client.get_node(node_id_Current).set_value(CURRENT)
        client.get_node(node_id_TempInChaud).set_value(TEMPINCHAUD)
        client.get_node(node_id_TempInFroid).set_value(TEMPINFROID)
        client.get_node(node_id_TempOutChaud).set_value(TEMPOUTCHAUD)
        client.get_node(node_id_TempOutFroid).set_value(TEMPOUTFROID)
        client.get_node(node_id_ProcessValue).set_value(PROCESS_VALUE)
        aerotherme_Control = client.get_node("ns=2;i=27")
        aerotherme_Control_val = aerotherme_Control.get_value()
        client.get_node(node_id_SetPointInChaudAquis).set_value(aerotherme_Control_val)
    
    except Exception as e:
        print("Erreur dans l'Ecriture des valeur", e)

    except ConnectionError:
        print("Echec de la connection au serveur OPC UA. Veuillez resaisir l'URL du Serveur.")

    client.disconnect()

def provide_sensor_data():
    file_path = 'HPSensor_data.csv'
    data = []

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Ignorer l’en-tête

            for row in reader:
                try:
                    float_row = [float(cell.strip()) for cell in row]
                    data.append(float_row)
                except ValueError:
                    print(f"Ligne ignorée (valeur non convertible) : {row}")
    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
        return

    interval = 1.0005  # secondes
    for line in data:
        start_time = time.perf_counter()  # Chrono haute précision

        formatted_line = [f"{num:.3f}" for num in line]
        update_data_server(*formatted_line)

        #Attente de 1.005
        elapsed = time.perf_counter() - start_time
        sleep_time = max(0, interval - elapsed)
        time.sleep(sleep_time)

def main():
    print("Hit 'q' ou 'Q' to stop providing sensor data to OPC UA Server.")
    while True:
        provide_sensor_data()
        if keyboard.is_pressed('q'):
            print("Stop providing data")
            break 

if __name__ == "__main__":
    main()