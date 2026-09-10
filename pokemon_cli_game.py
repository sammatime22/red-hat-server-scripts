#!/usr/bin/env python3
"""
Pokemon CLI Game - A simplified Pokemon battle game mimicking Gold/Silver style
Features only Fire, Water, and Grass types with a 50-turn limit per battle.
"""

import random
import sys
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class Type(Enum):
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"


@dataclass
class Move:
    name: str
    power: int
    accuracy: float
    pokemon_type: Type
    description: str = ""

    def execute(self, attacker: "Pokemon", defender: "Pokemon") -> Dict:
        if random.random() > self.accuracy:
            return {"hit": False, "message": f"{attacker.name} used {self.name}, but missed!"}

        damage = self._calculate_damage(attacker, defender)
        damage = max(1, damage)
        defender.current_hp -= damage

        message = f"{attacker.name} used {self.name}! {defender.name} took {damage} damage."
        effectiveness = self._get_effectiveness_message(defender.pokemon_type)
        if effectiveness:
            message += f" {effectiveness}"

        return {
            "hit": True,
            "damage": damage,
            "message": message,
            "defender_hp": defender.current_hp,
        }

    def _calculate_damage(self, attacker: "Pokemon", defender: "Pokemon") -> int:
        base_damage = self.power
        stab_bonus = 1.5 if self.pokemon_type == attacker.pokemon_type else 1.0
        type_advantage = self._get_type_effectiveness(defender.pokemon_type)

        critical = 1.5 if random.random() < 0.0625 else 1.0
        damage = int(base_damage * stab_bonus * type_advantage * critical * 0.85)

        if critical > 1:
            critical_message = " Critical hit!"
        return damage

    def _get_type_effectiveness(self, defender_type: Type) -> float:
        effectiveness_chart = {
            Type.FIRE: {Type.GRASS: 2.0, Type.WATER: 0.5, Type.FIRE: 1.0},
            Type.WATER: {Type.FIRE: 2.0, Type.GRASS: 0.5, Type.WATER: 1.0},
            Type.GRASS: {Type.WATER: 2.0, Type.FIRE: 0.5, Type.GRASS: 1.0},
        }
        return effectiveness_chart.get(self.pokemon_type, {}).get(defender_type, 1.0)

    def _get_effectiveness_message(self, defender_type: Type) -> Optional[str]:
        effectiveness = self._get_type_effectiveness(defender_type)
        if effectiveness > 1.0:
            return "It's super effective!"
        elif effectiveness < 1.0:
            return "It's not very effective..."
        return None


@dataclass
class Pokemon:
    name: str
    pokemon_type: Type
    max_hp: int
    current_hp: int
    level: int
    moves: List[Move]

    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def get_random_move(self) -> Move:
        return random.choice(self.moves)

    def heal_full(self):
        self.current_hp = self.max_hp

    def __str__(self) -> str:
        return f"{self.name} (Lvl {self.level}) - {self.pokemon_type.value} Type"


class PokemonFactory:
    FIRE_MOVES = [
        Move("Ember", 40, 1.0, Type.FIRE, "A small flame attack"),
        Move("Flame Burst", 70, 1.0, Type.FIRE, "Bursts into flames"),
        Move("Fire Punch", 75, 1.0, Type.FIRE, "Powerful fire punch"),
    ]

    WATER_MOVES = [
        Move("Water Gun", 40, 1.0, Type.WATER, "A water spray attack"),
        Move("Bubble Beam", 65, 1.0, Type.WATER, "Rapid bubble attack"),
        Move("Surf", 90, 1.0, Type.WATER, "Massive water wave"),
    ]

    GRASS_MOVES = [
        Move("Razor Leaf", 55, 0.95, Type.GRASS, "Cutting leaves attack"),
        Move("Solar Beam", 120, 1.0, Type.GRASS, "Powerful sun attack"),
        Move("Vine Whip", 45, 1.0, Type.GRASS, "Whipping vines"),
    ]

    FIRE_POKEMON = [
        ("Cyndaquil", 39),
        ("Flareon", 42),
        ("Ponyta", 35),
        ("Vulpix", 33),
        ("Growlithe", 36),
    ]

    WATER_POKEMON = [
        ("Totodile", 39),
        ("Lapras", 45),
        ("Squirtle", 35),
        ("Psyduck", 33),
        ("Shellder", 36),
    ]

    GRASS_POKEMON = [
        ("Chikorita", 39),
        ("Exeggcute", 37),
        ("Oddish", 33),
        ("Bellsprout", 33),
        ("Tangela", 38),
    ]

    @classmethod
    def create_random_pokemon(cls, level: int = 10) -> Pokemon:
        pokemon_type = random.choice(list(Type))

        if pokemon_type == Type.FIRE:
            name, base_level = random.choice(cls.FIRE_POKEMON)
            moves = cls.FIRE_MOVES.copy()
        elif pokemon_type == Type.WATER:
            name, base_level = random.choice(cls.WATER_POKEMON)
            moves = cls.WATER_MOVES.copy()
        else:
            name, base_level = random.choice(cls.GRASS_POKEMON)
            moves = cls.GRASS_MOVES.copy()

        max_hp = base_level * 2 + level
        return Pokemon(
            name=name,
            pokemon_type=pokemon_type,
            max_hp=max_hp,
            current_hp=max_hp,
            level=level,
            moves=random.sample(moves, 2),
        )


