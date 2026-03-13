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

import FreeCAD as App
import FreeCADGui as Gui
from FreeCAD import Spreadsheet

class cmdNewParams:

    def GetResources(self):

        return {
            "MenuText": "New Sheet",
            "ToolTip": "Create a new parameter spreadsheet."
        }


    def Activated(self):

        doc = App.ActiveDocument
        spreadsheet = doc.addObject("Spreadsheet::Sheet", "args")
        doc.recompute()
        Gui.Selection.addSelection(spreadsheet)
        Gui.ActiveDocument.setEdit(spreadsheet)


    def IsActive(self):

        return App.ActiveDocument is not None


Gui.addCommand("cmdNewParams", cmdNewParams())