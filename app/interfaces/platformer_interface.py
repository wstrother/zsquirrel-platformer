from zsquirrel.cameras.cameras import CameraLayer
from zsquirrel.entities import Layer, Group
from zsquirrel.physics.physics_interface import PhysicsInterface
from zsquirrel.utils.geometry import Wall

from app.layers.game_layer import CollisionLayer
from app.pygame_screen import render_graphics
import app.game_constants as con


class PlatformerInterface(PhysicsInterface):
    def __init__(self, *args):
        super(PlatformerInterface, self).__init__(*args)

        self.init_order = [
            self.set_sprite_layer.__name__,
            self.set_camera_layer.__name__,
            self.set_collision_layer.__name__,
            self.set_hud_layer.__name__
        ]

    @staticmethod
    def set_hud_layer(layer, hud_layer):
        layer.set_hud_layer(hud_layer)

    def set_sprite_layer(self, layer, name, *groups):
        sprite_layer = Layer(name)
        self.set_value(name, sprite_layer)

        sprite_layer.set_groups(*groups)
        layer.set_sprite_layer(sprite_layer)

    def set_camera_layer(self, layer, name):
        camera_layer = CameraLayer(name)
        self.set_value(name, camera_layer)

        camera_layer.set_size(*con.SCREEN_SIZE)
        camera_layer.set_camera_layers(layer.sprite_layer)
        camera_layer.set_render_function(render_graphics)

        layer.set_camera_layer(camera_layer)

    def set_collision_layer(self, layer, name, level):
        level = self.get_value(level)
        walls_group = self.get_walls_group("walls_group", level["walls"])
        sprite_group = self.get_value("sprite_group")

        collision_layer = CollisionLayer(name)
        self.set_value(name, collision_layer)

        layer.set_collision_layer(collision_layer)
        collision_layer.set_wall_cs(
            self.get_collision_system(
                self.test_wall_collision,
                self.smooth_wall_collision,
                walls_group,
                sprite_group
            )
        )

        collision_layer.set_sprite_cs(
            self.get_collision_system(
                self.sprite_sprite_collision,
                self.handle_sprite_collision,
                sprite_group
            )
        )

    def get_walls_group(self, name, walls):
        g = Group(name)
        self.set_value(name, g)

        for w in walls:
            start, end = w[0], w[1]
            g.add_member(Wall(start, end))

        return g
