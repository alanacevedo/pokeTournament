import random
import requests
import typing

class Pokemon:
    """
    Class that represents a Pokemon. When instanced, selects a random Pokemon from the first
    151 and gets its info from pokeAPI via GET requests.

    Attributes:
        id (int): National number of the Pokemon
        name (str): Name of the Pokemon
        defense (int): Defense points of the Pokemon
        attack (int): Attack points of the Pokemon
        max_hp (int): Maximum health points of the Pokemon
        current_hp (int): Current health points of the Pokemon
        speed (int): Speed points of the Pokemon
        isAlive (bool): Boolean value indicating if the Pokemon is alive or not.
        types (list[str]): List containing this Pokemon's types
        dd_types (list[str]): List containing the types which take double damage from this Pokemon.
        hd_types (list[str]): List containing the types which take half damage from this Pokemon.
        nd_types (list[str]): List containing the types which take no damage from this Pokemon.

    Methods:
        attack_enemy(enemy: Pokemon)->int : Attacks another Pokemon and returns the damage dealt
        heal_hp()->None: Heals Pokemon to full Health

    """

    def __init__(self):
        self.id: int = random.randint(1, 151)
        poke_url = f"https://pokeapi.co/api/v2/pokemon/{self.id}"
        data: dict = requests.request("GET", poke_url).json()

        self.name: str = data["name"].capitalize()

        for dicc in data["stats"]:
            stat: str = dicc["stat"]["name"]
            value = int(dicc["base_stat"])

            if stat == "defense":
                self.defense = value
            elif stat == "attack":
                self.attack = value
            elif stat == "hp":
                self.max_hp = value
                self.current_hp = value
                self.isAlive = True
            elif stat == "speed":
                self.speed = value

        self.types: list[str] = [dicc["type"]["name"] for dicc in data["types"]]

        for type in self.types:
            type_url = f"https://pokeapi.co/api/v2/type/{type}"
            damage_data: dict = requests.request("GET", type_url).json()["damage_relations"]

            self.dd_types: list[str] = [type["name"] for type in damage_data["double_damage_to"]]
            self.hd_types: list[str] = [type["name"] for type in damage_data["half_damage_to"]]
            self.nd_types: list[str] = [type["name"] for type in damage_data["no_damage_to"]]

    def attack_enemy(self, enemy) -> int:
        """
        This method reduces enemy's health depending on both Pokemon's stats
        and types. Returns the health substracted to enemy.

        :param enemy: (Pokemon) The Pokemon to be attacked
        :return damage_done: (int) The damage dealt to the Pokemon
        """
        variance = random.randint(0, 5)  # This will give a bit of randomness to the attack
        brute_damage = self.attack - int(enemy.defense * 0.5)
        damage_dealt = max(brute_damage, 0) + variance

        # Checks if a damage modifier should be applied to this attack.
        #a
        if any(type_ in self.dd_types for type_ in enemy.types):
            damage_dealt *= 2
        elif any(type_ in self.hd_types for type_ in enemy.types):
            damage_dealt //= 2
        elif any(type_ in self.nd_types for type_ in enemy.types):
            damage_dealt = 0

        enemy.current_hp -= damage_dealt
        enemy.current_hp = max(enemy.current_hp, 0)
        if enemy.current_hp == 0:
            enemy.isAlive = False

        return damage_dealt

    def restore_health(self) -> None:
        """ Restores Pokemon to full HP """
        self.current_hp = self.max_hp