class Battle:
    def __init__(self, player_pokemon: Pokemon, opponent_pokemon: Pokemon, max_turns: int = 50):
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon
        self.turn_count = 0
        self.max_turns = max_turns
        self.battle_log: List[str] = []
        self.game_over = False
        self.winner: Optional[str] = None

    def start(self):
        print("\n" + "=" * 60)
        print("POKEMON BATTLE START!")
        print("=" * 60)
        print(f"\nPlayer's Pokemon: {self.player_pokemon}")
        print(f"Opponent's Pokemon: {self.opponent_pokemon}")
        print("\n" + "-" * 60)

    def process_turn(self, player_move_choice: Optional[int] = None) -> bool:
        if self.game_over:
            return False

        self.turn_count += 1
        print(f"\n--- Turn {self.turn_count} ---")

        if player_move_choice is None:
            print("\nPlayer's Pokemon Moves:")
            for i, move in enumerate(self.player_pokemon.moves, 1):
                print(f"  {i}. {move.name} ({move.pokemon_type.value} Type) - Power: {move.power}")
            try:
                choice = int(input("Choose a move (1-2): ")) - 1
                if choice < 0 or choice >= len(self.player_pokemon.moves):
                    print("Invalid choice! Choosing randomly...")
                    choice = random.randint(0, len(self.player_pokemon.moves) - 1)
            except (ValueError, IndexError):
                print("Invalid input! Choosing randomly...")
                choice = random.randint(0, len(self.player_pokemon.moves) - 1)
            player_move = self.player_pokemon.moves[choice]
        else:
            player_move = self.player_pokemon.moves[player_move_choice]

        opponent_move = self.opponent_pokemon.get_random_move()

        player_speed = self.player_pokemon.level
        opponent_speed = self.opponent_pokemon.level

        if player_speed >= opponent_speed:
            player_result = player_move.execute(self.player_pokemon, self.opponent_pokemon)
            print(f"\n{player_result['message']}")
            print(f"{self.opponent_pokemon.name} HP: {self.opponent_pokemon.current_hp}/{self.opponent_pokemon.max_hp}")

            if self.opponent_pokemon.is_fainted():
                self._end_battle("Player")
                return False

            opponent_result = opponent_move.execute(self.opponent_pokemon, self.player_pokemon)
            print(f"\n{opponent_result['message']}")
            print(f"{self.player_pokemon.name} HP: {self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}")

            if self.player_pokemon.is_fainted():
                self._end_battle("Opponent")
                return False
        else:
            opponent_result = opponent_move.execute(self.opponent_pokemon, self.player_pokemon)
            print(f"\n{opponent_result['message']}")
            print(f"{self.player_pokemon.name} HP: {self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}")

            if self.player_pokemon.is_fainted():
                self._end_battle("Opponent")
                return False

            player_result = player_move.execute(self.player_pokemon, self.opponent_pokemon)
            print(f"\n{player_result['message']}")
            print(f"{self.opponent_pokemon.name} HP: {self.opponent_pokemon.current_hp}/{self.opponent_pokemon.max_hp}")

            if self.opponent_pokemon.is_fainted():
                self._end_battle("Player")
                return False

        if self.turn_count >= self.max_turns:
            self._end_battle("Draw")
            return False

        return True

    def _end_battle(self, winner: str):
        self.game_over = True
        self.winner = winner

        print("\n" + "=" * 60)
        if winner == "Draw":
            print("BATTLE DRAW!")
            print(f"Reached the 50-turn limit. Both Pokemon are still standing!")
        else:
            print(f"BATTLE OVER! {winner} WINS!")
            if winner == "Player":
                print(f"\n{self.opponent_pokemon.name} fainted!")
                print(f"\n{self.player_pokemon.name} wins the battle!")
            else:
                print(f"\n{self.player_pokemon.name} fainted!")
                print(f"\n{self.opponent_pokemon.name} wins the battle!")
        print("=" * 60)

    def run_auto_battle(self) -> str:
        self.start()
        while not self.game_over and self.process_turn(random.randint(0, 1)):
            pass
        return self.winner


