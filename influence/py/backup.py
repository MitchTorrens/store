#! /usr/bin/env python3
import curses

import locale
import time
from curses import ascii
from dataclasses import dataclass
from threading import Event
from typing import Any

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


@dataclass
class Entity:
    r: int
    c: int
    x: str = 'o'


class State:
    def __init__(self, exit: Event):
        self.exit = exit
        self.rows = 41
        self.cols = 81
        top_wall = [Entity(0, c, "=") for c in range(1, self.cols - 1)]
        bottom_wall = [Entity(self.rows, c, "=") for c in range(1, self.cols - 1)]
        left_wall = [Entity(r, 0, "|") for r in range(1, self.rows - 1)]
        right_wall = [Entity(r, self.cols, "|") for r in range(1, self.rows - 1)]
        self.player = Entity(20, 40, 'x')
        self.ens = top_wall + bottom_wall + left_wall + right_wall

    def print_env(self, stdscr):
        for en in self.ens:
            stdscr.addstr(en.r, en.c, en.x)
    
    def print(self, stdscr):
        stdscr.addstr(self.player.r, self.player.c, self.player.x)
        std.scr.refresh()


def process(state: State, c: Any):
    if ascii.isalnum(c):
        if ascii.unctrl(c) == 'w':
            state.player.r += -1
        elif ascii.unctrl(c) == 'a':
            state.player.c += -1
        elif ascii.unctrl(c) == 's':
            state.player.r += 1
        elif ascii.unctrl(c) == 'd':
            state.player.c += 1
        else:
            state.exit.set()
        return

    state.exit.set()


def main(stdscr):
    state = State(Event())
    chs = []
    try:
        state.print_env(stdscr)
        while not state.exit.is_set():
            state.print(stdscr)
            chs.append(stdscr.getch())

            process(state, chs[-1])

            time.sleep(0.01)
    except Exception:
        import traceback
        traceback.print_exc()
    print(chs)
    time.sleep(3)
curses.wrapper(main)
