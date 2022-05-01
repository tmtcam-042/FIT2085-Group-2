import random

from pokemon_base import PokemonBase
from poke_team import PokeTeam
from sorted_list import ListItem


class Battle:
    def __init__(self, trainer_one_name: str, trainer_two_name: str):
        """
        Constructor for Battle
        :param trainer_one_name: 1st trainers name
        :param trainer_two_name: 2nd trainers name
        """
        self.team1 = PokeTeam(trainer_one_name)
        self.team2 = PokeTeam(trainer_two_name)
        self.battle_mode = None

    def set_battle_mode_to(self, value: int) -> None:
        """
        method to alter the battle mode value
        :param value: value to set the battle mode to
        :return: None - it does not return anything
        """
        if 0 <= value <= 2:
            self.battle_mode = value
        else:
            raise Exception("Unexpected battle mode value")

    # Task 3, set_mode_battle is a battle mode just like rotating mode and optimised mode
    def set_mode_battle(self) -> str:
        """
        Sets battle mode to 0 and asks players to choose their team
        It then begins the fight
        :return: returns as a string the trainers name who won, otherwise DRAW
        """
        self.set_battle_mode_to(0)
        self.team1.choose_team()
        self.team2.choose_team()

        # FIGHT
        # loop continues till each team has at least 1 pokemon
        while len(self.team1) > 0 and len(self.team2) > 0:
            pokemon1 = self.team1.remove()  # normalised method remove, to get a pokemon from the ADT - for player 1
            pokemon2 = self.team2.remove()  # normalised method remove, to get a pokemon from the ADT - for player 2
            
            self.fight(pokemon1, pokemon2)  # make both pokemons fight

            if pokemon1.get_hp() > 0:
                # if pokemon 1 still has some hp, add it back to the ADT
                self.team1.push(pokemon1)
            if pokemon2.get_hp() > 0:
                # if pokemon 2 still has some hp, add it back to the ADT
                self.team2.push(pokemon2)

        # Return winner (trainer name) or draw
        if len(self.team1) > 0:
            return self.team1.trainer_name
        elif len(self.team2) > 0:
            return self.team2.trainer_name
        else:
            return "DRAW"

    def rotating_mode_battle(self) -> str:  # circular queues
        """Method for handling rotating battle mode. In this battle mode, the teams
        cycle after each fight, with the fighting pokemon moving to the end of the list.
        The corresponding battle mode number for rotating battle mode is 1, and it employs
        a Queue ADT.

        :complexity: O(n) worst and best case, where n is max(len(self.team1), len(self.team2))
        :pre:
        :return: string containing the winning team, or DRAW in case of a tie
        """

        self.set_battle_mode_to(1)
        self.team1.choose_team(1)
        self.team2.choose_team(1)

        while len(self.team1) > 0 and len(self.team2) > 0:

            pokemon1 = self.team1.team.serve()
            pokemon2 = self.team2.team.serve()

            self.fight(pokemon1, pokemon2)

            if pokemon1.get_hp() > 0:
                self.team1.team.append(pokemon1)
            if pokemon2.get_hp() > 0:
                self.team2.team.append(pokemon2)

        # Return winner or draw
        if len(self.team1) > 0:
            return self.team1.trainer_name
        elif self.team2.team.length > 0:
            return self.team2.trainer_name
        else:
            return "DRAW"

    def optimised_mode_battle(self, criterion_team1: str, criterion_team2: str) -> str:  # Task 5
        """Method for handling optimised battle mode. In this battle mode, the teams are constantly sorted
        by a user-specified attribute to order their team in non-increasing order. The battle mode number for this mode
        is 2, and it employs a sorted_list ADT.

        :pre: criterions are both strings, and one of lvl, hp, attack, defence, or speed. Not case sensitive.
        :raises Exception: valueError if an invalid criterion is passed.
        :param criterion_team1: Sorting criterion. Can be one of: lvl, hp, attack, defence, speed
        :param criterion_team2: Sorting criterion. Can be one of: lvl, hp, attack, defence, speed
        :return: string containing the winning team, or DRAW in case of a tie
        """

        criterion_list = ["lvl", "hp", "attack", "defence", "speed"]
        if criterion_team1.lower() not in criterion_list:
            raise ValueError("Criterion 1 invalid, not one of lvl, hp, attack, defence, or speed")
        if criterion_team2.lower() not in criterion_list:
            raise ValueError("Criterion 2 invalid, not one of lvl, hp, attack, defence, or speed")

        criterion_team1 = criterion_team1.lower()
        criterion_team2 = criterion_team2.lower()

        self.set_battle_mode_to(2)
        self.team1.choose_team(self.battle_mode, criterion_team1)
        self.team2.choose_team(self.battle_mode, criterion_team2)

        # FIGHT
        while len(self.team1) > 0 and len(self.team2) > 0:

            pokemon1 = self.team1.remove()  # Remove the item at the head of each list
            pokemon2 = self.team2.remove()

            self.fight(pokemon1, pokemon2)

            if pokemon1.get_hp() > 0:
                self.team1.team.add(ListItem(pokemon1, pokemon1.get_criterion(criterion_team1)))
                if pokemon2.get_hp() <= 0:
                    print(f"{pokemon2.get_name()} is unable to battle!\n")
            if pokemon2.get_hp() > 0:
                self.team2.team.add(ListItem(pokemon2, pokemon2.get_criterion(criterion_team2)))
                if pokemon1.get_hp() <= 0:
                    print(f"{pokemon1.get_name()} is unable to battle!\n")




        # Return winner or draw
        if len(self.team1) > 0:
            return self.team1.trainer_name
        elif len(self.team2) > 0:
            return self.team2.trainer_name
        else:
            return "DRAW"

    def fight(self, pokemon1: PokemonBase, pokemon2: PokemonBase,) -> None:

        
        print(f"{self.team1.trainer_name} chooses {pokemon1.get_name()}")
        print(f"{self.team2.trainer_name} chooses {pokemon2.get_name()}")

        if pokemon1.get_speed() > pokemon2.get_speed():  # P1 fights P2 first, then P2 defends
            print(f"{pokemon1.get_name()} uses Attack!")
            print(f"{pokemon2.get_name()} uses Defend!")
            # pokemon2.set_hp(pokemon2.get_hp() - pokemon2.calculate_damage_taken(pokemon1))
            pokemon2.got_hurt_by(pokemon1)

            if pokemon2.get_hp() > 0:
                # if said pokemon is giratina and the randon num is 0, use superpower class
                num = 0 # TODO: change this to make it random int

                if pokemon2.poke_type == "Unknown" and num == 0:
                    pokemon2.superpower()
                # pokemon1.set_hp(pokemon1.get_hp() - pokemon1.calculate_damage_taken(pokemon2))
                pokemon1.got_hurt_by(pokemon2)

            else:
                pokemon1.set_level(pokemon1.get_level() + 1)

        elif pokemon1.get_speed() < pokemon2.get_speed():  # P2 fights P1 first, then P1 has chance to retaliate.
            print(f"{pokemon2.get_name()} uses Attack!")
            print(f"{pokemon1.get_name()} uses Defend!")
            # pokemon1.set_hp(pokemon1.get_hp() - pokemon1.calculate_damage_taken(pokemon2))
            pokemon1.got_hurt_by(pokemon2)

            if pokemon1.get_hp() > 0:
                num = random.randint(0,3)

                if pokemon2.poke_type == "Unknown" and num == 0:
                    pokemon2.superpower()
                # pokemon2.set_hp(pokemon2.get_hp() - pokemon2.calculate_damage_taken(pokemon1))
                pokemon2.got_hurt_by(pokemon1)

            else:
                # pokemon2.set_level(pokemon2.get_level() + 1)
                pokemon2.level_up()

        else:  # Both fight at same time!
            print("Both Pokemon attack!")
            pokemon1.set_hp(pokemon1.get_hp() - pokemon1.calculate_damage_taken(pokemon2))  # P1 takes damage
            pokemon2.set_hp(pokemon2.get_hp() - pokemon2.calculate_damage_taken(pokemon1))  # P2 takes damage
            # Check conditions.
            if pokemon1.get_hp() > 0 and pokemon2.get_hp() > 0:  # Did both survive mutual clash
                pokemon1.set_hp(pokemon1.get_hp() - 1)  # Both lose 1 hp for the sin of surviving
                pokemon2.set_hp(pokemon2.get_hp() - 1)
                if pokemon1.get_hp() > 0 and pokemon2.get_hp() > 0:
                    pass
                elif pokemon1.get_hp() > 0:
                    pokemon1.level_up()
                else:
                    pokemon2.level_up()

            elif pokemon1.get_hp() > 0:  # P1 lived and P2 didn't
                pokemon1.level_up()
            else:  # P2 lived and P1 didn't
                pokemon2.level_up()

        print(f"{pokemon1.get_name()} hp: {str(pokemon1.get_hp())}")
        print(f"{pokemon2.get_name()} hp: {str(pokemon2.get_hp())}\n")


if __name__ == "__main__":
    # ================= EXAMPLE APP EXECUTION =================
    b = Battle("Ash", "Gary")
    print(b.set_mode_battle())
    # print(b.rotating_mode_battle())
    #print(b.optimised_mode_battle("hp", "lvl"))



