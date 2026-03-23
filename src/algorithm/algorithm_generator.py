# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  algorithm_generator.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 22:04:11 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 21:33:05 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.service import Config, BitPosition
from abc import ABC, abstractmethod
from typing import List


class AlgorithmGenerator(ABC):
    def __init__(self, config: Config) -> None:
        self.config: Config = config
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
        if x1 == x2:
            if y1 > y2:
                self.maze[y1][x1] |= BitPosition.NORTH.value
                self.maze[y2][x2] |= BitPosition.SOUTH.value
            else:
                self.maze[y1][x1] |= BitPosition.SOUTH.value
                self.maze[y2][x2] |= BitPosition.NORTH.value
        elif y1 == y2:
            if x1 > x2:
                self.maze[y1][x1] |= BitPosition.WEST.value
                self.maze[y2][x2] |= BitPosition.EAST.value
            else:
                self.maze[y1][x1] |= BitPosition.EAST.value
                self.maze[y2][x2] |= BitPosition.WEST.value
