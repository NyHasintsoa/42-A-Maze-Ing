# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  ui_manager.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/25 16:06:29 by nramalan        #+#    #+#               #
#  Updated: 2026/03/25 22:26:04 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Dict, Optional
from src.graphic.ui.mlx_component import MlxComponent
from src.graphic.mlx_utils import MlxVar


class UIManager:
    def __init__(self, mlx_var: MlxVar) -> None:
        self.components: Dict[str, MlxComponent] = {}
        self.mlx_var = mlx_var
        self._setup_mouse_hooks()

    def _setup_mouse_hooks(self) -> None:
        self.mlx_var.mlx.mlx_mouse_hook(
            self.mlx_var.window, self._handle_mouse_click, self.mlx_var
        )

    def _handle_mouse_click(
        self, button: int, x: int, y: int, mlx_var: MlxVar
    ) -> None:
        if button != 1:
            return

        for component in self.components.values():
            if component.is_point_inside(x, y):
                component.on_click()
                break

    def add_component(self, component: MlxComponent) -> None:
        component.mlx_var = self.mlx_var
        self.components[component.id] = component

    def remove_component(self, component_id: str) -> Optional[MlxComponent]:
        return self.components.pop(component_id, None)

    def get_component(self, component_id: str) -> Optional[MlxComponent]:
        return self.components.get(component_id)

    def draw_all(self) -> None:
        for component in self.components.values():
            component.render()

    def clear_all(self) -> None:
        self.components.clear()
