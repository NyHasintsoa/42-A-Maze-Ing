# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_exception.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/26 07:54:31 by nramalan        #+#    #+#               #
#  Updated: 2026/03/26 07:54:37 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


class MlxException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
