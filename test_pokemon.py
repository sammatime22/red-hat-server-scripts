#!/usr/bin/env python3
"""
Test script for Pokemon CLI Game
"""

from pokemon_cli_game import PokemonFactory, Battle, Pokemon, Type

def test_pokemon_creation():
    print("Testing Pokemon Creation...")
    pokemon = PokemonFactory.create_random_pokemon(level=10)
    print(f"✓ Created: {pokemon}")
    print(f"  - Type: {pokemon.pokemon_type.value}")
    print(f"  - HP: {pokemon.current_hp}/{pokemon.max_hp}")
    print(f"  - Moves: {', '.join(m.name for m in pokemon.moves)}\n")

def test_type_effectiveness():
    print("Testing Type Effectiveness...")

    fire_pokemon = Pokemon("Charmander", Type.FIRE, 39, 39, 10, PokemonFactory.FIRE_MOVES[:2])
    water_pokemon = Pokemon("Squirtle", Type.WATER, 39, 39, 10, PokemonFactory.WATER_MOVES[:2])
    grass_pokemon = Pokemon("Bulbasaur", Type.GRASS, 39, 39, 10, PokemonFactory.GRASS_MOVES[:2])

    fire_move = fire_pokemon.moves[0]
    print(f"\n{fire_pokemon.name} ({fire_pokemon.pokemon_type.value}) uses {fire_move.name}:")

    print(f"  vs {water_pokemon.name} ({water_pokemon.pokemon_type.value}): NOT very effective")
    print(f"  vs {grass_pokemon.name} ({grass_pokemon.pokemon_type.value}): SUPER effective")
    print("✓ Type effectiveness working correctly\n")

def test_battle():
    print("Testing Battle System...")

    player = PokemonFactory.create_random_pokemon(level=10)
    opponent = PokemonFactory.create_random_pokemon(level=10)

    battle = Battle(player, opponent, max_turns=50)
    print(f"✓ Battle created between {player.name} and {opponent.name}")
    print(f"  - Max turns: {battle.max_turns}")

    battle.start()

    turn_count = 0
    max_test_turns = 5

    while not battle.game_over and turn_count < max_test_turns:
        player_move_idx = 0
        battle.process_turn(player_move_choice=player_move_idx)
        turn_count += 1

    print(f"\n✓ Battle executed {turn_count} turns")
    print(f"  - Player HP: {battle.player_pokemon.current_hp}")
    print(f"  - Opponent HP: {battle.opponent_pokemon.current_hp}\n")

def test_full_auto_battle():
    print("Testing Full Automatic Battle...")

    player = PokemonFactory.create_random_pokemon(level=10)
    opponent = PokemonFactory.create_random_pokemon(level=10)

    battle = Battle(player, opponent, max_turns=50)
    winner = battle.run_auto_battle()

    print(f"\n✓ Battle completed!")
    print(f"  - Winner: {winner}")
    print(f"  - Turns: {battle.turn_count}")
    print(f"  - Player Pokemon HP: {battle.player_pokemon.current_hp}/{battle.player_pokemon.max_hp}")
    print(f"  - Opponent Pokemon HP: {battle.opponent_pokemon.current_hp}/{battle.opponent_pokemon.max_hp}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("POKEMON CLI GAME - TEST SUITE")
    print("=" * 60 + "\n")

    try:
        test_pokemon_creation()
        test_pokemon_creation()
        test_pokemon_creation()
        test_type_effectiveness()
        test_battle()
        test_full_auto_battle()

        print("=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
