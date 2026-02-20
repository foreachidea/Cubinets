import FreeCADGui as Gui
#from PySide2 import QtWidgets
#from PySide6 import QtWidgets
from SettingsDialog import SettingsDialog

class cmdSettings:
    def GetResources(self):
        return {
            "Pixmap": "",
            "MenuText": "Settings",
            "ToolTip": "Cabinet Workbench settings"
        }

    def IsActive(self):
        return True

    def Activated(self):
        dlg = SettingsDialog(Gui.getMainWindow())
        dlg.exec_()

Gui.addCommand("cmdSettings", cmdSettings())
