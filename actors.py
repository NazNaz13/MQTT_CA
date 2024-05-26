import paho.mqtt.publish as publish
# MQTT
MQTT_BROKER = "194.57.103.203"
MQTT_PORT = 1883
MQTT_TOPIC_REQUEST = "vehicle/nazim"

# Envoi des messages sur la file MQTT
def send_request(message):
    publish.single(MQTT_TOPIC_REQUEST, message, hostname=MQTT_BROKER, port=MQTT_PORT)

# Fonction pour générer un certificat pour un client ou un vendeur (non révoqué)
def generate_certificate(common_name, revoke=False):
    if revoke:
        send_request(f"generate_vendor_certificate:{common_name}:revoke")
    else:
        send_request(f"generate_client_certificate:{common_name}")
    # Ajout à la liste des révoqués ... si révoqué
    if revoke:
        with open("revoked_certs.txt", "a") as file:
            file.write(f"{common_name}_cert.pem\n")
# Générer client
generate_certificate("client1")
# Générer vendeur1
generate_certificate("vendeur1")
# Générer vendeur2
generate_certificate("vendeur2")
# Générer vendeur3 ... révoqué
generate_certificate("vendeur3", revoke=True)