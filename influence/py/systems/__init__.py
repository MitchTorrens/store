# NOTICE: ALL INFORMATION CONTAINED IN THIS PROGRAM IS, AND REMAINS THE PROPERTY OF MITCHELL TORRENS. THE INTELLECTUAL
# AND TECHNICAL CONCEPTS CONTAINED HEREIN ARE PROTECTED BT COPYRIGHT LAW. IT IS STRICTLY FORBIDDEN TO SHARE, COPY,
# REPRODUCE, MODIFY, OR DISSEMINATE ANY INFORMATION INCLUDED IN THIS PROGRAM UNLESS PRIOR WRITTEN PERMISSION IS OBTAINED
# FROM MITCHELL TORRENS.
# Copyright (c) 2023, Mitchell Torrens. All rights reserved.

"""systems"""

from threading import Event
from typing import List, Literal

from data import EntityIndex

# from ecs import CMD, EntityIndex, System

# class Draw(System):
#     def process(self, stdscr):
#         physics = State.components[CT.PHYSICS]
#         animation = State.components[CT.ANIMATION]

#         stdscr.clear()

#         for ei in self.entities:
#             stdscr.addstr(physics[ei].r, physics[ei].c, animation[ei].sprite)
#             stdscr.refresh()
CMD = Literal["X_NONE", "X_QUIT", "X_UP", "X_LEFT", "X_DOWN", "X_RIGHT"]

class System:
    _tag = "S_SYSTEM"

    @property
    def tag(self) -> str:
        return self._tag


class ControlError(RuntimeError):
    pass


class Control(System):
    def __init__(self, player_ei: EntityIndex):
        self._player_ei = player_ei
        
        self.exit = Event()

    def process(self, inputs: List[CMD]):
        pass



# class Render(System):
#     def __init__(self, player_ei: EntityIndex):
#         self._player_ei = player_ei

#     def draw(self, stdscr):
#         """TODO""" 
