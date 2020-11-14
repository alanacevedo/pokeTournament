from pokemon import Pokemon
import time  # time.sleep() will be used to slow down a bit and make the messages readable

def fight(poke1: Pokemon, poke2: Pokemon) -> tuple:
    """
    Makes poke1 attack poke2. Displays health for both Pokemon before the attack and
    then a message showing the attack. If a pokemon faints, returns the winner and loser.
    If no pokemon faints, returns (None, None).

    :param poke1: (Pokemon) The attacking Pokemon
    :param poke2: (Pokemon) The Pokemon being attacked
    :return: (tuple[Pokemon, Pokemon]) Winner and loser, (None, None) if no Pokemon faints.
    """
    damage_dealt = poke1.attack_enemy(poke2)
    print(f"{poke1.name} attacks {poke2.name} and deals {damage_dealt} damage!\n")
    return (poke1, poke2) if not poke2.isAlive else (None, None)


def match_up(poke1: Pokemon, poke2: Pokemon) -> Pokemon:
    """
    Simulates a round of the tournament. Makes both Pokemon attack each other until
    one of them faints. When this happens, displays a message indicating the winner and loser.
    Returns the winner.

    :param poke1: (Pokemon) First Pokemon
    :param poke2: (Pokemon) Second Pokemon
    :return winner: (Pokemon) Pokemon who won the match
    """
    winner, loser = None, None
    # Pokemon speed determines who attacks first
    attacker, defender = (poke1, poke2) if poke1.speed >= poke2.speed else (poke2, poke1)
    print(f"{attacker.name} is faster and gets the first attack!\n")
    time.sleep(1.5)

    while (winner is None):
        print(f"{poke1.name}'s HP = {poke1.current_hp}     {poke2.name}'s HP = {poke2.current_hp} ")
        (winner, loser) = fight(attacker, defender)
        (attacker, defender) = (defender, attacker)
        time.sleep(1.5)

    print(f"{loser.name} faints!\n{winner.name} is victorious!")
    return winner


def advance_stage(stage: str, participant_list: list) -> list:
    """
    Advances and displays a stage of the tournament (e.g. Semi Finals).

    :param stage: (str) Stage to be carried out
    :param participant_list: (list[Pokemon]) List of Pokemon participating in this stage
    :return winner_list: (list[Pokemon]) List of Pokemon who advance to the next stage
    """
    poke_list = participant_list.copy()
    winner_list = []

    for match in range(len(poke_list) // 2):
        poke1 = poke_list.pop(0)
        poke2 = poke_list.pop(0)
        print(f"\n{'#' * 5}  {stage} - Match {match + 1}  {'#' * 5} \n"
              f"{'#' * 5}{' ' * 4}{poke1.name} Vs. {poke2.name}!{' ' * 4}{'#' * 5}\n")
        time.sleep(2.5)
        winner = match_up(poke1, poke2)
        winner_list.append(winner)
        time.sleep(1.5)

    for poke in winner_list:
        poke.restore_health()

    return winner_list


def display_poke_list(poke_list: list) -> None:
    """
    Displays all Pokemon names from a list.

    :param poke_list: (list[Pokemon]) A list of Pokemon
    """
    for i in range(len(poke_list) - 1):
        print(pokemon_list[i].name, end=", ")
    print(f"and {pokemon_list[-1].name}!")
    time.sleep(1.5)


def display_tournament_state(quarters_list: list, semis_list: list = None, finals_list: list = None) -> None:
    """
    Displays an ascii-art image representing the current tournament state. If it isn't know which Pokemon will
    participate in a certain stage of the tournament, '????????' will be displayed instead of a name.

    :param quarters_list: (list[str]) List containing Quarter Finals participants
    :param semis_list: (list[str]) (optional) List containing Semi Finals participants
    :param finals_list: (list[str]) (optional) List containing Finals participants
    """
    qrt = [poke.name for poke in quarters_list]

    if semis_list:
        semis = [poke.name for poke in semis_list]
    else:
        semis = ["????????" for _ in range(1, 5)]

    if finals_list:
        finals = [poke.name for poke in finals_list]
    else:
        finals = ["????????" for _ in range(1, 3)]

    print(f"\n                                           Champion                                                  \n"
          f"                                               |                                                       \n"
          f"                         --------------------------------------------------                            \n"
          f"                         |                  Finals                        |                            \n"
          f"                    {finals[0]}                                           {finals[1]}                  \n"
          f"                         |                                                |                            \n"
          f"              -----------------------                         -------------------------                \n"
          f"              |       Semis 1       |                         |        Semis 2        |                \n"
          f"           {semis[0]}               {semis[1]}                 {semis[2]}                {semis[3]}    \n"
          f"              |                     |                         |                       |                \n"
          f"      -------------           ------------              ------------            --------------         \n"
          f"      |           |           |          |              |          |            |            |         \n"
          f"   {qrt[0]}     {qrt[1]}      {qrt[2]}    {qrt[3]}      {qrt[4]}   {qrt[5]}       {qrt[6]}    {qrt[7]} \n")
    time.sleep(3)


if __name__ == "__main__":
    print("Scouting 8 Pokemon to participate in the tournament...\n")

    pokemon_list: list = [Pokemon() for _ in range(8)]

    print("The chosen Pokemon are:")
    display_poke_list(pokemon_list)
    display_tournament_state(pokemon_list)

    semis_pokemon: list = advance_stage("Quarter Finals", pokemon_list)

    print("\nThe Pokemon advacing to Semi Finals are:")
    display_poke_list(semis_pokemon)
    display_tournament_state(pokemon_list, semis_pokemon)

    finals_pokemon: list = advance_stage("Semi Finals", semis_pokemon)

    print("\nThe Pokemon advacing to Finals are:")
    display_poke_list(finals_pokemon)
    display_tournament_state(pokemon_list, semis_pokemon, finals_pokemon)

    champion: Pokemon = advance_stage("Finals", finals_pokemon)[0]

    print(f"\nThe champion of the tournament is {champion.name}, congratulations!\n"
          f"""
                          ___________
                         '._==_==_=_.'
                         .-\:      /-.
                        | (|:.     |) |
                         '-|:.     |-'
                           \::.    /
                            '::. .'
                              ) (
                            _.' '._
                         ''''''''''''''
        """)
