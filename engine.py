from player import Player, PlayerAttribs
from scene import Scene
from shader_program import ShaderProgram
from path_finding import PathFinder
from ray_casting import RayCasting
from level_map import LevelMap
from textures import Textures
from sound import Sound
import pygame as pg


class Engine:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.num_level = 0

        self.textures = Textures(self)
        self.sound = Sound()

        self.player_attribs = PlayerAttribs()
        self.player: Player | None = None
        self.shader_program: ShaderProgram | None = None
        self.scene: Scene | None = None

        self.level_map: LevelMap | None = None
        self.ray_casting: RayCasting | None = None
        self.path_finder: PathFinder | None = None
        self.new_game()

    def new_game(self):
        pg.mixer.music.play(-1)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.level_map = LevelMap(
            self, tmx_file=f'level_{self.player_attribs.num_level}.tmx'
        )
        self.ray_casting = RayCasting(self)
        self.path_finder = PathFinder(self)
        self.scene = Scene(self)

    def update_npc_map(self):
        assert self.level_map is not None
        new_npc_map = {}
        for npc in self.level_map.npc_list:
            if npc.is_alive:
                new_npc_map[npc.tile_pos] = npc
            else:
                self.level_map.npc_list.remove(npc)
        #
        self.level_map.npc_map = new_npc_map

    def handle_events(self, event):
        assert self.player is not None
        self.player.handle_events(event=event)

    def update(self):
        assert self.player is not None
        assert self.shader_program is not None
        assert self.scene is not None
        self.update_npc_map()
        self.player.update()
        self.shader_program.update()
        self.scene.update()

    def render(self):
        assert self.scene is not None
        self.scene.render()
