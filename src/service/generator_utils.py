# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  generator_utils.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/23 14:28:49 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 14:29:38 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum


class BitPosition(Enum):
    VISITED = 0b10000
    NORTH = 0b00001
    EAST = 0b00010
    SOUTH = 0b00100
    WEST = 0b01000
