# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_button.py                                     :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/25 18:42:50 by nramalan        #+#    #+#               #
#  Updated: 2026/03/25 23:46:02 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Optional
from src.graphic.ui.mlx_component import MlxComponent


class MlxButton(MlxComponent):
    def __init__(
        self,
        pos_x: int = 0,
        pos_y: int = 0,
        width: int = 150,
        height: int = 45,
        text: str = "Button",
        bg_color: int = 0xBABABA,
        hover_color: int = 0xCCCCCC,
        text_color: int = 0x000000,
        border_color: int = 0x888888,
        border_width: int = 2,
        font_size: int = 12,
    ) -> None:
        super().__init__(pos_x, pos_y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.font_size = font_size
        self._is_hovering = False
        self._img_ptr = None
        self._on_click = lambda: print(f"Clicked: {self.text}")

    def render(self) -> None:
        self._create_image()
        self.mlx_var.mlx.mlx_put_image_to_window(
            self.mlx_var.mlx_ptr,
            self.mlx_var.window,
            self._img_ptr,
            self.pos_x,
            self.pos_y,
        )
        self._draw_text()

    def _create_image(self) -> None:
        if self._img_ptr:
            self.mlx_var.mlx.mlx_destroy_image(
                self.mlx_var.mlx_ptr, self._img_ptr
            )

        self._img_ptr = self.mlx_var.mlx.mlx_new_image(
            self.mlx_var.mlx_ptr, self.width, self.height
        )

        if not self._img_ptr:
            return

        buf, _, sl, _ = self.mlx_var.mlx.mlx_get_data_addr(self._img_ptr)

        fill_color = self.hover_color if self._is_hovering else self.bg_color
        fill_bytes = fill_color.to_bytes(4, "little")
        border_bytes = self.border_color.to_bytes(4, "little")

        for y in range(self.height):
            line_offset = y * sl
            for x in range(self.width):
                if (
                    y < self.border_width
                    or y >= self.height - self.border_width
                    or x < self.border_width
                    or x >= self.width - self.border_width
                ):
                    color_bytes = border_bytes
                else:
                    color_bytes = fill_bytes

                pixel_offset = line_offset + (x * 4)
                buf[pixel_offset:pixel_offset + 4] = color_bytes

    def _draw_text(self) -> None:
        if not self.mlx_var or not self.text:
            return

        char_width = self.font_size // 2 + 2
        text_width = len(self.text) * char_width
        text_x = self.pos_x + (self.width - text_width) // 2
        text_y = self.pos_y + (self.height // 2) + (self.font_size // 3)

        self.mlx_var.mlx.mlx_string_put(
            self.mlx_var.mlx_ptr,
            self.mlx_var.window,
            text_x,
            text_y,
            self.text_color,
            self.text,
        )

    def update_text(self, new_text: str) -> None:
        self.text = new_text
        self.render()

    def update_colors(
        self,
        bg_color: Optional[int] = None,
        hover_color: Optional[int] = None,
        text_color: Optional[int] = None,
    ) -> None:
        if bg_color is not None:
            self.bg_color = bg_color
        if hover_color is not None:
            self.hover_color = hover_color
        if text_color is not None:
            self.text_color = text_color
        self.render()
