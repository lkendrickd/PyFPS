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

### Core Files
- **`main.py`**: Entry point. Initializes pygame window, OpenGL context, and the main game loop with event handling, updates, and rendering.
- **`engine.py`**: Central hub managing the game state, player, scene, and level loading. Coordinates all subsystems and handles NPC lifecycle.
- **`settings.py`**: Configuration file for OpenGL settings, resolution, FOV, player stats, controls, texture IDs, NPC configurations, and HUD layout.
- **`player.py`**: Handles player movement, camera control, collision detection, shooting mechanics, and player attributes (health, ammo, weapons).
- **`camera.py`**: Implements first-person camera with position tracking, rotation matrices, and view/projection transformations.
- **`ray_casting.py`**: Implements the core raycasting algorithm using voxel traversal for collision detection, visibility testing, and wall/object intersection.
- **`path_finding.py`**: A* pathfinding implementation for NPC navigation using a grid-based system.
- **`level_map.py`**: Loads and parses Tiled map files (`.tmx`), extracts wall geometry, spawns NPCs and items.
- **`scene.py`**: Manages the rendering of the 3D scene, coordinates all renderable objects, and manages the HUD.
- **`shader_program.py`**: Manages GLSL shader programs, uniform updates, and provides shader access to other systems.
- **`textures.py`**: Loads PNG textures and creates OpenGL texture arrays for walls, sprites, and HUD elements.
- **`texture_builder.py`**: Utility to build sprite sheets and texture arrays from individual texture files.
- **`texture_id.py`**: Defines texture ID enumeration for walls, items, digits, and weapon sprites.
- **`sound.py`**: Handles background music and sound effects using pygame mixer.

### Game Objects (`game_objects/`)
- **`game_object.py`**: Base class for all game entities with position, rotation, scale, and model matrix calculation.
- **`npc.py`**: Enemy AI with states (idle, chase, attack, death), sprite animations, pathfinding, and health management.
- **`weapon.py`**: Weapon system managing shooting animations, ammo consumption, and different weapon types (knife, pistol, rifle).
- **`door.py`**: Interactive door objects with open/close animations and collision handling.
- **`item.py`**: Collectible items (health packs, ammo, weapons, keys) with pickup logic.
- **`hud.py`**: Heads-up display showing health, ammo, and FPS using digit sprites and icons.

### Meshes (`meshes/`)
- **`base_mesh.py`**: Abstract base class for OpenGL mesh objects defining the interface for VAO/VBO management.
- **`quad_mesh.py`**: Simple quad mesh for sprites and HUD elements.
- **`instanced_quad_mesh.py`**: Instanced rendering mesh for efficiently drawing multiple quads (doors, NPCs, items).
- **`level_mesh.py`**: Mesh for rendering the level geometry (walls and floors).
- **`level_mesh_builder.py`**: Builds optimized vertex data for level geometry from map data.
- **`weapon_mesh.py`**: Specialized mesh for first-person weapon rendering.

### Shaders (`shaders/`)
- **`level.vert/frag`**: Vertex and fragment shaders for rendering level geometry with texture mapping.
- **`weapon.vert/frag`**: Shaders for first-person weapon rendering.
- **`instanced_billboard.vert/frag`**: Billboard shaders for NPCs and items using instanced rendering.
- **`instanced_door.vert/frag`**: Specialized shaders for door rendering with proper depth handling.
- **`instanced_hud.vert/frag`**: Shaders for rendering HUD elements in screen space.

### Assets (`assets/`)
- **`textures/`**: Individual texture files for walls, sprites, and UI elements.
- **`texture_array/`**: Generated texture array for efficient GPU texture access.
- **`sprite_sheet/`**: Generated sprite sheet combining all textures.
- **`sounds/`**: Audio files for music and sound effects.

### Resources (`resources/`)
- **`levels/`**: Tiled map files (`.tmx`) defining level layouts, wall placement, and entity spawns.

### Project Management (`openspec/`)
- **`AGENTS.md`**: Instructions for AI assistants working on this project.
- **`project.md`**: Project-wide specifications and conventions.
- **`changes/`**: Proposed changes and feature designs (menu system, magic system, etc.).
- **`specs/`**: Detailed specifications for project components.

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
