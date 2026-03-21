# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_exception.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:27:44 by nramalan        #+#    #+#               #
#  Updated: 2026/03/21 22:32:12 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


class ConfigException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
