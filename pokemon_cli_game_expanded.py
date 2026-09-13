#!/usr/bin/env python3
"""
Pokemon CLI Game - Expanded Gold/Silver Edition with Full Storyline
Features 8 Pokemon types (Fire, Water, Grass, Flying, Psychic, Ghost, Fighting, Ground)
with full narrative campaign, NPC trainers, and 100-turn battles.
"""

import random
import sys
import time
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum


class Type(Enum):
    FIRE = "Fire"
    WATER = "Water"
    GRASS = "Grass"
    FLYING = "Flying"
    PSYCHIC = "Psychic"
    GHOST = "Ghost"
    FIGHTING = "Fighting"
    GROUND = "Ground"


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
        return damage

    def _get_type_effectiveness(self, defender_type: Type) -> float:
        effectiveness_chart = {
            Type.FIRE: {Type.GRASS: 2.0, Type.GROUND: 0.5, Type.WATER: 0.5, Type.FIRE: 0.5, Type.FLYING: 1.0, Type.PSYCHIC: 1.0, Type.GHOST: 1.0, Type.FIGHTING: 1.0},
            Type.WATER: {Type.FIRE: 2.0, Type.GROUND: 2.0, Type.GRASS: 0.5, Type.WATER: 0.5, Type.FLYING: 1.0, Type.PSYCHIC: 1.0, Type.GHOST: 1.0, Type.FIGHTING: 1.0},
            Type.GRASS: {Type.WATER: 2.0, Type.GROUND: 2.0, Type.FIRE: 0.5, Type.GRASS: 0.5, Type.FLYING: 0.5, Type.PSYCHIC: 1.0, Type.GHOST: 1.0, Type.FIGHTING: 1.0},
            Type.FLYING: {Type.GRASS: 2.0, Type.FIGHTING: 2.0, Type.GROUND: 2.0, Type.FIRE: 1.0, Type.WATER: 1.0, Type.FLYING: 1.0, Type.PSYCHIC: 1.0, Type.GHOST: 1.0},
            Type.PSYCHIC: {Type.FIGHTING: 2.0, Type.PSYCHIC: 2.0, Type.GHOST: 0.5, Type.FIRE: 1.0, Type.WATER: 1.0, Type.GRASS: 1.0, Type.FLYING: 1.0, Type.GROUND: 1.0},
            Type.GHOST: {Type.GHOST: 2.0, Type.PSYCHIC: 2.0, Type.FIGHTING: 0.5, Type.FIRE: 1.0, Type.WATER: 1.0, Type.GRASS: 1.0, Type.FLYING: 1.0, Type.GROUND: 1.0},
            Type.FIGHTING: {Type.FIRE: 1.0, Type.WATER: 1.0, Type.GRASS: 1.0, Type.FLYING: 0.5, Type.PSYCHIC: 0.5, Type.GHOST: 0.5, Type.FIGHTING: 1.0, Type.GROUND: 1.0},
            Type.GROUND: {Type.FIRE: 2.0, Type.PSYCHIC: 2.0, Type.GRASS: 0.5, Type.FLYING: 1.0, Type.WATER: 1.0, Type.GHOST: 1.0, Type.FIGHTING: 1.0, Type.GROUND: 1.0},
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

    FLYING_MOVES = [
        Move("Peck", 35, 1.0, Type.FLYING, "Sharp pecking attack"),
        Move("Aerial Ace", 60, 1.0, Type.FLYING, "Swift flying strike"),
        Move("Sky Attack", 140, 0.9, Type.FLYING, "Devastating sky assault"),
    ]

    PSYCHIC_MOVES = [
        Move("Confusion", 50, 1.0, Type.PSYCHIC, "Psychic wave attack"),
        Move("Psybeam", 65, 1.0, Type.PSYCHIC, "Mystical psychic beam"),
        Move("Psychic", 90, 1.0, Type.PSYCHIC, "Overwhelming psychic force"),
    ]

    GHOST_MOVES = [
        Move("Shadow Ball", 80, 1.0, Type.GHOST, "Ghostly shadow attack"),
        Move("Lick", 30, 1.0, Type.GHOST, "Spooky lick attack"),
        Move("Night Shade", 75, 1.0, Type.GHOST, "Eerie shade of night"),
    ]

    FIGHTING_MOVES = [
        Move("Karate Chop", 50, 1.0, Type.FIGHTING, "Martial arts chop"),
        Move("Close Combat", 120, 1.0, Type.FIGHTING, "Intense close-range battle"),
        Move("Dynamic Punch", 100, 0.9, Type.FIGHTING, "Devastating punch attack"),
    ]

    GROUND_MOVES = [
        Move("Mud Slap", 20, 1.0, Type.GROUND, "Mud slapping attack"),
        Move("Earthquake", 100, 1.0, Type.GROUND, "Earth-shaking tremor"),
        Move("Dig", 80, 1.0, Type.GROUND, "Tunneling earth attack"),
    ]

    FIRE_POKEMON = [("Cyndaquil", 39), ("Flareon", 42), ("Ponyta", 35), ("Vulpix", 33), ("Growlithe", 36)]
    WATER_POKEMON = [("Totodile", 39), ("Lapras", 45), ("Squirtle", 35), ("Psyduck", 33), ("Shellder", 36)]
    GRASS_POKEMON = [("Chikorita", 39), ("Exeggcute", 37), ("Oddish", 33), ("Bellsprout", 33), ("Tangela", 38)]
    FLYING_POKEMON = [("Pidgeotto", 38), ("Spearow", 32), ("Farfetch'd", 35), ("Doduo", 34), ("Aerodactyl", 40)]
    PSYCHIC_POKEMON = [("Slowbro", 38), ("Jynx", 35), ("Alakazam", 41), ("Mr. Mime", 36), ("Drowzee", 34)]
    GHOST_POKEMON = [("Haunter", 37), ("Gengar", 39), ("Misdreavus", 36), ("Lampent", 35), ("Golurk", 38)]
    FIGHTING_POKEMON = [("Mankey", 30), ("Primeape", 38), ("Machamp", 40), ("Hitmonlee", 37), ("Poliwrath", 38)]
    GROUND_POKEMON = [("Sandslash", 37), ("Dugtrio", 36), ("Rhyhorn", 35), ("Cubone", 32), ("Diglett", 30)]

    @classmethod
    def create_random_pokemon(cls, level: int = 10) -> Pokemon:
        pokemon_type = random.choice(list(Type))

        type_map = {
            Type.FIRE: (cls.FIRE_POKEMON, cls.FIRE_MOVES),
            Type.WATER: (cls.WATER_POKEMON, cls.WATER_MOVES),
            Type.GRASS: (cls.GRASS_POKEMON, cls.GRASS_MOVES),
            Type.FLYING: (cls.FLYING_POKEMON, cls.FLYING_MOVES),
            Type.PSYCHIC: (cls.PSYCHIC_POKEMON, cls.PSYCHIC_MOVES),
            Type.GHOST: (cls.GHOST_POKEMON, cls.GHOST_MOVES),
            Type.FIGHTING: (cls.FIGHTING_POKEMON, cls.FIGHTING_MOVES),
            Type.GROUND: (cls.GROUND_POKEMON, cls.GROUND_MOVES),
        }

        pokemon_list, move_list = type_map[pokemon_type]
        name, base_level = random.choice(pokemon_list)
        moves = random.sample(move_list, 2)

        max_hp = base_level * 2 + level
        return Pokemon(name=name, pokemon_type=pokemon_type, max_hp=max_hp, current_hp=max_hp, level=level, moves=moves)

    @classmethod
    def create_trainer_pokemon(cls, pokemon_type: Type, level: int = 10) -> Pokemon:
        type_map = {
            Type.FIRE: (cls.FIRE_POKEMON, cls.FIRE_MOVES),
            Type.WATER: (cls.WATER_POKEMON, cls.WATER_MOVES),
            Type.GRASS: (cls.GRASS_POKEMON, cls.GRASS_MOVES),
            Type.FLYING: (cls.FLYING_POKEMON, cls.FLYING_MOVES),
            Type.PSYCHIC: (cls.PSYCHIC_POKEMON, cls.PSYCHIC_MOVES),
            Type.GHOST: (cls.GHOST_POKEMON, cls.GHOST_MOVES),
            Type.FIGHTING: (cls.FIGHTING_POKEMON, cls.FIGHTING_MOVES),
            Type.GROUND: (cls.GROUND_POKEMON, cls.GROUND_MOVES),
        }

        pokemon_list, move_list = type_map[pokemon_type]
        name, base_level = random.choice(pokemon_list)
        moves = random.sample(move_list, 2)
        max_hp = base_level * 2 + level
        return Pokemon(name=name, pokemon_type=pokemon_type, max_hp=max_hp, current_hp=max_hp, level=level, moves=moves)


@dataclass
class Trainer:
    name: str
    title: str
    team: List[Pokemon]
    dialogue: Dict[str, str]

    def get_intro_dialogue(self) -> str:
        return self.dialogue.get("intro", f"I am {self.name}, the {self.title}!")

    def get_victory_dialogue(self) -> str:
        return self.dialogue.get("victory", "You've won this battle. Well done!")

    def get_defeat_dialogue(self) -> str:
        return self.dialogue.get("defeat", "I have been defeated... Impressive!")


class TrainerFactory:
    TRAINERS = [
        Trainer(
            name="Brock",
            title="Rock Specialist",
            team=[],
            dialogue={
                "intro": "I am Brock, the Rock-type specialist! My Pokemon are solid as stone!",
                "victory": "Your Pokemon are strong, but not strong enough against my rocks!",
                "defeat": "Incredible! I must reassess my training methods!",
                "commentary": "This battle is just beginning!",
            }
        ),
        Trainer(
            name="Misty",
            title="Water Master",
            team=[],
            dialogue={
                "intro": "Hi there! I'm Misty, a Water-type master! Let's see your Pokemon!",
                "victory": "My Water Pokemon are unbeatable! You need more training!",
                "defeat": "That was amazing! Your bond with your Pokemon is strong!",
                "commentary": "Come on, you can do better than that!",
            }
        ),
        Trainer(
            name="Lt. Surge",
            title="Electric Champion",
            team=[],
            dialogue={
                "intro": "Welcome, soldier! Lt. Surge here. Prepare for battle!",
                "victory": "The electric corps will crush you!",
                "defeat": "You've got guts, kid! I respect that!",
                "commentary": "Electrifying battle we're having!",
            }
        ),
        Trainer(
            name="Erika",
            title="Grass Specialist",
            team=[],
            dialogue={
                "intro": "Welcome. I am Erika, keeper of the grass garden.",
                "victory": "My flowers are more beautiful than your Pokemon!",
                "defeat": "Perhaps your Pokemon have their own beauty...",
                "commentary": "What a graceful battle this is...",
            }
        ),
        Trainer(
            name="Blaine",
            title="Fire Master",
            team=[],
            dialogue={
                "intro": "Heh heh heh! I'm Blaine, Master of Fire! Feel the heat!",
                "victory": "Volcanoes are no match for the strength of my flames!",
                "defeat": "Hot diggity! What an intense battle!",
                "commentary": "This is getting hotter!",
            }
        ),
        Trainer(
            name="Giovanni",
            title="Shadow Master",
            team=[],
            dialogue={
                "intro": "I am Giovanni, master of Team Rocket. You dare challenge me?",
                "victory": "The power of darkness cannot be overcome!",
                "defeat": "Impossible! The power of Team Rocket rejected!",
                "commentary": "Interesting... Your Pokemon have hidden strength...",
            }
        ),
    ]

    @classmethod
    def create_trainer(cls, trainer_template: Trainer, level: int) -> Trainer:
        team = [
            PokemonFactory.create_random_pokemon(level),
            PokemonFactory.create_random_pokemon(level),
            PokemonFactory.create_random_pokemon(level),
        ]
        return Trainer(
            name=trainer_template.name,
            title=trainer_template.title,
            team=team,
            dialogue=trainer_template.dialogue
        )


class Battle:
    def __init__(self, player_pokemon: Pokemon, opponent_pokemon: Pokemon, player_name: str = "Trainer", opponent_name: str = "Opponent", max_turns: int = 100, player_team: List[Pokemon] = None):
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon
        self.player_name = player_name
        self.opponent_name = opponent_name
        self.turn_count = 0
        self.max_turns = max_turns
        self.battle_log: List[str] = []
        self.game_over = False
        self.winner: Optional[str] = None
        self.player_team = player_team or [player_pokemon]
        self.opponent_team = [opponent_pokemon]

    def start(self):
        print("\n" + "=" * 70)
        print("POKEMON BATTLE START!")
        print("=" * 70)
        print(f"\n{self.player_name}'s Pokemon: {self.player_pokemon}")
        print(f"{self.opponent_name}'s Pokemon: {self.opponent_pokemon}")
        print(f"Team Size: {len([p for p in self.player_team if not p.is_fainted()])}/{len(self.player_team)} Pokemon remaining")
        print("\n" + "-" * 70)

    def get_active_team(self) -> List[Pokemon]:
        """Get all non-fainted Pokemon from team"""
        return [p for p in self.player_team if not p.is_fainted()]

    def switch_pokemon(self, new_pokemon: Pokemon) -> bool:
        """Switch to a different Pokemon"""
        if new_pokemon.is_fainted():
            return False
        if new_pokemon == self.player_pokemon:
            return False
        self.player_pokemon = new_pokemon
        print(f"\n{self.player_name} switched to {self.player_pokemon.name}!")
        print(f"{self.player_pokemon.name} HP: {self.player_pokemon.current_hp}/{self.player_pokemon.max_hp}")
        return True

    def prompt_pokemon_switch(self) -> Optional[Pokemon]:
        """Prompt player to switch Pokemon after fainting"""
        active_team = self.get_active_team()

        if not active_team:
            return None

        if len(active_team) == 1 and active_team[0] == self.player_pokemon:
            return None

        print(f"\n{self.player_pokemon.name} fainted!")
        print(f"\n{self.player_name}, choose your next Pokemon:")

        for i, pokemon in enumerate(active_team, 1):
            hp_bar_length = 15
            hp_percent = max(0, pokemon.current_hp) / pokemon.max_hp
            hp_bar = "█" * int(hp_bar_length * hp_percent) + "░" * (hp_bar_length - int(hp_bar_length * hp_percent))
            print(f"  {i}. {pokemon.name:<15} [{hp_bar}] {max(0, pokemon.current_hp)}/{pokemon.max_hp}")

        try:
            choice = int(input("\nChoose Pokemon (or 0 to forfeit): ")) - 1
            if choice == -1:
                return None
            if 0 <= choice < len(active_team):
                selected = active_team[choice]
                if selected != self.player_pokemon:
                    return selected
        except (ValueError, IndexError):
            pass

        return None

    def process_turn(self, player_move_choice: Optional[int] = None) -> bool:
        if self.game_over:
            return False

        self.turn_count += 1
        print(f"\n--- Turn {self.turn_count}/{self.max_turns} ---")

        if player_move_choice is None:
            print(f"\n{self.player_name}'s Pokemon Moves:")
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
            print(f"{self.opponent_pokemon.name} HP: {max(0, self.opponent_pokemon.current_hp)}/{self.opponent_pokemon.max_hp}")

            if self.opponent_pokemon.is_fainted():
                self._end_battle(self.player_name)
                return False

            opponent_result = opponent_move.execute(self.opponent_pokemon, self.player_pokemon)
            print(f"\n{opponent_result['message']}")
            print(f"{self.player_pokemon.name} HP: {max(0, self.player_pokemon.current_hp)}/{self.player_pokemon.max_hp}")

            if self.player_pokemon.is_fainted():
                new_pokemon = self.prompt_pokemon_switch()
                if new_pokemon:
                    self.switch_pokemon(new_pokemon)
                else:
                    self._end_battle(self.opponent_name)
                    return False
                return True
        else:
            opponent_result = opponent_move.execute(self.opponent_pokemon, self.player_pokemon)
            print(f"\n{opponent_result['message']}")
            print(f"{self.player_pokemon.name} HP: {max(0, self.player_pokemon.current_hp)}/{self.player_pokemon.max_hp}")

            if self.player_pokemon.is_fainted():
                new_pokemon = self.prompt_pokemon_switch()
                if new_pokemon:
                    self.switch_pokemon(new_pokemon)
                else:
                    self._end_battle(self.opponent_name)
                    return False
                return True

            player_result = player_move.execute(self.player_pokemon, self.opponent_pokemon)
            print(f"\n{player_result['message']}")
            print(f"{self.opponent_pokemon.name} HP: {max(0, self.opponent_pokemon.current_hp)}/{self.opponent_pokemon.max_hp}")

            if self.opponent_pokemon.is_fainted():
                self._end_battle(self.player_name)
                return False

        if self.turn_count >= self.max_turns:
            self._end_battle("Draw")
            return False

        return True

    def _end_battle(self, winner: str):
        self.game_over = True
        self.winner = winner

        print("\n" + "=" * 70)
        if winner == "Draw":
            print("BATTLE DRAW!")
            print(f"Reached the 100-turn limit. Both Pokemon are still standing!")
        else:
            print(f"BATTLE OVER! {winner} WINS!")
            if winner == self.player_name:
                print(f"\n{self.opponent_pokemon.name} fainted!")
                print(f"\n{self.player_pokemon.name} wins the battle!")
            else:
                print(f"\n{self.player_pokemon.name} fainted!")
                print(f"\n{self.opponent_pokemon.name} wins the battle!")
        print("=" * 70)

    def run_auto_battle(self) -> str:
        self.start()
        while not self.game_over and self.process_turn(random.randint(0, 1)):
            pass
        return self.winner


class Game:
    def __init__(self):
        self.player_team: List[Pokemon] = []
        self.player_name = "Trainer"
        self.current_battle: Optional[Battle] = None
        self.player_level = 10
        self.story_progress = 0
        self.defeated_trainers = []
        self.total_wins = 0

    def print_story_intro(self):
        print("\n" + "=" * 70)
        print("POKEMON: THE LEGEND OF POWER")
        print("Gold & Silver Edition - Expanded")
        print("=" * 70)
        print("""
Welcome, young trainer! You've embarked on an extraordinary journey to become
a Pokemon Master. The land is filled with eight elemental guilds, each guarding
ancient Pokemon mysteries.

Your quest: Challenge the eight guild masters, each specializing in a different
Pokemon type. Prove your worth, and you may uncover the legendary Pokemon that
has been hidden for centuries.

The eight types you will encounter:
  🔥 FIRE - Masters of Passion and Fury
  💧 WATER - Keepers of the Tides and Currents
  🌿 GRASS - Guardians of Life and Growth
  ✈️  FLYING - Riders of the Winds
  💫 PSYCHIC - Seers of the Mind
  👻 GHOST - Whispers from the Other Side
  ✊ FIGHTING - Champions of Combat
  ⛰️  GROUND - Shakers of the Earth

Your adventure awaits! Will you answer the call?
""")
        print("=" * 70)

    def main_menu(self):
        while True:
            print("\n" + "=" * 70)
            print("POKEMON QUEST - MAIN MENU")
            print("=" * 70)
            print(f"\nTrainer: {self.player_name} | Level: {self.player_level} | Wins: {self.total_wins}")
            print(f"Story Progress: {self.story_progress}/8 Guild Masters Defeated")
            print("\n1. Start a Battle")
            print("2. Challenge a Guild Master (Story Mode)")
            print("3. View Your Pokemon")
            print("4. Create a Custom Team")
            print("5. View Guild Status")
            print("6. Exit")

            try:
                choice = input("\nChoose an option (1-6): ").strip()
                if choice == "1":
                    self.start_battle()
                elif choice == "2":
                    self.challenge_guild_master()
                elif choice == "3":
                    self.view_team()
                elif choice == "4":
                    self.create_team()
                elif choice == "5":
                    self.view_guild_status()
                elif choice == "6":
                    self.print_farewell()
                    sys.exit(0)
                else:
                    print("Invalid choice! Please try again.")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Goodbye!")
                sys.exit(0)

    def print_farewell(self):
        print("\n" + "=" * 70)
        print("THANK YOU FOR PLAYING POKEMON QUEST!")
        print("=" * 70)
        print(f"""
Your Journey Summary:
- Trainer Name: {self.player_name}
- Guild Masters Defeated: {self.story_progress}/8
- Total Battles Won: {self.total_wins}
- Pokemon Team Size: {len(self.player_team)}

The legend of your adventures will be remembered! Until next time, trainer!
""")
        print("=" * 70)

    def view_guild_status(self):
        guilds = [
            ("Fire Guild", "Masters of Passion and Fury"),
            ("Water Guild", "Keepers of the Tides"),
            ("Grass Guild", "Guardians of Life"),
            ("Flying Guild", "Riders of the Winds"),
            ("Psychic Guild", "Seers of the Mind"),
            ("Ghost Guild", "Whispers from Beyond"),
            ("Fighting Guild", "Champions of Combat"),
            ("Ground Guild", "Shakers of the Earth"),
        ]

        print("\n" + "=" * 70)
        print("GUILD MASTER STATUS")
        print("=" * 70)
        for i, (guild_name, description) in enumerate(guilds, 1):
            status = "✓ DEFEATED" if i <= self.story_progress else "⊗ Not Yet Challenged"
            print(f"\n{i}. {guild_name:<20} - {description}")
            print(f"   Status: {status}")
        print("\n" + "=" * 70)

    def challenge_guild_master(self):
        if not self.player_team:
            print("\nYou don't have any Pokemon! Create a team first.")
            return

        guilds = [
            ("Fire Guild Master Blaine", Type.FIRE, "Blaine", "Fire Master"),
            ("Water Guild Master Misty", Type.WATER, "Misty", "Water Master"),
            ("Grass Guild Master Erika", Type.GRASS, "Erika", "Grass Specialist"),
            ("Flying Guild Master Pidgeot Trainer", Type.FLYING, "Sky Captain", "Flying Master"),
            ("Psychic Guild Master Alakazam Trainer", Type.PSYCHIC, "Psyche", "Psychic Master"),
            ("Ghost Guild Master Gengar Trainer", Type.GHOST, "Specter", "Ghost Master"),
            ("Fighting Guild Master Primeape Trainer", Type.FIGHTING, "Champion", "Fighting Master"),
            ("Ground Guild Master Rhydon Trainer", Type.GROUND, "Tremor", "Ground Master"),
        ]

        if self.story_progress >= len(guilds):
            print("\n" + "=" * 70)
            print("CONGRATULATIONS!")
            print("=" * 70)
            print("""
You have defeated all eight Guild Masters! The legendary Pokemon appears before you,
drawn by your incredible strength and the bond you share with your team.

The ancient legend speaks of a trainer worthy enough to stand with the legendary
Pokemon. That trainer... is YOU!

Your name will be remembered forever in the annals of Pokemon history!
""")
            print("=" * 70)
            return

        guild_name, guild_type, trainer_name, trainer_title = guilds[self.story_progress]

        print("\n" + "=" * 70)
        print(f"APPROACHING {guild_name.upper()}...")
        print("=" * 70)
        print(f"""
You arrive at the magnificent {guild_type.value} Guild, a place of power and mystery.
The Guild Master {trainer_name}, known as the {trainer_title}, stands before you.

"{trainer_name}: Young trainer, you have come far. But can you overcome the
mastery of {guild_type.value}-type Pokemon? Let us see your true strength!"
""")
        print("=" * 70)

        input("\nPress Enter to begin the battle...")

        player_pokemon = self.player_team[0]
        if player_pokemon.is_fainted():
            print(f"\n{player_pokemon.name} is fainted! You have no Pokemon left.")
            return

        opponent_pokemon = PokemonFactory.create_trainer_pokemon(guild_type, self.player_level + 2)

        self.current_battle = Battle(
            player_pokemon,
            opponent_pokemon,
            player_name=self.player_name,
            opponent_name=trainer_name,
            max_turns=100,
            player_team=self.player_team
        )

        print("\nWould you like to battle manually or automatically?")
        print("1. Manual (choose moves each turn)")
        print("2. Automatic (AI chooses moves)")

        try:
            choice = input("\nChoose (1-2): ").strip()
            if choice == "2":
                winner = self.current_battle.run_auto_battle()
            else:
                while not self.current_battle.game_over:
                    if not self.current_battle.process_turn():
                        break
                winner = self.current_battle.winner

            print(f"\nBattle Result: {winner}")

            if winner == self.player_name:
                print("\n" + "=" * 70)
                print(f"VICTORY! You have defeated {trainer_name}!")
                print("=" * 70)
                print(f"""
"{trainer_name}: Magnificent! Your Pokemon are truly exceptional. The {guild_type.value}
Guild recognizes you as a worthy challenger. Take this proof of your victory."

You receive the {guild_type.value} Guild Badge!
Your team grew stronger through this battle!
""")
                print("=" * 70)
                self.story_progress += 1
                self.total_wins += 1
                self.player_level += 1
            else:
                print("\n" + "=" * 70)
                print(f"DEFEAT! {trainer_name} has bested you.")
                print("=" * 70)
                print(f"""
"{trainer_name}: You fought well, but you still have much to learn.
Return when you are stronger, and we shall battle again!"

You may challenge the Guild Master again after training your Pokemon further.
""")
                print("=" * 70)

        except KeyboardInterrupt:
            print("\n\nBattle interrupted!")

    def create_team(self):
        print("\n" + "=" * 70)
        print("CREATE YOUR POKEMON TEAM")
        print("=" * 70)
        print("""
Every great trainer needs a team of Pokemon! You can have up to 6 Pokemon.
Each type brings unique strengths to your team.

Available Types:
  🔥 Fire    💧 Water    🌿 Grass    ✈️  Flying
  💫 Psychic 👻 Ghost    ✊ Fighting ⛰️  Ground
""")

        print("\nWhat is your trainer name, brave adventurer?")
        name = input("Enter your name: ").strip()
        if name:
            self.player_name = name
            print(f"\nWelcome, {self.player_name}! Your journey begins now!")

        self.player_team = []
        for i in range(1, 7):
            try:
                choice = input(f"\nAdd Pokemon {i}? (y/n): ").strip().lower()
                if choice == "y":
                    pokemon = PokemonFactory.create_random_pokemon(self.player_level)
                    self.player_team.append(pokemon)
                    print(f"✓ Caught: {pokemon}")
                    print(f"  This {pokemon.pokemon_type.value}-type Pokemon will serve you well!")
                elif choice == "n":
                    if self.player_team:
                        break
                    else:
                        print("You need at least 1 Pokemon to start your adventure!")
                else:
                    print("Invalid choice! Skipping...")
            except KeyboardInterrupt:
                break

        if self.player_team:
            print(f"\n✓ Your team is ready! {len(self.player_team)} Pokemon await your command!")
        else:
            print("\nNo Pokemon added. Generating a random team...")
            self.player_team = [PokemonFactory.create_random_pokemon(self.player_level) for _ in range(3)]

    def view_team(self):
        print("\n" + "=" * 70)
        print("YOUR POKEMON TEAM")
        print("=" * 70)

        if not self.player_team:
            print("\nYou don't have any Pokemon yet! Create a team first.")
            return

        for i, pokemon in enumerate(self.player_team, 1):
            hp_bar_length = 20
            hp_percent = max(0, pokemon.current_hp) / pokemon.max_hp
            hp_bar = "█" * int(hp_bar_length * hp_percent) + "░" * (hp_bar_length - int(hp_bar_length * hp_percent))

            print(f"\n{i}. {pokemon.name:<15} | Lvl {pokemon.level:<3} | {pokemon.pokemon_type.value:<10}")
            print(f"   HP: [{hp_bar}] {max(0, pokemon.current_hp)}/{pokemon.max_hp}")
            print(f"   Moves: {', '.join(move.name for move in pokemon.moves)}")

        print("\n" + "=" * 70)

    def start_battle(self):
        if not self.player_team:
            print("\nYou don't have any Pokemon! Create a team first.")
            return

        print("\n" + "=" * 70)
        print("WILD POKEMON BATTLE!")
        print("=" * 70)

        player_pokemon = self.player_team[0]
        if player_pokemon.is_fainted():
            print(f"\n{player_pokemon.name} is fainted! You have no Pokemon left to battle.")
            return

        opponent_pokemon = PokemonFactory.create_random_pokemon(self.player_level)

        print(f"""
As you walk through the tall grass, a wild {opponent_pokemon.pokemon_type.value}-type Pokemon
appears before you!

{opponent_pokemon.name} emerges! What do you do?
""")

        self.current_battle = Battle(
            player_pokemon,
            opponent_pokemon,
            player_name=self.player_name,
            opponent_name="Wild " + opponent_pokemon.name,
            max_turns=100,
            player_team=self.player_team
        )
        self.current_battle.start()

        print("\nWould you like to battle manually or automatically?")
        print("1. Manual (choose moves each turn)")
        print("2. Automatic (AI chooses moves)")

        try:
            choice = input("\nChoose (1-2): ").strip()
            if choice == "2":
                winner = self.current_battle.run_auto_battle()
            else:
                while not self.current_battle.game_over:
                    if not self.current_battle.process_turn():
                        break
                winner = self.current_battle.winner

            print(f"\nBattle Result: {winner}")
            if winner == self.player_name:
                self.total_wins += 1
                print("\n✓ Victory! Your Pokemon gained valuable experience!")

        except KeyboardInterrupt:
            print("\n\nBattle interrupted!")


def main():
    game = Game()
    game.print_story_intro()
    input("\nPress Enter to continue your journey...")
    game.create_team()
    game.main_menu()


if __name__ == "__main__":
    main()
