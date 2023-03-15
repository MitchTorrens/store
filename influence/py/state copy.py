"""state.py"""

import logging
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from queue import Queue
from threading import Lock
from typing import Any, Dict, Iterable, List, Optional, Tuple, TypedDict
from typing_extensions import Self

from ecs import *

log = logging.getLogger(__name__)


@dataclass
class CPhysics(Component):
    _tag = "C_PHYSICS"

    r: int
    c: int

    def __str__(self) -> str:
        return f"({self.r}, {self.c})"

    def update(self, other: Self):
        self.r, self.c = other.r, other.c


@dataclass
class CAnimation(Component):
    _tag = "C_ANIMATION"

    sprite: str

    def __str__(self) -> str:
        return self.sprite
    
    def update(self, other: Self):
        self.sprite = other.sprite


@dataclass
class CAction(Component):
    _tag = "C_ACTION"

    actions: List[Any] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        return f"{self.actions}"
    
    def update(self, other: Self):
        self.actions = other.actions

@dataclass
class CUserController(Component):
    _tag = "C_USER_CONTROLLER"

    command_map: Dict[int, CMD] = field(default_factory=lambda: {})
    
    def __str__(self) -> str:
        return f"{self.command_map}"

    def update(self, other: Self):
        self.command_map = other.command_map


class StateError(RuntimeError):
    """StateError."""



class ComponentsDict(TypedDict):
    C_COMPONENT: str
    C_PHYSICS: COMPONENTS_TUPLE[CPhysics]
    C_ANIMATION: COMPONENTS_TUPLE[CAnimation]
    C_ACTION: COMPONENTS_TUPLE[CAction]
    C_USER_CONTROLLER: COMPONENTS_TUPLE[CUserController]

a: ComponentsDict = {
    C_COMPONENT: "",
    C_PHYSICS: tuple(CPhysics(0, 0) for _ in range(MAX_COMPONENTS)),
    C_ANIMATION: tuple(CAnimation("") for _ in range(MAX_COMPONENTS)),
    C_ACTION: tuple(CAction() for _ in range(MAX_COMPONENTS)),
    C_USER_CONTROLLER: tuple(CUserController() for _ in range(MAX_COMPONENTS)),
}

@dataclass
class StateRecord:
    ts: float
    components: ComponentsDict
    entities: Dict[ET, List[EntityIndex]]

class State:
    # meta_components: List[MetaComponent] = []
    # components: Dict[CT, List[Optional[Component]]] = {
    #     CT.COMPONENT: [None] * MAX_ENTITIES,  # TODO
    #     CT.PHYSICS: [None] * MAX_ENTITIES,
    #     CT.ANIMATION: [None] * MAX_ENTITIES,
    #     CT.ACTION: [None] * MAX_ENTITIES,
    # }
    # components: Dict[CT, List[Optional[Component]]] = {
    #     ct: [None] * MAX_ENTITIES for ct in CT
    # }

    components: ComponentsDict = {
        C_COMPONENT: "",
        C_PHYSICS: (CPhysics(0, 0),) * MAX_COMPONENTS,
        C_ANIMATION: (CAnimation(""),) * MAX_COMPONENTS,
        C_ACTION: (CAction(),) * MAX_COMPONENTS,
        C_USER_CONTROLLER: (CUserController({}),) * MAX_COMPONENTS,
    }
    entities: Dict[ET, List[EntityIndex]] = {
        E_ENTITY: [],  # TODO
        E_PLAYER: [],
        E_NPC: [],
        E_THING: [],
    }

    _available_eis: Queue[EntityIndex] = Queue(maxsize=MAX_ENTITIES)
    for ei in range(0, MAX_ENTITIES - 1):
        _available_eis.put(EntityIndex(ei))

    t0 = time.perf_counter()

    @classmethod
    def new_ei(cls) -> EntityIndex:
        return cls._available_eis.get_nowait()


    @classmethod
    def new_entity(cls,
                   entity: ET,
                   *components: Component) -> EntityIndex:
        ei = cls.new_ei()
        for c in components:
            cls.components[c.tag][ei].update(c)

        cls.entities[entity].append(ei)
   
        return ei

    @classmethod
    def snapshot(cls) -> StateRecord:
        return StateRecord(
            time.perf_counter() - cls.t0,
            cls.components,
            cls.entities,
        )
                         

def process_state():
    pass


