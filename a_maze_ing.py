#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/17 00:07:46 by nramalan        #+#    #+#               #
#  Updated: 2026/03/26 15:17:16 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


import sys
from src.exception import ArgsException, ConfigException, MlxException
from src.service import ConfigParser, Config
from src.graphic import MlxWindow, MlxButton
from src.algorithm import Backtracking


def main() -> None:
    if len(sys.argv) <= 1:
        raise ArgsException("Not enough arguments")
    config_parser = ConfigParser(sys.argv[1])
    config_parser.parse()
    config: Config = config_parser.get_config()
    print(f"config = {config.__dict__}")
    mlx_window = MlxWindow(config, "A-Maze-Ing")
    ui_manager = mlx_window.ui_manager
    mlx_window.add_event_hook()
    width, _, _ = mlx_window.get_window_size()
    button = MlxButton(
        pos_x=(width - config.panel_size) + (config.panel_size // 4),
        pos_y=175,
        text="Click Me!",
        bg_color=0xFFFF9500,
        text_color=0xFFFFFFFF,
    )
    button.on_click = lambda: print("Button clicked! 🎉")
    ui_manager.add_component(button)
    ui_manager.render_components()
    algo = Backtracking(config, mlx_window.mlx_var)
    algo.init_maze()
    result = algo.generate()
    for y in result:
        for x in y:
            print(f"{x}", end=' ')
        print()
    mlx_window.render()
    mlx_window.close_window()


if __name__ == "__main__":
    print("Full Connextion")
    try:
        main()
    except ArgsException as e:
        print(f"Args error: {e}", file=sys.stderr)
    except ConfigException as e:
        print(f"Config error: {e}", file=sys.stderr)
    except MlxException as e:
        print(f"Mlx Error: {e}", file=sys.stderr)
