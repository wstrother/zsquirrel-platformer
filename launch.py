import pygame
from zsquirrel.context import Context
from zsquirrel.game import Game
from zsquirrel.control.controller_interface import ControllerInterface
from zsquirrel.graphics import GraphicsInterface
from zsquirrel.entities import Layer, Sprite
from app.pygame_screen import PygameScreen
from app.get_context import get_context_classes
import app.game_constants as con


if __name__ == "__main__":
    entities, interfaces = get_context_classes()
    entities += [
        Layer, Sprite
    ]
    interfaces += [
        ControllerInterface,
        GraphicsInterface
    ]

    c = Context.get_default_context(
        Game(
            screen=PygameScreen(con.SCREEN_SIZE),
            clock=pygame.time.Clock(),
            frame_rate=con.FPS
        ),
        entities,
        interfaces
    )
    c.load_environment("platformer.json")
    c.run_game()
