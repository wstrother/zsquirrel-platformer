from zsquirrel.entities import Sprite
from zsquirrel.physics.physics import Physics
from zsquirrel.utils.geometry import Wall, Rect


class GameSprite(Sprite):
    def __init__(self, name):
        super(GameSprite, self).__init__(name)

        self.last_state = "default"
        self.state_machine = None
        self.handle_state = None
        self.face_direction = 1

        self.grounded = False
        self.ground_vector = None
        self.default_g = 0

        self.ground_f = 0
        self.air_f = 0

        self.physics = Physics(self, 1, 0, 0, 1)

    def set_physics(self, m, g, e, f):
        self.set_mass(m)

        self.set_gravity(g)
        self.default_g = g

        self.set_elasticity(e)

        self.set_friction(f)
        self.ground_f = f
        self.air_f = f * 0.1

    def get_velocity(self):
        return self.physics.velocity

    def set_mass(self, value):
        self.physics.mass = value

    def set_gravity(self, g):
        self.physics.gravity = g

    def set_friction(self, f):
        self.physics.friction = f

    def set_elasticity(self, e):
        self.physics.elasticity = e

    def get_state(self):
        state = self.graphics.get_state()

        return state.replace("_left", "")

    def set_state(self, state):
        self.state_machine.set_state(state)

    def set_state_machine(self, machine):
        self.state_machine = machine

    def set_state_handler(self, method):
        self.handle_state = method

    def set_face_direction(self, value):
        self.face_direction = value

    def get_body_rect(self):
        r = self.graphics.animations[
            self.graphics.get_state()
        ].data["body"]
        rect = Rect(r["size"], r["position"])
        rect.move(self.position)

        return rect

    def get_collision_points(self):
        r = self.get_body_rect()

        return (
            r.topright, r.topleft,
            r.center,
            r.bottomright, r.bottomleft
        )

    def get_collision_skeleton(self):
        rect = self.get_body_rect()

        mt = rect.midtop
        mb = rect.midbottom
        ml = rect.midleft
        mr = rect.midright

        h = Wall(ml, mr)
        v = Wall(mt, mb)

        return h, v

    def on_wall_collision(self):
        e = self.event
        w = e["wall"]
        self.ground_vector = w
        self.grounded = True

    def on_change_state(self):
        e = self.event

        self.last_state = e["last_state"]

    def on_spawn(self):
        super(GameSprite, self).on_spawn()

        self.set_state("default")
