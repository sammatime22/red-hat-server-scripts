# Pokemon CLI Game - Gold/Silver Edition

A turn-based Pokemon battle game implemented in Python, mimicking the style of Pokemon Gold and Silver with a simplified type system.

## Features

- **Three Pokemon Types**: Fire, Water, and Grass only
- **Type Advantage System**: Rock-paper-scissors style type advantages
  - Fire beats Grass
  - Water beats Fire
  - Grass beats Water
- **50-Turn Battle Limit**: Battles end after 50 turns (Draw result if neither Pokemon faints)
- **Team Management**: Build and manage a team of up to 6 Pokemon
- **Manual and Automatic Battles**: Choose between manual move selection or automatic AI-controlled battles
- **HP System**: Pokemon have HP that decreases with damage taken
- **Move Variety**: Each Pokemon type has 3 unique moves with different power levels
- **Type Effectiveness Messages**: Get feedback on move effectiveness (super effective, not very effective)
- **Critical Hit Chance**: Moves have a 6.25% chance to deal 1.5x damage

## How to Play

### Running the Game

```bash
python3 pokemon_cli_game.py
```

### Main Menu Options

1. **Start a Battle**: Begin a battle with the first Pokemon in your team against a random opponent
2. **View Your Pokemon**: See details about your team (HP, moves, type)
3. **Create a Custom Team**: Build or modify your Pokemon team (1-6 Pokemon)
4. **Exit**: Quit the game

### During Battle

**Manual Mode**: Select a move each turn (1 or 2)
**Automatic Mode**: AI chooses moves automatically

### Battle Mechanics

- **Speed**: Pokemon with higher levels move first (simplified speed stat)
- **Damage Calculation**: 
  - Base move power
  - STAB (Same Type Attack Bonus): 1.5x damage if Pokemon type matches move type
  - Type Advantage: 2x damage if super effective, 0.5x if not very effective
  - Critical Hit: 1.5x damage (6.25% chance)
  - Random Variance: 0.85x multiplier for balance
- **Battle End Conditions**:
  - One Pokemon faints (fainted Pokemon has 0 or less HP)
  - Reach 50-turn limit (Draw)

## Pokemon Types

### Fire Type
- **Pokemon**: Cyndaquil, Flareon, Ponyta, Vulpix, Growlithe
- **Moves**: Ember (40 power), Flame Burst (70 power), Fire Punch (75 power)

### Water Type
- **Pokemon**: Totodile, Lapras, Squirtle, Psyduck, Shellder
- **Moves**: Water Gun (40 power), Bubble Beam (65 power), Surf (90 power)

### Grass Type
- **Pokemon**: Chikorita, Exeggcute, Oddish, Bellsprout, Tangela
- **Moves**: Razor Leaf (55 power), Solar Beam (120 power), Vine Whip (45 power)

## Type Matchups

| Type | Beats | Weak To |
|------|-------|---------|
| Fire | Grass | Water |
| Water | Fire | Grass |
| Grass | Water | Fire |

## Example Gameplay

```
============================================================
POKEMON BATTLE START!
============================================================

Player's Pokemon: Cyndaquil (Lvl 10) - Fire Type
Opponent's Pokemon: Totodile (Lvl 10) - Water Type

--- Turn 1 ---

Player's Pokemon Moves:
  1. Ember (Fire Type) - Power: 40
  2. Flame Burst (Fire Type) - Power: 70

Choose a move (1-2): 2

Cyndaquil used Flame Burst! Totodile took 30 damage. It's not very effective...
Totodile HP: 48/78

Totodile used Water Gun! Cyndaquil took 45 damage. It's super effective!
Cyndaquil HP: -6/39

============================================================
BATTLE OVER! Opponent WINS!

Cyndaquil fainted!

Totodile wins the battle!
============================================================
```

## Strategy Tips

- **Type Advantage is Key**: Always consider type matchups when choosing Pokemon
- **Move Selection**: Use moves with higher power when your type is at an advantage
- **Team Building**: Create a balanced team with representation from all three types
- **HP Management**: Keep track of your Pokemon's remaining HP for future battles

## Technical Details

- **Language**: Python 3
- **Dependencies**: None (uses only standard library)
- **Turn Limit**: 50 turns maximum per battle
- **Accuracy**: All moves in Fire/Water/Grass have 95-100% accuracy
- **Level**: All Pokemon start at level 10 by default
- **Random Selection**: Opponent Pokemon are randomly generated each battle

## Modifications from Original Pokemon

This simplified version differs from traditional Pokemon games:
- Only 3 types (Fire, Water, Grass) instead of 18
- Each Pokemon knows exactly 2 moves (chosen randomly from type pool)
- Simplified damage formula (no Attack/Special Attack/Defense stats)
- Maximum 50 turns per battle (prevents infinite battles)
- No items, abilities, status conditions, or held items
- Teams max out at 6 Pokemon (same as traditional Pokemon)

## Future Enhancements

Potential features for future versions:
- Level progression and experience points
- More Pokemon types
- Battle trainer NPCs with preset teams
- Save/load game state
- Pokemon storage system
- Battle statistics tracking
- Ability system
- Item usage
- Pokemon evolution
