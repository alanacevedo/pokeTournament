from pokemon import Pokemon

def fight(poke1: Pokemon, poke2: Pokemon):
    """
    Makes poke1 attack poke2. Displays health for both Pokemon before the attack and
    then a message showing the attack. If a pokemon faints, returns the winner and loser.
    If no pokemon faints, returns (None, None).

    :param poke1: (Pokemon) The attacking Pokemon
    :param poke2: (Pokemon) The Pokemon being attacked
    :return: (tuple[Pokemon, Pokemon]) Winner and loser, (None, None) if no Pokemon faints.
    """
    print(f"{poke1.name}'s HP = {poke1.hp}     {poke2.name}'s HP = {poke2.hp} ")
    damage_dealt = poke1.attack_enemy(poke2)
    print(f"{poke1.name} attacks {poke2.name} and deals {damage_dealt} damage!\n")
    return (poke1, poke2) if not poke2.isAlive else (None, None)


def match_up(poke1: Pokemon, poke2: Pokemon) -> None:
    """
    Simulates a round of the tournament. Makes both Pokemon attack each other until
    one of them faints. When this happens, displays a message indicating the winner and loser.

    :param poke1: (Pokemon) First Pokemon
    :param poke2: (Pokemon) Second Pokemon
    """
    # Pokemon speed determines who attacks first
    winner, loser = None, None
    attacker, defender = (poke1, poke2) if poke1.speed >= poke2.speed else (poke2, poke1)
    print(f"{attacker.name} is faster and gets the first attack!")

    while (winner is None):
        (winner, loser) = fight(poke1, poke2)
        (attacker, defender) = (defender, attacker)

    print(f"{loser.name} faints!\n{winner.name} is victorious!")


if __name__ == "__main__":
    print("Scouting 8 Pokemon to participate in the tournament...\n")

    pokemon_list = [Pokemon() for _ in range(8)]

    print("The chosen Pokemon are:")
    for i in range(7):
        print(pokemon_list[i].name, end=" ")
    print("\n")

    match_up(pokemon_list[1], pokemon_list[3])
