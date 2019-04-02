from zsquirrel.animations.animation_interface import AnimationInterface
from zsquirrel.animations.animations import AnimationMachine
from app.get_context import get_methods_from_module
from app.state_machine_methods import squirrel_machine
from app.state_machine_methods import state_handlers


class GameSpriteInterface(AnimationInterface):
    def __init__(self, *args):
        super(GameSpriteInterface, self).__init__(*args)

        self.state_conditions = {
            m.__name__: m for m in get_methods_from_module(squirrel_machine)
        }
        self.state_handlers = {
            m.__name__: m for m in get_methods_from_module(state_handlers)
        }

    def set_state_handler(self, entity, method_name):
        entity.set_state_handler(
            lambda: self.state_handlers[method_name](entity)
        )

    def set_animation_machine(self, entity, data_file):
        data = self.context.load_resource(data_file)

        states = self.get_states_dict(entity, data["state_conditions"])
        machine = AnimationMachine(entity, states)
        machine.sounds = self.get_sounds_dict(data["sounds"])

        def get_state():
            state = machine.get_state()
            face = entity.face_direction

            if face == -1:
                state += "_left"

            return state

        entity.graphics.get_state = get_state
        entity.state_machine = machine

        return machine

    def get_state_condition(self, entity, name, to, condition=True, buffer=False):
        return AnimationMachine.get_condition(
            lambda: self.state_conditions[name](entity),
            to, condition=condition, buffer=buffer, name=name
        )
