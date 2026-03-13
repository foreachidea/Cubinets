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
import os
import random
from collections import defaultdict
from Freezer import Freezer
from PySide import QtCore
import shutil
from Document import Document
from Spreadsheet import Spreadsheet

class cmdAssemble:

    def GetResources(self):
        return {
            "MenuText": "Assemble",
            "ToolTip": "Produce an assembly of cabinets using parameters from a selected spreadsheet."
        }


    def Activated(self):

        selections = App.Gui.Selection.getSelection()

        if not selections:

            App.Console.PrintError("[ ]]] Cubinets: No spreadseet selected\n")
            return

        if len(selections) > 1:

            App.Console.PrintError("[ ]]] Cubinets: More than one object selected. Please select one spreadsheet.\n")
            return

        selection = selections[0]

        if selection.TypeId != "Spreadsheet::Sheet":

            App.Console.PrintError("[ ]]] Cubinets: Selected object is not a spreadsheet\n")
            return

        if selection is None:

            App.Console.PrintError("[ ]]] Cubinets: Assembly spreadsheet not found\n")
            return

        argSheet = Spreadsheet(selection)
        document = Document(App.ActiveDocument)
        document.assemble(argSheet)


    def IsActive(self):

        return App.ActiveDocument is not None

Gui.addCommand("cmdAssemble", cmdAssemble())
