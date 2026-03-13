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

import FreeCADGui as Gui
from SettingsDialog import SettingsDialog

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
