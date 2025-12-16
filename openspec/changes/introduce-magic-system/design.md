# Design: Magic System Architecture

## Overview
The magic system will introduce `Spell` and `Projectile` entities. Spells are "equipped" or "cast" by the player, consuming `Mana`. Casting a spell spawns a `Projectile` into the `Scene`.

## Architecture

### 1. Player Attributes
-   Modify `PlayerAttribs` in `player.py` to include `self.mana` and `self.max_mana`.
-   Add regeneration logic or mana potions (future).

### 2. Spell Class
-   Create `game_objects/spell.py`.
-   `Spell` class manages:
    -   Cooldowns.
    -   Mana cost.
    -   Animation (hand casting animation).
    -   Spawning of `Projectile`.

### 3. Projectile Class
-   Create `game_objects/projectile.py`.
-   Inherits from `GameObject` (or similar base).
-   Attributes: `position`, `velocity`, `damage`, `speed`.
-   **Update Loop**: Moves along its velocity vector each frame.
-   **Collision**:
    -   Needs to check collision with `LevelMap` (walls) and `NPC`s.
    -   Raycasting check or simple distance check for collision?
    -   *Decision*: Use a simplified raycast or step-check for wall collisions. For NPCs, use distance check.

### 4. Rendering
-   Projectiles will be rendered as billboarded sprites (like NPCs/Items).
-   Need to ensure they are added to the `Scene`'s object list to be drawn.

### 5. Input
-   Update `settings.py` to add `CAST_SPELL` key.
-   Update `Player.handle_events` to trigger spell casting.

## Data Structures
-   `SPELL_SETTINGS` in `settings.py`:
    ```python
    SPELL_SETTINGS = {
        'fireball': {
            'mana_cost': 10,
            'damage': 50,
            'speed': 0.5,
            'sprite': 'fireball.png'
        }
    }
    ```
