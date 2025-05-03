# Déploiement de l’Environnement IIOTVM avec Docker et OPC UA  

Ce guide détaille l’ensemble des étapes pour déployer une **machine virtuelle sur Azure**, installer **Docker-Compose** et configurer un **serveur OPC UA** basé sur **open62541**. L’environnement comprend plusieurs services essentiels :  

- **Traefik** (Reverse Proxy)  
- **MariaDB** & **phpMyAdmin** (Base de données et interface de gestion)
- **Node-RED** (Automatisation et IoT)  
- **MQTT** (Communication IoT)  
- **Serveur OPC UA** (Protocole industriel, configuré via JSON)  

🎥 **Vidéo récapitulative des étapes :** [YouTube](https://youtu.be/HKy8vaBAl9k)  

---

# 1. Création de la Machine Virtuelle sur Azure  

## 1.1 Connexion au Portail Azure  
- Accédez à [Azure Portal](https://azure.microsoft.com/fr-fr/free/students) et connectez-vous avec votre compte.  

## 1.2 Création d’une Nouvelle VM  
- Cliquez sur **"Créer une ressource"**, puis sélectionnez **"Machine virtuelle"**.  
- Choisissez **Ubuntu Server 24.04 LTS** pour assurer la compatibilité avec Docker et les outils requis.  
- **Configuration recommandée :**  
  - Ouvrir les ports **80 (HTTP)**, **443 (HTTPS)**, **22 (SSH)**.  
  - Ouvrir le port **4840** pour **OPC UA** (à ajouter après la création de la VM).  

## 1.3 Connexion à la VM  
Une fois la VM créée, connectez-vous via Azure CLI ou SSH :  

```bash
az ssh vm --ip <adresse_ip_VM> --local_user <utilisateur>
# Si la méthode précédente échoue :
ssh <utilisateur>@<adresse_ip_VM>
```

---

# 2. Configuration d’un Domaine Gratuit  

## 2.1 Obtention d’un Domaine  
- Rendez-vous sur [freedomain.one](https://freedomain.one) et inscrivez-vous pour obtenir un domaine gratuit.  
- Exemple de domaine : `iiotvm.publicvm.com`.  

## 2.2 Configuration des Enregistrements DNS  
Dans l’interface de gestion DNS, ajoutez les enregistrements de type **A** pointant vers l’adresse IP publique de votre VM :  
- `pma.iiotvm.publicvm.com` → phpMyAdmin  
- `streamlit.iiotvm.publicvm.com` → Streamlit  
- `nodered.iiotvm.publicvm.com` → Node-RED  
- `portainer.iiotvm.publicvm.com` → Portainer  

**Exemple d’enregistrement DNS :**  
- **Nom :** `pma`  
- **Valeur :** `<adresse_ip_VM>`  

---

# 3. Installation de Docker et Déploiement de l’Environnement  

## 3.1 Exécution du Script d’Installation  
Téléchargez et exécutez le script avec la commande suivante :  

```bash
curl -sSL -o install.sh https://raw.githubusercontent.com/Chahid012/OPC-UA-Server-Azure/main/install.sh
chmod +x install.sh
./install.sh
```

Le script réalisera automatiquement les actions suivantes :  
- Installation de **Docker** et **Docker-Compose**.  
- Création des fichiers de configuration (ex. `docker-compose.yml`, `mosquitto.conf`).  
- Déploiement des services avec `docker-compose up -d`.  
- Installation et configuration du **serveur OPC UA** basé sur **open62541**.  

---

# 4. Configuration de Traefik et HTTPS  

- **Traefik** est configuré pour gérer les certificats SSL via **Let’s Encrypt**.  
- Vérifiez que vos **enregistrements DNS** sont bien configurés pour que la validation ACME fonctionne correctement.  

---

# 5. Personnalisation du Serveur OPC UA  

## 5.1 Modification du fichier de configuration  
- Le fichier **`opcua_config.json`** permet de définir les variables exposées par OPC UA.  

## 5.2 Redémarrage du serveur OPC UA  
Pour appliquer les modifications :  

```bash
pkill opcua_server
gcc -std=c99 -I/usr/local/include -L/usr/local/lib -o opcua_server opcua_server.c -lopen62541 -lcjson
./opcua_server &
```

---

# 6. Vérification et Accès aux Services  

## 6.1 Accès aux Interfaces Web  

| Service      | URL d’accès |
|-------------|------------|
| phpMyAdmin  | `https://pma.iiotvm.publicvm.com` |
| Streamlit   | `https://streamlit.iiotvm.publicvm.com` |
| Node-RED    | `https://nodered.iiotvm.publicvm.com` |
| Portainer   | `https://portainer.iiotvm.publicvm.com` |

📌 Remplacez `iiotvm.publicvm.com` par votre domaine personnalisé.  

## 6.2 Gestion des Conteneurs Docker  

Pour consulter les logs des services :  

```bash
docker-compose logs -f
```

## 6.3 Gestion du Serveur OPC UA  

Pour arrêter ou redémarrer le serveur OPC UA :  

```bash
pkill opcua_server
./opcua_server &
```

---

# 7. Conclusion  

L’environnement **IIOTVM** est désormais opérationnel, intégrant :  
✅ Une infrastructure **Docker-Compose** avec **Traefik** et SSL.  
✅ Un **serveur OPC UA** configurable via JSON.  
✅ Un écosystème IIoT fonctionnel prêt à être personnalisé.
