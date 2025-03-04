🚀 Déploiement de l’Environnement IIOTVM avec Docker et OPC UA
Ce guide décrit les étapes nécessaires pour la mise en place d’un environnement IIoT complet sur une machine virtuelle Azure, intégrant Docker-Compose et un serveur OPC UA basé sur open62541. L’installation comprend plusieurs services clés :

Traefik (Reverse Proxy)
MariaDB & phpMyAdmin (Base de données et interface de gestion)
Streamlit (Interface de visualisation)
Node-RED (Automatisation et IoT)
MQTT (Communication IoT)
Serveur OPC UA (Protocole industriel, configuré via JSON)
🎥 Résumé vidéo des étapes : YouTube

🌐 1. Création de la Machine Virtuelle sur Azure
1.1 Connexion et Création de la VM
Accédez à Azure Portal et connectez-vous.
Créez une machine virtuelle avec Ubuntu Server 24.04 LTS.
Configuration recommandée :
Ports ouverts : 80 (HTTP), 443 (HTTPS), 22 (SSH), 4840 (OPC UA) (à configurer après création).
Connexion à la VM via SSH :
bash
Copy
Edit
az ssh vm --ip <adresse_ip_VM> --local_user <utilisateur>
# Alternative si la première méthode échoue :
ssh <utilisateur>@<adresse_ip_VM>
🌍 2. Configuration d’un Domaine Gratuit
Obtenir un domaine sur freedomain.one.
Créer des enregistrements DNS pour pointer vers l’IP de votre VM :
pma.mondomaine.com → phpMyAdmin
streamlit.mondomaine.com → Streamlit
nodered.mondomaine.com → Node-RED
portainer.mondomaine.com → Portainer
🛠️ 3. Installation de Docker et Déploiement de l’Environnement
Exécutez le script d’installation :

bash
Copy
Edit
curl -sSL -o install.sh https://raw.githubusercontent.com/ibroche/IIOTVM/main/Docker+OPCUA/install.sh
chmod +x install.sh
./install.sh
Ce script :
✅ Installe Docker et Docker-Compose
✅ Génère la configuration des services
✅ Déploie les conteneurs avec docker-compose up -d
✅ Installe et configure le serveur OPC UA (open62541)

🔒 4. Configuration de Traefik et HTTPS
Traefik gère automatiquement les redirections HTTPS via Let’s Encrypt.
Vérifiez que les enregistrements DNS sont bien configurés pour valider les certificats SSL.
🏭 5. Personnalisation du Serveur OPC UA
Modifier le fichier opcua_config.json pour personnaliser les variables OPC UA.
Redémarrer le serveur OPC UA :
bash
Copy
Edit
pkill opcua_server
gcc -std=c99 -I/usr/local/include -L/usr/local/lib -o opcua_server opcua_server.c -lopen62541 -lcjson
./opcua_server &
📊 6. Accès aux Services Déployés
Service	URL d’accès
phpMyAdmin	https://pma.mondomaine.com
Streamlit	https://streamlit.mondomaine.com
Node-RED	https://nodered.mondomaine.com
Portainer	https://portainer.mondomaine.com
📌 Remplacez mondomaine.com par votre domaine personnalisé.

📌 7. Gestion et Supervision
📌 Consulter les logs des services :

bash
Copy
Edit
docker-compose logs -f
📌 Redémarrer le serveur OPC UA :

bash
Copy
Edit
pkill opcua_server
./opcua_server &
🎯 Conclusion
Vous avez désormais un environnement IIoT complet fonctionnant sur Azure, incluant :
✅ Une infrastructure conteneurisée avec Docker-Compose et Traefik
✅ Un serveur OPC UA configurable via JSON
✅ Une interface de supervision et de gestion

💡 Personnalisez et adaptez cet environnement selon vos besoins ! 🚀
