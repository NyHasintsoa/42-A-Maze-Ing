#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/17 00:07:46 by nramalan        #+#    #+#               #
#  Updated: 2026/03/25 16:30:39 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


import sys
from src.exception import ArgsException, ConfigException
from src.algorithm import Prim
from src.service.config_parser import ConfigParser, Config
from src.graphic import MlxWindow


def main() -> None:
    if len(sys.argv) <= 1:
        raise ArgsException("Not enought arguments")
    config_parser = ConfigParser(sys.argv[1])
    config_parser.parse()
    config: Config = config_parser.get_config()
    print(f"config = {config.__dict__}")
    mlx_window = MlxWindow(config, "A-Maze-Ing")
    algo = Prim(config, mlx_window.get_mlx_var())
    mlx_window.add_event()
    print(f"algo = {algo.init_maze()}")
    mlx_window.render()
    mlx_window.close_window()


if __name__ == "__main__":
    try:
        main()
    except ArgsException as e:
        print(f"Args error: {e}", file=sys.stderr)
    except ConfigException as e:
        print(f"Config error: {e}", file=sys.stderr)
