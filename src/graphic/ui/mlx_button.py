# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_button.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/25 18:42:50 by nramalan        #+#    #+#               #
#  Updated: 2026/03/26 09:32:30 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any
from src.graphic.ui.mlx_component import MlxComponent
from src.exception import MlxException


class MlxButton(MlxComponent):
    def __init__(
        self,
        pos_x: int = 0,
        pos_y: int = 0,
        width: int = 150,
        height: int = 45,
        text: str = "Button",
        bg_color: int = 0xBABABAFF,
        text_color: int = 0x000000,
    ) -> None:
        super().__init__(pos_x, pos_y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.bg_ptr: Any

    def render(self) -> None:
        self._create_bg_image()
        self.mlx_var.mlx.mlx_put_image_to_window(
            self.mlx_var.mlx_ptr, self.mlx_var.window,
            self.bg_ptr, self.pos_x, self.pos_y
        )
        self._draw_text()

    def _create_bg_image(self) -> None:
        self.bg_ptr = self.mlx_var.mlx.mlx_new_image(
            self.mlx_var.mlx_ptr, self.width, self.height
        )
        if not self.bg_ptr:
            raise MlxException("Can't create image 1")
        buf, _, sl, _ = self.mlx_var.mlx.mlx_get_data_addr(self.bg_ptr)
        color_bytes = self.bg_color.to_bytes(4, "little")
        for y in range(self.height):
            line_offset = y * sl
            for x in range(self.width):
                i = line_offset + x * 4
                if i + 4 <= len(buf):
                    buf[i:i+4] = color_bytes

    def _draw_text(self) -> None:
        text_x = self.pos_x + (self.width - len(self.text) * 10) // 2
        text_y = self.pos_y + (self.height - 20) // 2
        self.mlx_var.mlx.mlx_string_put(
            self.mlx_var.mlx_ptr,
            self.mlx_var.window,
            text_x,
            text_y,
            self.text_color,
            self.text,
        )
