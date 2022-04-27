from glitch_mon import GlitchMon
from pokemon import Charmander, Bulbasaur, Squirtle
from pokemon_base import PokemonBase


class Giratina(GlitchMon):
    def __init__(self):
        averageHp = int((Charmander().get_hp() + Bulbasaur().get_hp() + Squirtle().get_hp()) / 3)
        GlitchMon.__init__(self, averageHp, "Giratina")
        self.name = 'Giratina'
        self.attack = int((Charmander().get_hp() + Bulbasaur().get_hp() + Squirtle().get_hp()) / 3)
        self.defence = int((Charmander().get_hp() + Bulbasaur().get_hp() + Squirtle().get_hp()) / 3)
        self.speed = int((Charmander().get_hp() + Bulbasaur().get_hp() + Squirtle().get_hp()) / 3)

    def get_name(self) -> str:
        return self.name

    def get_attack(self) -> int:
        return self.attack + (self.level - 1)

    def get_defence(self) -> int:
        return self.defence + self.level - 1

    def get_speed(self) -> int:
        return self.speed + self.level - 1

    def calculate_damage_taken(self, opponent: PokemonBase) -> int:
        effective_damage = opponent.get_attack() * 1
        if effective_damage > self.get_defence():
            return effective_damage
        else:
            return effective_damage // 2

    # TODO: make sure Giratina can only be put into battle ONCE (append thru the stack/queue/list and check for other instances)
    # TODO: add Giratina to the back of the queue/stack/list in each mode
    # TODO: make sure Giratina has a 25% chance of using superpower

if __name__ == "__main__":
    charm = Charmander()
    hp = charm.__str__()
    gir = Giratina()
    print(gir.get_attack())
    gir.level_up()
    gir.level_up()
    gir.level_up()
    gir.level_up()
    gir.level_up()
    gir.level_up()
    print(gir.get_attack())
    print(gir.get_hp())
    print(Charmander().get_hp())
    print(Squirtle().get_hp())
    print(Bulbasaur().get_hp())

