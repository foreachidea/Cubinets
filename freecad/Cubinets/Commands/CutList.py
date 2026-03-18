# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from collections import defaultdict
from FreeCAD import Console, Placement , ParamGet , Gui , activeDocument

class cmdCutList:

    def GetResources(self):

        return {
            "MenuText": "Cut List",
            "ToolTip": "Produce a list of parts, group by dimensions."
        }

    def Activated(self):

        doc = activeDocument()
        cutlist = doc.addObject("Spreadsheet::Sheet", "cut list")
        headers = ["Width", "Height", "Qty", "Thickness"]

        for column, header in enumerate(headers):

            cutlist.set(f"{chr(65 + column)}1", header)


        parts = defaultdict(int)

        AXIS_MAP = {
            "xz": (0, 2, 1),
            "xy": (0, 1, 2),
            #"yz": (2, 0, 1),
        }
        
        settings = ParamGet("User parameter:BaseApp/Preferences/Mod/Cubinets")
        plane = settings.GetString("WorkingPlane", "xy")
        i_w, i_h, i_d = AXIS_MAP[plane]
        sort = settings.GetBool("CutlistSortByDimension", False)
        group = settings.GetBool("CutlistGroupByThickness", True)

        row = 2

        for obj in doc.Objects:
            # --- Collect geometry-bearing objects ---
            if not (
                obj.isDerivedFrom("Part::Feature")
                or obj.isDerivedFrom("PartDesign::Feature")
            ):
                continue

            ogPlacement = obj.Placement
            obj.Placement = Placement()

            # Bounding box dimensions
            bb = obj.Shape.BoundBox

            obj.Placement = ogPlacement

            dimensions = [bb.XLength, bb.YLength, bb.ZLength]
            
            if sort:
                dimensions = sorted(dimensions, reverse=True)
                width = round(dimensions[0], 3)
                height = round(dimensions[1], 3)
                depth = round(dimensions[2], 3)
            else:
                width = round(dimensions[i_w], 3)
                height = round(dimensions[i_h], 3)
                depth = round(dimensions[i_d], 3)

            if group:
                key = (width, height, depth)
                parts[key] += 1
            else:
                cutlist.set(f"A{row}", str(width))
                cutlist.set(f"B{row}", str(height))
                cutlist.set(f"C{row}", "1")
                cutlist.set(f"D{row}", str(depth))
                row += 1

        if group:
            for (width, height, depth), qty in sorted(parts.items(), key=lambda x: x[0][2]):
                cutlist.set(f"A{row}", str(width))
                cutlist.set(f"B{row}", str(height))
                cutlist.set(f"C{row}", str(qty))
                cutlist.set(f"D{row}", str(depth))
                row += 1
        
        doc.recompute()
        Gui.Selection.addSelection(cutlist)
        Gui.ActiveDocument.setEdit(cutlist)
        
        Console.PrintMessage("[ ]]] Cubinets: cut list produced!\n")


    def IsActive(self):

        return not not activeDocument()
