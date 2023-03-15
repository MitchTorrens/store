#! /usr/bin/env python3

import curses
import locale
import time
import logging
from typing import Any, Callable, List, Optional, Tuple, Protocol

import cfg
from ecs import *
from state import CAction, CAnimation, CT, ET, CPhysics, CUserController, State, process_state
from systems import Control
from systems.ui import UI, HMI, CursesUI, CursesHMI, TerminalUI, InputHMI, CursesWindow


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


COMMAND_MAP = {
    113: "X_QUIT",   # q
    119: "X_UP",     # w
    97:  "X_LEFT",   # a
    115: "X_DOWN",   # s
    100: "X_RIGHT",  # d
}
    
def new_wall(r: int, c: int):
    _ = State.new_entity(E_THING, CPhysics(r, c), CAnimation('#'))


def setup_state(ui):
    ui.render()
    _ = State.new_entity(
        E_PLAYER,
        CPhysics(20, 40),
        CAnimation('@'),
        CAction(),
        CUserController(COMMAND_MAP),
    )
    ui.render()
    for r in range(cfg.r_min, cfg.r_max):
        new_wall(r, 0)
        new_wall(r, cfg.c_max -1)

    for c in range(cfg.c_min + 1, cfg.c_max - 1):
        new_wall(0,c)
        new_wall(cfg.r_max - 1, c)


def adjacent(*args):
    pass


def think():
    for entity in range(MAX_ENTITIES):
        if State.components[C_ACTION][entity] and State.components[C_ACTION][entity].actions:
            if State.components[C_PHYSICS][entity]:
                physics = State.components[C_PHYSICS][entity]
                for other_entity in State.entities:
                    if entity == other_entity:
                        continue
                    if adjacent(physics, State.components[C_PHYSICS][entity]):
                        pass





UI_CONTEXT = Optional[CursesWindow]

def make_ui(ui_ctx: UI_CONTEXT) -> Tuple[UI, HMI]:
    if "nodelay" in dir(ui_ctx):
        return CursesUI(ui_ctx), CursesHMI(ui_ctx)
    return TerminalUI(), InputHMI()


def main(ui_ctx: UI_CONTEXT):

    ui, hmi = make_ui(ui_ctx)
    setup_data_state(ui)

    player_entity = State.entities[E_PLAYER][0]

    controller = Control(player_entity)  # TODO
    while not controller.exit.is_set():
        # ui.render()

        # controller.process(input_list(stdscr))
        hmi.process()
        think()

        process_state()

        time.sleep(1)

def main(ui_ctx: UI_CONTEXT):

    ui, hmi = make_ui(ui_ctx)
    setup_state(ui)

    player_entity = State.entities[E_PLAYER][0]

    controller = Control(player_entity)  # TODO
    while not controller.exit.is_set():
        # ui.render()

        # controller.process(input_list(stdscr))
        hmi.process()
        think()

        process_state()

        time.sleep(1)

log.info(State.snapshot())

# curses.wrapper(main)
main(None)
