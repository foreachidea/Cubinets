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

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore

class UI:

    @staticmethod
    def setActiveDocument(name):

        App.setActiveDocument(name)
        App.ActiveDocument = App.getDocument(name)

        Gui.setActiveDocument(name)
        Gui.ActiveDocument = Gui.getDocument(name)


    @staticmethod
    def focusInventorTab(name):

        gui_doc = Gui.getDocument(name)

        if not gui_doc:
            print(f"No GUI for document: {name}")
            return

        view = gui_doc.ActiveView
        if not view:
            print(f"No active 3D view for document: {name}")
            return

        # Get MDI area
        mw = Gui.getMainWindow()
        mdi = mw.centralWidget()

        # Look for the subwindow containing this view
        for sub in mdi.subWindowList():
            container = sub.widget()
            if not container:
                continue

            central = container.centralWidget()
            if not central:
                continue

            # Check stacked widget
            if central.metaObject().className() == "QStackedWidget":
                for i in range(central.count()):
                    page = central.widget(i)
                    if page is view:
                        mdi.setActiveSubWindow(sub)
                        sub.raise_()
                        sub.show()
                        #print(f"Focused document: {name}")
                        return

            # Direct view
            elif central is view:
                mdi.setActiveSubWindow(sub)
                sub.raise_()
                sub.show()
                #print(f"Focused document: {name}")
                return

        # fallback: raise the first MDI subwindow for this doc
        for sub in mdi.subWindowList():
            if name in sub.windowTitle():
                mdi.setActiveSubWindow(sub)
                sub.raise_()
                sub.show()
                #print(f"Focused document by window title fallback: {name}")
                return

        #print(f"Could not find MDI window for document: {name}")


    @staticmethod
    def setViewingAngleAntFitAll():

        view = Gui.ActiveDocument.ActiveView
        r = App.Base.Rotation(App.Base.Vector(0,1,0), 45) * App.Base.Rotation(App.Base.Vector(1,0,0), -35)

        view.viewIsometric()  # optional, to start from default iso
        view.setCameraType("Perspective")
        view.setCameraOrientation(r)
        
        QtCore.QTimer.singleShot(150, view.fitAll)