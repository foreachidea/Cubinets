# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from FreeCAD import Gui

from .Commands import cmdNewParams , cmdAssemble , cmdSettings , cmdCutList
from .Misc import asIcon


Gui.addCommand('Cubinets_Assemble',cmdAssemble())
Gui.addCommand('Cubinets_Settings',cmdSettings())
Gui.addCommand('Cubinets_CutList',cmdCutList())
Gui.addCommand('Cubinets_Sheet',cmdNewParams())


class CubinetsWorkbench ( Gui.Workbench ):

    MenuText = 'Cubinets'
    ToolTip = 'Visualise cabinet assemblies using parametric templates.'
    Icon = asIcon('Addon')

    def Initialize ( self ):
        
        list = [
            'Cubinets_Settings' , 
            'Cubinets_Assemble' , 
            'Cubinets_CutList' ,
            'Cubinets_Sheet'
        ]
        
        self.appendToolbar('Cubinets',list)
        self.appendMenu('Cubinets',list)


    def Activated ( self ):
        pass


    def Deactivated ( self ):
        pass


    def GetClassName ( self ):
        return 'Gui::PythonWorkbench'


Gui.addWorkbench(CubinetsWorkbench())
