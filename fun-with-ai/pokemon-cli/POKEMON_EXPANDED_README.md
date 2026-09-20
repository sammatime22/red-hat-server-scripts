# Pokemon Quest: Gold & Silver Edition - Expanded

A comprehensive turn-based Pokemon battle game with a full story campaign, featuring eight elemental types and extensive dialogue throughout gameplay.

## New Features

### Story & Campaign
- **Full Narrative Campaign**: Challenge 8 Guild Masters, one for each Pokemon type
- **Character-Driven Gameplay**: Each Guild Master has unique personality and dialogue
- **Progress Tracking**: Track your achievements across the 8 guild challenges
- **Story Progression**: Level up and grow stronger as you progress through the campaign
- **Memorable Moments**: Rich dialogue before, during, and after battles

### Eight Pokemon Types
Now featuring all 8 types instead of just 3:

1. **🔥 Fire Type** - Masters of Passion and Fury
   - Pokemon: Cyndaquil, Flareon, Ponyta, Vulpix, Growlithe
   - Moves: Ember, Flame Burst, Fire Punch

2. **💧 Water Type** - Keepers of the Tides and Currents
   - Pokemon: Totodile, Lapras, Squirtle, Psyduck, Shellder
   - Moves: Water Gun, Bubble Beam, Surf

3. **🌿 Grass Type** - Guardians of Life and Growth
   - Pokemon: Chikorita, Exeggcute, Oddish, Bellsprout, Tangela
   - Moves: Razor Leaf, Solar Beam, Vine Whip

4. **✈️ Flying Type** - Riders of the Winds
   - Pokemon: Pidgeotto, Spearow, Farfetch'd, Doduo, Aerodactyl
   - Moves: Peck, Aerial Ace, Sky Attack

5. **💫 Psychic Type** - Seers of the Mind
   - Pokemon: Slowbro, Jynx, Alakazam, Mr. Mime, Drowzee
   - Moves: Confusion, Psybeam, Psychic

6. **👻 Ghost Type** - Whispers from the Other Side
   - Pokemon: Haunter, Gengar, Misdreavus, Lampent, Golurk
   - Moves: Shadow Ball, Lick, Night Shade

7. **✊ Fighting Type** - Champions of Combat
   - Pokemon: Mankey, Primeape, Machamp, Hitmonlee, Poliwrath
   - Moves: Karate Chop, Close Combat, Dynamic Punch

8. **⛰️ Ground Type** - Shakers of the Earth
   - Pokemon: Sandslash, Dugtrio, Rhyhorn, Cubone, Diglett
   - Moves: Mud Slap, Earthquake, Dig

### Extended Battle System
- **100-Turn Limit**: Battles can last up to 100 turns (doubled from 50)
- **Type Effectiveness**: Full type matchup chart with all 8 types
- **Guild Master Battles**: Specialized battles against story trainers
- **Battle Dialogue**: Narrative context for each battle
- **Pokemon Switching**: Switch to another team member when your Pokemon faints
- **Team-Based Strategy**: Use your full team strategically across the battle
- **Battle Continuation**: Game continues until all team Pokemon are defeated

### Enhanced Dialogue
- **Character Personalities**: Each NPC has unique dialogue and personality
- **Story Introductions**: Rich narrative setup before guild battles
- **Battle Commentary**: In-game reactions and personality
- **Victory/Defeat Messages**: Character-specific responses to battle outcomes
- **Main Menu Narration**: Welcome message and story setup

### Expanded Menu System
- **Story Mode**: Challenge the 8 Guild Masters in sequence
- **Guild Status Display**: Track which Guild Masters you've defeated
- **Trainer Statistics**: View your progress and achievements
- **Team Management**: Improved team viewing with HP bars
- **Wild Pokemon Battles**: Random encounters to level up

## Story Structure

### The Legend
Your journey begins as a young trainer seeking to become a Pokemon Master. Legend speaks of eight ancient elemental guilds, each guarding mysteries of Pokemon types. By defeating all eight Guild Masters, you unlock the truth of the legendary Pokemon itself.

### The Eight Guilds

**Fire Guild Master - Blaine**
- "Heh heh heh! Feel the heat!"
- Master of intensity and passion
- Specializes in powerful Fire-type Pokemon

**Water Guild Master - Misty**
- "My Water Pokemon are unbeatable!"
- Keeper of aquatic secrets
- Masters of fluid strategy

**Grass Guild Master - Erika**
- "Welcome to the grass garden."
- Guardian of natural beauty and power
- Balances nature's harmony

**Flying Guild Master - Sky Captain**
- Rider of the winds
- Masters of aerial superiority
- Commands the skies

**Psychic Guild Master - Psyche**
- Seer of inner truths
- Masters of mental fortitude
- Reads the minds of opponents

**Ghost Guild Master - Specter**
- Whispers from beyond
- Masters of ethereal power
- Moves in mysterious ways

**Fighting Guild Master - Champion**
- Champion of martial arts
- Masters of combat technique
- Tests warrior spirit

**Ground Guild Master - Tremor**
- Shaker of the earth
- Masters of earthen power
- Stands unmovable

## How to Play

### Starting the Adventure

```bash
python3 pokemon_cli_game_expanded.py
```

### Main Menu Options

1. **Start a Battle** - Battle random wild Pokemon to level up
2. **Challenge a Guild Master** - Progress through the story campaign
3. **View Your Pokemon** - Examine your team with stats and HP bars
4. **Create a Custom Team** - Start a new adventure with your chosen team
5. **View Guild Status** - Track which Guild Masters you've defeated
6. **Exit** - End your adventure

### Story Campaign Flow