class Game:
    def __init__(self):
        self.player_team: List[Pokemon] = []
        self.current_battle: Optional[Battle] = None
        self.player_level = 10

    def main_menu(self):
        while True:
            print("\n" + "=" * 60)
            print("POKEMON CLI GAME - Gold/Silver Edition")
            print("=" * 60)
            print("\n1. Start a Battle")
            print("2. View Your Pokemon")
            print("3. Create a Custom Team")
            print("4. Exit")

            try:
                choice = input("\nChoose an option (1-4): ").strip()
                if choice == "1":
                    self.start_battle()
                elif choice == "2":
                    self.view_team()
                elif choice == "3":
                    self.create_team()
                elif choice == "4":
                    print("\nThanks for playing! Goodbye!")
                    sys.exit(0)
                else:
                    print("Invalid choice! Please try again.")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Goodbye!")
                sys.exit(0)

    def create_team(self):
        print("\n" + "=" * 60)
        print("CREATE YOUR TEAM")
        print("=" * 60)
        print("\nYour team can have up to 6 Pokemon.")
        print("You must have at least 1 Pokemon to battle.\n")

        self.player_team = []
        for i in range(1, 7):
            try:
                choice = input(f"Add Pokemon {i}? (y/n): ").strip().lower()
                if choice == "y":
                    pokemon = PokemonFactory.create_random_pokemon(self.player_level)
                    self.player_team.append(pokemon)
                    print(f"Added: {pokemon}")
                elif choice == "n":
                    if self.player_team:
                        break
                    else:
                        print("You need at least 1 Pokemon!")
                else:
                    print("Invalid choice! Skipping...")
            except KeyboardInterrupt:
                break

        if self.player_team:
            print(f"\nTeam created with {len(self.player_team)} Pokemon!")
        else:
            print("\nNo Pokemon added. Using random team...")
            self.player_team = [PokemonFactory.create_random_pokemon(self.player_level) for _ in range(3)]

    def view_team(self):
        print("\n" + "=" * 60)
        print("YOUR POKEMON TEAM")
        print("=" * 60)

        if not self.player_team:
            print("\nYou don't have any Pokemon yet! Create a team first.")
            return

        for i, pokemon in enumerate(self.player_team, 1):
            print(f"\n{i}. {pokemon}")
            print(f"   HP: {pokemon.current_hp}/{pokemon.max_hp}")
            print(f"   Moves: {', '.join(move.name for move in pokemon.moves)}")

    def start_battle(self):
        if not self.player_team:
            print("\nYou don't have any Pokemon! Create a team first.")
            return

        print("\n" + "=" * 60)
        print("PREPARING FOR BATTLE")
        print("=" * 60)

        player_pokemon = self.player_team[0]
        if player_pokemon.is_fainted():
            print(f"\n{player_pokemon.name} is fainted! You have no Pokemon left.")
            return

        opponent_pokemon = PokemonFactory.create_random_pokemon(self.player_level)

        self.current_battle = Battle(player_pokemon, opponent_pokemon, max_turns=50)
        self.current_battle.start()

        print("\nWould you like to battle manually or automatically?")
        print("1. Manual (choose moves each turn)")
        print("2. Automatic (AI chooses moves)")

        try:
            choice = input("\nChoose (1-2): ").strip()
            if choice == "2":
                winner = self.current_battle.run_auto_battle()
                print(f"\nBattle Result: {winner}")
            else:
                while not self.current_battle.game_over:
                    if not self.current_battle.process_turn():
                        break
                print(f"\nBattle Result: {self.current_battle.winner}")
        except KeyboardInterrupt:
            print("\n\nBattle interrupted!")


def main():
    game = Game()
    game.create_team()
    game.main_menu()


if __name__ == "__main__":
    main()
