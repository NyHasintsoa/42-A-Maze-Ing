# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_window.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/23 09:48:35 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 22:36:21 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


from mlx import Mlx
from typing import Any, Tuple
from src.service import Config


class MlxVar:
    def __init__(self, mlx: Mlx, mlx_ptr: Any, window: Any) -> None:
        self.mlx: Mlx = mlx
        self.mlx_ptr: Any = mlx_ptr
        self.window: Any = window


class MlxWindow:
    def __init__(self, config: Config, title: str) -> None:
        self.__mlx: Mlx = Mlx()
        self.__mlx_ptr: Any = self.__mlx.mlx_init()
        self.__config: Config = config
        width, height = self.__get_window_size()
        self.__window = self.__mlx.mlx_new_window(
            self.__mlx_ptr, width, height, title
        )
        self.__mlx_var = MlxVar(self.__mlx, self.__mlx_ptr, self.__window)
        self.title = title

    def add_event(self) -> None:
        self.__mlx.mlx_hook(
            self.__window, 33, 0, MlxEventHandler.manage_close, self.__mlx_var
        )

    def render(self) -> None:
        self.__mlx.mlx_loop(self.__mlx_ptr)

    def close_window(self) -> None:
        self.__mlx.mlx_destroy_window(
            self.__mlx_ptr,
            self.__window
        )
        self.__mlx.mlx_release(self.__mlx_ptr)

    def __get_window_size(self) -> Tuple[int, int]:
        _, screen_w, screen_h = self.__mlx.mlx_get_screen_size(self.__mlx_ptr)
        avail_w = (screen_w if screen_w else 1920) - 250
        avail_h = (screen_h if screen_h else 1080)
        scale_x = max(1, avail_w // self.__config.width)
        scale_y = max(1, avail_h // self.__config.height)
        scale = min(scale_x, scale_y, 16)
        img_w = self.__config.width * scale
        img_h = self.__config.height * scale
        return ((img_w + 250), img_h)

    def get_mlx_var(self) -> MlxVar:
        return self.__mlx_var


class MlxEventHandler:
    @staticmethod
    def manage_close(mlx_var: MlxVar) -> None:
        mlx_var.mlx.mlx_loop_exit(mlx_var.mlx_ptr)

    @staticmethod
    def manage_key_simple(key: int, mlx_var: MlxVar) -> None:
        if key in (113, 27, 65307):
            mlx_var.mlx.mlx_loop_exit(mlx_var.mlx_ptr)
            return
