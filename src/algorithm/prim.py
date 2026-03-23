# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  prim.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:33:54 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 15:03:27 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.algorithm.algorithm_generator import AlgorithmGenerator
from typing import List


class Prim(AlgorithmGenerator):
    def generate(self) -> List[List[int]]:
        return self.maze
