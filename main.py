"""
RobiBot - Fichier principal
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fichier contenant le code pour démarrer le bot.
"""

# Importation des modules
import discord
from discord.ext import commands
import os
import yaml
import asyncio
import logging


logging.basicConfig(level=logging.INFO)


def read_config(file_name: str) -> dict:
    """Récupère les informations de configuration du fichier YAML.

    Args:
        file_name (str): Nom du fichier YAML.

    Raises:
        FileNotFoundError: Si le fichier n'est pas trouvé.
        Exception: Si une autre erreur survient.

    Returns:
        dict: Dictionnaire contenant les informations de configuration.
    """
    # Essayer d'ouvrir le fichier
    try:
        with open(file_name, "r") as config_file:
            return yaml.safe_load(config_file)
    # Si le fichier n'est pas trouvé, lever une FileNotFoundError
    except FileNotFoundError:
        raise FileNotFoundError("Fichier de configuration introuvable")
    # Si une autre erreur survient, lever une Exception
    except:
        raise Exception(
            "Une erreur est survenue lors de la lecture du fichier de configuration")


def read_extensions(folder_name: str) -> list:
    """Récupère la liste des extensions à charger.

    Args:
        folder_name (str): Nom du dossier contenant les extensions.

    Raises:
        NotADirectoryError: Si le dossier n'existe pas.
        FileNotFoundError: Si le dossier n'est pas un dossier.

    Returns:
        list: Liste des extensions à charger.
    """
    # Initialisation de la liste contenant les noms des fichiers d'extensions
    ext_files = []
    # Vérification de l'existence du dossier
    if os.path.exists(folder_name):
        # Vérification que le dossier est un dossier
        if os.path.isdir(folder_name):
            # Parcours du dossier pour récupérer les fichiers python
            for file in os.listdir(folder_name):
                if file.endswith(".py"):
                    # Ajout du nom du fichier dans la liste sans l'extension
                    ext_files.append(f"{folder_name}.{file[:-3]}")
        # Si le dossier n'est pas un dossier, on lève une exception
        else:
            raise NotADirectoryError(f"{folder_name} n'est pas un dossier!")
    # Si le dossier n'existe pas, on lève une exception
    else:
        raise FileNotFoundError(f"{folder_name} n'existe pas!")
    # Retourne la liste des noms des fichiers d'extensions
    return ext_files


if __name__ == "__main__":
    # Création du bot
    client = commands.Bot(command_prefix="!",
                          intents=discord.Intents.default(), help_command=None)

    # Récupération des informations de configuration
    try:
        config = read_config("settings.yaml")
    except FileNotFoundError:
        config = read_config("settings.yml")

    # Récupération des noms des fichiers d'extensions
    extensions_files = read_extensions("extensions")

    @client.event
    async def on_ready() -> None:
        """Fonction appelée lorsque le bot est prêt."""
        # Synchronisation des commandes slash
        await client.tree.sync()

        # Confirmation de la connexion
        print("Le bot est prêt!")

    async def main() -> None:
        """Fonction principale du bot."""
        # Chargement des extensions
        for file in extensions_files:
            try:
                await client.load_extension(file)
                print(f"{file} a été chargé avec succès.")
            except Exception as error:
                print(f"{file} n'a pas pu être chargé : {error}")

        # Lancement du bot
        await client.start(config["Token"])

    asyncio.run(main())  # Lancement de la fonction principale
