import FreeCADGui as Gui

class CubinetsWorkbench(Gui.Workbench):
    MenuText = "Cubinets"
    ToolTip = "Assemble cabinets from spreadsheet templates"
    Icon = ""

    def Initialize(self):
        import cmdScan, cmdAssemble, cmdCutList, cmdSettings

        # hiding settings for demo; settings must be reviewed
        #self.list = ["cmdAssemble", "cmdCutList", "cmdSettings"]
        self.list = ["cmdAssemble", "cmdCutList"]
        self.appendToolbar("My Commands", self.list) # creates a new toolbar with your commands
        self.appendMenu("My New Menu", self.list) # creates a new menu

    def Activated(self):
        pass

    def Deactivated(self):
        pass

    def GetClassName(self):
        return "Gui::PythonWorkbench"

Gui.addWorkbench(CubinetsWorkbench())
