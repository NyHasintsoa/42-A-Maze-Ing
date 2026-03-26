# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  generator_utils.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/23 14:28:49 by nramalan        #+#    #+#               #
#  Updated: 2026/03/26 14:52:57 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum


class BitPosition(Enum):
    VISITED = 0b10000  # 16
    NORTH = 0b00001  # 1
    EAST = 0b00010  # 2
    SOUTH = 0b00100  # 4
    WEST = 0b01000  # 8
