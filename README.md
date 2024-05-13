# Bot Discord

## Qu'est-ce que ce projet ?
Ce projet consiste à créer un bot Discord avec diverses fonctionnalités telles que le lancement en ligne de commande (CLI), la gestion des paramètres via la console, la configuration à l'aide d'un fichier dédié, la journalisation des actions du bot dans des fichiers de logs, et la mise en place d'une liste de commandes avec un !help pour afficher les commandes disponibles. Le tout est développé en programmation orientée objet.

## Qu'est-ce qu'un bot Discord ?
Un bot Discord est un programme automatisé qui interagit avec les utilisateurs via la plateforme Discord. Il peut effectuer diverses actions en réponse à des commandes ou des événements spécifiques.

## Qu'est-ce que le logging et à quoi servent les logs ?
Le logging est le processus d'enregistrement des activités et des événements survenant dans un système. Les logs sont utiles pour le suivi, le débogage et la sécurité, car ils fournissent un historique des actions effectuées par le bot, ce qui permet de diagnostiquer les problèmes et de surveiller son comportement.

## Configuration
Avant de commencer, vous devez créer une application sur le portail de Discord et lier votre bot au serveur Discord de votre choix. Suivez les étapes ci-dessous :

1. Créez une application sur le portail de Discord.
2. Cliquez sur "New Application".
3. Sélectionnez "Bot" puis "New Bot".
4. Dans l'Oauth2 Url Generator, cliquez sur "Bot" et "Administrator".
5. Copiez l'URL généré dans votre navigateur.
6. Liez le bot au serveur Discord souhaité.
7. Cliquez sur "Continuer" et autorisez l'accès.

Une fois ces étapes effectuées, le bot rejoindra le canal #general de votre serveur Discord.

## Installation des dépendances Python et Discord
```bash
pip install discord
```
```python
import discord
from discord import Client
```

## Utilisation en ligne de commande (CLI)
Ce projet utilise ArgumentParser pour gérer les paramètres de ligne de commande.

```python
from argparse import ArgumentParser

def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-c", "--config", help="Config file", required=True, dest="config"
    )
    return parser.parse_args()
```

## Journalisation (Logging)
Un tutoriel pour la journalisation est disponible [ici](https://docs.python.org/3/howto/logging.html).


---

**Note**: Assurez-vous d'avoir installé Python et les dépendances requises avant d'exécuter le bot Discord.
