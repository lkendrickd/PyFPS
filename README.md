# Wolfenstein-3D-Clone
Wolfenstein 3D using OpenGL

Wolfeinstein 3D clone written in Python using Pygame, ModernGL, Numpy, PyTMX, PyGLM

You can create your own level in the Tiled editor, see more details here:
https://youtu.be/yJXuvK_eLrQ?si=ShmzXXb1uSqtDC4u




## Project Overview

This project is a modern implementation of the classic Wolfenstein 3D engine using Python and OpenGL (via ModernGL). It serves as an educational platform for understanding 2.5D game engines, raycasting, and shader programming.

### Key Features
- **Rendering Engine**: Uses ModernGL for hardware-accelerated rendering.
- **Raycasting**: Implements a voxel traversal algorithm for visibility and collision detection.
- **Level Editor Support**: Loads levels directly from Tiled (`.tmx`) files.
- **Entity System**: Includes support for NPCs, weapons, and interactive objects like doors.

## Quickstart

Get up and running in seconds:

```bash
# 1. Clone and enter the repository
git clone <repository-url>
cd PyFPS

# 2. Set up the environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the game
python main.py
```

### Prerequisites
- Python 3.10+
- A graphics card supporting OpenGL 3.3+

## Controls

| Key | Action |
| :--- | :--- |
| **W, A, S, D** | Move Forward, Left, Backward, Right |
| **Q, E** | Rotate Camera Left / Right |
| **Mouse** | Look around |
| **Left Click** | Shoot |
| **F** | Interact (Open Doors) |
| **1, 2, 3** | Switch Weapons (Knife, Pistol, Rifle) |
| **Esc** | Exit Game |

## Project Structure

- **`main.py`**: Entry point. Initializes the game loop and context.
- **`engine.py`**: Central hub managing the game state, player, scene, and level loading.
- **`settings.py`**: Configuration file for resolution, FOV, player stats, and keys.
- **`player.py`**: Handles player movement, camera control, and attributes (health, ammo).
- **`ray_casting.py`**: Implements the core raycasting algorithm for collision and visibility.
- **`level_map.py`**: Loads and parses Tiled map files (`.tmx`).
- **`scene.py`**: Manages the rendering of the 3D scene.
- **`game_objects/`**: Contains classes for entities like `NPC`, `Weapon`, `Door`, etc.
- **`shaders/`**: GLSL shader files for rendering the level, sprites, and HUD.
- **`assets/`**: Stores textures, sounds, and sprite sheets.

## Architecture

The project follows an engine-centric architecture:
1.  **Engine**: The `Engine` class initializes all subsystems (`Player`, `LevelMap`, `RayCasting`, `Scene`).
2.  **Update Loop**: The `Game` class in `main.py` calls `engine.update()`, which propagates updates to the player and active objects.
3.  **Rendering**: The `Scene` class handles drawing. It uses `RayCasting` to determine visible walls and objects, then renders them using `ShaderProgram` and ModernGL.

## Customizing Levels

Levels are created using the [Tiled Map Editor](https://www.mapeditor.org/).
1.  Open `resources/levels/level_0.tmx` in Tiled.
2.  Edit the tile layer to change walls and doors.
3.  Use the object layer to place NPCs and items.
4.  Save the file and restart the game.
