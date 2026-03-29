# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ui_manager.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/25 16:06:29 by nramalan        #+#    #+#               #
#  Updated: 2026/03/29 17:40:22 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Dict
from src.graphic.ui.mlx_component import MlxComponent
from src.graphic.mlx_utils import MlxVar
from src.service import Config


class UIManager:
    def __init__(self, mlx_var: MlxVar, config: Config) -> None:
        self.components: Dict[str, MlxComponent] = {}
        self.mlx_var = mlx_var
        self.config = config

    def setup_mouse_hooks(self) -> None:
        self.mlx_var.mlx.mlx_mouse_hook(
            self.mlx_var.window, self._handle_mouse_click, self.mlx_var
        )

    def _handle_mouse_click(
        self, button: int, x: int, y: int, mlx_var: MlxVar
    ) -> None:
        if button != 1:
            return
        for component in self.components.values():
            if (
                component.is_point_inside(x, y)
                and component.on_click
            ):
                self.mlx_var.mlx.mlx_do_sync(self.mlx_var.mlx_ptr)
                self.mlx_var.mlx.mlx_clear_window(
                    mlx_var.mlx_ptr, mlx_var.window
                )
                self.mlx_var.mlx.mlx_do_sync(self.mlx_var.mlx_ptr)
                self.render_components()
                component.on_click(self.config, mlx_var)
                break

    def add_component(self, component: MlxComponent) -> None:
        component.mlx_var = self.mlx_var
        self.components[component.id] = component

    def render_components(self) -> None:
        for component in self.components.values():
            component.render()

    def destroy_component(self) -> None:
        for component in self.components.values():
            if component.bg_ptr:
                self.mlx_var.mlx.mlx_destroy_image(
                    self.mlx_var.mlx_ptr, component.bg_ptr
                )
