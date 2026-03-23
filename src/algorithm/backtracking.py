# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  backtracking.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:34:28 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 21:31:21 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.algorithm.algorithm_generator import AlgorithmGenerator
from typing import List


class Backtracking(AlgorithmGenerator):
    def generate(self) -> List[List[int]]:
        return self.maze
