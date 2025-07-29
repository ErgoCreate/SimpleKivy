# SPDX-License-Identifier: GPL-3.0-only
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 only.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# For commercial licensing options, please contact the author at: [miguel_nunez95@hotmail.com].

# __name__="SimpleKivy"

# from kivy.config import Config
# size=(800,600)
# exit_on_escape=False
# desktop=True
# resizable=True
# multitouch_emulation=False

# Config.set('kivy', 'desktop', int(desktop))
# Config.set('kivy', 'exit_on_escape', int(exit_on_escape))
# Config.set('graphics', 'resizable', int(resizable))
# Config.set('graphics', 'multisamples', 0)
# if not multitouch_emulation:
#     Config.set('input', 'mouse', 'mouse,disable_multitouch')
# if size[0]:
#     Config.set('graphics', 'width', size[0])
# if size[1]:
#     Config.set('graphics', 'height', size[1])

from kivy.logger import Logger
import os
Logger.info(f'SimpleKivy: Installed at "{os.path.abspath(__file__)}"')

# from .SimpleKivy import *

# from .SimpleKivy import __version__
# def __getattr__(name):
# 	import .SimpleKivy as _sk
# 	return getattr(_sk,name)