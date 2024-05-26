from OpenSSL import crypto

def generate_ca_certificate():
    # Générer une paire de clés RSA
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    # Certif X509
    cert = crypto.X509()
    cert.get_subject().CN = "CA"  # Nom de CA
    cert.set_serial_number(1000)  # Numéro de série
    cert.gmtime_adj_notBefore(0)  # Validité
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # Validité
    cert.set_issuer(cert.get_subject())  # Auto signature
    cert.set_pubkey(key)  # Définir la clé publique
    cert.sign(key, 'sha256')  # Signature du certif avec clé privée

    with open("ca_key.pem", "wb") as key_file:
        key_file.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
    
    with open("ca_cert.pem", "wb") as cert_file:
        cert_file.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

    print("Clé et certificat du CA ont été créés.")
generate_ca_certificate()