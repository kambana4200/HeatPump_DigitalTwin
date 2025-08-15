import sys
sys.path.insert(0, "..")
import time
from opcua import ua, uamethod, Server, Client, Node
from datetime import datetime

#Declaration de variable globale
ENDPOINT = "opc.tcp://10.10.10.10:4840/" #IP fixe du server et prot fixe 4840 
CERTIFICATE = 'D:\\certificate\\digitaltwincert.der'
PRIVATE_KEY = 'D:\\certificate\\key2.pem'
SEUIL_AEROTHERME = 35 #en degree Celcius
    
class GestionSouscription():
    def notification_datachgmnt(self, node: Node, val, data):
        print(str(datetime.now().strftime("%Y-%m-%d %H:%M %p")) + " : " + str(node) + " : " + str(val))

def ensure_twining_setpoint_chaud():
    """
    ATTENTION : Apres chaque deploiement vérifier/changer le nodeID
    """
    ### Peut être bloquer si le socket est occupée sur le port 4840 
    client = Client(ENDPOINT)
    # securication de la communication
    str = "Basic256Sha256,SignAndEncrypt,"+CERTIFICATE+","+PRIVATE_KEY
    client.set_security_string(str)
    
    client.application_uri = "urn:DigitalTwinv1:YRPolytechAngers"
    client.secure_channel_timeout = 10000
    client.session_timeout = 10000
    
    try:
        # Connection sur le serveur
        client.connect()

        aerothermeAquis = client.get_node("ns=2;i=21")
        aerothermeAquis_val = aerothermeAquis.get_value()
        
        aerotherme_Control = client.get_node("ns=2;i=25")
        aerotherme_Control_val = aerotherme_Control.get_value()

    except Exception as e:
        print("Erreur dans la lecture de la valeur", e)

    except ConnectionError:
        print("Echec de la connection au serveur OPC UA. Veuillez resaisir l'URL du Serveur.")

    if aerothermeAquis_val == aerotherme_Control_val : #La variable de controle du DT et du SCI sont en phase
        if aerotherme_Control_val >= SEUIL_AEROTHERME: # valeur au dessus de la seuil nominale de l'aerotherme
            client.disconnect()
            return 1 #PROTECTION ICS : NE PAS MODIFIER LA VALEUR DE CONTROL => VALEUR DT PRIORITAIRE % AU SCI
        client.disconnect()
        return 1 #DT STABLE ie VALEUR DE CONTROLE == VALEUR CONTROLE SUR DT: NE PAS MODIFIER LA VALEUR DE CONTROL
    else:
        client.disconnect()
        return 0 #DT EN RETARD PAR RAPPORT AU SCI : MODIFIER LA VALEUR DE CONTROL

def command_setpoint_chaud():
    """
    ATTENTION : Apres chaque deploiement vérifier/changer le nodeID
    """
    client = Client(ENDPOINT)
    # securication de la communication
    str = "Basic256Sha256,SignAndEncrypt,"+CERTIFICATE+","+PRIVATE_KEY
    client.set_security_string(str)
    client.application_uri = "urn:DigitalTwinv1:YRPolytechAngers"
    client.secure_channel_timeout = 10000
    client.session_timeout = 10000
    
    try:
        # Connection sur le serveur
        client.connect()

        aerotherme_Control = client.get_node("ns=2;i=25")
        aerotherme_Control_val = aerotherme_Control.get_value()
        
    except Exception as e:
        print("Erreur dans la lecture de la valeur sur DT", e)

    except ConnectionError:
        print("Echec de la connection au serveur OPC UA. Veuillez resaisir l'URL du Serveur.")

    valeur_de_ctrl = aerotherme_Control_val
    client.disconnect()
    return valeur_de_ctrl


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

    client.application_uri = "urn:DigitalTwinv1:YRPolytechAngers"
    client.secure_channel_timeout = 10000
    client.session_timeout = 10000
    
    try:
        # Connection sur le serveur
        client.connect()
        
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
        SETPOINTINCHAUD_ACQ = float(aerotherme_aquis)
        PROCESS_VALUE = float(process_value)

        node_id_OutHeatExchanger = "ns=2;i=10"
        node_id_OutAerotherme = "ns=2;i=11"
        node_id_FroidFlowrate = "ns=2;i=12"
        node_id_ChaudFlowrate = "ns=2;i=13"
        node_id_MixingCycleFlowrate = "ns=2;i=14"
        node_id_AmbiantTemperature = "ns=2;i=15"
        node_id_Current = "ns=2;i=16"
        node_id_TempInChaud = "ns=2;i=17"
        node_id_TempInFroid = "ns=2;i=18"
        node_id_TempOutChaud = "ns=2;i=19"
        node_id_TempOutFroid = "ns=2;i=20"
        node_id_SetPointInChaudAquis = "ns=2;i=21"
        node_id_ProcessValue = "ns=2;i=24"

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
        client.get_node(node_id_SetPointInChaudAquis).set_value(SETPOINTINCHAUD_ACQ)
        client.get_node(node_id_ProcessValue).set_value(PROCESS_VALUE)
            
    except Exception as e:
        print("Erreur dans l'Ecriture des valeur", e)

    except ConnectionError:
        print("Echec de la connection au serveur OPC UA. Veuillez resaisir l'URL du Serveur.")

    client.disconnect() 
