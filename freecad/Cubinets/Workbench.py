# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from FreeCAD import Gui, ParamGet

from .Misc import asIcon


class CubinetsWorkbench ( Gui.Workbench ):

    MenuText = 'Cubinets'
    ToolTip = 'Visualize cabinet assemblies using parametric templates.'
    Icon = asIcon('Addon')

    def Initialize ( self ):
        
        list = [
            #'Cubinets_Settings' , hidden for demo
            'Cubinets_NewSheet' ,
            'Cubinets_Assemble' , 
            'Cubinets_CutList'
        ]
        
        self.appendToolbar('Cubinets',list)
        self.appendMenu('Cubinets',list)

        # in dev environment show Hot Reload button
        # to run latest workbench code edition
        preferences = ParamGet("User parameter:BaseApp/Preferences/Mod/Cubinets")
        dev = preferences.GetBool("DevelopmentEnvironment", False)
        
        if dev:
            self.appendToolbar("Hot Reload", ["Cubinets_HotReload"])


    def Activated ( self ):
        pass


    def Deactivated ( self ):
        pass


    def GetClassName ( self ):
        return 'Gui::PythonWorkbench'
