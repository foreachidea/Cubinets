# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from FreeCAD import Console , Gui , activeDocument

from ..Spreadsheet import Spreadsheet
from ..Document import Document

class cmdAssemble:

    def GetResources(self):
        return {
            "MenuText": "Assemble",
            "ToolTip": "Produce an assembly of cabinets using parameters from a selected spreadsheet."
        }


    def Activated(self):

        selections = Gui.Selection.getSelection()

        if not selections:

            Console.PrintError("[ ]]] Cubinets: No spreadseet selected\n")
            return

        if len(selections) > 1:

            Console.PrintError("[ ]]] Cubinets: More than one object selected. Please select one spreadsheet.\n")
            return

        selection = selections[0]

        if selection.TypeId != "Spreadsheet::Sheet":

            Console.PrintError("[ ]]] Cubinets: Selected object is not a spreadsheet\n")
            return

        if selection is None:

            Console.PrintError("[ ]]] Cubinets: Assembly spreadsheet not found\n")
            return

        argSheet = Spreadsheet(selection)
        document = Document(activeDocument())
        document.assemble(argSheet)


    def IsActive(self):
        return not not activeDocument()
