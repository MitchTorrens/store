# NOTICE: ALL INFORMATION CONTAINED IN THIS PROGRAM IS, AND REMAINS THE PROPERTY OF MITCHELL TORRENS. THE INTELLECTUAL
# AND TECHNICAL CONCEPTS CONTAINED HEREIN ARE PROTECTED BT COPYRIGHT LAW. IT IS STRICTLY FORBIDDEN TO SHARE, COPY,
# REPRODUCE, MODIFY, OR DISSEMINATE ANY INFORMATION INCLUDED IN THIS PROGRAM UNLESS PRIOR WRITTEN PERMISSION IS OBTAINED
# FROM MITCHELL TORRENS.
# Copyright (c) 2023, Mitchell Torrens. All rights reserved.

"""TODO."""

import logging
import struct
import itertools
from functools import cached_property
from threading import Lock
from typing import Final, Literal, Dict, Callable, Iterator
from dataclasses import dataclass, field, asdict

log = logging.getLogger(__name__)
debug_log = logging.getLogger(f"debug.{__name__}")

# _SIZE_LOOKUP: Final = {
#     "c": 1,
#     "b": 1,
#     "B": 1,
#     "?": 1,
#     "h": 2,
#     "H": 2,
#     "i": 4,
#     "I": 4,
#     "l": 4,
#     "L": 4,
#     "q": 8,
#     "Q": 8,
#     "e": 2,
#     "f": 4,
#     "d": 8,
# }

NUM_ENTITIES: Final = 1024
NUM_COMPONENTS: Final = NUM_ENTITIES

EntityIndex = int
ComponentIndex = int

X_QUIT: Final = 113
X_UP: Final = 119
X_LEFT: Final = 97
X_DOWN: Final = 115
X_RIGHT: Final = 100

ENTITY_ACTIONS: Final = (
    X_UP,
    X_LEFT,
    X_DOWN,
    X_RIGHT,
)


@dataclass(frozen=True)
class DataView:
    item: struct.Struct
    num_items: int
    offset: int

    @cached_property
    def format(self) -> str:
        return f"{self.item.format[0]}{''.join(self.item.format[1:]for _ in range(self.num_items))}"

    @cached_property
    def size(self) -> int:
        return self.item.size * self.num_items
    
    @cached_property
    def item_size(self) -> int:
        return self.item.size

    @cached_property
    def item_format(self) -> int:
        return self.item.format
    
    def component_offset(self, ei: EntityIndex) -> int:
        return self.offset + self.item_size * ei


free_component_index = itertools.count()

LOCATION: Final[ComponentIndex] = free_component_index.__next__()
ANIMATION: Final[ComponentIndex] = free_component_index.__next__()
ACTIONS: Final[ComponentIndex] = free_component_index.__next__()

C_LOCATION: Final = DataView(struct.Struct(">?hh"), NUM_COMPONENTS, 0)
C_ANIMATION: Final = DataView(struct.Struct(">?c"), NUM_COMPONENTS, C_LOCATION.size + C_LOCATION.offset)
C_ACTIONS: Final = DataView(struct.Struct(f">?{'?'*len(ENTITY_ACTIONS)}"), NUM_COMPONENTS, C_ANIMATION.size + C_ANIMATION.offset)


COMPONENT_VIEWS = (
    C_LOCATION,
    C_ANIMATION,
    C_ACTIONS,
)


def component_offsets(ei: EntityIndex) -> Iterator[int]:
    for v in range(len(COMPONENT_VIEWS)):
        yield COMPONENT_VIEWS[v].component_offset(ei)


@dataclass(frozen=True)
class Data:
    raw: bytearray

    def __str__(self):
        return self.raw.hex()


_DATA = Data(bytearray(sum(view.size for view in COMPONENT_VIEWS)))
DATA = memoryview(_DATA.raw)

D_LOCATION = memoryview(_DATA.raw[C_LOCATION.offset:C_LOCATION.size])
D_ANIMATION = memoryview(_DATA.raw[C_ANIMATION.offset:C_ANIMATION.size])
D_ACTIONS = memoryview(_DATA.raw[C_ACTIONS.offset:C_ACTIONS.size])


def log_schema(to_log: logging.Logger = debug_log):

    to_log.info("=== Components Schema ===")
    for ci, c in enumerate(COMPONENT_VIEWS):
        to_log.info(f"Component {ci}:")
        to_log.info(f"  item_format: '{c.item_format}'")
        to_log.info(f"  num_items:   {c.num_items}")
        to_log.info(f"  offset:      {c.offset}")
