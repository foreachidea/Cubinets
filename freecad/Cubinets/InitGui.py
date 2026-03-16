#   []]] Cubinets, Copyright (C) 2026, Vytautas Rimkevicius
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import FreeCAD as App
import FreeCADGui as Gui

class CubinetsWorkbench(Gui.Workbench):

    MenuText = "Cubinets"
    ToolTip = "Visualise cabinet assemblies using Parametric Templates"
    Icon = os.path.join(App.getUserAppDataDir(), 'Mod', 'Cubinets', 'freecad', 'Cubinets', "resources", "cubinets_icon.svg")

    def Initialize(self):
        
        import cmdNewParams, cmdAssemble, cmdCutList

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
