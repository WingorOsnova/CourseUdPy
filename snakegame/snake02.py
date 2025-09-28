#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Set, Optional

import pygame as pg

# ============================== CONFIG ==============================

DATA_FILE = Path("snake_data.json")      # highscore + настройки
FONT_NAME = "arial"
BASE_FPS = 60                            # FPS отрисовки
INIT_GRID = (30, 30)                     # стартовая сетка (клеток)
INIT_TILE = 22                           # размер одной клетки (px)
INIT_MODE = "CLASSIC"                    # стартовый режим

# Цвета
COLORS = {
    "bg": (18, 20, 26),
    "grid": (35, 37, 46),
    "snake": (60, 205, 140),
    "snake_head": (90, 235, 165),
    "food": (240, 95, 95),
    "gold": (250, 210, 90),
    "slow": (110, 170, 255),
    "ghost": (170, 110, 255),
    "shrink": (255, 130, 190),
    "reverse": (255, 180, 90),
    "obstacle": (120, 125, 140),
    "text": (235, 237, 245),
    "shadow": (0, 0, 0),
    "hud": (255, 255, 255),
}

# Режимы
MODES = {
    "CLASSIC": "Классика: стены смертельны",
    "WRAP": "Wrap: вылетел за край — появился с другой стороны",
    "OBSTACLES": "Препятствия + классика",
    "MARATHON": "Марафон: постепенное ускорение",
}

# Вероятности спавна бустов (в процентах от обычной еды)
POWERUP_WEIGHTS = {
    "gold": 0.06,     # золотое яблоко (много очков, быстро исчезает)
    "slow": 0.06,     # замедление времени
    "ghost": 0.06,    # режим “призрак” — игнор самоукус
    "shrink": 0.04,   # уменьшение хвоста
    "reverse": 0.04,  # инвертировать управление
}

# Длительности эффектов (в секундах)
EFFECT_DUR = {
    "slow": 5.0,
    "ghost": 8.0,
    "reverse": 6.0,
}

# Начальная задержка между шагами змейки (мс) и минимальная
BASE_STEP_MS = 140
MIN_STEP_MS = 60

# Сколько очков — ускорение на 2 мс
MARATHON_ACCEL_EVERY = 4

# Сколько очков дают предметы
SCORES = {
    "food": 1,
    "gold": 5,
}

# Сколько клеток расти/уменьшаться
GROW_BY = {
    "food": 1,
    "gold": 3,
    "shrink": -3,
}

# ===================================================================


Vec = Tuple[int, int]


def clamp(v, a, b):
    return max(a, min(b, v))


def load_data():
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text("utf-8"))
        except Exception:
            pass
    return {"highscores": {}, "settings": {}}


