# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  prim.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:33:54 by nramalan        #+#    #+#               #
#  Updated: 2026/03/26 15:31:05 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
import time
from src.algorithm.algorithm_generator import AlgorithmGenerator
from typing import List, Tuple
from src.service import BitPosition


class Prim(AlgorithmGenerator):
    def generate(self) -> List[List[int]]:
        w, h = self.config.width, self.config.height
        sx, sy = self.config.entry
        for y in range(h):
            for x in range(w):
                if not (self.maze[y][x] & BitPosition.VISITED.value):
                    self.maze[y][x] = 0
        sx, sy = max(0, min(sx, w - 1)), max(0, min(sy, h - 1))
        frontier: List[Tuple[int, int, int, int]] = []
        self.maze[sy][sx] |= BitPosition.VISITED.value
        self.update_cell(sx, sy, self.maze[sy][sx])
        time.sleep(self.config.delay)
        self.mlx_var.mlx.mlx_do_sync(self.mlx_var.mlx_ptr)
        self._add_to_frontier(sx, sy, frontier)
        while frontier:
            idx = random.randrange(len(frontier))
            cx, cy, nx, ny = frontier.pop(idx)
            if not (self.maze[ny][nx] & BitPosition.VISITED.value):
                self.remove_wall(cx, cy, nx, ny)
                self.maze[ny][nx] |= BitPosition.VISITED.value
                self.update_cell(cx, cy, self.maze[cy][cx])
                time.sleep(self.config.delay)
                self.mlx_var.mlx.mlx_do_sync(self.mlx_var.mlx_ptr)
                self.update_cell(nx, ny, self.maze[ny][nx])
                time.sleep(self.config.delay)
                self.mlx_var.mlx.mlx_do_sync(self.mlx_var.mlx_ptr)
                self._add_to_frontier(nx, ny, frontier)
        return self.maze

    def _add_to_frontier(
        self, x: int, y: int, frontier: List[Tuple[int, int, int, int]]
    ) -> None:
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.config.width and 0 <= ny < self.config.height:
                if not (self.maze[ny][nx] & BitPosition.VISITED.value):
                    frontier.append((x, y, nx, ny))
