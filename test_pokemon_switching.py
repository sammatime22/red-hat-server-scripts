#!/usr/bin/env python3
"""
Test script for Pokemon switching feature
"""

from pokemon_cli_game_expanded import (
    PokemonFactory, Battle, Pokemon, Type
)

def test_pokemon_switching():
    print("Testing Pokemon Switching Feature...\n")

    player_team = [
        PokemonFactory.create_trainer_pokemon(Type.FIRE, level=10),
        PokemonFactory.create_trainer_pokemon(Type.WATER, level=10),
        PokemonFactory.create_trainer_pokemon(Type.GRASS, level=10),
    ]

    print("✓ Player Team Created:")
    for i, pokemon in enumerate(player_team, 1):
        print(f"  {i}. {pokemon.name} ({pokemon.pokemon_type.value} Type) - HP: {pokemon.current_hp}/{pokemon.max_hp}")

    opponent = PokemonFactory.create_trainer_pokemon(Type.WATER, level=10)

    battle = Battle(
        player_team[0],
        opponent,
        player_name="Trainer",
        opponent_name="Opponent",
        max_turns=100,
        player_team=player_team
    )

    print(f"\n✓ Battle created with team size: {len(battle.player_team)}")

    # Test get_active_team
    active_team = battle.get_active_team()
    print(f"✓ Active team size: {len(active_team)}")
    assert len(active_team) == 3, "All Pokemon should be active initially"

    # Faint the first Pokemon
    print(f"\n✓ Fainting {battle.player_pokemon.name}...")
    battle.player_pokemon.current_hp = 0
    assert battle.player_pokemon.is_fainted(), "Pokemon should be fainted"

    # Check active team after fainting
    active_team = battle.get_active_team()
    print(f"✓ Active team after fainting: {len(active_team)}")
    assert len(active_team) == 2, "Should have 2 active Pokemon left"

    # Test switching Pokemon
    new_pokemon = player_team[1]
    print(f"\n✓ Switching to {new_pokemon.name}...")
    success = battle.switch_pokemon(new_pokemon)
    assert success, "Should successfully switch Pokemon"
    assert battle.player_pokemon == new_pokemon, "Current Pokemon should be the new one"
    print(f"✓ Successfully switched to {battle.player_pokemon.name}")

    # Test switching to fainted Pokemon (should fail)
    fainted_pokemon = player_team[0]
    print(f"\n✓ Testing switch to fainted Pokemon...")
    success = battle.switch_pokemon(fainted_pokemon)
    assert not success, "Should not be able to switch to fainted Pokemon"
    print(f"✓ Correctly prevented switching to fainted Pokemon")

    # Test switching to current Pokemon (should fail)
    print(f"\n✓ Testing switch to current Pokemon...")
    success = battle.switch_pokemon(battle.player_pokemon)
    assert not success, "Should not be able to switch to current Pokemon"
    print(f"✓ Correctly prevented switching to current Pokemon")

    # Test with all Pokemon fainted except one
    print(f"\n✓ Testing with only one active Pokemon...")
    player_team[0].current_hp = 0  # Already fainted
    player_team[2].current_hp = 0
    player_team[1].current_hp = 50  # Only this one is active

    active_team = battle.get_active_team()
    print(f"✓ Active team: {len(active_team)} Pokemon")
    assert len(active_team) == 1, "Should have only 1 active Pokemon"

    print("\n" + "=" * 60)
    print("ALL SWITCHING TESTS PASSED! ✓")
    print("=" * 60)
    print("\nFeatures verified:")
    print("  ✓ Team passing to Battle")
    print("  ✓ get_active_team() method")
    print("  ✓ switch_pokemon() method")
    print("  ✓ Cannot switch to fainted Pokemon")
    print("  ✓ Cannot switch to current Pokemon")
    print("  ✓ Correct active team tracking")

if __name__ == "__main__":
    try:
        test_pokemon_switching()
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
