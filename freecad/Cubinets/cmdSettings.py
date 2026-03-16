# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

import FreeCADGui as Gui
from .SettingsDialog import SettingsDialog

class cmdSettings:
    def GetResources(self):
        return {
            "MenuText": "Settings",
            "ToolTip": "Cabinet Workbench settings"
        }

    def IsActive(self):
        return True

    def Activated(self):
        dlg = SettingsDialog(Gui.getMainWindow())
        dlg.exec_()

Gui.addCommand("cmdSettings", cmdSettings())
