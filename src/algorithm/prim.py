# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  prim.py                                           :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:33:54 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 13:28:32 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from src.algorithm import AlgorithmGenerator


class Prim(AlgorithmGenerator):
    def generate(self, value: int) -> None:
        print(value)
