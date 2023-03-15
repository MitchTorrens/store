# NOTICE: ALL INFORMATION CONTAINED IN THIS PROGRAM IS, AND REMAINS THE PROPERTY OF MITCHELL TORRENS. THE INTELLECTUAL
# AND TECHNICAL CONCEPTS CONTAINED HEREIN ARE PROTECTED BT COPYRIGHT LAW. IT IS STRICTLY FORBIDDEN TO SHARE, COPY,
# REPRODUCE, MODIFY, OR DISSEMINATE ANY INFORMATION INCLUDED IN THIS PROGRAM UNLESS PRIOR WRITTEN PERMISSION IS OBTAINED
# FROM MITCHELL TORRENS.
# Copyright (c) 2023, Mitchell Torrens. All rights reserved.

"""systems.ui"""

import curses
import logging
import os
import struct
import sys
# import time
from logging.handlers import QueueHandler, QueueListener
from queue import Queue, Empty
from functools import cached_property
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Protocol, Optional, Final, Tuple, Callable
# from typing_extensions import Self

# from ecs import *
# from state import CT, CMD, ET, EntityIndex, State, StateRecord
from systems import CMD
from data import DATA, C_LOCATION, C_ANIMATION, NUM_COMPONENTS, X_QUIT, X_UP, X_LEFT, X_DOWN, X_RIGHT
import cfg

if TYPE_CHECKING:
    from _curses import _CursesWindow
    CursesWindow = _CursesWindow
else:
    CursesWindow = Any

log = logging.getLogger(__name__)
debug_log = logging.getLogger(f"debug.{__name__}")

MAX_INPUTS = 128

X_BINDINGS: Final = Any  # X_QUIT | X_UP | X_LEFT | X_DOWN | X_RIGHT



class UI(Protocol):
    """."""
    def setup(self): ...

    def render(self): ...

    @property
    def handler(self): ...


class HMI(Protocol):
    """."""
    
    def process(self): ...

_q_log = Queue()


class CursesUI(UI):
    """."""

    def __init__(self, stdscr: CursesWindow):
        self.stdscr = stdscr
        self._log_handler = QueueHandler(_q_log)
        self._log_listener = QueueListener(_q_log, respect_handler_level=True)
        self._log_handler.listener = self._log_listener
        self._message = ""
    

    def setup(self):
        pass


    def render(self):
        pass


class CursesWindowUI(UI):
    """."""

    def __init__(self, window_params: cfg.WindowParams, border_params: Iterable[int], color_pair: Optional[int] = None):
        self._win = curses.newwin(*window_params)
        self._border_params = border_params
        if color_pair:
            self._win.bkgd(' ', curses.color_pair(color_pair))
    
    def _render(self):
        raise NotImplementedError("TODO.")

    def render(self):
        self._win.erase()
        self._win.border(*self._border_params)
        self._render()
        self._win.refresh()

class CursesGameWindow(CursesWindowUI):
    """."""

    def _render(self):
        location = struct.unpack_from(C_LOCATION.format, DATA, C_LOCATION.offset)
        animation = struct.unpack_from(C_ANIMATION.format, DATA, C_ANIMATION.offset)
        for ei in range(NUM_COMPONENTS):
            if location[3*ei] and animation[2*ei]:
                self._win.addstr(location[3*ei + 1], location[3*ei + 2], animation[2*ei + 1])

class CursesHudWindow(CursesWindowUI):
    """."""

    def _render(self):
        self._win.addstr(1, 1, "HUD Window")

class CursesConsoleWindow(CursesWindowUI):
    """."""

    def _render(self):
        self._win.move(1,1)


class CursesOutputWindow(CursesWindowUI):
    """."""

    def __init__(self, handler: logging.Handler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._handler = handler

    def _render(self):
        # w.addstr(1, 1, "Output Window")
        while not _q_log.empty():
            self._win.addstr(1, 1, _q_log.get_nowait().msg)



def make_curses_windows(stdscr: CursesWindow) -> Tuple[CursesUI, CursesUI, CursesUI, CursesUI]:
    """."""
    curses.initscr()

    term_size = os.get_terminal_size()
    if not (term_size.columns == 282 and term_size.lines == 77):
        raise RuntimeError(f"Resize Terminal: {term_size.columns}x{term_size.lines}")
    debug_log.info("INITING")

    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

    w_game_border_params = []
    w_hud_border_params = [0, 0, 0, 0, curses.ACS_TTEE]
    w_output_border_params = [0, 0, 0, 0, 0, curses.ACS_RTEE, 0, curses.ACS_BTEE]
    w_console_border_params = [0, 0, 0, 0, curses.ACS_LTEE, curses.ACS_TTEE, 0, curses.ACS_BTEE]

    w_game = CursesGameWindow(cfg.w_game_params, w_game_border_params, 1)
    w_hud = CursesHudWindow(cfg.w_hud_params, w_hud_border_params, 1)
    w_console = CursesConsoleWindow(cfg.w_console_params, w_console_border_params)
    w_output = CursesOutputWindow(QueueHandler(_q_log), cfg.w_output_params, w_output_border_params)
    logging.getLogger().addHandler(w_output._handler)

    stdscr.nodelay(True)
    stdscr.clear()

    return w_game, w_hud, w_output,  w_console, 


class CursesHMI(HMI):
    """."""

    X_MAP: Final = {
        113: X_QUIT,   # q
        119: X_UP,     # w
        97:  X_LEFT,   # a
        115: X_DOWN,   # s
        100: X_RIGHT,  # d
    }

    def __init__(self, stdscr: CursesWindow):
        self.stdscr = stdscr

    def _input_list(self) -> List[X_BINDINGS]:
        chs = []
        # TODO: Benchmarking opportunity
        while (c := self.stdscr.getch()) != -1:
            try:
                chs.append(self.X_MAP[c])
            except KeyError:
                debug_log.exception("Unexpected character: %s", c)
            if len(chs) > MAX_INPUTS:
                raise RuntimeError("TODO: input error")
        return chs

    def process(self) -> List[X_BINDINGS]:                
        return self._input_list()


class TerminalUI(UI):
    """."""

    def __init__(self):
        pass

    def setup(self):
        pass

    def render(self):
        location = struct.unpack_from(C_LOCATION.format, DATA, C_LOCATION.offset)
        animation = struct.unpack_from(C_ANIMATION.format, DATA, C_ANIMATION.offset)

        log.info("--- RENDERING ---")

        for ei in range(NUM_COMPONENTS):
            if location[3*ei] and animation[2*ei]:
                log.info(
                    "Entity: %s: %s, %s, %s, %s, %s",
                    ei, location[3*ei], location[ei*3 + 1], location[ei*3 + 2],
                    animation[2*ei], animation[2*ei + 1])

        log.info("--- END RENDERING ---\n")

    @cached_property
    def handler(self) -> logging.Handler:
        return logging.StreamHandler(sys.stdout)

class InputHMI(HMI):
    """."""

    def process(self):
        pass
