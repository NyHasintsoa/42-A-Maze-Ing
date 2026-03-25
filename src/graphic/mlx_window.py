# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_window.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/23 09:48:35 by nramalan        #+#    #+#               #
#  Updated: 2026/03/25 22:29:33 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from mlx import Mlx
from typing import Any, Tuple, Optional
from src.service import Config
from src.graphic.mlx_utils import MlxVar
from src.graphic.ui_manager import UIManager


class MlxWindow:
    def __init__(self, config: Config, title: str) -> None:
        self.mlx: Mlx = Mlx()
        self.mlx_ptr: Any = self.mlx.mlx_init()
        self.config: Config = config
        width, height, self.scale = self.get_window_size()
        self.window = self.mlx.mlx_new_window(
            self.mlx_ptr, width, height, title
        )
        self.mlx.mlx_clear_window(self.mlx_ptr, self.window)
        self.mlx_var = MlxVar(self.mlx, self.mlx_ptr, self.window)
        self.title = title
        self.ui_manager: Optional[UIManager] = None

    def set_ui_manager(self, ui_manager: UIManager) -> None:
        self.ui_manager = ui_manager

    def add_hook(self) -> None:
        self.mlx.mlx_key_hook(
            self.window, MlxEventHandler.manage_key_simple, self.mlx_var
        )
        self.mlx.mlx_hook(
            self.window, 33, 0, MlxEventHandler.manage_close, self.mlx_var
        )

    def render(self) -> None:
        if self.ui_manager:
            self.ui_manager.draw_all()
        self.mlx.mlx_loop(self.mlx_ptr)

    def refresh(self) -> None:
        if self.ui_manager:
            self.ui_manager.draw_all()

    def close_window(self) -> None:
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.window)

    def get_window_size(self) -> Tuple[int, int, int]:
        _, screen_w, screen_h = self.mlx.mlx_get_screen_size(self.mlx_ptr)
        avail_w = screen_w - self.config.panel_size
        avail_h = screen_h
        scale_x = max(1, avail_w // self.config.width)
        scale_y = max(1, avail_h // self.config.height)
        scale = min(scale_x, scale_y, 16)
        img_w = self.config.width * scale
        img_h = self.config.height * scale
        return ((img_w + self.config.panel_size), img_h, scale)


class MlxEventHandler:
    @staticmethod
    def manage_close(mlx_var: MlxVar) -> None:
        mlx_var.mlx.mlx_loop_exit(mlx_var.mlx_ptr)

    @staticmethod
    def manage_key_simple(key: int, mlx_var: MlxVar) -> None:
        if key in (113, 27, 65307):  # q, ESC
            mlx_var.mlx.mlx_loop_exit(mlx_var.mlx_ptr)
            return
