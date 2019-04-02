def double_tap(sprite):
    if sprite.controller:
        commands = sprite.controller.commands
        left, right = commands["DT_LEFT"], commands["DT_RIGHT"]

        return left.active or right.active


def auto(sprite):
    if sprite.graphics:
        return sprite.graphics.animation_cycles > 0


def press_forward(sprite):
    if sprite.controller:
        stick = sprite.controller.get_device("Stick")
        x, y = stick.get_value()

        if abs(x) > .2:
            stick_p = x > 0
            face_p = sprite.face_direction > 0

            return stick_p == face_p


def full_forward(sprite):
    if sprite.controller:
        stick = sprite.controller.get_device("Stick")
        x, y = stick.get_value()

        if abs(x) > .95:
            stick_p = x > 0
            face_p = sprite.face_direction > 0

            return stick_p == face_p


def tap_down(sprite):
    if sprite.controller:
        commands = sprite.controller.commands
        down = commands["DT_DOWN"]

        return down.active


def press_back(sprite):
    if sprite.controller:
        stick = sprite.controller.get_device("Stick")
        x, y = stick.get_value()

        if abs(x) > .5:
            stick_p = x > 0
            face_p = sprite.face_direction > 0

            return stick_p != face_p


def press_direction(sprite):
    if sprite.controller:
        stick = sprite.controller.get_device("Stick")
        x, y = stick.get_value()

        return abs(x) > .1


def press_down(sprite):
    if sprite.controller:
        stick = sprite.controller.get_device("Stick")
        x, y = stick.get_value()

        return y > .1


def press_jump(sprite):
    if sprite.controller:
        return sprite.controller.get_device("A").held == 1


def press_dodge(sprite):
    if sprite.controller:
        return sprite.controller.get_device("Z").held == 1


def in_air(sprite):
    return not sprite.grounded


def ground_collision(sprite):
    return sprite.grounded


def peak_jump(sprite):
    if sprite.physics:
        cycles = sprite.graphics.animation_cycles
        j = sprite.physics.velocity.j_hat

        return j >= 0 and cycles > 1
