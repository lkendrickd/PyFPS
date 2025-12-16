# Project Context

## Purpose
A Wolfenstein 3D clone developed in Python, aiming to recreate the classic FPS experience using modern OpenGL rendering techniques while maintaining the retro aesthetic. The project serves as an educational exploration of game engine development, raycasting, and shader programming.

## Tech Stack
- **Language:** Python 3.x
- **Rendering:** ModernGL (OpenGL 3.3+ bindings)
- **Windowing & Input:** Pygame
- **Math:** PyGLM (Vectors/Matrices), Numpy
- **Level Data:** PyTMX (Tiled Map Editor support)

## Project Conventions

### Code Style
- **Naming:** Snake_case for variables/functions, PascalCase for classes.
- **Math:** Extensive use of `glm` for vector math (e.g., `glm.vec2`, `glm.vec3`).
- **Imports:** 
  - `import pygame as pg`
  - `import moderngl as mgl`
  - `from settings import *` (Common pattern in this project)
- **Configuration:** All game constants and configuration are centralized in `settings.py`.

### Architecture Patterns
- **Engine-Centric:** The `Engine` class (`engine.py`) serves as the central coordinator, managing subsystems like `Player`, `Scene`, `Sound`, and `LevelMap`.
- **Game Loop:** Controlled by `Game` class in `main.py`, delegating updates to `Engine`.
- **Rendering Pipeline:** 
  - Uses `ShaderProgram` to manage GLSL shaders.
  - `Scene` handles the rendering of game objects.
  - `RayCasting` is used for visibility/rendering logic typical of 2.5D games.
- **Level Management:** Levels are designed in Tiled (`.tmx` files) and loaded via `LevelMap`.
- **Entity Component:** `Player` inherits from `Camera`. `PlayerAttribs` manages persistent state (health, ammo).

### Testing Strategy
- Currently, no automated testing framework is in place.
- Testing is primarily manual, involving running the game and verifying gameplay mechanics.

### Git Workflow
- Standard feature branch workflow recommended.

## Domain Context
- **Raycasting:** The project implements raycasting techniques for wall rendering and collision detection.
- **Shaders:** Custom GLSL shaders (`.vert`, `.frag`) in `shaders/` directory handle rendering of levels, sprites, and HUD.
- **Asset Management:** Textures and sprites are loaded from `assets/` and managed by `Textures` class.

## Important Constraints
- **OpenGL Version:** Requires OpenGL 3.3 Core Profile.
- **Performance:** Critical reliance on `numpy` and `moderngl` for efficient rendering in Python.

## External Dependencies
- **Tiled Map Editor:** Used for creating level maps (`.tmx` files).
