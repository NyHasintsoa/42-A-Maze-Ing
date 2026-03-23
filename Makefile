# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: nramalan <nramalan@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/21 18:02:15 by nramalan          #+#    #+#              #
#    Updated: 2026/03/21 20:00:18 by nramalan         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

SRCS_DIR := src
ALROGITHM_DIR := $(SRCS_DIR)/algorithm
EXCEPTIONS_DIR := $(SRCS_DIR)/exception
SERVICE_DIR := $(SRCS_DIR)/service

SRCS_ALGORITHM := __init__.py algorithm_generator.py \
				backtracking.py prims.py
SRCS_SERVICE := __init__.py config_parser.py maze_resolver.py
SRCS_EXCEPTION := __init__.py config_exception.py maze_exception.py \
				args_exception.py

SRCS := $(addprefix $(ALROGITHM_DIR)/, $(SRCS_ALGORITHM)) \
	$(addprefix $(SERVICE_DIR)/, $(SRCS_SERVICE)) \
	$(addprefix $(EXCEPTIONS_DIR)/, $(SRCS_EXCEPTION)) \
	$(SRCS_DIR)/maze_generator.py \
	$(SRCS_DIR)/__init__.py
	

VENV := .venv
VENV_BIN := @$(VENV)/bin

PYTHON := $(VENV_BIN)/python
PIP := $(VENV_BIN)/pip
PDB := $(VENV_BIN)/pdb
FLAKE8 := $(VENV_BIN)/flake8
MYPY := $(VENV_BIN)/mypy

NAME := mazegen-1.0.0-py3-none-any.whl

.DEFAULT_GOAL := $(NAME)

#----------------------------------------------
# Main Commands
#----------------------------------------------
.PHONY: install
install: $(VENV)
	@echo "Installing project and its dependencies"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install lib/mlx-2.2-py3-none-any.whl

.PHONY: run
run: $(VENV)
	@echo "Running project"
	$(PYTHON) a_maze_ing.py config.txt

.PHONY: debug
debug: $(VENV)
	@echo "Debugging project"
	$(PDB) a_maze_ing.py

.PHONY: clean
clean:
	@echo "Cleaning project"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@rm -rf .mypy_cache .pytest_cache
	@rm -rf $(NAME) dist/
	@rm -rf src/mazegen.egg-info

.PHONY: lint
lint: $(VENV)
	@echo "Check Project Types"
	$(FLAKE8) .
	$(MYPY) . --warn-return-any --warn-unused-ignores \
			--ignore-missing-imports --disallow-untyped-defs \
			--check-untyped-defs

.PHONY: lint-strict
lint-strict: $(VENV)
	@echo "Check Project Types Strict Mode"
	$(FLAKE8) .
	$(MYPY) . --strict

#----------------------------------------------
# Other Commands
#----------------------------------------------
$(NAME): $(VENV) $(SRCS)
	@echo "Building project"
	$(PYTHON) -m build
	@cp dist/$(NAME) .
	@rm -rf dist

#----------------------------------------------
# Dependencies
#----------------------------------------------
$(VENV):
	@echo "Creating virtual environment and installing dependencies"
	@python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install lib/mlx-2.2-py3-none-any.whl