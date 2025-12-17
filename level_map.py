import pytmx
from settings import *
from game_objects.door import Door
from game_objects.item import Item
from game_objects.npc import NPC


class LevelMap:
    def __init__(self, eng, tmx_file='test.tmx'):
        self.eng = eng
        self.tiled_map = pytmx.TiledMap(f'resources/levels/{tmx_file}')
        self.gid_map = self.tiled_map.tiledgidmap

        self.width = self.tiled_map.width
        self.depth = self.tiled_map.height

        self.wall_map, self.floor_map, self.ceil_map = {}, {}, {}
        self.door_map, self.item_map,  = {}, {}
        self.npc_map, self.npc_list = {}, []
        #
        self.parse_level()

    def get_id(self, gid):
        return self.gid_map[gid] - 1

    def parse_level(self):
        # get player pos
        player_layer = self.tiled_map.get_layer_by_name('player')
        player = player_layer.pop()  # type: ignore
        player_pos = glm.vec3(player.x / TEX_SIZE, PLAYER_HEIGHT, player.y / TEX_SIZE)
        # set pos
        self.eng.player.position = player_pos

        walls = self.tiled_map.get_layer_by_name('walls')  # type: ignore
        floors = self.tiled_map.get_layer_by_name('floors')  # type: ignore
        ceilings = self.tiled_map.get_layer_by_name('ceilings')  # type: ignore

        for ix in range(self.width):
            for iz in range(self.depth):
                if gid := walls.data[iz][ix]:  # type: ignore
                    # wall hash map
                    self.wall_map[(ix, iz)] = self.get_id(gid)

                if gid := floors.data[iz][ix]:  # type: ignore
                    # floor hash map
                    self.floor_map[(ix, iz)] = self.get_id(gid)

                if gid := ceilings.data[iz][ix]:  # type: ignore
                    # ceiling  hash map
                    self.ceil_map[(ix, iz)] = self.get_id(gid)

        # get doors
        door_objects = self.tiled_map.get_layer_by_name('doors')  # type: ignore
        for obj in door_objects:  # type: ignore
            # door hash map
            pos = int(obj.x / TEX_SIZE), int(obj.y / TEX_SIZE)
            door = Door(self, tex_id=self.get_id(obj.gid), x=pos[0], z=pos[1])
            self.door_map[pos] = door

        # get items
        items = self.tiled_map.get_layer_by_name('items')  # type: ignore
        for obj in items:  # type: ignore
            # item hash map
            pos = int(obj.x / TEX_SIZE), int(obj.y / TEX_SIZE)
            item = Item(self, tex_id=self.get_id(obj.gid), x=pos[0], z=pos[1])
            self.item_map[pos] = item

        # get npc
        npc = self.tiled_map.get_layer_by_name('npc')  # type: ignore
        for obj in npc:  # type: ignore
            # npc map
            pos = int(obj.x / TEX_SIZE), int(obj.y / TEX_SIZE)
            npc = NPC(self, tex_id=self.get_id(obj.gid), x=pos[0], z=pos[1])
            self.npc_map[pos] = npc
            self.npc_list.append(npc)

        # update player data
        self.eng.player.wall_map = self.wall_map
        self.eng.player.door_map = self.door_map
        self.eng.player.item_map = self.item_map
