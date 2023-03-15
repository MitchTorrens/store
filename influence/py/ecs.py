# NOTICE: ALL INFORMATION CONTAINED IN THIS PROGRAM IS, AND REMAINS THE PROPERTY OF MITCHELL TORRENS. THE INTELLECTUAL
# AND TECHNICAL CONCEPTS CONTAINED HEREIN ARE PROTECTED BT COPYRIGHT LAW. IT IS STRICTLY FORBIDDEN TO SHARE, COPY,
# REPRODUCE, MODIFY, OR DISSEMINATE ANY INFORMATION INCLUDED IN THIS PROGRAM UNLESS PRIOR WRITTEN PERMISSION IS OBTAINED
# FROM MITCHELL TORRENS.
# Copyright (c) 2023, Mitchell Torrens. All rights reserved.

"""ecs.py"""

from dataclasses import dataclass
from typing import Final, Literal, Tuple, TypeVar
from typing_extensions import Self


E_ENTITY: Final = "E_ENTITY"
E_PLAYER: Final = "E_PLAYER"
E_NPC: Final = "E_NPC"
E_THING: Final = "E_THING"

ET = Literal["E_ENTITY", "E_PLAYER", "E_NPC", "E_THING"]

C_COMPONENT = "C_COMPONENT"
C_PHYSICS = "C_PHYSICS"
C_ANIMATION = "C_ANIMATION"
C_ACTION = "C_ACTION"
C_USER_CONTROLLER = "C_USER_CONTROLLER"

CT = Literal["C_COMPONENT", "C_PHYSICS", "C_ANIMATION", "C_ACTION", "C_USER_CONTROLLER"]

S_SYSTEM = "S_SYSTEM"
S_INPUT = "S_INPUT"
S_DRAW ="S_DRAW"

ST = Literal["S_SYSTEM", "S_INPUT", "S_DRAW"]

X_NONE = "X_NONE"
X_QUIT = "X_QUIT"
X_UP = "X_UP"
X_LEFT = "X_LEFT"
X_DOWN = "X_DOWN"
X_RIGHT = "X_RIGHT"

CMD = Literal["X_NONE", "X_QUIT", "X_UP", "X_LEFT", "X_DOWN", "X_RIGHT"]

ENUM = Literal["E_ENTITY", "E_PLAYER", "E_NPC", "E_THING", "C_COMPONENT", "C_PHYSICS", "C_ANIMATION", "C_ACTION",
              "C_USER_CONTROLLER", "S_SYSTEM", "S_INPUT", "S_DRAW", "X_NONE", "X_QUIT", "X_UP", "X_LEFT", "X_DOWN",
              "X_RIGHT"]


@dataclass
class Component:
    _tag = "C_COMPONENT"

    @property
    def tag(self) -> CT:
        return self._tag
    
    def update(self, other: Self):
        raise NotImplementedError("")


@dataclass
class MetaComponent:
    pass


class System:
    _tag: ST = "S_SYSTEM"

    @property
    def tag(self) -> ST:
        return self._tag
