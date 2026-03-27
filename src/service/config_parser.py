# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_parser.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:31:32 by nramalan        #+#    #+#               #
#  Updated: 2026/03/27 11:25:27 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


from src.exception import ConfigException
from typing import Dict, Tuple, Any, List
from enum import Enum


class AlgorithmType(Enum):
    BACKTRACKING = "backtracking"
    PRIM = "prim"


class Config:
    def __init__(self) -> None:
        self.algorithm: AlgorithmType = AlgorithmType.BACKTRACKING
        self.width: int = 10
        self.height: int = 10
        self.panel_size: int = 250
        self.delay: float = 0
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.output_file: str = "output.txt"
        self.perfect: bool = True
        self.animation: bool = False
        self.seed: int = 0
        self.colors: List[Dict[int, int]] = [
            {
                0: 0xFF1E1E2E,  # empty -> Dark Blue/Black background (Base)
                1: 0xFF45475A,  # wall -> Soft Grey/Blue (Surface)
                2: 0xFFF9E2AF,  # ft symbol -> Gold/Yellow (Accent principal)
                3: 0xFFA6E3A1,  # start -> Soft Green
                4: 0xFFF38BA8,  # end -> Soft Red
                5: 0xFFFFFFFF   # path -> White
            },
            {
                0: 0xFFF5F5F7,  # empty -> White
                1: 0xFFD1D1D6,  # wall -> Gray
                2: 0xFFFF9500,  # ft symbol -> Orange
                3: 0xFF34C759,  # start -> Green
                4: 0xFFFF3B30,  # end -> Red
                5: 0xFF1C1C1E   # path -> black
            },
            {
                0: 0xFF0F380F,  # empty -> Dark Green
                1: 0xFF306230,  # wall -> Green
                2: 0xFF8BAC0F,  # ft symbol -> Accent Green
                3: 0xFFFFFFFF,  # start -> White
                4: 0xFF000000,  # end -> Black
                5: 0xFF9BBC0F   # path -> Green
            },
            {
                0: 0xFF001F3F,  # empty -> Dark Blue
                1: 0xFF3A6D8C,  # wall -> Steel Blue
                2: 0xFFFF851B,  # ft symbol -> Orange
                3: 0xFF2ECC40,  # start -> Green
                4: 0xFFFF4136,  # end -> Red Brick
                5: 0xFF7FDBFF   # path -> Blue
            },
            {
                0: 0xFF240046,  # empty -> Dark Purple
                1: 0xFF5A189A,  # wall -> Purple
                2: 0xFFFF9E00,  # ft symbol -> Orange
                3: 0xFF00B4D8,  # start -> Blue
                4: 0xFFF72585,  # end -> Magenta
                5: 0xFFE0AAFF   # path -> Lavander
            }
        ]


class ConfigParser:
    def __init__(self, config_path: str) -> None:
        self.config_path: str = config_path
        self.__config: Config = Config()

    def __apply_config(self, config: Dict[str, str]) -> None:
        def str_to_bool(name: str, value: str) -> bool:
            if value not in ["True", "False"]:
                raise ConfigException(f"Invalid value for '{name}': '{value}' \
(must be 'True' or 'False')")
            return value == "True"

        parsers: Dict[str, Any] = {
            "width": int,
            "height": int,
            "seed": int,
            "perfect": lambda v: str_to_bool("perfect", v),
            "animation": lambda v: str_to_bool("animation", v),
            "output_file": str,
            "entry": lambda v: tuple(map(int, v.split(",", 1))),
            "exit": lambda v: tuple(map(int, v.split(",", 1))),
            "algorithm": lambda v: AlgorithmType(v.lower())
        }
        for name, value in config.items():
            if not hasattr(self.__config, name):
                raise ConfigException(
                    f"Unknown configuration option: '{name}'"
                )
            if name not in parsers:
                continue
            try:
                parsed_value = parsers[name](value)
                setattr(self.__config, name, parsed_value)
            except (ValueError, KeyError):
                raise ConfigException(f"Invalid value for '{name}': {value}")

    def parse(self) -> Dict[str, str]:
        config: Dict[str, str] = {}
        try:
            with open(self.config_path, "r") as config_file:
                for _, line in enumerate(config_file.readlines()):
                    if line.strip().startswith("#") or len(line.strip()) == 0:
                        continue
                    name, value = line.strip().split("=", 1)
                    if "=" in value.lower():
                        raise ConfigException(f"Invalid value for '{name}': \
'{value}' contains '='")
                    if name.lower() in config:
                        raise ConfigException(
                            f"Duplicate configuration for '{name}'"
                        )
                    config[name.lower()] = value
        except FileNotFoundError:
            raise ConfigException(
                f"Configuration file '{self.config_path}' not found."
            )
        except PermissionError:
            raise ConfigException(f"Error: Permission denied when trying \
to read '{self.config_path}'.")
        except Exception as e:
            raise ConfigException(
                f"An error occurred while parsing the configuration: {e}"
            )
        self.__apply_config(config)
        return config

    def validate_config(self) -> None:
        if not (self.validate_coordonates(self.__config.entry)):
            raise ConfigException("Entry coordinates not in Size")
        if not (self.validate_coordonates(self.__config.exit)):
            raise ConfigException("Exit coordinates not in Size")
        entry_x, entry_y = self.__config.entry
        exit_x, exit_y = self.__config.exit
        if entry_x == exit_x and entry_y == exit_y:
            raise ConfigException(
                "Entry and Exit coordinates must be different"
            )
        if self.__config.height < 5 and self.__config.width:
            raise ConfigException(
                "Maze size (height, width) must greater or equal to 15"
            )

    def validate_coordonates(self, coordonates: Tuple[int, int]) -> bool:
        x, y = coordonates
        return (
            (0 <= x < self.__config.width)
            and (0 <= y < self.__config.height)
        )

    def get_config(self) -> Config:
        self.validate_config()
        return self.__config
