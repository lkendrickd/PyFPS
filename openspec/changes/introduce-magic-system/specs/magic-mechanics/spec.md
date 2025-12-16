# Spec: Magic Mechanics

## ADDED Requirements

#### Requirement: Mana Resource
The player must have a Mana resource that is consumed when casting spells.
- **Scenario:** Player starts game
  - Given a new game starts
  - Then the player should have full Mana (e.g., 100/100).
- **Scenario:** Casting consumes mana
  - Given the player has 50 Mana
  - When the player casts a "Fireball" (cost 10)
  - Then the player's Mana should decrease to 40.
- **Scenario:** Insufficient mana
  - Given the player has 5 Mana
  - When the player tries to cast "Fireball" (cost 10)
  - Then the spell should not cast
  - And the Mana should remain at 5.

#### Requirement: Fireball Spell
The player can cast a Fireball spell that launches a projectile.
- **Scenario:** Casting Fireball
  - Given the player has sufficient Mana
  - When the "Cast" action is triggered
  - Then a Fireball projectile should spawn at the player's position
  - And it should travel in the direction the player is facing.

#### Requirement: Projectile Collision
Projectiles must collide with walls and enemies.
- **Scenario:** Hitting a wall
  - Given a Fireball is traveling towards a wall
  - When it reaches the wall
  - Then the projectile should be destroyed (removed from scene).
- **Scenario:** Hitting an enemy
  - Given a Fireball is traveling towards an NPC
  - When it collides with the NPC
  - Then the NPC should take damage
  - And the projectile should be destroyed.