1. Create your trainer name and initial team
2. Challenge Guild Masters in order (Fire → Water → Grass → Flying → Psychic → Ghost → Fighting → Ground)
3. Each Guild Master battle increases in difficulty
4. Defeat all 8 Guild Masters to unlock the legendary Pokemon
5. Experience the epilogue and legendary encounter

### Team Management

- Start with 1-6 Pokemon
- Each Pokemon has 2 random moves from their type's move pool
- Pokemon gain experience through battles
- View HP bars for each Pokemon
- Replace fainted Pokemon before guild battles

### Pokemon Switching During Battle

When your active Pokemon faints during battle:
1. You'll be prompted to choose your next Pokemon from your team
2. Select from any non-fainted team members with visual HP bars
3. Your newly selected Pokemon enters the battle
4. The battle continues until all your Pokemon are defeated
5. Choose "0" (forfeit) to end the battle early if desired

**Strategy Tips:**
- Use type advantages when switching Pokemon
- Check opponent Pokemon HP before deciding which team member to use
- Keep your team balanced with different types
- Save high-HP Pokemon for critical moments
- Don't waste strong Pokemon on weakened opponents

### Battle Mechanics

**Type Matchup Example:**
- Fire beats Grass (super effective = 2x damage)
- Water beats Fire (super effective = 2x damage)
- Grass beats Water (super effective = 2x damage)
- Flying beats Fighting (super effective = 2x damage)
- Psychic beats Fighting & Ghost (super effective = 2x damage)
- Ghost beats Psychic (super effective = 2x damage)
- And many more strategic combinations!

**Turn Calculation:**
- Faster Pokemon (higher level) attack first
- Both Pokemon attack each turn
- Damage is calculated with type effectiveness, STAB, and critical chance
- Turns continue until someone faints or 100-turn limit is reached

## Strategy Guide

### Type Advantages
Study the type matchup chart! Knowing which types beat others is crucial.

### Team Composition
- Include diverse types to handle any opponent
- Water types are strong against Fire types
- Grass types are strong against Water types
- Flying types counter Fighting types
- Psychic types counter Fighting types

### Guild Master Tips
- Each Guild Master specializes in one type
- Anticipate their type and prepare counters
- Your team will level up as you progress
- Defeat wild Pokemon between guild battles to gain experience

### Battle Strategy
- Use super-effective moves whenever possible
- Save high-power moves for critical moments
- Track opponent Pokemon health
- Choose Pokemon based on type advantage

## Game Statistics

- **Total Pokemon Types**: 8
- **Total Pokemon Available**: 40 (5 per type)
- **Total Moves Available**: 24 (3 per type)
- **Maximum Team Size**: 6 Pokemon
- **Story Length**: 8 Guild Master battles
- **Maximum Battle Duration**: 100 turns
- **Experience Gain**: +1 level per guild victory

## NPCs & Trainers

### Guild Masters

| Name | Title | Type | Specialty |
|------|-------|------|-----------|
| Blaine | Fire Master | Fire | Intense passion, volcanic power |
| Misty | Water Master | Water | Fluid strategy, aquatic wisdom |
| Erika | Grass Specialist | Grass | Natural harmony, growth |
| Sky Captain | Flying Master | Flying | Aerial dominance, wind mastery |
| Psyche | Psychic Master | Psychic | Mental power, mystic insight |
| Specter | Ghost Master | Ghost | Ethereal realm, spectral arts |
| Champion | Fighting Master | Fighting | Combat expertise, warrior spirit |
| Tremor | Ground Master | Ground | Earthen strength, stability |

## Achievements & Milestones

- **First Victory**: Defeat your first wild Pokemon
- **Guild Initiate**: Defeat your first Guild Master
- **Type Hunter**: Defeat 3 Guild Masters
- **Master Trainer**: Defeat 5 Guild Masters
- **Legendary Finder**: Defeat all 8 Guild Masters
- **Champion Status**: Complete the full campaign

## Technical Details

- **Language**: Python 3
- **Framework**: Pure Python with no external dependencies
- **Battle Turn Limit**: 100 (doubled for longer campaigns)
- **Pokemon Generation**: Fully randomized per battle
- **Save System**: Track progress through story_progress variable
- **Performance**: Optimized for smooth turn-based gameplay

## Gameplay Example

```
============================================================
POKEMON QUEST - MAIN MENU
============================================================

Trainer: Ash | Level: 11 | Wins: 15
Story Progress: 3/8 Guild Masters Defeated

--- Turn 23/100 ---

Ash's Pokemon Moves:
  1. Fire Punch (Fire Type) - Power: 75
  2. Flame Burst (Fire Type) - Power: 70

Choose a move (1-2): 1

Cyndaquil used Fire Punch! Bellsprout took 95 damage. It's super effective!
Bellsprout HP: 0/85

============================================================
BATTLE OVER! Ash WINS!

Bellsprout fainted!

Cyndaquil wins the battle!
============================================================
```

## Controls

- **Number Keys (1-6)**: Menu selections and move choices
- **Y/N**: Yes/No prompts
- **Enter**: Confirm selections and progress
- **Ctrl+C**: Interrupt game (graceful shutdown)

## Future Enhancement Ideas

- Trainer-specific Pokemon specialization
- Pokemon evolution system
- Multiple save files
- Battle recorder and replay system
- Leaderboard for fastest completion
- Randomized guild master order
- Legendary Pokemon encounters
- Post-game super-trainers
- Pokemon breeding system
- Trading system for multiplayer

## Version History

- **v1.0**: Original game with 3 types and 50-turn limit
- **v2.0**: Expanded version with 8 types, full story, and 100-turn limit

## Credits

Pokemon Quest: Gold & Silver Edition - Expanded
An original text-based game inspired by the Pokemon series
Created for adventure and strategy enthusiasts

Developed with Python 3 and a passion for classic Pokemon games!
