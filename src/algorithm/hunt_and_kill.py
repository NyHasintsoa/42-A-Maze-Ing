# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  hunt_and_kill.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/23 22:18:10 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 22:49:29 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


import random
from typing import List, Tuple, Optional
from src.algorithm.algorithm_generator import AlgorithmGenerator
from src.service import BitPosition


class HuntAndKill(AlgorithmGenerator):
    def generate(self) -> List[List[int]]:
        w, h = self.config.width, self.config.height
        try:
            cx, cy = self.config.entry
        except (TypeError, ValueError):
            cx, cy = 0, 0
        cx = max(0, min(cx, w - 1))
        cy = max(0, min(cy, h - 1))
        self.maze[cy][cx] |= BitPosition.VISITED.value
        self.update_cell(cx, cy, self.maze[cy][cx])
        while True:
            self.__kill_phase(cx, cy, w, h)
            hunt_result = self.__hunt_phase(w, h)
            if not hunt_result:
                break
            cx, cy = hunt_result
        return self.maze

    def __kill_phase(self, x: int, y: int, w: int, h: int) -> None:
        curr_x, curr_y = x, y
        while True:
            neighbors = self.__get_neighbors(
                curr_x, curr_y, w, h, visited=False
            )
            if not neighbors:
                break
            nx, ny = random.choice(neighbors)
            self.remove_wall(curr_x, curr_y, nx, ny)
            self.maze[ny][nx] |= BitPosition.VISITED.value
            self.update_cell(curr_x, curr_y, self.maze[curr_y][curr_x])
            self.update_cell(nx, ny, self.maze[ny][nx])
            curr_x, curr_y = nx, ny

    def __hunt_phase(self, w: int, h: int) -> Optional[Tuple[int, int]]:
        for y in range(h):
            for x in range(w):
                if self.maze[y][x] & BitPosition.VISITED.value:
                    continue
                visited_neighbors = self.__get_neighbors(
                    x, y, w, h, visited=True
                )
                if visited_neighbors:
                    nx, ny = random.choice(visited_neighbors)
                    self.remove_wall(x, y, nx, ny)
                    self.maze[y][x] |= BitPosition.VISITED.value
                    self.update_cell(nx, ny, self.maze[ny][nx])
                    self.update_cell(x, y, self.maze[y][x])
                    return (x, y)
        return None

    def __get_neighbors(
        self, x: int, y: int, w: int, h: int, visited: bool
    ) -> List[Tuple[int, int]]:
        results: List[Tuple[int, int]] = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                is_visited = bool(
                    self.maze[ny][nx] & BitPosition.VISITED.value
                )
                if is_visited == visited:
                    results.append((nx, ny))
        return results
