# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from FreeCAD import Gui

from .Workbench import CubinetsWorkbench
from .Commands import cmdNewArgs , cmdAssemble , cmdSettings , cmdCutList


Gui.addCommand('Cubinets_Assemble',cmdAssemble())
Gui.addCommand('Cubinets_Settings',cmdSettings())
Gui.addCommand('Cubinets_CutList',cmdCutList())
Gui.addCommand('Cubinets_NewArgs',cmdNewArgs())

Gui.addWorkbench(CubinetsWorkbench())
