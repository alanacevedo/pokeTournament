import random
import requests

class Pokemon:
    """
    Class that represents a Pokemon.

    Attributes:
        id (int): National number of the Pokemon
        name (str): Name of the Pokemon
        defense (str): Defense points of the Pokemon
        attack (str): Attack points of the Pokemon
        hp (str): Health points of the Pokemon
        types (list[str]): List containing this Pokemon's types
        dd_types (list[str]): List containing the types which take double damage from this Pokemon.
        hd_types (list[str]): List containing the types which take half damage from this Pokemon.
        nd_types (list[str]): List containing the types which take no damage from this Pokemon.

    """

    def __init__(self):
        self.id: int = random.randint(1, 151)
        poke_url = f"https://pokeapi.co/api/v2/pokemon/{self.id}"
        data: dict = requests.request("GET", poke_url).json()

        self.name: str = data["name"]

        for dicc in data["stats"]:
            stat: str = dicc["stat"]["name"]
            value = int(dicc["base_stat"])

            if stat == "defense":
                self.defense = value
            elif stat == "attack":
                self.attack = value
            elif stat == "hp":
                self.hp = value

        self.types: list[str] = [dicc["type"]["name"] for dicc in data["types"]]

        for type in self.types:
            type_url = f"https://pokeapi.co/api/v2/type/{type}"
            damage_data: dict = requests.request("GET", type_url).json()["damage_relations"]

            self.dd_types: list[str] = [type["name"] for type in damage_data["double_damage_to"]]
            self.hd_types: list[str] = [type["name"] for type in damage_data["half_damage_to"]]
            self.nd_types: list[str] = [type["name"] for type in damage_data["no_damage_to"]]

