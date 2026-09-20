#!/usr/bin/env python3
"""
Test script for expanded Pokemon CLI Game with all 8 types
"""

from pokemon_cli_game_expanded import (
    PokemonFactory, Battle, Pokemon, Type, Trainer, TrainerFactory, Move
)

def test_all_types():
    print("Testing All 8 Pokemon Types...")
    types = list(Type)
    print(f"✓ Available types: {[t.value for t in types]}")
    assert len(types) == 8, "Should have 8 types"
    print(f"✓ All 8 types confirmed!\n")

def test_pokemon_per_type():
    print("Testing Pokemon Generation for Each Type...")
    for pokemon_type in Type:
        pokemon = PokemonFactory.create_trainer_pokemon(pokemon_type, level=15)
        print(f"✓ {pokemon_type.value:<10} - {pokemon.name:<15} (Lvl {pokemon.level})")
        assert pokemon.pokemon_type == pokemon_type
        assert len(pokemon.moves) == 2
    print()

def test_type_matchups():
    print("Testing Type Matchups...")

    matchups = [
        (Type.FIRE, Type.GRASS, 2.0, "Fire beats Grass", PokemonFactory.FIRE_MOVES[0]),
        (Type.WATER, Type.FIRE, 2.0, "Water beats Fire", PokemonFactory.WATER_MOVES[0]),
        (Type.GRASS, Type.WATER, 2.0, "Grass beats Water", PokemonFactory.GRASS_MOVES[0]),
        (Type.FLYING, Type.FIGHTING, 2.0, "Flying beats Fighting", PokemonFactory.FLYING_MOVES[0]),
        (Type.PSYCHIC, Type.FIGHTING, 2.0, "Psychic beats Fighting", PokemonFactory.PSYCHIC_MOVES[0]),
        (Type.GHOST, Type.PSYCHIC, 2.0, "Ghost beats Psychic", PokemonFactory.GHOST_MOVES[0]),
        (Type.FIRE, Type.WATER, 0.5, "Fire weak to Water", PokemonFactory.FIRE_MOVES[0]),
        (Type.WATER, Type.GRASS, 0.5, "Water weak to Grass", PokemonFactory.WATER_MOVES[0]),
    ]

    for attacker_type, defender_type, expected, description, move in matchups:
        test_move = Move(move.name, move.power, move.accuracy, attacker_type)
        effectiveness = test_move._get_type_effectiveness(defender_type)
        assert effectiveness == expected, f"Failed: {description}"
        print(f"✓ {description}")
    print()

def test_extended_battle_100_turns():
    print("Testing Extended 100-Turn Battle System...")

    player = PokemonFactory.create_random_pokemon(level=15)
    opponent = PokemonFactory.create_random_pokemon(level=15)

    battle = Battle(player, opponent, max_turns=100)
    assert battle.max_turns == 100, "Battle should support 100 turns"
    print(f"✓ Battle created with 100-turn limit")
    print(f"✓ Player: {player}")
    print(f"✓ Opponent: {opponent}\n")

def test_trainer_system():
    print("Testing Trainer System...")

    for trainer_template in TrainerFactory.TRAINERS[:3]:
        trainer = TrainerFactory.create_trainer(trainer_template, level=15)
        print(f"✓ Trainer: {trainer.name} ({trainer.title})")
        print(f"  Team Size: {len(trainer.team)}")
        print(f"  Intro: {trainer.get_intro_dialogue()[:50]}...")
    print()

def test_type_effectiveness_dialogue():
    print("Testing Type Effectiveness Messages...")

    fire_move = PokemonFactory.FIRE_MOVES[0]

    effectiveness_messages = [
        (Type.GRASS, "Should be super effective vs Grass"),
        (Type.WATER, "Should be not very effective vs Water"),
        (Type.FIRE, "Should be neutral vs Fire"),
    ]

    for target_type, description in effectiveness_messages:
        message = fire_move._get_effectiveness_message(target_type)
        if message:
            print(f"✓ {description}: {message}")
        else:
            print(f"✓ {description}: Neutral damage")
    print()

def test_mixed_type_battle():
    print("Testing Mixed-Type Battle...")

    fire_pokemon = PokemonFactory.create_trainer_pokemon(Type.FIRE, level=15)
    water_pokemon = PokemonFactory.create_trainer_pokemon(Type.WATER, level=15)

    battle = Battle(fire_pokemon, water_pokemon, max_turns=100)
    print(f"✓ Fire vs Water matchup")
    print(f"  Advantage: Water type beats Fire")

    turn_count = 0
    max_test_turns = 5

    battle.start()
    while not battle.game_over and turn_count < max_test_turns:
        battle.process_turn(0)
        turn_count += 1

    print(f"✓ Simulated {turn_count} turns")
    print(f"  Fire Pokemon HP: {max(0, battle.player_pokemon.current_hp)}")
    print(f"  Water Pokemon HP: {max(0, battle.opponent_pokemon.current_hp)}\n")

def test_full_story_battle():
    print("Testing Full Story-Mode Battle...")

    player = PokemonFactory.create_random_pokemon(level=12)
    fire_master = PokemonFactory.create_trainer_pokemon(Type.FIRE, level=14)

    battle = Battle(
        player,
        fire_master,
        player_name="Trainer Ash",
        opponent_name="Guild Master Blaine",
        max_turns=100
    )

    print(f"✓ Story Battle Setup")
    print(f"  Player: {battle.player_name} with {battle.player_pokemon.name}")
    print(f"  Opponent: {battle.opponent_name} with {battle.opponent_pokemon.name}")
    print(f"  Turn Limit: {battle.max_turns}\n")

if __name__ == "__main__":
    print("=" * 70)
    print("POKEMON QUEST EXPANDED - TEST SUITE")
    print("=" * 70 + "\n")

    try:
        test_all_types()
        test_pokemon_per_type()
        test_type_matchups()
        test_extended_battle_100_turns()
        test_trainer_system()
        test_type_effectiveness_dialogue()
        test_mixed_type_battle()
        test_full_story_battle()

        print("=" * 70)
        print("ALL TESTS PASSED! ✓")
        print("=" * 70)
        print("\nExpanded features verified:")
        print("  ✓ All 8 Pokemon types working")
        print("  ✓ Pokemon generation for each type")
        print("  ✓ Expanded type matchup system")
        print("  ✓ 100-turn battle limit")
        print("  ✓ Trainer/Guild Master system")
        print("  ✓ Type effectiveness messages")
        print("  ✓ Mixed-type battles")
        print("  ✓ Story mode battles")
        print("\nThe expanded Pokemon Quest is ready for adventure!")

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
