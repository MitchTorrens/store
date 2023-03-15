#! /usr/bin/env python3

# NOTICE: ALL INFORMATION CONTAINED IN THIS PROGRAM IS, AND REMAINS THE PROPERTY OF MITCHELL TORRENS. THE INTELLECTUAL
# AND TECHNICAL CONCEPTS CONTAINED HEREIN ARE PROTECTED BT COPYRIGHT LAW. IT IS STRICTLY FORBIDDEN TO SHARE, COPY,
# REPRODUCE, MODIFY, OR DISSEMINATE ANY INFORMATION INCLUDED IN THIS PROGRAM UNLESS PRIOR WRITTEN PERMISSION IS OBTAINED
# FROM MITCHELL TORRENS.
# Copyright (c) 2023, Mitchell Torrens. All rights reserved.

import curses
import locale
import time
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, List, Optional, Tuple, Protocol, Final, Literal

import click

import cfg
from data import EntityIndex, log_schema, ENTITY_ACTIONS
# from ecs import *
from state import available_eis, release, write_animation, write_location, write_actions
from systems import Control
from systems.ui import UI, HMI, CursesUI, CursesHMI, TerminalUI, InputHMI, CursesWindow, CursesWindowUI, make_curses_windows


log = logging.getLogger(__name__)
debug_log = logging.getLogger("debug")

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


def new_wall(r: int, c: int):
    ei = available_eis.get_nowait()
    write_location(ei, r, c)
    write_animation(ei, b"#")


def setup_state(ui: UI) -> EntityIndex:
    ui.render()
    player_entity = available_eis.get_nowait()
    write_location(player_entity, 32, 112)
    write_animation(player_entity, b"@")
    write_actions(player_entity, True, True, True, True)
    ui.render()

    for r in range(cfg.r_min, cfg.r_max):
        new_wall(r, cfg.c_min)
        new_wall(r, cfg.c_max -1)

    for c in range(cfg.c_min + 1, cfg.c_max - 1):
        new_wall(cfg.r_min, c)
        new_wall(cfg.r_max - 1, c)


def adjacent(*args):
    pass


def think():
    pass
    # for entity in range(MAX_ENTITIES):
    #     if State.components[C_ACTION][entity] and State.components[C_ACTION][entity].actions:
    #         if State.components[C_PHYSICS][entity]:
    #             physics = State.components[C_PHYSICS][entity]
    #             for other_entity in State.entities:
    #                 if entity == other_entity:
    #                     continue
    #                 if adjacent(physics, State.components[C_PHYSICS][entity]):
    #                     pass





UI_CONTEXT = Optional[CursesWindow]



def make_windows(ui_ctx: UI_CONTEXT) -> Tuple[UI, UI, UI, UI]:
    if "nodelay" in dir(ui_ctx):
        return make_curses_windows(ui_ctx)
    return TerminalUI(), InputHMI()


def make_hmi(hmi_ctx: UI_CONTEXT) -> HMI:
    if "nodelay" in dir(hmi_ctx):
        return CursesHMI(hmi_ctx)
    return InputHMI()
    

def main(ui_ctx: UI_CONTEXT):

    w_game, w_hud, w_console, w_output = make_windows(ui_ctx)
    uis = (w_game, w_hud, w_console, w_output)
    hmi = make_hmi(ui_ctx)
    setup_root_logger(w_console)
    # debug_log.info(w_console.handler)
    w_console.setup()
    player_ei = setup_state(w_console)

    controller = Control(player_ei)  # TODO
    while not controller.exit.is_set():
        # ui.render()

        # controller.process(input_list(stdscr))

        # TODO(v0.0.1): Run systems synchronously in some static sequence
        # TODO(v0.0.2): Design some standard interface for systems where each system knows what components it mutates.
        # Then schedule systems in parallel: prescan systems and generate a graph that ensures exclusive access to all
        # components for systems that mutate the component.
        # commands = hmi.process()
        # think(commands)

        # process_state()
        log.info(datetime.now())
        for ui in uis:
            ui.render()
        time.sleep(1)


DEFAULT_LOGFILE: Final = Path.home() / ".influence" / "logs" / f"{datetime.now().isoformat(timespec='seconds')}.log"

def setup_root_logger(ui: UI):
    root_log = logging.getLogger()
    # root_log.addHandler()
    root_log.setLevel(logging.INFO)


def setup_debug_logger(debug_log_filepath: Path):

    debug_log_filepath.parent.mkdir(parents=True, exist_ok=True)
    debug_log.addHandler(
        logging.FileHandler(debug_log_filepath)
    )
    debug_log.propagate = False
    debug_log.level = logging.INFO
    debug_log.info(f"\nDebug Log: {datetime.now().isoformat(timespec='seconds')}")
    log_schema()


@click.command()
@click.option("-l", "--logfile", type=click.Path(dir_okay=False, path_type=Path), default=DEFAULT_LOGFILE)
@click.option("-g", "--graphics", type=click.Choice(["curses", "text"]), default="curses")
def cli(logfile: Path, graphics: Literal["curses","text"]):
    setup_debug_logger(logfile)

    curses.wrapper(main)

cli()


