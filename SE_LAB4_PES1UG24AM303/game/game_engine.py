"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic, including the 30-second round timer.
"""

import random

import pygame

from game.hook import Hook, IDLE
from game.fish import random_fish
from game.catch import check_catch
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y

ROUND_SECONDS = 30
FISH_COUNT = 5
FISH_MIN_Y = SURFACE_Y + 50
FISH_MAX_Y = MAX_DEPTH_Y - 25

PLAYING = "playing"
GAME_OVER = "game_over"

CAST_KEYS = (pygame.K_SPACE, pygame.K_DOWN, pygame.K_RETURN)
RESTART_KEYS = (pygame.K_r,)


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a fresh round: score, timer, hook and fish all reset."""
        self._events = set()        # keys seen via handle_event (if main.py forwards them)
        self._prev_down = set()     # keys that were held last frame (polling)
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            random_fish(WIDTH, FISH_MIN_Y, FISH_MAX_Y, x=random.randint(0, WIDTH))
            for _ in range(FISH_COUNT)
        ]
        self.hooked_fish = None
        self.score = 0
        self.state = PLAYING
        self.round_start = pygame.time.get_ticks()
        self.time_left = float(ROUND_SECONDS)

    def handle_event(self, event):
        """Optional: main.py may forward events. The engine works without it too."""
        if event.type == pygame.KEYDOWN:
            self._events.add(event.key)

    def _keys_pressed_now(self):
        """Keys newly pressed this frame, from events AND keyboard polling."""
        held = pygame.key.get_pressed()
        down = {k for k in CAST_KEYS + RESTART_KEYS if held[k]}
        newly = (down - self._prev_down) | self._events
        self._prev_down = down
        self._events = set()
        return newly

    def update(self):
        newly = self._keys_pressed_now()

        if self.state == GAME_OVER:
            if any(k in newly for k in RESTART_KEYS):
                self.reset()
            return

        if any(k in newly for k in CAST_KEYS):
            self.hook.start_cast()   # ignored unless the hook is idle

        elapsed = (pygame.time.get_ticks() - self.round_start) / 1000.0
        self.time_left = max(0.0, ROUND_SECONDS - elapsed)
        if self.time_left <= 0:
            # Round over: no more catches. A fish still on the line doesn't count.
            self.state = GAME_OVER
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self.hooked_fish = None
                # Replace the landed fish so the water stays populated.
                self.fish_list.append(random_fish(WIDTH, FISH_MIN_Y, FISH_MAX_Y))
        else:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    def draw(self, surface, font):
        from game import renderer
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Time: {int(self.time_left + 0.999)}s",
                           (WIDTH - 120, 10))

        if self.state == PLAYING:
            if self.hook.state == IDLE:
                renderer.draw_text(surface, font, "SPACE / DOWN: cast", (10, HEIGHT - 30))
        else:
            renderer.draw_game_over(surface, font, self.score)
