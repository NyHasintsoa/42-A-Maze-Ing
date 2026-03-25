#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/17 00:07:46 by nramalan        #+#    #+#               #
#  Updated: 2026/03/25 22:25:16 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


import sys
from src.exception import ArgsException, ConfigException
from src.service.config_parser import ConfigParser, Config
from src.graphic import MlxWindow, MlxButton, UIManager


def main() -> None:
    if len(sys.argv) <= 1:
        raise ArgsException("Not enough arguments")

    config_parser = ConfigParser(sys.argv[1])
    config_parser.parse()
    config: Config = config_parser.get_config()
    print(f"config = {config.__dict__}")
    mlx_window = MlxWindow(config, "A-Maze-Ing")
    mlx_window.add_hook()
    ui_manager = UIManager(mlx_window.mlx_var)
    mlx_window.set_ui_manager(ui_manager)
    button = MlxButton(
        pos_x=25,
        pos_y=25,
        text="Click Me!",
        bg_color=0x4CAF50,  # Green background
        hover_color=0x45A049,  # Darker green on hover
        text_color=0xFFFFFF,  # White text
        border_color=0x2E7D32,  # Dark green border
    )
    button.on_click = lambda: print("Button clicked! 🎉")
    ui_manager.add_component(button)
    second_button = MlxButton(
        pos_x=25,
        pos_y=85,
        text="Exit",
        bg_color=0xF44336,  # Red background
        hover_color=0xD32F2F,  # Darker red on hover
        text_color=0xFFFFFF,
    )
    second_button.on_click = lambda: mlx_window.close_window()
    ui_manager.add_component(second_button)
    mlx_window.render()
    mlx_window.close_window()


if __name__ == "__main__":
    try:
        main()
    except ArgsException as e:
        print(f"Args error: {e}", file=sys.stderr)
    except ConfigException as e:
        print(f"Config error: {e}", file=sys.stderr)
