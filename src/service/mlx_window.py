# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_window.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/23 09:48:35 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 10:42:26 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


from mlx import Mlx
from typing import Tuple, Any


class MlxWindow:

    def __init__(self, width: int, height: int, title: str) -> None:
        self.__mlx = Mlx()
        self.__mlx_ptr = self.__mlx.mlx_init()
        self.__window = None
        self.width = width
        self.height = height
        self.title = title

    def create_window(self) -> None:
        self.__window = self.__mlx.mlx_new_window(
            self.__mlx_ptr, self.width, self.height, self.title
        )

    def close_window(self) -> None:
        self.__mlx.mlx_destroy_window(self.__mlx_ptr, self.__window)

    def render(self) -> None:
        self.__mlx.mlx_loop(self.__mlx_ptr)

    def get_screen_size(self) -> Tuple[Any, int, int]:
        return self.__mlx.mlx_get_screen_size(self.__mlx_ptr)

    def get_mlx(self) -> Mlx:
        return self.__mlx

    def get_window(self) -> Any:
        return self.__window
