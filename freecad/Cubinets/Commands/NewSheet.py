# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from FreeCAD import Gui , activeDocument


class cmdNewSheet:

    def GetResources(self):

        return {
            "MenuText": "New Sheet",
            "ToolTip": "Create a new spreadsheet."
        }


    def Activated(self):

        doc = activeDocument()
        spreadsheet = doc.addObject("Spreadsheet::Sheet", "spreadsheet")
        doc.recompute()
        Gui.Selection.addSelection(spreadsheet)
        Gui.ActiveDocument.setEdit(spreadsheet)


    def IsActive(self):
        return not not activeDocument()
