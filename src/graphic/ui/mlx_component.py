# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_component.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/25 18:34:13 by nramalan        #+#    #+#               #
#  Updated: 2026/03/26 09:50:05 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Callable, Optional
from src.graphic.mlx_utils import MlxVar
import random


class MlxComponent(ABC):
    def __init__(
        self, pos_x: int = 0, pos_y: int = 0,
        width: int = 100, height: int = 100,
    ) -> None:
        self.mlx_var: MlxVar
        self.id: str = f"component_{random.randint(1000, 9999)}"
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.on_click: Optional[Callable[[], None]]
        self.bg_ptr = None

    @abstractmethod
    def render(self) -> None:
        pass

    def is_point_inside(self, x: int, y: int) -> bool:
        return (
            self.pos_x <= x <= self.pos_x + self.width
            and self.pos_y <= y <= self.pos_y + self.height
        )

    @staticmethod
    def create_trgb(
        transparency: int, red: int, green: int, blue: int
    ) -> int:
        return transparency << 24 | red << 16 | green << 8 | blue;