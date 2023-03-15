# NOTICE: ALL INFORMATION CONTAINED IN THIS PROGRAM IS, AND REMAINS THE PROPERTY OF MITCHELL TORRENS. THE INTELLECTUAL
# AND TECHNICAL CONCEPTS CONTAINED HEREIN ARE PROTECTED BT COPYRIGHT LAW. IT IS STRICTLY FORBIDDEN TO SHARE, COPY,
# REPRODUCE, MODIFY, OR DISSEMINATE ANY INFORMATION INCLUDED IN THIS PROGRAM UNLESS PRIOR WRITTEN PERMISSION IS OBTAINED
# FROM MITCHELL TORRENS.
# Copyright (c) 2023, Mitchell Torrens. All rights reserved.

import curses
from typing import NamedTuple
# from dataclasses import dataclass

r_min = 12
r_max = 53
c_min = 72
c_max = 153

class WindowParams(NamedTuple):
    height: int
    width: int
    begin_y: int
    begin_x: int

w_game_params = WindowParams(
    height=65+2,
    width=225 + 2,
    begin_y=0,
    begin_x= 0,
)

w_hud_params = WindowParams(
    height=77,
    width=56,
    begin_y=0,
    begin_x=226,
)

w_console_params = WindowParams(
    height=11,
    width=108,
    begin_y=66,
    begin_x=0,
)

w_output_params = WindowParams(
    height=11,
    width=120,
    begin_y=66,
    begin_x=107,
)
