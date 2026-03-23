# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from FreeCAD import Console, ParamGet

import importlib
import sys


class cmdHotReload:
    def GetResources(self):

        return {
            "MenuText": "Hot Reload",
            "ToolTip": "Reload workbench to run the latest code edition."
        }


    def Activated(self):

        for name in list(sys.modules.keys()):

            if name.startswith("freecad.Cubinets") and not name.endswith("init_gui"):

                module = sys.modules[name]
                importlib.reload(module)
                
                Console.PrintMessage(f"[ ]]] Cubinets: {module} reloaded.\n")

        Console.PrintMessage("[ ]]] Cubinets: workbench reloaded.\n")


    def IsActive(self):

        preferences = ParamGet("User parameter:BaseApp/Preferences/Mod/Cubinets")
        dev = preferences.GetBool("DevelopmentEnvironment", False)

        return dev

