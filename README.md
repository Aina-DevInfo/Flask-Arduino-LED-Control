Nom du Projet : Flask-Arduino-LED-Control

Description :

Ce projet est une application web développée avec Flask permettant de contrôler une LED connectée à une carte Arduino via une interface utilisateur sécurisée. L'application inclut une authentification utilisateur, une gestion de sessions, et une communication série avec l'Arduino pour allumer/éteindre une LED et lire les données d'une photorésistance. Le projet est conçu pour fonctionner avec une simulation dans Proteus ou du matériel Arduino physique.

Fonctionnalités principales :

    Authentification utilisateur : Connexion sécurisée avec gestion de sessions et messages flash pour les erreurs/succès.
    Contrôle de LED : Allumer/éteindre une LED via des routes /on et /off en envoyant des commandes série à l'Arduino.
    Lecture de photorésistance : Récupération des données de la photorésistance via la route /photoresistance.
    Gestion des erreurs : Gestion robuste des erreurs de connexion série avec l'Arduino.
    Interface utilisateur : Pages web simples (login.html et index.html) pour l'interaction utilisateur.

Technologies utilisées :

    Backend : Flask (Python) pour le serveur web.
    Communication série : Bibliothèque pyserial pour interagir avec l'Arduino.
    Frontend : HTML (templates Flask) pour l'interface utilisateur.
    Matériel/Simulation : Arduino connecté sur le port COM2 (configurable) ou simulé dans Proteus.

Prérequis :

    Python 3.x avec les bibliothèques Flask et pyserial (pip install flask pyserial).
    Arduino avec un firmware configuré pour recevoir des commandes série (0 pour éteindre, 1 pour allumer) et envoyer des données de photorésistance.
    Port série disponible (par exemple, COM2) ou simulation Proteus configurée.

Installation et exécution :

    Clonez le dépôt : git clone <URL-du-dépôt>.
    Installez les dépendances : pip install -r requirements.txt.
    Connectez l'Arduino au port série spécifié (par défaut COM2).
    Lancez l'application : python app.py.
    Accédez à l'application via http://localhost:5000.

Utilisation :

    Connectez-vous avec un utilisateur prédéfini (par exemple, admin/solofo1.).
    Depuis le tableau de bord, contrôlez la LED ou lisez les données de la photorésistance.

Notes :

    Le dictionnaire users est utilisé pour une authentification simple (à remplacer par une base de données en production).
    Assurez-vous que l'Arduino est configuré pour communiquer à 9600 bauds.
    Le mode debug est désactivé pour une exécution stable.

Améliorations possibles :

    Intégration d'une base de données pour la gestion des utilisateurs.
    Ajout d'une interface utilisateur plus avancée (CSS/JavaScript).
    Support multi-plateformes pour différents ports série.