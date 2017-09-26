import time

from ccs.core.color import BLACK
from ccs.core.decorators import registered_singleton
from .mode import LedMode, MODES


@registered_singleton(MODES, 'fade')
class FadeMode(LedMode):

    def __init__(self):
        super().__init__()
        self._color_index = 0
        self._fade_start_time = 0

    def _get_color(self, settings):
        fade_colors = settings.get('led.fade.colors')
        fade_time = settings.get('led.fade.fade_time')

        if len(fade_colors) == 0:
            return BLACK

        def get_fade_color(index):
            return fade_colors[index % len(fade_colors)]

        now = time.time()
        if now - self._fade_start_time >= fade_time:
            # Reached the next color
            self._color_index += 1
            self._color_index %= len(fade_colors)
            self._fade_start_time = now

        # Interpolate between the two boundary colors based on time
        last_color = get_fade_color(self._color_index)
        next_color = get_fade_color(self._color_index + 1)
        bias = (now - self._fade_start_time) / fade_time
        current_color = last_color * (1 - bias) + next_color * bias
        return current_color