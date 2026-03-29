#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/17 00:07:46 by nramalan        #+#    #+#               #
#  Updated: 2026/03/29 19:26:23 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


import sys
from src.exception import ArgsException, ConfigException, MlxException
from src.service import ConfigParser, Config, FileGenerator
from src.graphic import MlxWindow, MlxButton, MlxVar
from src.algorithm import Prim, MazeResolver


def regenerate_maze(
    config: Config, mlx_var: MlxVar
) -> None:
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
    print(f"animation = {config.animation}")
    mlx_window = MlxWindow(config, "A-Maze-Ing")
    ui_manager = mlx_window.ui_manager
    mlx_window.add_event_hook()
    width, _, _ = mlx_window.get_window_size()

    algo = Prim(config, mlx_window.mlx_var)
    algo.init_maze()
    result = algo.generate()
    algo.render_maze_to_mlx()
    resolver = MazeResolver(config, result)
    path = resolver.solve()
    file_generator = FileGenerator(config, result, path)
    file_generator.generate_output()

    path_visible = True
    algo.render_path_to_mlx(path)

    button = MlxButton(
        pos_x=(width - config.panel_size) + (config.panel_size // 4),
        pos_y=175,
        text="Hide Path",
        bg_color=0xFFFF9500,
        text_color=0xFFFFFFFF,
    )

    def toggle_path(config_arg: Config, mlx_var: MlxVar) -> None:
        nonlocal path_visible, path, algo
        if path_visible:
            algo.clear_path()
            path_visible = False
            button.text = "Show Path"
        else:
            algo.render_path_to_mlx(path)
            path_visible = True
            button.text = "Hide Path"
        ui_manager.render_components()

    button.on_click = toggle_path
    ui_manager.add_component(button)
    ui_manager.render_components()

    def regenerate_on_demand(config_arg: Config, mlx_var: MlxVar) -> None:
        nonlocal path_visible, path, algo, result
        result, path, algo = regenerate_maze(config_arg, mlx_var)
        path_visible = True
        algo.render_path_to_mlx(path)
        button.text = "Hide Path"
        ui_manager.render_components()

    # Optional: second button to regenerate with path visible.
    regen_button = MlxButton(
        pos_x=(width - config.panel_size) + (config.panel_size // 4),
        pos_y=240,
        text="Regenerate",
        bg_color=0xFF00BBFF,
        text_color=0xFFFFFFFF,
    )
    regen_button.on_click = regenerate_on_demand
    ui_manager.add_component(regen_button)
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
