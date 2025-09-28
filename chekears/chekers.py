#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame as pg
import sys
from copy import deepcopy

# ----------------------- Константы и цвета -----------------------

ROWS, COLS = 8, 8
TILE = 80
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE
FPS = 60

LIGHT = (240, 235, 210)      # светлые клетки
DARK = (118, 150, 86)        # тёмные клетки (игровые)
GRID = (70, 95, 55)
SEL = (255, 210, 80)         # подсветка выбранной шашки
MOVE = (60, 160, 250)        # подсветка доступного хода
CAPT = (255, 90, 90)         # подсветка взятия
OUTLINE = (25, 25, 25)

WHITE = (245, 245, 245)
BLACK = (25, 25, 25)
WHITE_EDGE = (200, 200, 200)
BLACK_EDGE = (55, 55, 55)
KING_RING = (255, 215, 0)

# Игровые коды в матрице:
# 0 — пусто, 'w'/'b' — обычные, 'W'/'B' — дамки
DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

# ----------------------- Утилиты -----------------------


def inside(r, c): return 0 <= r < ROWS and 0 <= c < COLS
def dark_square(r, c): return (r + c) % 2 == 1


def encode_matrix(board):
    """Преобразуем объектное поле в простую матрицу кодов."""
    M = [[0 for _ in range(COLS)] for __ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            p = board[r][c]
            if not p:
                continue
            if p["color"] == "w":
                M[r][c] = 'W' if p["king"] else 'w'
            else:
                M[r][c] = 'B' if p["king"] else 'b'
    return M


def decode_color(ch):
    return 'w' if ch in ('w', 'W') else 'b'


def is_king(ch):
    return ch in ('W', 'B')


def forward_dirs(color):
    # простые шашки ходят только вперёд
    return [(-1, -1), (-1, 1)] if color == 'w' else [(1, -1), (1, 1)]

# ----------------------- Генерация ходов -----------------------


def gen_man_captures(M, r, c, color):
    """Все цепочки взятий для простой шашки (бить можно в любую сторону)."""
    res = []
    me = 'w' if color == 'w' else 'b'
    king_row = 0 if color == 'w' else ROWS-1

    def dfs(mat, rr, cc, path):
        found = False
        for dr, dc in DIRS:  # бить разрешено и назад
            r1, c1 = rr + dr, cc + dc
            r2, c2 = rr + 2*dr, cc + 2*dc
            if not (inside(r2, c2) and inside(r1, c1)):
                continue
            if mat[r1][c1] != 0 and decode_color(mat[r1][c1]) != color and mat[r2][c2] == 0:
                # пробуем удар
                mat2 = deepcopy(mat)
                # снимаем и ставим
                mat2[rr][cc] = 0
                mat2[r1][c1] = 0
                # повышение?
                became_king = (color == 'w' and r2 == king_row) or (
                    color == 'b' and r2 == king_row)
                mat2[r2][c2] = (
                    'W' if color == 'w' else 'B') if became_king else me
                # продолжение: если стал дамкой — дальше дамочные взятия
                if became_king:
                    cont = gen_king_captures(mat2, r2, c2, color)
                    if cont:
                        for seq in cont:
                            res.append([((r2, c2), (r1, c1))] + seq)
                    else:
                        res.append([((r2, c2), (r1, c1))])
                else:
                    dfs(mat2, r2, c2, path + [((r2, c2), (r1, c1))])
                found = True
        if not found and path:
            res.append(path)

    dfs(deepcopy(M), r, c, [])
    return res


def gen_king_captures(M, r, c, color):
    """Все цепочки взятий для дамки (летающая)."""
    res = []

    def dfs(mat, rr, cc, path):
        found_any = False
        for dr, dc in DIRS:
            i = 1
            captured = None
            # идём до первого встреченного
            while True:
                r1, c1 = rr + dr*i, cc + dc*i
                if not inside(r1, c1):
                    break
                if mat[r1][c1] == 0:
                    i += 1
                    continue
                # своя фигура — блок
                if decode_color(mat[r1][c1]) == color:
                    break
                # противник — ищем посадку дальше
                captured = (r1, c1)
                j = i + 1
                while True:
                    r2, c2 = rr + dr*j, cc + dc*j
                    if not inside(r2, c2):
                        break
                    if mat[r2][c2] != 0:
                        break
                    # посадка возможна
                    mat2 = deepcopy(mat)
                    mat2[rr][cc] = 0
                    mat2[captured[0]][captured[1]] = 0
                    mat2[r2][c2] = mat[rr][cc]  # дамка остаётся дамкой
                    dfs_res_len_before = len(res)
                    dfs(mat2, r2, c2, path + [((r2, c2), captured)])
                    # если глубже не нашли — фиксируем конечный путь
                    if len(res) == dfs_res_len_before:
                        res.append(path + [((r2, c2), captured)])
                    j += 1
                break  # дальше в этом направлении второй бьющий не бывает
        # если на этом уровне не было возможных взятий и есть уже путь — добавим
        # (добавление конечных путей делается выше, когда не разветвляемся)

    dfs(deepcopy(M), r, c, [])
    return res


def gen_man_moves(M, r, c, color):
    """Обычные ходы для простой шашки (только вперёд)."""
    res = []
    for dr, dc in forward_dirs(color):
        r2, c2 = r + dr, c + dc
        if inside(r2, c2) and M[r2][c2] == 0:
            res.append((r2, c2))
    return res


def gen_king_moves(M, r, c):
    """Обычные ходы для дамки — скольжение по диагонали."""
    res = []
    for dr, dc in DIRS:
        i = 1
        while True:
            r2, c2 = r + dr*i, c + dc*i
            if not inside(r2, c2):
                break
            if M[r2][c2] != 0:
                break
            res.append((r2, c2))
            i += 1
    return res


def all_legal(color, M):
    """Список всех легальных действий для стороны.
       Возвращает:
         captures_mode: bool
         seqs_by_start: dict[(r,c)] -> list[sequence], где sequence = [((to_r,to_c),(cap_r,cap_c)), ...]
         normals_by_start: dict[(r,c)] -> list[(to_r,to_c)]  (если взятий нет)
       При наличии хотя бы одного взятия — normals_by_start пуст, а seqs оставлены только максимальной длины.
    """
    seqs_by_start = {}
    max_len = 0

    # Сначала все взятия
    for r in range(ROWS):
        for c in range(COLS):
            if M[r][c] == 0:
                continue
            if decode_color(M[r][c]) != color:
                continue
            if is_king(M[r][c]):
                seqs = gen_king_captures(M, r, c, color)
            else:
                seqs = gen_man_captures(M, r, c, color)
            if seqs:
                seqs_by_start[(r, c)] = seqs
                for s in seqs:
                    if len(s) > max_len:
                        max_len = len(s)

    if seqs_by_start:
        # применить правило максимального боя
        filtered = {}
        for pos, seqs in seqs_by_start.items():
            xs = [s for s in seqs if len(s) == max_len]
            if xs:
                filtered[pos] = xs
        return True, filtered, {}

    # Иначе — обычные ходы
    normals = {}
    for r in range(ROWS):
        for c in range(COLS):
            if M[r][c] == 0:
                continue
            if decode_color(M[r][c]) != color:
                continue
            if is_king(M[r][c]):
                mv = gen_king_moves(M, r, c)
            else:
                mv = gen_man_moves(M, r, c, color)
            if mv:
                normals[(r, c)] = mv
    return False, {}, normals

# ----------------------- Игра и UI -----------------------


class Checkers:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Advanced Checkers — Russian rules")
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("arial", 20)

        # поле: в каждой клетке либо None, либо {"color": 'w'/'b', "king": bool}
        self.board = [[None for _ in range(COLS)] for __ in range(ROWS)]
        self.turn = 'w'   # 'w' ходит снизу вверх
        self.selected = None  # (r,c) выбранная шашка
        self.seqs_by_start = {}
        self.normals_by_start = {}
        self.captures_mode = False

        # для маршрута захвата (если игрок в процессе длинной цепочки)
        self.active_sequences = []  # список допустимых последовательностей для выбранной шашки
        self.prefix = []            # пройденные шаги: [((to),(capt)), ...]

        self.reset()

    def reset(self):
        # расстановка: чёрные сверху, белые снизу
        for r in range(ROWS):
            for c in range(COLS):
                self.board[r][c] = None
                if not dark_square(r, c):
                    continue
                if r < 3:
                    self.board[r][c] = {"color": 'b', "king": False}
                elif r > 4:
                    self.board[r][c] = {"color": 'w', "king": False}
        self.turn = 'w'
        self.selected = None
        self.active_sequences = []
        self.prefix = []
        self.recompute_legal()

    def recompute_legal(self):
        M = encode_matrix(self.board)
        self.captures_mode, self.seqs_by_start, self.normals_by_start = all_legal(
            self.turn, M)

    # ---------- применить один шаг (hop) из цепочки ----------
    def apply_capture_hop(self, fr, to, captured):
        fr_r, fr_c = fr
        to_r, to_c = to
        cap_r, cap_c = captured

        piece = self.board[fr_r][fr_c]
        assert piece is not None
        # движение
        self.board[fr_r][fr_c] = None
        self.board[to_r][to_c] = piece
        # снять побитую
        self.board[cap_r][cap_c] = None
        # повышение, если достигли последней линии
        if not piece["king"]:
            if (piece["color"] == 'w' and to_r == 0) or (piece["color"] == 'b' and to_r == ROWS-1):
                piece["king"] = True

    def apply_normal_move(self, fr, to):
        fr_r, fr_c = fr
        to_r, to_c = to
        piece = self.board[fr_r][fr_c]
        self.board[fr_r][fr_c] = None
        self.board[to_r][to_c] = piece
        if not piece["king"]:
            if (piece["color"] == 'w' and to_r == 0) or (piece["color"] == 'b' and to_r == ROWS-1):
                piece["king"] = True

    # ---------- ход завершён ----------
    def end_turn(self):
        self.turn = 'b' if self.turn == 'w' else 'w'
        self.selected = None
        self.active_sequences = []
        self.prefix = []
        self.recompute_legal()
        # Проверка на конец игры (нет ходов)
        if not self.captures_mode and not self.normals_by_start:
            # предыдущий игрок победил
            winner = 'w' if self.turn == 'b' else 'b'
            self.show_gameover(winner)

    def show_gameover(self, winner):
        overlay = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.screen.blit(overlay, (0, 0))
        text = f"Победа {'White' if winner == 'w' else 'Black'}!  (R — рестарт, Esc — выход)"
        img = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(img, img.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pg.display.flip()
        # блок до действия
        waiting = True
        while waiting:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit(0)
                    if e.key == pg.K_r:
                        self.reset()
                        waiting = False
            self.clock.tick(30)

    # ---------- обработка кликов ----------
    def handle_click(self, mx, my):
        r, c = my // TILE, mx // TILE
        if not inside(r, c) or not dark_square(r, c):
            self.selected = None
            self.active_sequences = []
            self.prefix = []
            return

        if self.captures_mode:
            # если нет выбранной — выбираем только разрешённые фигуры
            if self.selected is None:
                if (r, c) in self.seqs_by_start:
                    self.selected = (r, c)
                    self.active_sequences = deepcopy(
                        self.seqs_by_start[(r, c)])
                    self.prefix = []
                return
            # если выбранная есть — проверяем, клик по возможной следующей посадке?
            # соберём варианты следующего шага по активным последовательностям с данным префиксом
            next_options = self.next_capture_options()
            if (r, c) in [pos for (pos, _cap) in next_options]:
                # найдём соответствующий шаг и применим
                fr = self.current_pos_of_selected()
                # что именно съедаем на этом шаге
                cap = None
                for (pos, cap_) in next_options:
                    if pos == (r, c):
                        cap = cap_
                        break
                assert cap is not None
                self.apply_capture_hop(fr, (r, c), cap)
                # дополним префикс и сузим активные последовательности
                self.prefix.append(((r, c), cap))
                self.filter_sequences_by_prefix()
                # продолжается ли цепочка?
                if self.next_capture_options():
                    # продолжаем той же шашкой
                    return
                # иначе ход закончен
                self.end_turn()
                return
            else:
                # повторный выбор фигуры с началом максимальной цепочки
                if (r, c) in self.seqs_by_start:
                    self.selected = (r, c)
                    self.active_sequences = deepcopy(
                        self.seqs_by_start[(r, c)])
                    self.prefix = []
                else:
                    # кликнули мимо — снять выделение
                    self.selected = None
                    self.active_sequences = []
                    self.prefix = []
                return
        else:
            # обычный режим
            if self.selected is None:
                if (r, c) in self.normals_by_start:
                    self.selected = (r, c)
                return
            else:
                fr = self.selected
                moves = self.normals_by_start.get(fr, [])
                if (r, c) in moves:
                    self.apply_normal_move(fr, (r, c))
                    self.end_turn()
                # снять выделение в любом случае
                self.selected = None
                return

    def current_pos_of_selected(self):
        """Где сейчас стоит выбранная шашка (меняется при пошаговом бое)."""
        if not self.selected:
            return None
        if not self.prefix:
            return self.selected
        else:
            return self.prefix[-1][0]

    def filter_sequences_by_prefix(self):
        """Оставляем только те активные последовательности, которые начинаются с нашего пройденного префикса."""
        def starts_with(seq, pref):
            if len(pref) > len(seq):
                return False
            for i in range(len(pref)):
                if seq[i] != pref[i]:
                    return False
            return True
        self.active_sequences = [
            s for s in self.active_sequences if starts_with(s, self.prefix)]

    def next_capture_options(self):
        """Множество следующих посадок из активных последовательностей с данным префиксом."""
        k = len(self.prefix)
        opts = []
        for s in self.active_sequences:
            if len(s) > k:
                opts.append(s[k])  # ((to_r,to_c),(cap_r,cap_c))
        # уникализируем по посадке
        uniq = {}
        for to, cap in opts:
            uniq[to] = cap
        return list(uniq.items())

    # ----------------------- Рендер -----------------------

    def draw_board(self):
        for r in range(ROWS):
            for c in range(COLS):
                color = DARK if dark_square(r, c) else LIGHT
                pg.draw.rect(self.screen, color, (c*TILE, r*TILE, TILE, TILE))
        # сетка
        for x in range(0, WIDTH+1, TILE):
            pg.draw.line(self.screen, GRID, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT+1, TILE):
            pg.draw.line(self.screen, GRID, (0, y), (WIDTH, y), 1)

    def draw_pieces(self):
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if not p:
                    continue
                cx, cy = c*TILE + TILE//2, r*TILE + TILE//2
                rad = TILE//2 - 10
                col = WHITE if p["color"] == 'w' else BLACK
                edge = WHITE_EDGE if p["color"] == 'w' else BLACK_EDGE
                pg.draw.circle(self.screen, col, (cx, cy), rad)
                pg.draw.circle(self.screen, edge, (cx, cy), rad, 3)
                if p["king"]:
                    pg.draw.circle(self.screen, KING_RING, (cx, cy), rad//2, 5)

    def draw_highlights(self):
        # Подсветка доступных фигур
        if self.captures_mode:
            # можно выбирать только стартовые фигуры с макс-боем
            for (r, c) in self.seqs_by_start.keys():
                cx, cy = c*TILE + TILE//2, r*TILE + TILE//2
                pg.draw.circle(self.screen, CAPT, (cx, cy), 8)
        else:
            for (r, c) in self.normals_by_start.keys():
                cx, cy = c*TILE + TILE//2, r*TILE + TILE//2
                pg.draw.circle(self.screen, MOVE, (cx, cy), 6)

        # Подсветка выбранной
        if self.selected:
            r, c = self.current_pos_of_selected()
            pg.draw.rect(self.screen, SEL, (c*TILE+2,
                         r*TILE+2, TILE-4, TILE-4), 3)

        # Подсветка доступных клеток хода
        if self.selected:
            if self.captures_mode:
                for (to_r, to_c), cap in self.next_capture_options():
                    x, y = to_c*TILE + TILE//2, to_r*TILE + TILE//2
                    pg.draw.circle(self.screen, CAPT, (x, y), 10)
            else:
                for (to_r, to_c) in self.normals_by_start.get(self.selected, []):
                    x, y = to_c*TILE + TILE//2, to_r*TILE + TILE//2
                    pg.draw.circle(self.screen, MOVE, (x, y), 10)

    def draw_hud(self):
        txt = f"Ход: {'White' if self.turn == 'w' else 'Black'}"
        if self.captures_mode:
            # найдём максимальную длину для красоты
            maxcap = 0
            for seqs in self.seqs_by_start.values():
                for s in seqs:
                    maxcap = max(maxcap, len(s))
            txt += f" • ОБЯЗАТЕЛЬНЫЙ БОЙ (макс {maxcap})"
        img = self.font.render(txt, True, OUTLINE)
        self.screen.blit(img, (10, 8))

        help_txt = "Клик — ход • R — рестарт • Esc — выход"
        img2 = self.font.render(help_txt, True, OUTLINE)
        self.screen.blit(img2, (10, HEIGHT - 28))

    def draw(self):
        self.screen.fill((15, 18, 20))
        self.draw_board()
        self.draw_highlights()
        self.draw_pieces()
        self.draw_hud()
        pg.display.flip()

    # ----------------------- Цикл -----------------------

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit(0)
                    if e.key == pg.K_r:
                        self.reset()
                if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    x, y = pg.mouse.get_pos()
                    self.handle_click(x, y)
            self.draw()

# ----------------------- main -----------------------


def main():
    game = Checkers()
    game.run()


if __name__ == "__main__":
    main()
