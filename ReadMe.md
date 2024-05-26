# MISE EN PLACE D’UNE CA SIMULEE ET GESTION DES CERTIFICATS VIA MQTT 

Ce projet propose une simulation de gestion des certificats et de vérification via MQTT, en utilisant des acteurs (client et vendeurs) et une CA (Autorité de certification).

**Fonctionnalités**

- Génération de certificat de CA: Le script ca.py permet de générer une paire de clés et un certificat auto-signé pour une Autorité de Certification (CA).

- Génération de certificats clients et vendeurs: Le script caFun.py permet de générer des certificats pour les clients et les vendeurs, en signant ces certificats avec la clé privée de la CA. Il agit également comme un serveur MQTT, écoutant les requêtes arrivant sur un certain sujet MQTT et les exécutant.

- Révocation de certificats: Les certificats peuvent être révoqués à tout moment en ajoutant leur nom à une liste de certificats révoqués en utilisant une fonction dans le script caFun.py, stockée dans le fichier revoked_certs.txt.

- Canal de communication MQTT: Les clients et vendeurs peuvent utiliser la file MQTT pour communiquer avec la CA pour la génération des certifs et la vérification de la validité et l'origine de ces derniers.

- Fichier revoked_certs.txt : Le fichier revoked_certs.txt est créé pour stocker la liste des certificats révoqués.

**Installation et exécution**

1. Installez Python sur votre système.

2. Installez les dépendances en exécutant pip install paho-mqtt pyOpenSSL.

3. Exécutez le script ca.py pour générer la clé privée et le certificat de la CA.

4. Exécutez le script caFun.py pour générer des certificats clients et vendeurs.

5. Exécutez le script actors.py pour gérer les transactions et les vérifications de certificats.

6. Exécutez le script client.py pour simuler des scénarios d'achat et de vérification de certificats.

**Versions utilisées**

| Bibliothèque   | Version  |
| -------------- | -------- |
| Python         | 3.12.2   |
| Paho MQTT      | 1.6.0    |
| pyOpenSSL      | 24.1.0   |

**Auteur**

ADDOU Nazim