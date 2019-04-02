from zsquirrel.ui.hud_interface import HudSprite


class SpriteStateHud(HudSprite):
    def __init__(self, *args):
        super(SpriteStateHud, self).__init__(*args)

        self.cache_size = 1
        self.set_cache_func(
            lambda: self.get_cache_changes(1)
        )

    def set_sprite(self, sprite):
        self.set_value_func(sprite.get_state)

    def set_cache_size(self, size):
        self.cache_size = size
        self.set_cache_func(
            lambda: self.get_cache_changes(size)
        )


class EventStreamHud(HudSprite):
    def __init__(self, *args):
        super(EventStreamHud, self).__init__(*args)

        self.cache_size = 1
        self.set_cache_func(
            self.get_cache_any
        )

    def on_cache_event(self):
        trigger = self.event["trigger"]["name"]
        entity = self.event["entity"]

        self.cache.append(
            "{}: {}".format(entity.name, trigger)
        )
