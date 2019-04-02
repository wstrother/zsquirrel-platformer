from zsquirrel.entities import Layer


class GameLayer(Layer):
    def __init__(self, name):
        super(GameLayer, self).__init__(name)

        self.sprite_layer = None
        self.collision_layer = None
        self.camera_layer = None
        self.hud_layer = None

        self.update_methods = [
            # handle own events
            self.clock.tick,

            # handle sub_layer events
            self.update_sub_layers,

            # handle command inputs / input devices
            self.update_controllers,

            # apply inputs to sprite state machines
            self.update_state_machines,

            # handle forces / collisions
            self.update_physics,

            # handle sprite events
            self.update_sprites
        ]

    def set_sprite_layer(self, layer):
        self.sprite_layer = layer
        layer.set_parent_layer(self)

    def set_collision_layer(self, layer):
        self.collision_layer = layer
        layer.set_parent_layer(self)

    def set_camera_layer(self, layer):
        self.camera_layer = layer
        layer.set_parent_layer(self)

    def set_hud_layer(self, layer):
        self.hud_layer = layer
        layer.set_parent_layer(self)

    def update_state_machines(self):
        for sprite in self.get_sprites():
            if sprite.state_machine:
                sprite.state_machine.update()

                if sprite.handle_state:
                    sprite.handle_state()

    def update_physics(self):
        cl = self.collision_layer

        if cl:
            if cl.wall_cs:
                cl.handle_sprite_collisions()

            if cl.sprite_cs:
                cl.handle_wall_collisions()

        for sprite in self.get_sprites():
            if sprite.physics:
                sprite.physics.update()

    def get_graphics(self, offset=None):
        args = []

        args += self.camera_layer.get_graphics()

        if self.hud_layer:
            args += self.hud_layer.get_graphics()

        return args


class CollisionLayer(Layer):
    def __init__(self, name):
        super(CollisionLayer, self).__init__(name)

        self.wall_cs = None
        self.sprite_cs = None

    def set_wall_cs(self, cs):
        self.wall_cs = cs

    def set_sprite_cs(self, cs):
        self.sprite_cs = cs

    def handle_wall_collisions(self):
        wall_cs = self.wall_cs
        for (wall, sprite) in wall_cs.get_pairs():
            collision = wall_cs.test_method(wall, sprite)

            if collision:
                sprite.handle_event({
                    "name": "wall_collision",
                    "wall": wall
                })
                wall_cs.handle_method(wall, sprite, collision)

    def handle_sprite_collisions(self):
        self.sprite_cs.update()


# class HudLayer(Layer):
#     def __init__(self, name):
#         super(HudLayer, self).__init__(name)
