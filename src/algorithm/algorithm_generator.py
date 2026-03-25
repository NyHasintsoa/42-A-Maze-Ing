# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  algorithm_generator.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 22:04:11 by nramalan        #+#    #+#               #
#  Updated: 2026/03/25 16:05:59 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.service import Config, BitPosition
from src.graphic import MlxVar
from abc import ABC, abstractmethod
from typing import List, ByteString
import struct


class AlgorithmGenerator(ABC):
    def __init__(self, config: Config, mlx_var: MlxVar) -> None:
        self.config: Config = config
        self.mlx_var: MlxVar = mlx_var
        self.maze: List[List[int]] = []
        self.init_maze()

    @abstractmethod
    def generate(self) -> List[List[int]]:
        pass

    def init_maze(self) -> List[List[int]]:
        self.maze.clear()
        full_connections = (
            BitPosition.NORTH.value | BitPosition.EAST.value |
            BitPosition.SOUTH.value | BitPosition.WEST.value
        )
        for _ in range(self.config.height):
            self.maze.append(
                [full_connections for _ in range(self.config.width)]
            )
        self.__generate_42_walls()
        return self.maze

    def __generate_42_walls(self) -> List[List[int]]:
        symbol: List[List[int]] = [
            [16, 31, 31, 29, 16, 16, 16],
            [16, 31, 31, 31, 26, 26, 16],
            [16, 16, 16, 21, 16, 16, 16],
            [31, 31, 16, 21, 16, 18, 26],
            [31, 31, 16, 21, 16, 16, 16],
        ]
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
        directions = {
            (0, -1): (BitPosition.NORTH.value, BitPosition.SOUTH.value),
            (0, 1):  (BitPosition.SOUTH.value, BitPosition.NORTH.value),
            (-1, 0): (BitPosition.WEST.value,  BitPosition.EAST.value),
            (1, 0):  (BitPosition.EAST.value,  BitPosition.WEST.value),
        }

        delta = (x2 - x1, y2 - y1)
        if delta in directions:
            bit1, bit2 = directions[delta]
            self.maze[y1][x1] |= bit1
            self.maze[y2][x2] |= bit2

    def update_cell(self, mx: int, my: int, mask: int) -> None:
        screen_w, screen_h = 1920, 1080
        avail_w = screen_w - 250
        avail_h = screen_h

        scale_x = max(1, avail_w // self.config.width)
        scale_y = max(1, avail_h // self.config.height)
        scale = min(scale_x, scale_y, 16)
        border_thick = max(1, scale // 5)

        def get_color_bytes(color_int: int) -> ByteString:
            return struct.pack("<I", color_int)

        palette = self.config.colors[0]
        wall_bytes = get_color_bytes(palette.get(1, 0x000000))
        path_bytes = get_color_bytes(palette.get(0, 0xFFFFFF))

        if (mx, my) == self.config.entry:
            bg_bytes = get_color_bytes(palette.get(3, 0x00FF00))
        elif (mx, my) == self.config.exit:
            bg_bytes = get_color_bytes(palette.get(4, 0x0000FF))
        elif (mask & 0xF) == 0:
            bg_bytes = get_color_bytes(palette.get(2, 0xFF0000))
        else:
            bg_bytes = path_bytes
        start_y = my * scale
        start_x = mx * scale
        for dy in range(scale):
            for dx in range(scale):
                is_wall = (
                    (
                        dy < border_thick and not (
                            mask & BitPosition.NORTH.value
                        )
                    ) or
                    (
                        dx >= scale - border_thick and not (
                            mask & BitPosition.EAST.value
                        )
                    ) or
                    (
                        dy >= scale - border_thick and not (
                            mask & BitPosition.SOUTH.value
                        )
                    ) or
                    (dx < border_thick and not (mask & BitPosition.WEST.value))
                )

                color = wall_bytes if is_wall else bg_bytes
                color_int = struct.unpack("<I", color)[0]
                self.mlx_var.mlx.mlx_pixel_put(
                    self.mlx_var.mlx_ptr,
                    self.mlx_var.window,
                    start_x + dx,
                    start_y + dy,
                    color_int
                )
