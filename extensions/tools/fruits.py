"""
RobiBot - Fruits.py
~~~~~~~~~~~~~~~~~~~
Fichier contenant la classe Fruit et les fonctions list_fruits et random_fruit
Fonctions servant à récupérer des informations sur les fruits
"""

__author__ = "RobiPoire"


from requests import get
from json import loads
from random import choice
import logging
import csv


class Fruit():
    """Classe Fruit, permettant de récupérer la description et l'image d'un fruit"""

    def __init__(self, name: str, csv_file: str):
        """Création de l'objet Fruit

        Args:
            name (str): Nom du fruit
            csv_file (str, optional): Chemin vers le fichier CSV.
        """
        self.name = name
        self.csv_file = csv_file
        self.__csv_exists()  # Vérification de l'existence du fichier CSV
        self.description = self.__set_description()
        self.image_url = self.__set_image()

    def __csv_exists(self) -> bool:
        """Vérifie si le fichier CSV existe

        Returns:
            bool: True si le fichier existe, False sinon
        """
        try:
            open(self.csv_file)
            return True
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Le fichier \"{self.csv_file}\" n'a pas été trouvé")

    def __set_description(self) -> str | None:
        """Récupère la description du fruit dans le fichier csv

        Returns:
            str | None: Description du fruit ou None si le fruit n'est pas trouvé
        """
        with open(self.csv_file) as csv_file:  # Ouverture du fichier
            # Création d'un lecteur de fichier CSV
            reader = csv.reader(csv_file, delimiter=';')
            next(reader)  # On saute la première ligne (les titres)
            for row in reader:  # Pour chaque ligne du fichier
                if row[0] == self.name:  # Si le nom du fruit est trouvé
                    return row[1]  # On retourne la description
            logging.warning(
                f"Le fruit \"{self.name}\" n'a pas été trouvé dans le fichier \"{self.csv_file}\"")
            return None  # Si le fruit n'est pas trouvé, on retourne None

    def __set_image(self) -> str | None:
        """Récupère une image du fruit sur Qwant

        Returns:
            str | None: URL de l'image ou None si l'image n'a pas été trouvée
        """
        # Paramètres de la requête
        search_url = "https://api.qwant.com/v3/search/images"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"}
        params = {
            "count": 20,
            "q": self.name,
            "safesearch": "1",
            "locale": "fr_FR",
        }
        # Nombre d'essais
        max_tries = 5
        while max_tries > 0:  # Tant qu'il reste des essais
            try:
                # Envoi de la requête
                response = get(search_url, headers=headers, params=params)
                # Récupération des images
                image_urls = loads(response.text)["data"]["result"]["items"]
                # Retourner l'image
                return choice(image_urls)["media"]
            except Exception as e:  # Si une erreur survient
                logging.debug(
                    f"Erreur lors de la récupération de l'image de \"{self.name}\" : {e}")
                max_tries -= 1  # On enlève un essai
        # On log l'erreur
        logging.warning(f"Impossible de récupérer l'image de \"{self.name}\"")
        return None  # On retourne None si on a épuisé les essais

    def get_name(self) -> str:
        """Retourne le nom du fruit

        Returns:
            str: Nom du fruit
        """
        return self.name

    def get_description(self) -> str:
        """Retourne la description du fruit

        Returns:
            str: Description du fruit
        """
        return self.description

    def get_image(self) -> str:
        """Retourne l'URL de l'image du fruit

        Returns:
            str: URL de l'image du fruit
        """
        return self.image_url

    def __str__(self) -> str:
        """Retourne une chaîne de caractères contenant les informations du fruit

        Returns:
            str: Chaîne de caractères contenant les informations du fruit
        """
        return f"Nom: {self.name}\nDescription: {self.description}\nImage: {self.image_url}"


def list_fruits(csv_file: str) -> list:
    """Retourne la liste des fruits

    Args:
        csv_file (str): Fichier CSV contenant les fruits

    Returns:
        list: Liste des fruits
    """
    with open(csv_file) as file:
        fruits = [line.split(';')[0] for line in file]
        fruits.pop(0)
    return fruits


def random_fruit(csv_file: str) -> Fruit:
    """Retourne un fruit aléatoire

    Args:
        csv_file (str): Fichier CSV contenant les fruits

    Returns:
        Fruit: Fruit aléatoire
    """
    fruits = list_fruits(csv_file)
    fruit = choice(fruits)
    return Fruit(fruit, csv_file)
