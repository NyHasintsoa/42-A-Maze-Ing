# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ArgsException.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:28:07 by nramalan        #+#    #+#               #
#  Updated: 2026/03/21 21:29:09 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


class ArgsException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
