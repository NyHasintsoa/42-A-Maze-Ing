# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  file_generator.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/27 10:59:09 by nramalan        #+#    #+#               #
#  Updated: 2026/03/27 11:18:41 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import List
from src.service import Config, BitPosition


class FileGenerator:
    def __init__(
        self, config: Config, maze_result: List[List[int]], resolver: List[str]
    ) -> None:
        self.maze: List[List[int]] = maze_result
        self.config: Config = config
        self.resolver: List[str] = resolver

    def generate_output(self) -> bool:
        try:
            with open(self.config.output_file, "w") as f:
                for y in range(self.config.height):
                    line = ""
                    for x in range(self.config.width):
                        n = 0 if (
                            self.maze[y][x] & BitPosition.NORTH.value
                        ) else 1
                        e = 0 if (
                            self.maze[y][x] & BitPosition.EAST.value
                        ) else 1
                        s = 0 if (
                            self.maze[y][x] & BitPosition.SOUTH.value
                        ) else 1
                        w = 0 if (
                            self.maze[y][x] & BitPosition.WEST.value
                        ) else 1
                        hexa = (w << 3) | (s << 2) | (e << 1) | n
                        hex_charset = "0123456789ABCDEF"
                        line += hex_charset[hexa]
                    f.write(line+"\n")
                f.write("\n")
                f.write(f"{self.config.entry[0]},{self.config.entry[1]}\n")
                f.write(f"{self.config.exit[0]},{self.config.exit[1]}\n")
                f.write(f"{"".join(self.resolver)}\n")
            return True
        except Exception:
            return False
