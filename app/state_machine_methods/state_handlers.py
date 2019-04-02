from zsquirrel.utils.geometry import Vector


class StateUpdate:
    def __init__(self, sprite):
        self.sprite = sprite
        self.movement = Vector(0, 0)
        self.x, self.y = sprite.controller.get_device("Stick").get_value()
        self.a_button = sprite.controller.get_device("A")

        self.state = sprite.get_state()
        self.last = sprite.last_state
        self.frame = sprite.graphics.animation_meter.value
        self.cycle = sprite.graphics.animation_cycles

        self.direction = sprite.face_direction
        self.grounded = sprite.grounded

    @property
    def friction(self):
        return self.sprite.physics.friction

    @property
    def first_frame(self):
        return self.frame == 0 and self.cycle == 0

    @property
    def velocity(self):
        return self.sprite.physics.velocity

    def set_move_x(self, value):
        self.movement.i_hat = value

    def set_move_y(self, value):
        self.movement.j_hat = value

    def set_move(self, dx, dy):
        self.set_move_x(dx)
        self.set_move_y(dy)

    def apply_movement(self, scale=None):
        if scale:
            self.movement.scale(scale)

        self.sprite.physics.apply_force(
            *self.movement.get_value()
        )


def handle_pivot(update):
    if update.last == "pivot" and update.first_frame:
        update.sprite.face_direction *= -1


def handle_move_state(update, state, speed):
    dx = 0
    if update.state == state:
        dx = speed * update.friction * abs(update.x)

    update.set_move_x(dx)


def handle_walk(update, speed):
    handle_move_state(update, "walk", speed)


def handle_run(update, speed):
    handle_move_state(update, "run", speed)


def handle_dash(update, speed, mod):
    if update.state == "dash" and update.first_frame:
        speed *= mod
        update.velocity.i_hat = 0

        handle_move_state(update, "dash", speed)


def handle_jump_squat(update, *speeds):
    if update.state == "jump_squat":
        for s in speeds:
            state, speed = s
            if update.last == state:
                handle_move_state(update, "jump_squat", speed)


def handle_air_dodge(update, start, mod, end, g_mod):
    if update.state == "air_dodge":
        frame = update.frame
        sprite = update.sprite
        dx, dy = 0, 0

        if frame <= start:
            update.velocity.scale(0)

        if frame == start:
            dx = update.x * mod
            dy = update.y * (mod - 1)

        if frame < end and not update.grounded:
            sprite.physics.gravity = sprite.default_g * g_mod
        else:
            sprite.physics.gravity = sprite.default_g

        update.set_move(dx, dy)


def handle_jump_up(update, full, short):
    if update.state == "jump_up" and update.first_frame:
        update.sprite.grounded = False

        if update.a_button.held:
            dy = -full
        else:
            dy = -short

        update.set_move_y(dy)


def handle_fast_fall(update, speed):
    if update.state == "fast_fall" and update.first_frame:
        update.set_move_y(speed)


def handle_air_drift(update, mod, v_mod, *states):
    if update.state in states:
        dx = update.x * mod
        update.velocity.i_hat *= v_mod
        update.set_move_x(dx)


def handle_special_fall(update, mod):
    if update.state == "special_fall" and update.first_frame:
        update.velocity.i_hat *= mod


def squirrel_state_handler(sprite):
    update = StateUpdate(sprite)

    if sprite.grounded:
        sprite.physics.friction = sprite.ground_f

        handle_pivot(update)

        handle_walk(update, 8)
        handle_dash(update, 20, 1.5)
        handle_run(update, 16)
        handle_jump_squat(
            update,
            ("walk", 8),
            ("dash", 20),
            ("run", 16)
        )

        update.movement.i_hat *= update.direction
        update.movement.rotate(
            sprite.ground_vector.get_angle()
        )

    else:
        sprite.physics.friction = sprite.air_f

        handle_air_dodge(update, 2, 14, 16, .25)
        handle_jump_up(update, 35, 24)
        handle_fast_fall(update, 10)
        handle_special_fall(update, .55)

        handle_air_drift(
            update, .75, .95,
            "jump_up",
            "jump_apex",
            "jump_fall",
            "fast_fall"
        )

    update.apply_movement(1.4)
