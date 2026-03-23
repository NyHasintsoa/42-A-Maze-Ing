# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config_parser.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: nramalan <nramalan@student.42antananari   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/21 21:31:32 by nramalan        #+#    #+#               #
#  Updated: 2026/03/23 13:40:22 by nramalan        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #


from src.exception import ConfigException
from typing import Dict, Tuple, Any
from enum import Enum


class AlgorithmType(Enum):
    BACKTRACKING = "backtracking"
    PRIM = "prim"


class Config:
    def __init__(self) -> None:
        self.algorithm: AlgorithmType = AlgorithmType.BACKTRACKING
        self.width: int = 10
        self.height: int = 10
        self.entry: Tuple[int, int] = (0, 0)
        self.exit: Tuple[int, int] = (0, 0)
        self.output_file: str = "output.txt"
        self.perfect: bool = True
        self.animation: bool = False
        self.seed: int = 0


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

    def get_config(self) -> Config:
        return self.__config
