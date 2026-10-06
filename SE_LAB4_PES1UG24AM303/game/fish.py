"""
Fish: swims horizontally at a fixed depth, wrapping around when it
exits the screen. Several fish types exist, differing in speed, point
value, size and color.
"""

import random

import pygame

# name: (speed, point_value, width, height, color)
FISH_TYPES = {
    "minnow": {"speed": 2, "point_value": 10, "width": 30, "height": 14, "color": (120, 220, 120)},
    "bass":   {"speed": 3, "point_value": 25, "width": 42, "height": 20, "color": (240, 170, 60)},
    "tuna":   {"speed": 6, "point_value": 60, "width": 56, "height": 24, "color": (230, 70, 90)},
}

# Relative spawn likelihood: fast, valuable fish are rarer.
SPAWN_WEIGHTS = {"minnow": 5, "bass": 3, "tuna": 1}


class Fish:
    def __init__(self, x, y, speed, width=36, height=18, point_value=10,
                 color=(80, 180, 220), kind="minnow"):
        self.x = float(x)
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.point_value = point_value
        self.color = color
        self.kind = kind

    def update(self, screen_width):
        self.x += self.speed
        if self.speed > 0 and self.x > screen_width:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = screen_width

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )


def make_fish(kind, x, y, direction=1):
    """Build a fish of the given type. direction is +1 (right) or -1 (left)."""
    t = FISH_TYPES[kind]
    return Fish(x=x, y=y, speed=t["speed"] * direction, width=t["width"],
                height=t["height"], point_value=t["point_value"],
                color=t["color"], kind=kind)


def random_fish(screen_width, min_y, max_y, x=None):
    """Create a random fish type at a random depth and direction."""
    kind = random.choices(list(SPAWN_WEIGHTS), weights=list(SPAWN_WEIGHTS.values()))[0]
    direction = random.choice((-1, 1))
    if x is None:
        x = -40 if direction > 0 else screen_width + 40
    return make_fish(kind, x, random.randint(min_y, max_y), direction)
