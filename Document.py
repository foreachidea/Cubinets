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
from Spreadsheet import Spreadsheet
from Template import Template
from spreadsheet import Row
from Freezer import Freezer
from UI import UI

class Document:

    def __init__(self, fc_doc):

        self._fc_doc = fc_doc

        self.__x = 0
        self.__y = 1000
        self.__z = 1000

        self.__unitCount = 0


    def assemble(self, argSheet):

        rowCount = argSheet.rowCount()

        if rowCount == 0:

                App.Console.PrintMessage("[ ]]] Cubinets: argument sheet has no instructions.\n")
                return

        with Freezer(profile = "geometry", steps = rowCount + 1, cancel=False) as guiFreezer:

            # todo: fix: status bar must be drawn on show
            # update must only be used in the end of the cycle
            # it is used here to draw the status bar. dirty, but better this way for demo. and staus update percentage shown prematurely 
            guiFreezer.update(self.__unitCount, f"Loading assets...")

            for name, *arguments in argSheet.rows():
            
                match name:

                    case 'void':

                        # todo: check if arguments[0] is valid
                        self.__x += arguments[0]
                        #document.setPosition('x', arguments)

                    case None:

                        self.__x = 0
                        self.__y = 0
                        #document.setPosition('z', arguments)

                    case _:

                        template = Template(name, arguments)
                        objs = template.extractVisibleCubes()
                        self.addObjects(name, objs)

                        width = arguments[0]
                        if width is None:
                            width = sheet.get("B1")
                            if width is None:
                                width = 0
                            else:
                                try:
                                    width = float(width)
                                except Exception as e:
                                    App.Console.PrintError(f"[ ] Cubinets: Invalid numeric value in B1: \"{width}\"; Unit width expected. \n")
                                    raise

                        self.__x += width
                        self.__unitCount += 1

                        # todo:
                        #cubinet = template.getCubinet()
                        #document.addCubinet(cubinet)
                        
                        # todo: make this automatic
                        template.destroy()

                guiFreezer.update(self.__unitCount, f"Creating unit {self.__unitCount}")

        App.Console.PrintMessage("[ ]]] Cubinets: assembly complete!\n")

        UI.setActiveDocument(self._fc_doc.Name)
        UI.focusInventorTab(self._fc_doc.Name)
        UI.setViewingAngleAntFitAll()


    def addObjects(self, name, objs):

        group = self._fc_doc.getObject("BakedParts") or self._fc_doc.addObject("App::DocumentObjectGroup")
        group.Label = f"{self.__unitCount:02d}_{name}"

        for i, (shape, placement, label) in enumerate(objs):

            baked = self._fc_doc.addObject("Part::Box")
            
            shape.Placement = App.Placement()

            bbox = shape.BoundBox
            baked.Length = bbox.XLength
            baked.Width  = bbox.YLength
            baked.Height = bbox.ZLength
            baked.Placement = App.Placement(
                placement.Base + App.Vector(self.__x, self.__y, self.__z),
                placement.Rotation
            )
            baked.Label = f"{self.__unitCount:02d}_{label}"
            group.addObject(baked)


    def addCubinet(self, name, arguments):

        pass


    def addVoid(self, width):

        pass


    def setPosition(self, axis, arguments):

        pass