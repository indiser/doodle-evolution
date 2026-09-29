import random
import numpy as np
import pygame

from config import *
import assets
from Doodle import Player
from Platform import Platform, ExplodingPlatform, MovingPlatform
from Feeder import Feeder
from Monster import Monster
from Trampoline import Trampoline

BAT_FRAMES = [assets.bat1, assets.bat2, assets.bat3]
BROKEN_FRAMES = [assets.broken_platform0, assets.broken_platform1,
                 assets.broken_platform2, assets.broken_platform3]
EXPLOSIVE_FRAMES = [assets.exploding_platform0, assets.exploding_platform1,
                    assets.exploding_platform2]

STAGNATION_LIMIT = 300   # frames with no new max height -> dead
MAX_FRAMES = 40000       # hard cap per run
SCROLL_THRESHOLD = HEIGHT // 3


class World:
    """One doodler + its own private level. Same seed => same level sequence."""

    def __init__(self, brain, seed):
        self.brain = brain
        self.rng = random.Random(seed)

        self.platforms = []
        self.feeders = []
        self.monsters = []
        self.trampolines = []

        self.alive = True
        self.score = 0.0
        self.scrolled = 0.0
        self.max_height = 0.0
        self.frames_alive = 0
        self.last_progress = 0

        start_x = WIDTH // 2 - PLATFORM_WIDTH // 2
        start_p = Platform(start_x, HEIGHT - 20, assets.platform)
        self.platforms.append(start_p)

        self.player = Player(WIDTH // 2, start_p.rect.top,
                             assets.doodle_right, assets.doodle_left)
        self.start_top = self.player.rect.top

        y = start_p.rect.top
        while y > 0:
            y -= self.rng.randint(60, 120)
            x = self.rng.randint(0, WIDTH - PLATFORM_WIDTH)
            self.platforms.append(self._make_platform(x, y))

    # GA reads this
    @property
    def fitness(self):
        return self.max_height

    # ---------- level generation ----------
    def _make_platform(self, x, y):
        roll = self.rng.randint(1, 100)
        if roll <= 10:
            return MovingPlatform(x, y, assets.horizental_platform, 'horizontal', self.score)
        elif roll <= 20:
            return MovingPlatform(x, y, assets.vertical_platform, 'vertical', self.score)
        elif roll <= 35:
            return ExplodingPlatform(x, y, EXPLOSIVE_FRAMES)
        elif roll <= 50:
            return Platform(x, y, assets.broken_platform0, breakable=True,
                            broken_frames=BROKEN_FRAMES)
        return Platform(x, y, assets.platform)

    def _spawn_entities(self, plat):
        if type(plat) is Platform and not plat.breakable:
            roll = self.rng.randint(1, 100)
            if roll <= 5 and self.score > 1000:
                self.trampolines.append(Trampoline(
                    plat.rect.centerx + 15, plat.rect.top - 5,
                    assets.trampoline_down, assets.trampoline_up))
            elif 5 < roll <= 15 and self.score > FEEDER_THRESHOLD:
                self.feeders.append(Feeder(
                    plat.rect.centerx + 15, plat.rect.top - 5,
                    assets.feeder_down, assets.feeder_up))
            elif 15 < roll <= 25 and self.score > 1:
                m = Monster(plat, 0, BAT_FRAMES)
                m.update()  # rect starts at (0,0) until first update
                self.monsters.append(m)

    def _add_platform(self):
        x = self.rng.randint(0, WIDTH - PLATFORM_WIDTH)
        highest_y = min((p.rect.y for p in self.platforms), default=0)
        y = highest_y - self.rng.randint(60, 120)
        plat = self._make_platform(x, y)
        self.platforms.append(plat)
        self._spawn_entities(plat)

    # ---------- collisions ----------
    def _collide(self):
        p = self.player

        for t in self.trampolines:
            if p.rect.colliderect(t.rect):
                p.rect.bottom = t.rect.top
                p.jump(JUMP_STRENGTH, boost_multiplier=2.5, flip=True)
                t.trigger()
                self.score += 700
                return

        for f in self.feeders:
            if p.rect.colliderect(f.rect):
                p.rect.bottom = f.rect.top
                p.jump(JUMP_STRENGTH, boost_multiplier=1.8)
                f.trigger()
                return

        for pl in self.platforms:
            if not pl.broken and p.rect.colliderect(pl.rect):
                p.rect.bottom = pl.rect.top
                p.jump(JUMP_STRENGTH)
                if pl.breakable:
                    pl.break_platform()
                return

    # ---------- one frame ----------
    def step(self, action):
        """action: -1 left, 0 stay, 1 right"""
        if not self.alive:
            return
        self.frames_alive += 1
        p = self.player

        keys = {pygame.K_LEFT: action < 0, pygame.K_RIGHT: action > 0}
        p.move(keys, MOVE_SPEED, WIDTH)
        p.apply_gravity(GRAVITY)

        if p.y_velocity > 0:
            self._collide()

        if p.rect.top > HEIGHT:
            self.alive = False
            return

        for m in self.monsters[:]:
            if p.rect.colliderect(m.rect):
                if p.y_velocity > 0 and p.rect.bottom < m.rect.centery + 10:
                    p.jump(JUMP_STRENGTH)
                    self.monsters.remove(m)
                else:
                    self.alive = False
                    return

        for pl in self.platforms[:]:
            pl.update()
            if pl.finished or pl.rect.top >= HEIGHT:
                self.platforms.remove(pl)
                self._add_platform()

        for m in self.monsters[:]:
            m.update()
            if m.platform not in self.platforms:
                self.monsters.remove(m)

        # camera
        if p.rect.top <= SCROLL_THRESHOLD:
            p.rect.top = SCROLL_THRESHOLD
            shift = min(p.y_velocity, 0)  # never scroll backwards
            self.score -= shift
            self.scrolled -= shift

            for pl in self.platforms[:]:
                pl.scroll(shift)
                if pl.rect.top >= HEIGHT:
                    self.platforms.remove(pl)
                    self._add_platform()

            for f in self.feeders[:]:
                f.scroll(shift)
                if f.rect.top >= HEIGHT:
                    self.feeders.remove(f)

            for t in self.trampolines[:]:
                t.scroll(shift)
                if t.rect.top >= HEIGHT:
                    self.trampolines.remove(t)

        # progress / stagnation
        height = self.scrolled + (self.start_top - p.rect.top)
        if height > self.max_height + 1:
            self.max_height = height
            self.last_progress = self.frames_alive
        if (self.frames_alive - self.last_progress > STAGNATION_LIMIT
                or self.frames_alive >= MAX_FRAMES):
            self.alive = False

    # ---------- brain input ----------
    def get_state(self):
        """8 inputs, all roughly in -1..1"""
        p = self.player
        cx, bottom = p.rect.centerx, p.rect.bottom
        half = WIDTH / 2

        def rel(rect, y):
            dx = rect.centerx - cx
            if dx > half:
                dx -= WIDTH          # wrap-aware, screen edges wrap
            elif dx < -half:
                dx += WIDTH
            return dx / half, (y - bottom) / HEIGHT

        def nearest(items, y_of):
            out = [rel(i.rect, y_of(i)) for i in items]
            out.sort(key=lambda r: r[0] ** 2 + r[1] ** 2)
            return out

        plats = nearest([pl for pl in self.platforms if not pl.broken],
                        lambda pl: pl.rect.top)
        while len(plats) < 2:
            plats.append((0.0, -1.0))

        mons = nearest(self.monsters, lambda m: m.rect.centery)
        mdx, mdy = mons[0] if mons else (0.0, 1.0)

        return np.array([
            (cx - half) / half,
            p.y_velocity / 20.0,
            plats[0][0], plats[0][1],
            plats[1][0], plats[1][1],
            mdx, mdy,
        ], dtype=float)

    # ---------- render ----------
    def draw(self, surface):
        surface.blit(assets.background, (0, 0))
        for pl in self.platforms:
            pl.draw(surface)
        for f in self.feeders:
            f.draw(surface)
        for m in self.monsters:
            m.draw(surface)
        for t in self.trampolines:
            t.draw(surface)
        self.player.draw(surface)