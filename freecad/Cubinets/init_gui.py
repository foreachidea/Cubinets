# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

import os
import FreeCAD as App
import FreeCADGui as Gui

from .Commands import cmdNewParams , cmdAssemble , cmdSettings , cmdCutList
from .Misc import asIcon


Gui.addCommand('cmdNewParams',cmdNewParams())
Gui.addCommand('cmdAssemble',cmdAssemble())
Gui.addCommand('cmdSettings',cmdSettings())
Gui.addCommand('cmdCutList',cmdCutList())


class CubinetsWorkbench(Gui.Workbench):

    MenuText = "Cubinets"
    ToolTip = "Visualise cabinet assemblies using Parametric Templates"
    Icon = asIcon('Addon')

    def Initialize(self):

        # hiding settings for demo; settings must be reviewed
        self.list = ["cmdNewParams", "cmdAssemble", "cmdCutList"]
        self.appendToolbar("Cubinets", self.list) # creates a new toolbar with your commands
        self.appendMenu("Cubinets", self.list) # creates a new menu


    def Activated(self):

        pass


    def Deactivated(self):

        pass


    def GetClassName(self):
        
        return "Gui::PythonWorkbench"


Gui.addWorkbench(CubinetsWorkbench())
