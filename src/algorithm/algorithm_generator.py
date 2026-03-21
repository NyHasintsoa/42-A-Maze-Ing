# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  algorithm_generator.py                            :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 22:04:11 by nramalan        #+#    #+#               #
#  Updated: 2026/03/21 22:32:24 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod


class AlgorithmGenerator(ABC):
    def __init__(self) -> None:
        self.view: int = 5

    @abstractmethod
    def generate(self, value: int) -> None:
        pass
