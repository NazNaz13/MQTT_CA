import paho.mqtt.client as mqtt

# MQTT
MQTT_BROKER = "194.57.103.203"
MQTT_PORT = 1883
MQTT_TOPIC_REQUEST = "vehicle/nazim"

def send_request(message):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.publish(MQTT_TOPIC_REQUEST, message)
    client.disconnect()

# Vérification du certif du vendeur1
def scenario_vendeur1():
    send_request("Achat_du_vendeur1")
# Vérification du certif du vendeur2
def scenario_vendeur2():
    send_request("Achat_du_vendeur2")
# Vérification du certif du vendeur3 (révoqué)
def scenario_vendeur3():
    send_request("Achat_du_vendeur3")

scenario_vendeur1()
scenario_vendeur2()
scenario_vendeur3()