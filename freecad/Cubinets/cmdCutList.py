# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

import FreeCAD as App
import FreeCADGui as Gui
import os
from collections import defaultdict

class cmdCutList:

    def GetResources(self):
        return {
            "MenuText": "Cut List",
            "ToolTip": "Produce a list of parts, group by dimensions."
        }

    def Activated(self):
        DOC = App.ActiveDocument

        # --- Step 1: Create or get Spreadsheet ---
        '''
        sheet_name = "Cut List"
        ss = DOC.getObject(sheet_name)
        if ss is None:
            ss = DOC.addObject("Spreadsheet::Sheet", sheet_name)
        ss.clearAll()  # remove old data
        '''
        ss = DOC.addObject("Spreadsheet::Sheet", "cut list")
        # todo: if file exsists, confirm overwrite

        '''
        # --- Step 2: Prepare header row ---
        headers = ["Qty", "Section", "Depth"]
        for col, h in enumerate(headers):
            ss.set(f"{chr(65+col)}1", h)

        # --- Step 3: Collect parts (ignore compounds) ---
        parts = defaultdict(int)

        for obj in DOC.Objects:
            # --- Collect geometry-bearing objects ---
            if not (
                obj.isDerivedFrom("Part::Feature")
                or obj.isDerivedFrom("PartDesign::Feature")
            ):
                continue

            # Bounding box dimensions
            bb = obj.Shape.BoundBox
            dims = sorted([bb.XLength, bb.YLength, bb.ZLength])
            width = round(dims[1], 3)
            height = round(dims[2], 3)
            depth = round(dims[0], 3)

            key = (width, height, depth)
            parts[key] += 1

        # --- Step 4: Write to spreadsheet ---
        row = 2
        for (width, height, depth), qty in sorted(parts.items(), key=lambda x: x[0][2]):  # sort by depth
            section = f"{width} x {height}"
            ss.set(f"A{row}", str(qty))
            ss.set(f"B{row}", section)
            ss.set(f"C{row}", str(depth))
            row += 1
        
        DOC.recompute()
        print(f"Cut list written to spreadsheet '{sheet_name}'")
        '''

        headers = ["Width", "Height", "Qty", "Thickness"]
        for col, h in enumerate(headers):
            ss.set(f"{chr(65+col)}1", h)

        # First row bold/right aligned
        '''
        for col in range(1, len(headers) + 1):
            addr = ss.getCellAddress("A1")     # get an App::CellAddress for A1
            cell = ss.getCell(addr)            # get the cell object
            cell.setStyle({"Bold", "AlignRight"})  # set bold + right align
            ss.execute()
        '''

        parts = defaultdict(int)

        AXIS_MAP = {
            "xz": (0, 2, 1),
            "xy": (0, 1, 2),
            #"yz": (2, 0, 1),
        }
        
        params = App.ParamGet("User parameter:BaseApp/Mod/Cubinets")
        plane = params.GetString("WorkingPlane", "xy")
        i_w, i_h, i_d = AXIS_MAP[plane]
        sort = params.GetBool("CutlistSortByDimension", False)
        group = params.GetBool("CutlistGroupByThickness", True)

        row = 2

        for obj in DOC.Objects:
            # --- Collect geometry-bearing objects ---
            if not (
                obj.isDerivedFrom("Part::Feature")
                or obj.isDerivedFrom("PartDesign::Feature")
            ):
                continue

            ogPlacement = obj.Placement
            obj.Placement = App.Placement()

            # Bounding box dimensions
            bb = obj.Shape.BoundBox

            obj.Placement = ogPlacement

            dims = [bb.XLength, bb.YLength, bb.ZLength]
            
            if sort:
                dims = sorted(dims, reverse=True)
                width = round(dims[0], 3)
                height = round(dims[1], 3)
                depth = round(dims[2], 3)
            else:
                width = round(dims[i_w], 3)
                height = round(dims[i_h], 3)
                depth = round(dims[i_d], 3)

            if group:
                key = (width, height, depth)
                parts[key] += 1
            else:
                ss.set(f"A{row}", str(width))
                ss.set(f"B{row}", str(height))
                ss.set(f"C{row}", "1")
                ss.set(f"D{row}", str(depth))
                row += 1

        if group:
            for (width, height, depth), qty in sorted(parts.items(), key=lambda x: x[0][2]):
                ss.set(f"A{row}", str(width))
                ss.set(f"B{row}", str(height))
                ss.set(f"C{row}", str(qty))
                ss.set(f"D{row}", str(depth))
                row += 1
        
        DOC.recompute()
        Gui.Selection.addSelection(ss)
        Gui.ActiveDocument.setEdit(ss)
        #print(f"Cut list written to spreadsheet '{sheet_name}'")


    def IsActive(self):
        return App.ActiveDocument is not None

Gui.addCommand("cmdCutList", cmdCutList())