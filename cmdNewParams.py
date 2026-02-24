import FreeCAD as App
import FreeCADGui as Gui
import Spreadsheet

class cmdNewParams:

    def GetResources(self):
        return {
            "MenuText": "New Parameter Sheet",
            "ToolTip": "Create new parameter spreadsheet.",
            "Pixmap": ""
        }

    def Activated(self):

        doc = App.activeDocument()
        spreadsheet = doc.addObject("Spreadsheet::Sheet", "params")
        doc.recompute()
        Gui.Selection.addSelection(spreadsheet)
        Gui.ActiveDocument.setEdit(spreadsheet)

    def IsActive(self):
        return App.ActiveDocument is not None

Gui.addCommand("cmdNewParams", cmdNewParams())