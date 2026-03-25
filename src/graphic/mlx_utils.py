# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_utils.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/25 18:37:05 by nramalan        #+#    #+#               #
#  Updated: 2026/03/25 21:45:05 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any
from mlx import Mlx


class MlxVar:
    def __init__(self, mlx: Mlx, mlx_ptr: Any, window: Any) -> None:
        self.mlx: Mlx = mlx
        self.mlx_ptr: Any = mlx_ptr
        self.window: Any = window
