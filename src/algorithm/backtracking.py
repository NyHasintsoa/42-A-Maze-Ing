# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  backtracking.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:34:28 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 22:12:13 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import random
from src.algorithm.algorithm_generator import AlgorithmGenerator
from src.service import BitPosition
from typing import List, Tuple


class Backtracking(AlgorithmGenerator):
    def generate(self) -> List[List[int]]:
        w, h = self.config.width, self.config.height
        try:
            ex, ey = self.config.entry
        except (TypeError, ValueError):
            ex, ey = 0, 0
        start_x = max(0, min(ex, w - 1))
        start_y = max(0, min(ey, h - 1))
        self.__stacking(start_x, start_y, w, h)
        return self.maze

    def __get_unvisited_neighbors(
        self, x: int, y: int, w: int, h: int
    ) -> List[Tuple[int, int]]:
        neighbors: List[Tuple[int, int]] = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                if not (self.maze[ny][nx] & BitPosition.VISITED.value):
                    neighbors.append((nx, ny))
        return neighbors

    def __stacking(self, x: int, y: int, w: int, h: int) -> None:
        stack = [(x, y)]
        self.maze[y][x] |= BitPosition.VISITED.value
        while stack:
            cx, cy = stack[-1]
            neighbors = self.__get_unvisited_neighbors(cx, cy, w, h)
            if neighbors:
                nx, ny = random.choice(neighbors)
                self.maze[ny][nx] |= BitPosition.VISITED.value
                self.remove_wall(cx, cy, nx, ny)
                stack.append((nx, ny))
            else:
                stack.pop()
