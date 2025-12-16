# Tasks

- [ ] **Core Attributes**
    - [ ] Add `mana` and `max_mana` to `PlayerAttribs` in `player.py`.
    - [ ] Add `mana` to `Player` class sync logic.
    - [ ] Add `MANA_MAX` and `MANA_INIT` to `settings.py`.

- [ ] **Spell Infrastructure**
    - [ ] Create `game_objects/spell.py` with base `Spell` class.
    - [ ] Define `SPELL_SETTINGS` in `settings.py`.
    - [ ] Implement `cast()` method in `Spell` that checks mana and cooldown.

- [ ] **Projectile System**
    - [ ] Create `game_objects/projectile.py`.
    - [ ] Implement `Projectile` class inheriting from `GameObject`.
    - [ ] Implement `update()` for movement and wall collision detection.
    - [ ] Implement `check_hit()` for NPC collision.

- [ ] **Integration**
    - [ ] Add `spells` list/dict to `Player`.
    - [ ] Bind input (e.g., Right Click) to cast active spell.
    - [ ] Ensure projectiles are added to `Scene` objects list for rendering.

- [ ] **Assets & UI**
    - [ ] Add placeholder sprite for Fireball projectile.
    - [ ] Add placeholder sprite for Hand Casting animation.
    - [ ] Update HUD to display Mana value/bar.
