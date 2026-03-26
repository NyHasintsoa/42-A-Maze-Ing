#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/17 00:07:46 by nramalan        #+#    #+#               #
#  Updated: 2026/03/26 09:42:20 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


import sys
from src.exception import ArgsException, ConfigException, MlxException
from src.service.config_parser import ConfigParser, Config
from src.graphic import MlxWindow, MlxButton


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
    button = MlxButton(
        pos_x=500,
        pos_y=175,
        text="Click Me!",
        bg_color=0xFF58FFFA,
        text_color=0xFFFFFF,
    )
    button.on_click = lambda: print("Button clicked! 🎉")
    ui_manager.add_component(button)
    ui_manager.render_components()
    mlx_window.render()
    mlx_window.close_window()


if __name__ == "__main__":
    try:
        main()
    except ArgsException as e:
        print(f"Args error: {e}", file=sys.stderr)
    except ConfigException as e:
        print(f"Config error: {e}", file=sys.stderr)
    except MlxException as e:
        print(f"Mlx Error: {e}", file=sys.stderr)
