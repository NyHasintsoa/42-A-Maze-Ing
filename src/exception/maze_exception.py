# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  MazeException.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:27:56 by nramalan        #+#    #+#               #
#  Updated: 2026/03/21 21:29:50 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


class MazeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
