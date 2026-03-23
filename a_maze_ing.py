#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/17 00:07:46 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 14:58:29 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


import sys
from src.exception import ArgsException, ConfigException
from src.service.config_parser import ConfigParser
from src.algorithm import Backtracking


def main() -> None:
    if len(sys.argv) <= 1:
        raise ArgsException("Not enought arguments")
    config_parser = ConfigParser(sys.argv[1])
    config_parser.parse()
    algorithm = Backtracking(config_parser.get_config())
    print(algorithm.generate())


if __name__ == "__main__":
    try:
        main()
    except ArgsException as e:
        print(f"Args error: {e}", file=sys.stderr)
    except ConfigException as e:
        print(f"Config error: {e}", file=sys.stderr)
