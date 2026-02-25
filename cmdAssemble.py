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
import os
import random
from collections import defaultdict
from Freezer import Freezer
from PySide2 import QtCore
import shutil

class cmdAssemble:

    def GetResources(self):
        return {
            "MenuText": "Assemble",
            "ToolTip": "Produce an assembly of cabinets using parameters from a selected spreadsheet.",
            "Pixmap": ""
        }

    def Activated(self):
        DOC = App.ActiveDocument
        sel = App.Gui.Selection.getSelection()

        if not sel:
            App.Console.PrintError("[ ] Cubinets: No spreadseet selected\n")
            return

        if len(sel) > 1:
            App.Console.PrintError("[ ] Cubinets: More than one object selected. Please select only one spreadsheet.\n")
            return

        ASM = sel[0]
        if ASM.TypeId != "Spreadsheet::Sheet":
            App.Console.PrintError("[ ] Cubinets: Selected object is not a spreadsheet\n")
            return

        if ASM is None:
            App.Console.PrintError("[ ] Cubinets: Assembly spreadsheet not found\n")
            return


        target_doc = App.ActiveDocument
        params = App.ParamGet("User parameter:BaseApp/Mod/Cubinets")
        
        TEMPLATE_DIR = params.GetString("TemplateFolder", os.path.join(App.getUserAppDataDir(), 'Mod', 'Cubinets', 'templates'))

        top_row_z = 2000.0
        top_row_y = 2000.0
        x = 0.0
        topRow = True
        row = 1
        empty_count = 0
        unit = 1

        def cell(addr):
            try:
                v = ASM.get(addr)
                return None if v == "" else v
            except:
                return None

        def find_solid(doc):
            for o in doc.Objects:
                if hasattr(o, "Shape") and not o.Shape.isNull():
                    return o
            return None
        '''
        def extract_final_objects(doc):
            objs = []

            for obj in doc.Objects:
                # PartDesign: one solid per Body
                if obj.TypeId == "PartDesign::Body":
                    if obj.Shape and not obj.Shape.isNull():
                        objs.append(obj)

                # Part / Shape-based objects
                elif hasattr(obj, "Shape"):
                    if obj.Shape and not obj.Shape.isNull():
                        objs.append(obj)

            return objs
        '''
        def is_visible(obj):
            try:
                return obj.ViewObject.Visibility
            except Exception:
                return False

        def extract_visible_cubes(doc):
            """
            Extract only visible Part::Box objects.
            Arrays are exploded into separate solids.

            Returns:
                List of tuples:
                (shape_copy, placement_copy, label)
            """

            objs = []

            for obj in doc.Objects:

                #App.Console.PrintMessage(f"Label: {obj.Label}, TypeId: {obj.TypeId}, Class: {type(obj)}\n")
                
                if not is_visible(obj):
                    continue
                
                # -------------------------------------------------
                # 1️⃣ Direct Part::Box objects
                # -------------------------------------------------
                if obj.TypeId == "Part::Box":

                    if obj.Shape and not obj.Shape.isNull():
                        objs.append(
                            (
                                obj.Shape.copy(),
                                obj.Placement.copy(),
                                obj.Label
                            )
                        )
                    continue

                # -------------------------------------------------
                # 2️⃣ Draft Arrays of Part::Box
                # -------------------------------------------------
                '''
                if obj.TypeId == "Draft::Array":

                    App.Console.PrintMessage(f"DRAFT::ARRAY FOUND!")
                    base = getattr(obj, "Base", None)

                    # Only process arrays whose base is Part::Box
                    if not base or base.TypeId != "Part::Box":
                        continue

                    if not obj.Shape or obj.Shape.isNull():
                        continue

                    solids = obj.Shape.Solids

                    App.Console.PrintMessage(f"  Number of solids in Shape.Solids: {len(solids)}")
                    for i, s in enumerate(solids, start=1):
                        App.Console.PrintMessage(f"    Solid {i}: BoundBox = {s.BoundBox}")

                    base_label = base.Label

                    for i, solid in enumerate(solids, start=1):

                        name = f"{base_label}_{i:03d}"

                        # Shape already contains placement baked in
                        objs.append(
                            (
                                solid.copy(),
                                App.Placement(),
                                name
                            )
                        )
                '''
                if obj.TypeId == "Part::FeaturePython" and hasattr(obj, "Base"):

                    base = getattr(obj, "Base", None)

                    # Only process arrays whose base is a Part::Box
                    if not base or base.TypeId != "Part::Box":
                        continue

                    if not obj.Shape or obj.Shape.isNull():
                        continue

                    solids = obj.Shape.Solids
                    base_label = base.Label

                    for i, solid in enumerate(solids, start=1):

                        placement = solid.Placement.copy()
                        name = f"{base_label}_{i:02d}"

                        # Shape already has baked placement
                        objs.append(
                            (
                                solid.copy(),
                                placement,
                                name
                            )
                        )

            return objs

        # todo: and the name is 'params'
        def find_sheet(doc):
            for o in doc.Objects:
                if o.TypeId == "Spreadsheet::Sheet":
                    return o
            return None

        '''Convert 0-based column index to letters: 0->A, 25->Z, 26->AA, ..., 701->ZZ
        def col_index_to_letter(col_index):
            letters = ""
            temp = col_index
            while True:
                letters = chr(65 + temp % 26) + letters
                temp = temp // 26 - 1
                if temp < 0:
                    break
            return letters
        '''
        '''Convert 1-based column index to letters: 1->A, 26->Z, 27->AA, ..., 702->ZZ'''
        def col_index_to_letter(col_index):
            letters = ""
            temp = col_index
            while temp > 0:
                temp -= 1
                letters = chr(65 + (temp % 26)) + letters
                temp = temp // 26
            return letters


        # UIFreezer test:
        def get_row_count(sheet):
            used = sheet.getUsedRange()
            if not used:
                return 0
            return int(''.join(filter(str.isdigit, used[1])))

        def get_column_count(sheet):
            used = sheet.getUsedRange()
            if not used:
                return 0

            # Get the column letters from the end cell
            end_cell = used[1]  # e.g., 'C5' or 'AA10'
            col_letters = ''.join(filter(str.isalpha, end_cell)).upper()

            if len(col_letters) == 1:       # A..Z
                return ord(col_letters) - ord('A') + 1
            elif len(col_letters) == 2:     # AA..ZZ
                return (ord(col_letters[0]) - ord('A') + 1) * 26 + (ord(col_letters[1]) - ord('A') + 1)
            else:
                raise ValueError(f"Column '{col_letters}' exceeds ZZ")

        row_count = get_row_count(ASM)        
        
        with Freezer(profile="geometry", steps=row_count, cancel=False) as guiFreezer:

            # todo: fix: status bar must be drawn on show
            # update must only be used in the end of the cycle
            # it is used here to draw the status bar. dirty, but better this way for demo. and staus update percentage shown prematurely 
            guiFreezer.update(unit, f"Creating box {unit}")

            while True:

                name = cell(f"A{row}")

                # ---- EMPTY ROW HANDLING ----
                if name is None:
                    empty_count += 1
                    if empty_count == 1:
                        topRow = False
                        x = 0.0
                        row += 1
                        continue
                    else:
                        break
                
                # ---- VOID ----
                # todo: consider renaming void to hollow.
                if name == "void":
                    void_width = cell(f"B{row}") or 1000
                    x += void_width
                    row += 1
                    continue
                
                # ---- LOAD TEMPLATE ----
                path = os.path.join(TEMPLATE_DIR, f"{name}.FCStd")

                if not os.path.exists(path):
                    App.Console.PrintError(f"[ ] Cubinets: Template: {name} not found.\n")
                    row += 1
                    continue


                temp_opened = None
                dest = None
                temp_path = os.path.normcase(os.path.normpath(os.path.abspath(path)))
                
                for opened_doc in App.listDocuments().values():
                    if not opened_doc.FileName:
                        continue  # skip unsaved docs

                    opened_doc_path = os.path.normcase(os.path.normpath(opened_doc.FileName))

                    if opened_doc_path == temp_path:
                        temp_opened = opened_doc
                        break
                
                if temp_opened:
                #if filename in App.listDocuments().values():

                    # fix: firslty always find and copy over the sheet. geometry might get capricious without it.

                    byte_string = random.randbytes(8)
                    rand_hex = byte_string.hex()
                    '''
                    #opened_doc = App.getDocument(name)
                    tpl = App.newDocument(name + "_" + rand_hex)

                    #for obj in opened_doc.Objects:
                    for obj in temp_opened.Objects:
                        if obj.TypeId == "Spreadsheet::Sheet":
                            copy_obj = tpl.copyObject(obj, False)
                            for r in range(1, get_row_count(obj) + 1):
                                for c in range(1, get_column_count(obj) + 1):
                                    cell_addr = f"{col_index_to_letter(c)}{r}"
                                    try:
                                        val = obj.get(cell_addr)
                                    except AttributeError:
                                        continue
                                    if val not in (None, ""):
                                        copy_obj.set(cell_addr, str(val))
                                        try:
                                            alias = obj.getAlias(cell_addr)  # copy alias if exists
                                            if alias:
                                                copy_obj.setAlias(cell_addr, alias)
                                        except AttributeError:
                                            pass
                        elif obj.TypeId == "Part::Box":
                            copy_obj = tpl.copyObject(obj, False)
                            copy_obj.Label = obj.Label
                        elif obj.TypeId == "Part::FeaturePython":
                            copy_obj = tpl.copyObject(obj, False)
                            copy_obj.Label = obj.Label

                    tpl.recompute()                                 
                    '''
                    dest = os.path.normcase(os.path.normpath(App.getTempPath() + f"{rand_hex}_" + os.path.basename(opened_doc.FileName)))
                    
                    shutil.copy(opened_doc_path, dest, follow_symlinks=True)
                    tpl = App.openDocument(dest, hidden=True)
                else:
                    tpl = App.openDocument(path, hidden=True)

                sheet = find_sheet(tpl)

                width = cell(f"B{row}")

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


                # 1️⃣ Set all parameters in spreadsheet
                # try doesnt do anything
                #try:
                values = [cell(f"{col_index_to_letter(col)}{row}") for col in range(2, 702 + 1)]
                #except:
                #    row += 1
                #    continue

                # bug! should this be done to temp doc and not DOC :)
                DOC.openTransaction("Write parameters") # prevent recomputing

                for i, v in enumerate(values):
                    if v is not None:  
                        sheet.set(f"B{i+1}", str(v))

                DOC.commitTransaction()

                # 2️⃣ Recompute the template completely
                # Force all objects to recompute
                tpl.recompute()
                for obj in tpl.Objects:
                    if hasattr(obj, "recompute"):
                        obj.recompute()

                # 3️⃣ Extract shapes + placements AFTER recompute
                '''
                extracted = [
                    (obj.Shape.copy(), obj.Placement.copy(), obj.Label)
                    for obj in extract_final_objects(tpl)
                ]
                '''
                extracted = extract_visible_cubes(tpl)

                App.closeDocument(tpl.Name)

                if dest is not None and os.path.exists(dest):
                    os.remove(dest)

                # 4️⃣ Bake into target document
                #target_doc = App.ActiveDocument
                group = target_doc.getObject("BakedParts") or target_doc.addObject("App::DocumentObjectGroup")
                group.Label = f"{unit:02d}_{name}"

                
                
                y = top_row_y if topRow else 0.0
                z = top_row_z if topRow else 0.0
                plane = params.GetString("WorkingPlane", "xy")
                if plane == "xy":
                    z = 0
                else:
                    y = 0

                for i, (shape, placement, label) in enumerate(extracted):
                    baked = target_doc.addObject("Part::Feature")
                    baked.Shape = shape
                    baked.Placement = App.Placement(
                        placement.Base + App.Vector(x, y, z),
                        placement.Rotation
                    )
                    baked.Label = f"{unit:02d}_{label}"
                    group.addObject(baked)

                x += width
                row += 1
                unit += 1

                guiFreezer.update(unit, f"Creating box {unit}")

        App.Console.PrintMessage("[ ] Cubinets: Cabinet assembly complete!\n")


        DOC.recompute()

        App.setActiveDocument(DOC.Name)
        App.ActiveDocument = App.getDocument(DOC.Name)
        Gui.ActiveDocument = Gui.getDocument(DOC.Name)
        Gui.setActiveDocument(DOC.Name)
        
        def focus_document_view(doc_name):
            """
            Focus the 3D view of the given document in FreeCAD.
            Safe for modern builds without activateDocument.
            """
            gui_doc = Gui.getDocument(doc_name)
            if not gui_doc:
                print(f"No GUI for document: {doc_name}")
                return

            view = gui_doc.ActiveView
            if not view:
                print(f"No active 3D view for document: {doc_name}")
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
                            #print(f"Focused document: {doc_name}")
                            return

                # Direct view
                elif central is view:
                    mdi.setActiveSubWindow(sub)
                    sub.raise_()
                    sub.show()
                    #print(f"Focused document: {doc_name}")
                    return

            # fallback: raise the first MDI subwindow for this doc
            for sub in mdi.subWindowList():
                if doc_name in sub.windowTitle():
                    mdi.setActiveSubWindow(sub)
                    sub.raise_()
                    sub.show()
                    #print(f"Focused document by window title fallback: {doc_name}")
                    return

            #print(f"Could not find MDI window for document: {doc_name}")

        focus_document_view(DOC.Name)
        
        
        view = Gui.ActiveDocument.ActiveView
        r = App.Base.Rotation(App.Base.Vector(0,1,0), 45) * App.Base.Rotation(App.Base.Vector(1,0,0), -35)
        view.viewIsometric()  # optional, to start from default iso
        view.setCameraType("Perspective")
        view.setCameraOrientation(r)
        
        QtCore.QTimer.singleShot(150, view.fitAll)

    def IsActive(self):
        return App.ActiveDocument is not None

Gui.addCommand("cmdAssemble", cmdAssemble())
