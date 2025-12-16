# Proposal: Introduce Magic System

## Summary
Implement a magic combat system to complement the existing weapon mechanics. This includes a Mana resource, spell casting mechanics (starting with a "Fireball" spell), and UI updates to display Mana.

## Motivation
The project aims to evolve into a "guns and magic spells game". Currently, only hitscan weapons (knife, pistol, rifle) are implemented. Adding a magic system is the first step towards this goal, allowing for projectile-based combat and resource management beyond ammo.

## Proposed Changes
1.  **Mana Resource**: Add `mana` attribute to `PlayerAttribs` and `Player`.
2.  **Spell System**: Create a `Spell` class (similar to `Weapon`) but for casting magic.
3.  **Fireball Spell**: Implement a specific `Fireball` spell that launches a projectile.
4.  **Projectile Logic**: Create a `Projectile` class to handle moving objects that deal damage on impact.
5.  **UI Update**: Update the HUD to display a Mana bar or counter.
6.  **Input Handling**: Map a key (e.g., `Mouse Right Click` or `4`) to cast spells.

## Alternatives Considered
-   **Magic as Weapons**: We could implement spells just as another "weapon" ID. However, separating them allows for dual-wielding in the future (gun in one hand, spell in other) or different resource mechanics (cooldowns vs ammo).
-   **Hitscan Magic**: Making spells hitscan (instant hit) like guns would be easier but less "magical". Projectiles offer more gameplay depth (dodging, travel time).

## Risks
-   **Performance**: Adding many projectiles might impact performance if not optimized, though for a Wolfenstein clone this should be negligible.
-   **Complexity**: Integrating projectiles into the raycasting engine might be tricky if we want them to be true 3D objects vs 2D sprites. We will start with billboarded sprites.
