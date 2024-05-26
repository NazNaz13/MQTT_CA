import paho.mqtt.client as mqtt
from OpenSSL import crypto
import os

# MQTT
MQTT_BROKER = "194.57.103.203"
MQTT_PORT = 1883
MQTT_TOPIC_REQUEST = "vehicle/nazim"

# Création de fichier des certifs révoqués
if not os.path.exists("revoked_certs.txt"):
    with open("revoked_certs.txt", "w"):
        pass

# Certif de client ou vendeur
def generate_certificate(common_name, revoke=False, client=False):
    # Clés RSA du nouveau certif
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    # Caractérestiques du certif X509
    cert = crypto.X509()
    cert.get_subject().CN = common_name  # Nom
    cert.set_serial_number(1001)  # Numéro de série
    cert.gmtime_adj_notBefore(0)  # Validité
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # Validité
    
    # Clé de CA
    with open("ca_key.pem", "rb") as key_file:
        ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_file.read())

    # Certif de CA
    with open("ca_cert.pem", "rb") as cert_file:
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_file.read())

    if not revoke or client:
        cert_type = "client" if client else "vendeur"
        print(f"Génération du certificat {cert_type} pour {common_name} en cours...")

    if client:
        cert.set_issuer(ca_cert.get_subject())  # Provient du CA
    else:
        cert.set_issuer(ca_cert.get_subject())  # Provient du CA
    
    cert.set_pubkey(key)
    cert.sign(ca_key, 'sha256')  # Signatue du certif avec clé privée de CA

    cert_filename = f"{common_name}_cert.pem"
    key_filename = f"{common_name}_key.pem"
    with open(cert_filename, "wb") as cert_file:
        cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        
    with open(key_filename, "wb") as key_file:
        key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

    if not revoke or client:
        print(f"Le certificat de {common_name} a été généré avec succès.")
    elif revoke:
        add_to_revoked_list(common_name)
        print(f"Le certificat de {common_name} a été généré et ajouté à la liste des certificats révoqués.")

# Vérification de révocation de certif
def is_certificate_revoked(cert_filename):
    if not os.path.isfile("revoked_certs.txt"):
        return False  
    
    # Affichage du contenu de revoked_certs.txt
    with open("revoked_certs.txt", "r") as file:
        revoked_certs = [line.strip() for line in file]

    if cert_filename in revoked_certs:
        return True
    else:
        return False

# Certif provient du CA ???
def is_certificate_from_ca(cert_filename):
    # Certif du CA
    with open("ca_cert.pem", "rb") as cert_file:
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_file.read())

    # Certif du vendeur
    with open(cert_filename, "rb") as cert_file:
        vendor_cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_file.read())

    # Vérification
    store = crypto.X509Store()
    store.add_cert(ca_cert)
    store_ctx = crypto.X509StoreContext(store, vendor_cert)
    try:
        store_ctx.verify_certificate()
        return True
    except Exception as e:
        print("Erreur de vérification du certificat :", e)
        return False

# Ajout a la liste des revoqués
def add_to_revoked_list(cert_filename):
    if not os.path.isfile("revoked_certs.txt"):
        with open("revoked_certs.txt", "w") as file:
            file.write(cert_filename + "\n")
        print(f"Le fichier revoked_certs.txt a été créé et le certificat {cert_filename} a été ajouté.")
    else:
        # Le certif est déjà dans la liste ??
        if not is_certificate_revoked(cert_filename):
            with open("revoked_certs.txt", "a") as file:
                file.write(cert_filename + "\n")
            print(f"Le certificat {cert_filename} a été ajouté à la liste des certificats révoqués.")
        else:
            print(f"Le certificat {cert_filename} est déjà dans la liste des certificats révoqués.")
    
    # Afficher la listes des certifs révoqués
    with open("revoked_certs.txt", "r") as file:
        print("Contenu du fichier revoked_certs.txt après l'ajout :")
        print(file.read())

# Réponse aux requetes
def on_connect(client, userdata, flags, rc):
    print("Connecté au broker MQTT :", rc)
    client.subscribe(MQTT_TOPIC_REQUEST)

def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print(f"Message reçu sur le topic {msg.topic}: {message}")
    
    if message.startswith("generate_client_certificate"):
        client_name = message.split(":")[1]
        generate_certificate(client_name, client=True)
    elif message.startswith("generate_vendor_certificate"):
        vendor_name = message.split(":")[1]
        revoke = message.split(":")[2] == "revoke"
        generate_certificate(vendor_name, revoke)

    if message.startswith("Achat_du_vendeur1"):
        vendor_cert = "vendeur1_cert.pem"
        if is_certificate_from_ca(vendor_cert):
            print("Le certificat du vendeur1 provient du CA.")
            print("Achat effectué.")
        else:
            print("Le certificat du vendeur1 ne provient pas du CA. Annulation de l'achat.")
    elif message.startswith("Achat_du_vendeur2"):
        vendor_cert = "vendeur2_cert.pem"
        if is_certificate_from_ca(vendor_cert):
            print("Le certificat du vendeur2 provient du CA.")
            if not is_certificate_revoked(vendor_cert):
                print("Le certificat du vendeur2 n'est pas révoqué.")
                print("Achat effectué.")
            else:
                print("Le certificat du vendeur2 est révoqué. Annulation de l'achat.")
        else:
            print("Le certificat du vendeur2 ne provient pas du CA. Annulation de l'achat.")
    elif message.startswith("Achat_du_vendeur3"):
        vendor_cert = "vendeur3_cert.pem"
        if is_certificate_from_ca(vendor_cert):
            print("Le certificat du vendeur3 provient du CA.")
            if not is_certificate_revoked(vendor_cert):
                print("Le certificat du vendeur3 n'est pas révoqué.")
                print("Achat effectué.")
            else:
                print("Le certificat du vendeur3 est révoqué.") 
                print("Annulation de l'achat.")
        else:
            print("Le certificat du vendeur3 ne provient pas du CA.")
            print("Annulation de l'achat.")

# Client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connexion MQTT
client.connect(MQTT_BROKER, MQTT_PORT)

client.loop_forever()