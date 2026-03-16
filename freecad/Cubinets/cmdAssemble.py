# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon for FreeCAD.

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
