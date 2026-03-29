# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  backtracking.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:34:28 by nramalan        #+#    #+#               #
#  Updated: 2026/03/29 17:58:40 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
import time
from src.algorithm.algorithm_generator import AlgorithmGenerator
from typing import List, Tuple
from src.service import BitPosition


class Backtracking(AlgorithmGenerator):
    def generate(self) -> List[List[int]]:
        w, h = self.config.width, self.config.height
        ex, ey = self.config.entry
        for y in range(h):
            for x in range(w):
                if not (self.maze[y][x] & BitPosition.VISITED.value):
                    self.maze[y][x] = 0
        start_x = max(0, min(ex, w - 1))
        start_y = max(0, min(ey, h - 1))
        self._stacking(start_x, start_y, w, h)
        return self.maze

    def _get_unvisited_neighbors(
        self, x: int, y: int, w: int, h: int
    ) -> List[Tuple[int, int]]:
        neighbors: List[Tuple[int, int]] = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if not (self.maze[ny][nx] & BitPosition.VISITED.value):
                    neighbors.append((nx, ny))
        return neighbors

    def _stacking(self, x: int, y: int, w: int, h: int) -> None:
        stack = [(x, y)]
        self.maze[y][x] |= BitPosition.VISITED.value
        self.update_cell(x, y, self.maze[y][x])
        time.sleep(self.config.delay)
        self.mlx_var.mlx.mlx_do_sync(self.mlx_var.mlx_ptr)
        while stack:
            cx, cy = stack[-1]
            neighbors = self._get_unvisited_neighbors(cx, cy, w, h)
            if neighbors:
                nx, ny = random.choice(neighbors)
                self.maze[ny][nx] |= BitPosition.VISITED.value
                self.remove_wall(cx, cy, nx, ny)
                self.update_cell(cx, cy, self.maze[cy][cx])
                self.update_cell(nx, ny, self.maze[ny][nx])
                time.sleep(self.config.delay)
                self.mlx_var.mlx.mlx_do_sync(self.mlx_var.mlx_ptr)
                stack.append((nx, ny))
            else:
                stack.pop()
