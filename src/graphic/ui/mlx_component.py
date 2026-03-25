# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_component.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/25 18:34:13 by nramalan        #+#    #+#               #
#  Updated: 2026/03/25 22:24:39 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Callable
from src.graphic.mlx_utils import MlxVar
import random


class MlxComponent(ABC):
    def __init__(
        self, pos_x: int = 0, pos_y: int = 0,
        width: int = 100, height: int = 100
    ) -> None:
        self.mlx_var: MlxVar
        self.id: str = f"component_{random.randint(1000, 9999)}"
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.visible = True
        self.enabled = True
        self._on_click: Callable[[], None]
        self._img_ptr = None

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def _create_image(self) -> None:
        pass

    def is_point_inside(self, x: int, y: int) -> bool:
        """Check if a point is inside the component"""
        return (
            self.visible
            and self.enabled
            and self.pos_x <= x <= self.pos_x + self.width
            and self.pos_y <= y <= self.pos_y + self.height
        )

    @property
    def on_click(self) -> Callable[[], None]:
        return self._on_click

    @on_click.setter
    def on_click(self, handler: Callable[[], None]) -> None:
        self._on_click = handler

    def show(self) -> None:
        self.visible = True
        self.render()

    def hide(self) -> None:
        self.visible = False
        self._clear_image()

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def _clear_image(self) -> None:
        if self._img_ptr and self.mlx_var:
            self.mlx_var.mlx.mlx_destroy_image(
                self.mlx_var.mlx_ptr, self._img_ptr
            )
            self._img_ptr = None

    def __del__(self):
        self._clear_image()
