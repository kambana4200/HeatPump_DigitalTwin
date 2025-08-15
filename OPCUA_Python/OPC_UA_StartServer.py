import sys
sys.path.insert(0, "..")
import time
import csv
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

def launch_server():
    """ 
        construire le serveur OPC UA
    """
    server = Server()
    server.set_endpoint(ENDPOINT)
    # configurer la couche de securite pour la communication OPC UA Serveur / client avec TLS
    server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
    # cle public de chiffrement
    server.load_certificate(CERTIFICATE)
    # cle prive pour le dechiffrement
    server.load_private_key(PRIVATE_KEY)
    # enregistrer le namespace de notre serveur
    uri = "urn:DigitalTwinv1"
    idx = server.register_namespace(uri)

    #nom de l'espace d'adresse
    nom = "OPC_UA_pour_JN"
    namespace = server.register_namespace(nom) 

    """
        Configurer les nodes d'aquisition sur OPC UA Server
    """
    noeud_racine = server.get_root_node()
    noeud_objet = server.get_objects_node()

    heatExchanger = noeud_objet.add_object(idx, "HeatExchanger")
    aerotherme = noeud_objet.add_object(idx, "Aerotherme")
    flowrate = noeud_objet.add_object(idx, "Flowrate")
    temperature = noeud_objet.add_object(idx, "Temperature")
    current = noeud_objet.add_object(idx, "Current")
    geoHeatpump = noeud_objet.add_object(idx, "GEOHeatpump")
    aerothermeAquis = noeud_objet.add_object(idx, "Aerotherme_Aquisition")
    waterGlycolTankAquis = noeud_objet.add_object(idx, "WaterGlycolTank_Aquisition")
    processValue = noeud_objet.add_object(idx, "processValue")

    #Creation des donnees pour chaque variables
    OutHeatExchanger = heatExchanger.add_variable(idx, "OutHeatExchanger", 0.0, ua.VariantType.Float)
    OutAerotherme = aerotherme.add_variable(idx, "OutAerotherme", 0.0, ua.VariantType.Float)
    FroidFlowrate = flowrate.add_variable(idx, "FroidFlowrate", 0.0, ua.VariantType.Float)
    ChaudFlowrate = flowrate.add_variable(idx, "ChaudFlowrate", 0.0, ua.VariantType.Float)
    MixingCycleFlowrate = flowrate.add_variable(idx, "MixingCycleFlowrate", 0.0, ua.VariantType.Float)
    AmbiantTemperature = temperature.add_variable(idx, "AmbiantTemperature", 0.0, ua.VariantType.Float)
    Current = current.add_variable(idx, "Current", 0.0, ua.VariantType.Float)
    TempInChaud = geoHeatpump.add_variable(idx, "TempInChaud", 0.0, ua.VariantType.Float)
    TempInFroid = geoHeatpump.add_variable(idx, "TempInFroid", 0.0, ua.VariantType.Float)
    TempOutChaud = geoHeatpump.add_variable(idx, "TempOutChaud", 0.0, ua.VariantType.Float)
    TempOutFroid = geoHeatpump.add_variable(idx, "TempOutFroid", 0.0, ua.VariantType.Float)
    SetPointInChaudAquis = aerothermeAquis.add_variable(idx, "SetPointInChaudAquis", 0.0, ua.VariantType.Float)
    SetPointInFroidAquis = waterGlycolTankAquis.add_variable(idx, "SetPointInFroidAquis", 0.0, ua.VariantType.Float)
    ProcessValue = processValue.add_variable(idx, "ProcessValue", 0.0, ua.VariantType.Float)

    OutHeatExchanger.set_writable() #droit d'ecriture sur la variable depuis un OPC UA Client
    OutAerotherme.set_writable()
    FroidFlowrate.set_writable()
    ChaudFlowrate.set_writable()
    MixingCycleFlowrate.set_writable()
    AmbiantTemperature.set_writable()
    Current.set_writable()
    TempInChaud.set_writable()
    TempInFroid.set_writable()
    TempOutChaud.set_writable()
    TempOutFroid.set_writable()
    SetPointInChaudAquis.set_writable()
    SetPointInFroidAquis.set_writable()
    ProcessValue.set_writable()


    """
        Configurer les nodes de commande/controle sur OPC UA Server   
    """
    aerotherme_Control = noeud_objet.add_object(idx, "Aerotherme_Control")
    waterGlycolTank_Control = noeud_objet.add_object(idx, "WaterGlycolTank_Control")

    #Creation des donnees pour chaque variables de controle
    SetPointInChaud = aerotherme_Control.add_variable(idx, "SetPointInChaud", 0.0, ua.VariantType.Float)
    SetPointInFroid = waterGlycolTank_Control.add_variable(idx, "SetPointInFroid", 0.0, ua.VariantType.Float)

    SetPointInChaud.set_writable() #droit d'ecriture sur la variable depuis un OPC UA Client
    SetPointInFroid.set_writable() #droit d'ecriture sur la variable depuis un OPC UA Client

    """
        Serveur OPC UA demarree
    """
    server.start()
