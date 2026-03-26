# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  mlx_panel.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/25 23:47:52 by nramalan        #+#    #+#               #
#  Updated: 2026/03/25 23:51:17 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Optional
from src.graphic.ui.mlx_component import MlxComponent


class MlxPanel(MlxComponent):
    def __init__(
        self,
        pos_x: int = 0,
        pos_y: int = 0,
        width: int = 200,
        height: int = 100,
        bg_color: int = 0xFF0000,  # Red by default
        border_color: Optional[int] = None,
        border_width: int = 0,
        transparency: int = 0,  # 0 = opaque, 255 = fully transparent
    ) -> None:
        super().__init__(pos_x, pos_y, width, height)
        self.bg_color = bg_color
        self.border_color = border_color if border_color is not None else bg_color
        self.border_width = border_width
        self.transparency = transparency
        self._img_ptr = None
        self._on_click = None

    def render(self) -> None:
        """Render the panel"""
        if not self.mlx_var:
            return

        self._create_image()
        if self._img_ptr:
            self.mlx_var.mlx.mlx_put_image_to_window(
                self.mlx_var.mlx_ptr,
                self.mlx_var.window,
                self._img_ptr,
                self.pos_x,
                self.pos_y,
            )

    def _create_image(self) -> None:
        """Create the panel image with background and optional border"""
        if not self.mlx_var:
            return

        # Clean up old image if exists
        if self._img_ptr:
            self.mlx_var.mlx.mlx_destroy_image(self.mlx_var.mlx_ptr, self._img_ptr)

        self._img_ptr = self.mlx_var.mlx.mlx_new_image(
            self.mlx_var.mlx_ptr, self.width, self.height
        )

        if not self._img_ptr:
            return

        buf, _, sl, _ = self.mlx_var.mlx.mlx_get_data_addr(self._img_ptr)

        # Apply transparency to background color if needed
        bg_color_with_alpha = self._apply_transparency(self.bg_color)
        bg_bytes = bg_color_with_alpha.to_bytes(4, "little")

        # Prepare border color
        border_bytes = self._apply_transparency(self.border_color).to_bytes(4, "little")

        # Fill the panel
        for y in range(self.height):
            line_offset = y * sl
            for x in range(self.width):
                # Draw border if border_width > 0
                if self.border_width > 0 and (
                    y < self.border_width
                    or y >= self.height - self.border_width
                    or x < self.border_width
                    or x >= self.width - self.border_width
                ):
                    color_bytes = border_bytes
                else:
                    color_bytes = bg_bytes

                pixel_offset = line_offset + (x * 4)
                buf[pixel_offset : pixel_offset + 4] = color_bytes

    def _apply_transparency(self, color: int) -> int:
        """Apply transparency to a color"""
        if self.transparency == 0:
            return color

        # Extract RGB components
        red = (color >> 16) & 0xFF
        green = (color >> 8) & 0xFF
        blue = color & 0xFF

        # Apply transparency (alpha is in the highest byte)
        # MinilibX expects ARGB format: (alpha << 24) | (red << 16) | (green << 8) | blue
        return (self.transparency << 24) | (red << 16) | (green << 8) | blue

    def update_color(self, new_color: int) -> None:
        """Update the panel's background color"""
        self.bg_color = new_color
        self.render()

    def update_border(
        self, border_color: Optional[int] = None, border_width: int = None
    ) -> None:
        """Update the panel's border"""
        if border_color is not None:
            self.border_color = border_color
        if border_width is not None:
            self.border_width = border_width
        self.render()
