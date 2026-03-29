#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/17 00:07:46 by nramalan        #+#    #+#               #
#  Updated: 2026/03/29 19:43:30 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


import sys
from typing import List
from src.exception import ArgsException, ConfigException, MlxException
from src.service import ConfigParser, Config, FileGenerator
from src.graphic import MlxWindow, MlxButton, MlxVar
from src.algorithm import Prim, MazeResolver


def regenerate_maze(
    config: Config,
    mlx_var: MlxVar,
    algo: Prim,
    palette_idx: int,
) -> tuple[List[List[int]], List[str]]:
    algo.set_palette(palette_idx)
    algo.init_maze()
    result = algo.generate()
    algo.render_maze_to_mlx()
    resolver = MazeResolver(config, result)
    path = resolver.solve()
    file_generator = FileGenerator(config, result, path)
    if not file_generator.generate_output():
        raise RuntimeError("Failed to generate output file")
    return result, path


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

    palette_idx = 0
    algo = Prim(config, mlx_window.mlx_var)

    try:
        result, path = regenerate_maze(
            config, mlx_window.mlx_var, algo, palette_idx
        )
    except Exception as e:
        raise MlxException(f"Failed to generate or solve maze: {e}")

    path_visible = True
    algo.render_path_to_mlx(path, palette_idx)

    def toggle_path(config_arg: Config, mlx_var: MlxVar) -> None:
        nonlocal path_visible, path, algo, palette_idx
        if path_visible:
            algo.clear_path()
            path_visible = False
            toggle_button.text = "Show Path"
        else:
            algo.render_path_to_mlx(path, palette_idx)
            path_visible = True
            toggle_button.text = "Hide Path"
        ui_manager.render_components()

    toggle_button = MlxButton(
        pos_x=(width - config.panel_size) + (config.panel_size // 4),
        pos_y=175,
        text="Hide Path",
        bg_color=config.colors[palette_idx].get(2, 0xFFFF9500),
        text_color=config.colors[palette_idx].get(5, 0xFFFFFFFF),
    )
    toggle_button.on_click = toggle_path
    ui_manager.add_component(toggle_button)

    def change_palette(_config_arg: Config, _mlx_var: MlxVar) -> None:
        nonlocal palette_idx, path_visible, path, algo
        palette_idx = (palette_idx + 1) % len(config.colors)
        algo.set_palette(palette_idx)
        algo.render_maze_to_mlx()
        if path_visible:
            algo.render_path_to_mlx(path, palette_idx)
        color_button.bg_color = config.colors[palette_idx].get(1, 0xFF00BBFF)
        color_button.text_color = config.colors[palette_idx].get(5, 0xFFFFFFFF)
        ui_manager.render_components()

    color_button = MlxButton(
        pos_x=(width - config.panel_size) + (config.panel_size // 4),
        pos_y=240,
        text="Change Theme",
        bg_color=config.colors[palette_idx].get(1, 0xFF00BBFF),
        text_color=config.colors[palette_idx].get(5, 0xFFFFFFFF),
    )
    color_button.on_click = change_palette
    ui_manager.add_component(color_button)

    def exit_app(_config_arg: Config, _mlx_var: MlxVar) -> None:
        mlx_window.mlx.mlx_loop_exit(mlx_window.mlx_ptr)

    exit_button = MlxButton(
        pos_x=(width - config.panel_size) + (config.panel_size // 4),
        pos_y=305,
        text="Exit",
        bg_color=config.colors[palette_idx].get(4, 0xFFFF4136),
        text_color=config.colors[palette_idx].get(0, 0xFFFFFFFF),
    )
    exit_button.on_click = exit_app
    ui_manager.add_component(exit_button)

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
