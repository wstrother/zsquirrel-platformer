from zsquirrel.ui.hud_interface import HudInterface
from app.sprites.hud_sprites import SpriteStateHud, EventStreamHud


class DebugInterface(HudInterface):
    def set_sprite_state_hud(self, layer, sprite, size):
        name = "{} State Hud Sprite".format(sprite.name)
        hud = SpriteStateHud(name, 60, 12)
        self.set_value(name, hud)

        hud.set_sprite(sprite)
        hud.set_cache_size(size)
        self.set_text(hud, "")

        layer.groups[0].add_member(hud)

    def set_event_stream_hud(self, layer, *listeners):
        name = "Event Stream Hud"
        hud = EventStreamHud(name, 5, 12)

        self.set_text(hud, "")
        hud.set_position(200, 0)

        layer.groups[0].add_member(hud)

        for l in listeners:
            entity, *names = l
            for n in names:
                entity.add_listener(
                    {"target": hud, "name": n, "response": {
                        "name": "cache_event", "entity": entity
                    }}
                )
