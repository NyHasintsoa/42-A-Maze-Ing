# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  algorithm_generator.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 22:04:11 by nramalan        #+#    #+#               #
#  Updated: 2026/03/29 19:50:19 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.service import Config, BitPosition
from src.graphic.mlx_utils import MlxVar
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple, Any
import struct
import random
import time


class AlgorithmGenerator(ABC):
    _instance: Optional["AlgorithmGenerator"] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "AlgorithmGenerator":
        if cls._instance is None:
            cls._instance = super(AlgorithmGenerator, cls).__new__(cls)
        return cls._instance

    def __init__(self, config: "Config", mlx_var: "MlxVar") -> None:
        if not hasattr(self, "_initialized"):
            self.config: "Config" = config
            self.mlx_var: "MlxVar" = mlx_var
            self.maze: List[List[int]] = []
            self.palette_idx: int = 0
            self._initialized = True

    def set_palette(self, palette_idx: int) -> None:
        if not (0 <= palette_idx < len(self.config.colors)):
            raise ValueError("Invalid palette index")
        self.palette_idx = palette_idx

    @abstractmethod
    def generate(self) -> List[List[int]]:
        pass

    def get_42_symbol(self) -> List[List[int]]:
        return [
            [16, 31, 31, 29, 16, 16, 16],
            [16, 31, 31, 31, 26, 26, 16],
            [16, 16, 16, 21, 16, 16, 16],
            [31, 31, 16, 21, 16, 18, 26],
            [31, 31, 16, 21, 16, 16, 16],
        ]

    def init_maze(self) -> List[List[int]]:
        self.maze.clear()
        full_connections = (
            BitPosition.NORTH.value
            | BitPosition.EAST.value
            | BitPosition.SOUTH.value
            | BitPosition.WEST.value
        )
        for _ in range(self.config.height):
            self.maze.append(
                [full_connections for _ in range(self.config.width)]
            )
        self.__generate_42_symbol()
        return self.maze

    def __generate_42_symbol(self) -> List[List[int]]:
        symbol: List[List[int]] = self.get_42_symbol()
        maze_h = len(self.maze)
        maze_w = len(self.maze[0])
        sym_h = len(symbol)
        sym_w = len(symbol[0])
        y_start = (maze_h - sym_h) // 2
        x_start = (maze_w - sym_w) // 2
        for y in range(len(symbol)):
            last_x = x_start
            for x in range(len(symbol[y])):
                if symbol[y][x] == 16:
                    self.maze[y_start][last_x] = symbol[y][x]
                else:
                    self.maze[y_start][last_x] = symbol[y][x] & (
                        ~BitPosition.VISITED.value
                    )
                last_x += 1
            y_start += 1
        return self.maze

    def remove_wall(self, x1: int, y1: int, x2: int, y2: int) -> None:
        directions: Dict[Tuple[int, int], Tuple[Any, Any]] = {
            (0, -1): (BitPosition.NORTH.value, BitPosition.SOUTH.value),
            (0, 1): (BitPosition.SOUTH.value, BitPosition.NORTH.value),
            (-1, 0): (BitPosition.WEST.value, BitPosition.EAST.value),
            (1, 0): (BitPosition.EAST.value, BitPosition.WEST.value),
        }

        delta = (x2 - x1, y2 - y1)
        if delta in directions:
            bit1, bit2 = directions[delta]
            self.maze[y1][x1] |= bit1
            self.maze[y2][x2] |= bit2

    def make_non_perfect(self) -> None:
        h = len(self.maze)
        w = len(self.maze[0])
        target_loops = max(2, (w * h) // 20)
        loops_added = 0
        all_cells = [(x, y) for y in range(h) for x in range(w)]
        random.shuffle(all_cells)

        for cx, cy in all_cells:
            if loops_added >= target_loops:
                break

            neighbors = [
                (0, -1, BitPosition.NORTH.value, BitPosition.SOUTH.value),
                (1, 0, BitPosition.EAST.value, BitPosition.WEST.value),
                (0, 1, BitPosition.SOUTH.value, BitPosition.NORTH.value),
                (-1, 0, BitPosition.WEST.value, BitPosition.EAST.value),
            ]
            random.shuffle(neighbors)

            for dx, dy, bit_curr, bit_neigh in neighbors:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                if not (self.maze[cy][cx] & bit_curr) and (
                    self.maze[ny][nx] != 16 and self.maze[cy][cx] != 16
                ):
                    self.maze[cy][cx] |= bit_curr
                    self.maze[ny][nx] |= bit_neigh
                    loops_added += 1
                    break

    def _get_render_params(self) -> Tuple[int, int]:
        _, screen_w, screen_h = self.mlx_var.mlx.mlx_get_screen_size(
            self.mlx_var.mlx_ptr
        )
        avail_w = screen_w - self.config.panel_size
        scale_x = max(1, avail_w // self.config.width)
        scale_y = max(1, screen_h // self.config.height)
        scale = min(scale_x, scale_y, 16)
        return scale, max(1, scale // 5)

    def _get_path_cells(self, path: List[str]) -> List[Tuple[int, int]]:
        x, y = self.config.entry
        cells = [(x, y)]
        movement = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0),
        }
        for direction in path:
            if direction in movement:
                dx, dy = movement[direction]
                x += dx
                y += dy
                if 0 <= x < self.config.width and 0 <= y < self.config.height:
                    cells.append((x, y))
        return cells

    def render_path_to_mlx(
        self, path: List[str], palette_idx: int | None = None
    ) -> None:
        if not path:
            return

        if palette_idx is None:
            palette_idx = self.palette_idx

        if not (0 <= palette_idx < len(self.config.colors)):
            palette_idx = 0

        self.set_palette(palette_idx)
        path_color = self.config.colors[palette_idx].get(5, 0xFFFF0000)

        coords = self._get_path_cells(path)
        scale, _ = self._get_render_params()
        radius = max(1, scale // 8)

        for cx, cy in coords:
            center_x = cx * scale + scale // 2
            center_y = cy * scale + scale // 2
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    px = center_x + dx
                    py = center_y + dy
                    if (
                        0 <= px < self.config.width * scale
                        and 0 <= py < self.config.height * scale
                    ):
                        self.mlx_var.mlx.mlx_pixel_put(
                            self.mlx_var.mlx_ptr,
                            self.mlx_var.window,
                            px,
                            py,
                            path_color,
                        )
        self.mlx_var.mlx.mlx_do_sync(self.mlx_var.mlx_ptr)
        self.mlx_var.path_coords = coords
        self.mlx_var.is_path_visible = True

    def clear_path(self) -> None:
        if not self.mlx_var.is_path_visible:
            return
        if self.mlx_var.maze_img:
            self.mlx_var.mlx.mlx_put_image_to_window(
                self.mlx_var.mlx_ptr,
                self.mlx_var.window,
                self.mlx_var.maze_img,
                0,
                0,
            )
        self.mlx_var.mlx.mlx_do_sync(self.mlx_var.mlx_ptr)
        self.mlx_var.is_path_visible = False
        self.mlx_var.path_coords = None

    def _get_cell_color(
        self, mx: int, my: int, mask: int, palette_idx: int | None = None
    ) -> bytes:
        if palette_idx is None:
            palette_idx = self.palette_idx
        if not (0 <= palette_idx < len(self.config.colors)):
            palette_idx = 0
        palette = self.config.colors[palette_idx]

        def to_bytes(c_idx: int, default: int) -> bytes:
            return struct.pack("<I", palette.get(c_idx, default))

        if (mx, my) == self.config.entry:
            return to_bytes(3, 0x00FF00)  # Entry
        if (mx, my) == self.config.exit:
            return to_bytes(4, 0x0000FF)  # Exit
        if (mask & 0xF) == 0:
            return to_bytes(2, 0xFF0000)  # Isolated
        return to_bytes(0, 0xFFFFFF)  # Path

    def _is_wall(
        self, dx: int, dy: int, scale: int, border: int, mask: int
    ) -> bool:
        return (
            (dy < border and not (mask & BitPosition.NORTH.value))
            or (dx >= scale - border and not (mask & BitPosition.EAST.value))
            or (dy >= scale - border and not (mask & BitPosition.SOUTH.value))
            or (dx < border and not (mask & BitPosition.WEST.value))
        )

    def update_cell(self, mx: int, my: int, mask: int) -> None:
        scale, border = self._get_render_params()
        wall_bytes = struct.pack("<I", self.config.colors[3].get(1, 0x000000))
        bg_bytes = self._get_cell_color(mx, my, mask)

        for dy in range(scale):
            for dx in range(scale):
                is_wall = self._is_wall(dx, dy, scale, border, mask)
                color_bytes = wall_bytes if is_wall else bg_bytes
                color_int = struct.unpack("<I", color_bytes)[0]
                self.mlx_var.mlx.mlx_pixel_put(
                    self.mlx_var.mlx_ptr,
                    self.mlx_var.window,
                    (mx * scale) + dx,
                    (my * scale) + dy,
                    color_int,
                )

    def render_maze_to_mlx(self) -> None:
        scale, border = self._get_render_params()
        if not self.mlx_var.maze_img:
            self.mlx_var.maze_img = self.mlx_var.mlx.mlx_new_image(
                self.mlx_var.mlx_ptr,
                self.config.width * scale,
                self.config.height * scale,
            )
        data, _, sl, _ = self.mlx_var.mlx.mlx_get_data_addr(
            self.mlx_var.maze_img
        )
        wall_bytes = struct.pack("<I", self.config.colors[3].get(1, 0x000000))

        for my in range(self.config.height):
            for mx in range(self.config.width):
                mask = self.maze[my][mx]
                bg_bytes = self._get_cell_color(mx, my, mask)

                cell_y_off = my * scale
                cell_x_off = mx * scale

                for dy in range(scale):
                    row_off = (cell_y_off + dy) * sl
                    for dx in range(scale):
                        is_wall = self._is_wall(dx, dy, scale, border, mask)
                        off = row_off + (cell_x_off + dx) * 4
                        if off + 4 <= len(data):
                            data[off: off + 4] = wall_bytes \
                                if is_wall else bg_bytes

        self.mlx_var.mlx.mlx_put_image_to_window(
            self.mlx_var.mlx_ptr, self.mlx_var.window,
            self.mlx_var.maze_img, 0, 0
        )
        if self.config.animation:
            time.sleep(self.config.delay)
            self.mlx_var.mlx.mlx_do_sync(self.mlx_var.mlx_ptr)
