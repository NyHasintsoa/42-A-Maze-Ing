# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  maze_resolver.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:48:39 by nramalan        #+#    #+#               #
#  Updated: 2026/03/26 18:03:46 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List, Dict, Any
from collections import deque
from src.service import Config, BitPosition


class MazeResolver:
    def __init__(self, config: Config, maze: List[List[int]]) -> None:
        self.maze = maze
        self.entry = tuple(config.entry)
        self.exit = tuple(config.exit)
        self.width = config.width
        self.height = config.height

    def solve(self) -> List[str]:
        queue = deque([self.entry])
        came_from: Dict[Any, Any] = {self.entry: None}
        movements = [
            (0, -1, BitPosition.NORTH.value, "N"),
            (1, 0, BitPosition.EAST.value, "E"),
            (0, 1, BitPosition.SOUTH.value, "S"),
            (-1, 0, BitPosition.WEST.value, "W")
        ]

        while queue:
            curr_x, curr_y = queue.popleft()
            if (curr_x, curr_y) == self.exit:
                return self._reconstruct_path(came_from)
            for dx, dy, bit, label in movements:
                if self.maze[curr_y][curr_x] & bit:
                    nx, ny = curr_x + dx, curr_y + dy
                    if (
                        0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) not in came_from
                    ):
                        came_from[(nx, ny)] = ((curr_x, curr_y), label)
                        queue.append((nx, ny))
        return []

    def _reconstruct_path(
        self, came_from: Dict[Any, Any]
    ) -> List[str]:
        path: List[str] = []
        curr = self.exit
        while curr != self.entry:
            parent, direction = came_from[curr]
            path.append(direction)
            curr = parent
        return path[::-1]
