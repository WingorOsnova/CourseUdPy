import pygame as pg
import random
from pathlib import Path

# ---------- Настройки ----------
TILE = 20           # размер клетки (px)
GRID_W, GRID_H = 30, 30  # сетка 30x30 => окно 600x600
WIDTH, HEIGHT = GRID_W * TILE, GRID_H * TILE
FPS = 12            # скорость игры (кадров в секунду)
FONT_NAME = "arial"
HIGHSCORE_FILE = Path("highscore.txt")
# -------------------------------

# Цвета
BG = (20, 20, 25)
SNAKE = (70, 200, 120)
SNAKE_HEAD = (90, 230, 150)
FOOD = (230, 90, 90)
GRID = (35, 35, 45)
TEXT = (235, 235, 245)
SHADOW = (0, 0, 0)

# Векторы направления
DIRS = {
    pg.K_UP: (0, -1),
    pg.K_DOWN: (0, 1),
    pg.K_LEFT: (-1, 0),
    pg.K_RIGHT: (1, 0),
}
OPPOSITE = {
    (0, -1): (0, 1),
    (0, 1): (0, -1),
    (-1, 0): (1, 0),
    (1, 0): (-1, 0),
}


def load_highscore() -> int:
    try:
        return int(HIGHSCORE_FILE.read_text().strip())
    except Exception:
        return 0


def save_highscore(value: int) -> None:
    try:
        HIGHSCORE_FILE.write_text(str(value))
    except Exception:
        pass


def draw_grid(surface: pg.Surface):
    # Нежная сетка, чтобы ориентироваться
    for x in range(0, WIDTH, TILE):
        pg.draw.line(surface, GRID, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, TILE):
        pg.draw.line(surface, GRID, (0, y), (WIDTH, y), 1)


def random_empty_cell(snake_body):
    while True:
        pos = (random.randrange(GRID_W), random.randrange(GRID_H))
        if pos not in snake_body:
            return pos


def draw_rect_cell(surface: pg.Surface, color, cell, border=0):
    x, y = cell
    r = pg.Rect(x * TILE, y * TILE, TILE, TILE)
    if border:
        pg.draw.rect(surface, color, r, border)
    else:
        pg.draw.rect(surface, color, r, border)


def render_text(surface, text, size, pos, color=TEXT, center=False, bold=False):
    font = pg.font.SysFont(FONT_NAME, size, bold=bold)
    img = font.render(text, True, color)
    rect = img.get_rect()
    rect.center = pos if center else pos
    if not center:
        surface.blit(img, rect)
    else:
        surface.blit(img, rect)


def main():
    pg.init()
    pg.display.set_caption("Snake — Pygame")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    font_small = pg.font.SysFont(FONT_NAME, 18)
    font_big = pg.font.SysFont(FONT_NAME, 42, bold=True)

    highscore = load_highscore()

    def reset_game():
        snake = [(GRID_W // 2, GRID_H // 2)]
        direction = (1, 0)  # старт вправо
        grow = 0
        food = random_empty_cell(set(snake))
        score = 0
        paused = False
        alive = True
        return snake, direction, grow, food, score, paused, alive

    snake, direction, grow, food, score, paused, alive = reset_game()

    # Основной цикл
    while True:
        # --- события ---
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            if event.type == pg.KEYDOWN:
                if event.key in DIRS:
                    new_dir = DIRS[event.key]
                    # запрет разворота на 180°
                    if len(snake) == 1 or new_dir != OPPOSITE.get(direction):
                        direction = new_dir
                elif event.key == pg.K_p:
                    paused = not paused
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    return
                elif event.key == pg.K_r and not alive:
                    snake, direction, grow, food, score, paused, alive = reset_game()

        if not paused and alive:
            # --- логика движения ---
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Проверка стены
            if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
                alive = False
            # Проверка самоукуса
            elif new_head in snake:
                alive = False
            else:
                snake.insert(0, new_head)

                # Еда?
                if new_head == food:
                    score += 1
                    grow += 1
                    food = random_empty_cell(set(snake))
                if grow > 0:
                    grow -= 1
                else:
                    snake.pop()

        # Обновление рекорда
        if score > highscore:
            highscore = score
            save_highscore(highscore)

        # --- отрисовка ---
        screen.fill(BG)
        draw_grid(screen)

        # Еда
        draw_rect_cell(screen, FOOD, food)

        # Змейка
        # Голова
        if snake:
            draw_rect_cell(screen, SNAKE_HEAD, snake[0])
        # Тело
        for cell in snake[1:]:
            draw_rect_cell(screen, SNAKE, cell)

        # HUD
        score_text = f"Score: {score}   Best: {highscore}   FPS: {FPS}"
        hud = font_small.render(score_text, True, TEXT)
        screen.blit(hud, (10, 8))

        if paused:
            overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            render_text(screen, "PAUSE", 48, (WIDTH // 2, HEIGHT //
                        2 - 10), color=TEXT, center=True, bold=True)
            render_text(screen, "Press P to continue", 22,
                        (WIDTH // 2, HEIGHT // 2 + 30), color=TEXT, center=True)

        if not alive:
            overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            render_text(screen, "GAME OVER", 56, (WIDTH // 2,
                        HEIGHT // 2 - 20), color=TEXT, center=True, bold=True)
            render_text(screen, f"Score: {score}   Best: {highscore}", 24, (
                WIDTH // 2, HEIGHT // 2 + 20), color=TEXT, center=True)
            render_text(screen, "Press R to restart • Esc to quit", 20,
                        (WIDTH // 2, HEIGHT // 2 + 54), color=TEXT, center=True)

        pg.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
