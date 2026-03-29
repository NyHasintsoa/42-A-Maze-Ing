# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_utils.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/25 18:37:05 by nramalan        #+#    #+#               #
#  Updated: 2026/03/29 19:08:30 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, Optional
from mlx import Mlx


class MlxVar:
    def __init__(self, mlx: Mlx, mlx_ptr: Any, window: Any) -> None:
        self.mlx: Mlx = mlx
        self.mlx_ptr: Any = mlx_ptr
        self.window: Any = window
        self.maze_img: Optional[Any] = None
        self.path_img: Optional[Any] = None
        self.path_coords: Optional[list[tuple[int, int]]] = None
        self.is_path_visible: bool = False
