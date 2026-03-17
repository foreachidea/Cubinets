# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from FreeCAD import Base , Gui , setActiveDocument
from .Qt import QtWidgets , QtCore

class UI:

    @staticmethod
    def setActiveDocument(name):

        setActiveDocument(name)
        # App.ActiveDocument = App.getDocument(name)

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
        mdi : QtWidgets.QMdiArea = mw.centralWidget()

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

        view = Gui.activeView()

        r = Base.Rotation(Base.Vector(0,1,0), 45) * Base.Rotation(Base.Vector(1,0,0), -35)

        view.viewIsometric()  # optional, to start from default iso
        view.setCameraType("Perspective")
        view.setCameraOrientation(r)
        
        QtCore.QTimer.singleShot(150, view.fitAll)