def save_data(d):
    try:
        DATA_FILE.write_text(json.dumps(
            d, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def grid_to_px(cell: Vec, tile: int) -> pg.Rect:
    x, y = cell
    return pg.Rect(x * tile, y * tile, tile, tile)


def sign(n: int) -> int:
    return (n > 0) - (n < 0)


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    color: Tuple[int, int, int]

    def update(self, dt: float):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    def draw(self, surf: pg.Surface):
        if self.life <= 0:
            return
        alpha = clamp(int(255 * (self.life / 0.5)), 0, 255)
        s = pg.Surface((4, 4), pg.SRCALPHA)
        s.fill((*self.color, alpha))
        surf.blit(s, (self.x, self.y))


@dataclass
class Item:
    pos: Vec
    kind: str           # 'food', 'gold', 'slow', 'ghost', 'shrink', 'reverse'
    ttl: Optional[float] = None  # для временных, например gold


class Snake:
    def __init__(self, start: Vec):
        self.body: List[Vec] = [start]
        self.dir: Vec = (1, 0)
        self.grow: int = 0
        self.alive: bool = True

    def head(self) -> Vec:
        return self.body[0]

    def set_dir(self, new_dir: Vec):
        # запрет разворота на 180°
        if len(self.body) == 1:
            self.dir = new_dir
            return
        if (new_dir[0] == -self.dir[0] and new_dir[1] == -self.dir[1]):
            return
        self.dir = new_dir

    def step(self, wrap: bool, grid_w: int, grid_h: int, ignore_self=False) -> Optional[Vec]:
        hx, hy = self.body[0]
        dx, dy = self.dir
        nx, ny = hx + dx, hy + dy

        if wrap:
            nx %= grid_w
            ny %= grid_h
        else:
            if not (0 <= nx < grid_w and 0 <= ny < grid_h):
                self.alive = False
                return None

        new_head = (nx, ny)

        # самоукус
        if not ignore_self and new_head in self.body:
            self.alive = False
            return None

        self.body.insert(0, new_head)
        if self.grow > 0:
            self.grow -= 1
        else:
            self.body.pop()

        return new_head

    def change_length(self, delta: int):
        if delta > 0:
            self.grow += delta
        elif delta < 0:
            # уменьшаем хвост, но минимум 1 сегмент
            for _ in range(min(-delta, max(0, len(self.body) - 1))):
                if len(self.body) > 1:
                    self.body.pop()


class ObstacleField:
    def __init__(self, grid_w: int, grid_h: int):
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.cells: Set[Vec] = set()

    def generate(self, kind: str = "rings"):
        self.cells.clear()
        w, h = self.grid_w, self.grid_h

        if kind == "rings":
            # Несколько прямоугольных колец
            for inset in (2, 6, 10):
                for x in range(inset, w - inset):
                    self.cells.add((x, inset))
                    self.cells.add((x, h - inset - 1))
                for y in range(inset, h - inset):
                    self.cells.add((inset, y))
                    self.cells.add((w - inset - 1, y))
        elif kind == "cross":
            cx, cy = w // 2, h // 2
            for x in range(w):
                if abs(x - cx) > 1:
                    self.cells.add((x, cy))
            for y in range(h):
                if abs(y - cy) > 1:
                    self.cells.add((cx, y))
        elif kind == "random":
            density = 0.08
            for x in range(w):
                for y in range(h):
                    if random.random() < density:
                        self.cells.add((x, y))
        else:
            # без препятствий
            pass

    def draw(self, surf: pg.Surface, tile: int):
        col = COLORS["obstacle"]
        for cell in self.cells:
            pg.draw.rect(surf, col, grid_to_px(cell, tile))

    def is_blocked(self, pos: Vec) -> bool:
        return pos in self.cells


class Game:
    def __init__(self, grid_w: int, grid_h: int, tile: int, mode: str):
        pg.init()
        pg.display.set_caption("Advanced Snake — Pygame")
        self.grid_w, self.grid_h = grid_w, grid_h
        self.tile = tile
        self.width, self.height = grid_w * tile, grid_h * tile
        self.screen = pg.display.set_mode(
            (self.width, self.height), pg.RESIZABLE)
        self.clock = pg.time.Clock()

        self.font_small = pg.font.SysFont(FONT_NAME, 18)
        self.font = pg.font.SysFont(FONT_NAME, 22)
        self.font_big = pg.font.SysFont(FONT_NAME, 48, bold=True)
        self.font_mid = pg.font.SysFont(FONT_NAME, 28, bold=True)

        self.state = "menu"  # menu, playing, paused, gameover, settings
        self.mode = mode
        self.data = load_data()
        self.highscores = self.data.get("highscores", {})
        self.settings = self.data.get("settings", {})

        # Параметры шага
        self.base_step_ms = self.settings.get("base_step_ms", BASE_STEP_MS)
        self.min_step_ms = self.settings.get("min_step_ms", MIN_STEP_MS)

        # Объекты уровня
        self.snake: Snake = None  # type: ignore
        self.items: List[Item] = []
        self.particles: List[Particle] = []
        self.obstacles = ObstacleField(grid_w, grid_h)

        # Таймеры эффектов
        self.effects = {
            "slow": 0.0,
            "ghost": 0.0,
            "reverse": 0.0,
        }

        self.score = 0
        self.step_timer = 0.0
        self.step_ms = self.base_step_ms
        self.fullscreen = False

        self.reset_level(full_reset=True)

    # -------------------- Вспомогательное --------------------

    def current_best(self) -> int:
        return int(self.highscores.get(self.mode, 0))

    def record_best(self):
        if self.score > self.current_best():
            self.highscores[self.mode] = self.score
            self.data["highscores"] = self.highscores
            save_data(self.data)

    def resize_window(self, width, height):
        # Подогнать размер тайла при ресайзе окна
        new_tile_x = max(8, width // self.grid_w)
        new_tile_y = max(8, height // self.grid_h)
        self.tile = min(new_tile_x, new_tile_y)
        self.width, self.height = self.grid_w * self.tile, self.grid_h * self.tile
        self.screen = pg.display.set_mode(
            (self.width, self.height), pg.RESIZABLE)

    def random_empty_cell(self) -> Vec:
        occupied = set(self.snake.body) | {
            it.pos for it in self.items} | set(self.obstacles.cells)
        while True:
            pos = (random.randrange(self.grid_w),
                   random.randrange(self.grid_h))
            if pos not in occupied:
                return pos

    def spawn_item(self, kind: Optional[str] = None):
        if kind is None:
            # 80–85% обычная еда, остальное — бусты по весам
            if random.random() < 0.84:
                kind = "food"
            else:
                kinds = list(POWERUP_WEIGHTS.keys())
                weights = [POWERUP_WEIGHTS[k] for k in kinds]
                kind = random.choices(kinds, weights=weights, k=1)[0]
        pos = self.random_empty_cell()
        ttl = None
        if kind == "gold":
            ttl = 6.0  # золотое быстро пропадает
        self.items.append(Item(pos=pos, kind=kind, ttl=ttl))

    def reset_level(self, full_reset=False):
        cx, cy = self.grid_w // 2, self.grid_h // 2
        self.snake = Snake((cx, cy))
        self.items.clear()
        self.particles.clear()
        self.effects = {k: 0.0 for k in self.effects}
        self.score = 0
        self.step_timer = 0.0
        self.step_ms = self.base_step_ms
        # Генерация препятствий по режиму
        self.obstacles = ObstacleField(self.grid_w, self.grid_h)
        if self.mode == "OBSTACLES":
            self.obstacles.generate(
                random.choice(["rings", "cross", "random"]))
            # уберём стартовую точку и вокруг чуть-чуть
            safe = {(cx, cy), (cx + 1, cy), (cx - 1, cy),
                    (cx, cy + 1), (cx, cy - 1)}
            self.obstacles.cells -= safe
        # стартовые предметы
        for _ in range(2):
            self.spawn_item("food")
        if full_reset:
            # дополнительные “медленные” флаги
            self.state = "menu"

    # -------------------- Эффекты --------------------

    def add_particles_burst(self, cell: Vec, color: Tuple[int, int, int]):
        x, y = cell
        cx = x * self.tile + self.tile / 2
        cy = y * self.tile + self.tile / 2
        for _ in range(12):
            ang = random.random() * math.tau
            speed = 160 + 80 * random.random()
            vx = math.cos(ang) * speed
            vy = math.sin(ang) * speed
            life = 0.35 + random.random() * 0.25
            self.particles.append(Particle(cx, cy, vx, vy, life, color))

    def apply_effect(self, kind: str):
        if kind == "food":
            self.score += SCORES["food"]
            self.snake.change_length(GROW_BY["food"])
        elif kind == "gold":
            self.score += SCORES["gold"]
            self.snake.change_length(GROW_BY["gold"])
        elif kind == "slow":
            self.effects["slow"] = EFFECT_DUR["slow"]
        elif kind == "ghost":
            self.effects["ghost"] = EFFECT_DUR["ghost"]
        elif kind == "shrink":
            self.snake.change_length(GROW_BY["shrink"])
        elif kind == "reverse":
            self.effects["reverse"] = EFFECT_DUR["reverse"]

        # Марафон — ускорять шаг
        if self.mode == "MARATHON":
            if self.score > 0 and self.score % MARATHON_ACCEL_EVERY == 0:
                self.step_ms = max(self.min_step_ms, self.step_ms - 2)

    # -------------------- Обновление/логика --------------------

    def dir_from_key(self, key: int) -> Optional[Vec]:
        mapping = {
            pg.K_UP: (0, -1),
            pg.K_w: (0, -1),
            pg.K_DOWN: (0, 1),
            pg.K_s: (0, 1),
            pg.K_LEFT: (-1, 0),
            pg.K_a: (-1, 0),
            pg.K_RIGHT: (1, 0),
            pg.K_d: (1, 0),
        }
        if key not in mapping:
            return None
        dx, dy = mapping[key]
        if self.effects["reverse"] > 0:
            dx, dy = -dx, -dy
        return (dx, dy)

    def handle_events(self) -> bool:
        # return False -> выход
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return False
            if e.type == pg.VIDEORESIZE:
                self.resize_window(e.w, e.h)
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    if self.state == "playing":
                        self.state = "menu"
                    elif self.state in ("paused", "gameover"):
                        self.state = "menu"
                    else:
                        return False
                elif e.key == pg.K_f:
                    self.fullscreen = not self.fullscreen
                    flags = pg.FULLSCREEN if self.fullscreen else pg.RESIZABLE
                    self.screen = pg.display.set_mode(
                        (self.width, self.height), flags)
                elif self.state == "menu":
                    if e.key in (pg.K_SPACE, pg.K_RETURN):
                        self.state = "playing"
                        self.reset_level()
                    elif e.key == pg.K_1:
                        self.mode = "CLASSIC"
                        self.reset_level(full_reset=True)
                    elif e.key == pg.K_2:
                        self.mode = "WRAP"
                        self.reset_level(full_reset=True)
                    elif e.key == pg.K_3:
                        self.mode = "OBSTACLES"
                        self.reset_level(full_reset=True)
                    elif e.key == pg.K_4:
                        self.mode = "MARATHON"
                        self.reset_level(full_reset=True)
                    elif e.key == pg.K_TAB:
                        self.state = "settings"
                elif self.state == "settings":
                    if e.key == pg.K_LEFT:
                        self.base_step_ms = clamp(
                            self.base_step_ms + 5, self.min_step_ms, 300)
                    elif e.key == pg.K_RIGHT:
                        self.base_step_ms = clamp(
                            self.base_step_ms - 5, self.min_step_ms, 300)
                    elif e.key == pg.K_UP:
                        gw, gh = self.grid_w, self.grid_h
                        self.grid_w, self.grid_h = gw + 2, gh + 2
                        self.resize_window(
                            self.width + 2 * self.tile, self.height + 2 * self.tile)
                    elif e.key == pg.K_DOWN:
                        if self.grid_w > 12 and self.grid_h > 12:
                            self.grid_w -= 2
                            self.grid_h -= 2
                            self.resize_window(
                                self.width - 2 * self.tile, self.height - 2 * self.tile)
                    elif e.key in (pg.K_RETURN, pg.K_SPACE):
                        # применить
                        self.data["settings"] = {
                            "base_step_ms": self.base_step_ms,
                            "min_step_ms": self.min_step_ms,
                        }
                        save_data(self.data)
                        # пересоздать игру с новыми размерами
                        self.__init__(self.grid_w, self.grid_h,
                                      self.tile, self.mode)
                        self.state = "menu"
                    elif e.key == pg.K_ESCAPE:
                        self.state = "menu"
                elif self.state == "playing":
                    if e.key == pg.K_p:
                        self.state = "paused"
                    elif e.key == pg.K_r:
                        self.reset_level()
                        self.state = "playing"
                    else:
                        d = self.dir_from_key(e.key)
                        if d:
                            self.snake.set_dir(d)
                elif self.state == "paused":
                    if e.key in (pg.K_p, pg.K_SPACE, pg.K_RETURN):
                        self.state = "playing"
                    elif e.key == pg.K_r:
                        self.reset_level()
                        self.state = "playing"
                elif self.state == "gameover":
                    if e.key == pg.K_r:
                        self.reset_level()
                        self.state = "playing"
                    elif e.key in (pg.K_SPACE, pg.K_RETURN):
                        self.state = "menu"
        return True

    def update(self, dt_ms: float):
        # обновление таймеров эффектов
        for k in list(self.effects.keys()):
            if self.effects[k] > 0:
                self.effects[k] = max(0.0, self.effects[k] - dt_ms / 1000.0)

        slow_factor = 0.55 if self.effects["slow"] > 0 else 1.0
        step_ms = self.step_ms / slow_factor
        wrap = (self.mode == "WRAP")

        if self.state == "playing" and self.snake.alive:
            # тик движения
            self.step_timer += dt_ms
            if self.step_timer >= step_ms:
                self.step_timer -= step_ms

                # следующий шаг
                new_head = self.snake.step(
                    wrap=wrap,
                    grid_w=self.grid_w,
                    grid_h=self.grid_h,
                    ignore_self=(self.effects["ghost"] > 0),
                )

                # столкновение с препятствиями
                if new_head is None:
                    pass  # уже умер
                else:
                    if self.obstacles.is_blocked(new_head):
                        self.snake.alive = False

                if self.snake.alive and new_head is not None:
                    # предметы
                    for it in list(self.items):
                        if it.pos == self.snake.head():
                            self.apply_effect(it.kind)
                            self.add_particles_burst(
                                it.pos, COLORS.get(it.kind, COLORS["food"]))
                            self.items.remove(it)
                            # всегда поддерживаем минимум 2 предмета на карте
                            if sum(1 for i in self.items if i.kind == "food") < 1:
                                self.spawn_item("food")
                            if len(self.items) < 3 and random.random() < 0.35:
                                self.spawn_item(None)

            # TTL у временных предметов (gold)
            for it in list(self.items):
                if it.ttl is not None:
                    it.ttl -= dt_ms / 1000.0
                    if it.ttl <= 0:
                        self.items.remove(it)

        # Частицы
        for p in list(self.particles):
            p.update(dt_ms / 1000.0)
            if p.life <= 0:
                self.particles.remove(p)

        # конец игры?
        if self.state == "playing" and not self.snake.alive:
            self.record_best()
            self.state = "gameover"

    # -------------------- Отрисовка --------------------

    def draw_grid(self):
        col = COLORS["grid"]
        for x in range(0, self.width, self.tile):
            pg.draw.line(self.screen, col, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, self.tile):
            pg.draw.line(self.screen, col, (0, y), (self.width, y), 1)

    def draw_snake(self):
        body = self.snake.body
        if not body:
            return

        # рисуем голову чуть светлее
        head_col = COLORS["snake_head"]
        if self.effects["ghost"] > 0:
            head_col = (COLORS["ghost"][0], COLORS["ghost"]
                        [1], COLORS["ghost"][2])

        pg.draw.rect(self.screen, head_col, grid_to_px(body[0], self.tile))
        # глаза
        hx, hy = body[0]
        dx, dy = self.snake.dir
        eye_offset = 0.25
        ex = (hx + 0.5 + 0.25 * dx) * self.tile
        ey = (hy + 0.5 + 0.25 * dy) * self.tile
        r = max(2, self.tile // 8)
        pg.draw.circle(self.screen, (12, 12, 12), (int(
            ex - eye_offset * self.tile), int(ey - eye_offset * self.tile)), r)
        pg.draw.circle(self.screen, (12, 12, 12), (int(
            ex + eye_offset * self.tile), int(ey + eye_offset * self.tile)), r)

        # тело — лёгкий градиент
        n = len(body)
        for i, cell in enumerate(body[1:], start=1):
            t = i / max(1, n - 1)
            r = int(COLORS["snake"][0] * (1 - 0.4 * t))
            g = int(COLORS["snake"][1] * (1 - 0.4 * t))
            b = int(COLORS["snake"][2] * (1 - 0.4 * t))
            pg.draw.rect(self.screen, (r, g, b), grid_to_px(cell, self.tile))

    def draw_items(self):
        for it in self.items:
            rect = grid_to_px(it.pos, self.tile)
            col = COLORS.get(it.kind, COLORS["food"])
            # пульсация золота по ttl
            if it.kind == "gold" and it.ttl is not None:
                pulse = 0.5 + 0.5 * math.sin(pg.time.get_ticks() / 120.0)
                col = (
                    clamp(int(col[0] * (0.9 + 0.3 * pulse)), 0, 255),
                    clamp(int(col[1] * (0.9 + 0.2 * pulse)), 0, 255),
                    clamp(int(col[2] * (0.8 + 0.3 * pulse)), 0, 255),
                )
            pg.draw.rect(self.screen, col, rect)

    def draw_hud(self):
        best = self.current_best()
        speed = int(1000 / self.step_ms)
        slow_icon = "⏳" if self.effects["slow"] > 0 else ""
        ghost_icon = "👻" if self.effects["ghost"] > 0 else ""
        rev_icon = "🔁" if self.effects["reverse"] > 0 else ""
        mode_txt = f"[{self.mode}]"

        text = f"Score: {self.score}   Best: {best}   Step/s: {speed}  {mode_txt} {slow_icon}{ghost_icon}{rev_icon}"
        img = self.font.render(text, True, COLORS["text"])
        self.screen.blit(img, (10, 8))

        # Текст помощи
        help_txt = "P — пауза, R — рестарт, Esc — меню, F — фулл-скрин"
        img2 = self.font_small.render(help_txt, True, (200, 200, 210))
        self.screen.blit(img2, (10, self.height - 24))

    def draw_menu(self):
        title = "ADVANCED SNAKE"
        sub = "Space/Enter — старт • 1–4 — выбор режима • Tab — Настройки"
        desc_lines = [f"1) CLASSIC — {MODES['CLASSIC']}",
                      f"2) WRAP — {MODES['WRAP']}",
                      f"3) OBSTACLES — {MODES['OBSTACLES']}",
                      f"4) MARATHON — {MODES['MARATHON']}"]

        t_img = self.font_big.render(title, True, COLORS["text"])
        t_rect = t_img.get_rect(
            center=(self.width // 2, self.height // 2 - 120))
        self.screen.blit(t_img, t_rect)

        s_img = self.font.render(sub, True, (205, 205, 215))
        s_rect = s_img.get_rect(
            center=(self.width // 2, self.height // 2 - 75))
        self.screen.blit(s_img, s_rect)

        for i, line in enumerate(desc_lines):
            img = self.font_mid.render(line, True, COLORS["text"] if str(
                i + 1) in "1234" else (200, 200, 210))
            rect = img.get_rect(
                center=(self.width // 2, self.height // 2 - 10 + i * 36))
            self.screen.blit(img, rect)

        best_info = f"Best: CLASSIC {self.highscores.get('CLASSIC', 0)} • WRAP {self.highscores.get('WRAP', 0)} • OBST {self.highscores.get('OBSTACLES', 0)} • MARA {self.highscores.get('MARATHON', 0)}"
        b_img = self.font_small.render(best_info, True, (190, 190, 200))
        b_rect = b_img.get_rect(
            center=(self.width // 2, self.height // 2 + 160))
        self.screen.blit(b_img, b_rect)

    def draw_settings(self):
        title = "Настройки"
        lines = [
            f"←/→ скорость шага: {self.base_step_ms} ms (меньше — быстрее)",
            f"↑/↓ размер сетки: {self.grid_w}x{self.grid_h}",
            "Enter/Space — применить и перезапустить • Esc — назад",
        ]
        t_img = self.font_big.render(title, True, COLORS["text"])
        t_rect = t_img.get_rect(
            center=(self.width // 2, self.height // 2 - 100))
        self.screen.blit(t_img, t_rect)
        for i, ln in enumerate(lines):
            img = self.font_mid.render(ln, True, (210, 210, 220))
            rect = img.get_rect(
                center=(self.width // 2, self.height // 2 - 20 + i * 36))
            self.screen.blit(img, rect)

    def draw_overlay(self, title: str, subtitle: str):
        overlay = pg.Surface((self.width, self.height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))
        t = self.font_big.render(title, True, COLORS["text"])
        ts = self.font_mid.render(subtitle, True, (210, 210, 220))
        self.screen.blit(t, t.get_rect(
            center=(self.width // 2, self.height // 2 - 12)))
        self.screen.blit(ts, ts.get_rect(
            center=(self.width // 2, self.height // 2 + 34)))

    def draw(self):
        self.screen.fill(COLORS["bg"])
        self.draw_grid()
        if self.mode == "OBSTACLES":
            self.obstacles.draw(self.screen, self.tile)
        if self.state in ("playing", "paused", "gameover"):
            self.draw_items()
            self.draw_snake()
            for p in self.particles:
                p.draw(self.screen)
            self.draw_hud()
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "settings":
            self.draw_settings()
        elif self.state == "paused":
            self.draw_overlay(
                "PAUSE", "P/Space — продолжить • R — рестарт • Esc — меню")
        elif self.state == "gameover":
            self.draw_overlay(
                "GAME OVER", f"Score: {self.score}   Best: {self.current_best()}   (R — рестарт, Space — меню)")

        pg.display.flip()

    # -------------------- Главный цикл --------------------

    def run(self):
        # старт из меню
        self.state = "menu"
        running = True
        while running:
            dt = self.clock.tick(BASE_FPS)
            running = self.handle_events()
            self.update(dt)
            self.draw()


def main():
    # Можно передать размеры сетки в аргументах: python advanced_snake.py 28 28
    gw, gh = INIT_GRID
    if len(sys.argv) >= 3:
        try:
            gw, gh = int(sys.argv[1]), int(sys.argv[2])
        except Exception:
            pass
    game = Game(gw, gh, INIT_TILE, INIT_MODE)
    game.run()
    pg.quit()


if __name__ == "__main__":
    main()
