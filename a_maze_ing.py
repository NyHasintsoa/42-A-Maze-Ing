#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/17 00:07:46 by nramalan        #+#    #+#               #
#  Updated: 2026/03/27 13:11:03 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


import sys
from src.exception import ArgsException, ConfigException, MlxException
from src.service import ConfigParser, Config, FileGenerator
from src.graphic import MlxWindow, MlxButton, MlxVar
from src.algorithm import Prim, MazeResolver


def regenerate_maze(config: Config, mlx_var: MlxVar) -> None:
    algo = Prim(config, mlx_var)
    algo.init_maze()
    result = algo.generate()
    algo.render_maze_to_mlx()
    resolver = MazeResolver(config, result)
    path = resolver.solve()
    file_generator = FileGenerator(config, result, path)
    file_generator.generate_output()


def main() -> None:
    if len(sys.argv) <= 1:
        raise ArgsException("Not enough arguments")
    config_parser = ConfigParser(sys.argv[1])
    config_parser.parse()
    config: Config = config_parser.get_config()
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
    button.on_click = lambda config, mlx_var: regenerate_maze(config, mlx_var)
    ui_manager.add_component(button)
    ui_manager.render_components()
    algo = Prim(config, mlx_window.mlx_var)
    algo.init_maze()
    result = algo.generate()
    # algo.make_non_perfect()
    # print("after making non perfect")
    # for y in result:
    #     for x in y:
    #         print(f"{x}", end=' ')
    #     print()
    algo.render_maze_to_mlx()
    resolver = MazeResolver(config, result)
    path = resolver.solve()
    file_generator = FileGenerator(config, result, path)
    file_generator.generate_output()
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
