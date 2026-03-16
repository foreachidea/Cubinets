# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

import FreeCAD as App
import os
import shutil
from File import File

class Template:

    def __init__(self, name, args):

        self._name = name
        self._file = File(self.getPath(name))
        self._doc = None

        self.open()
        self.setParams(args)
        self.recompute()


    def open(self):

        self._doc = self._file.open()


    def setParams(self, args):

        params = self.findSheet()

        App.ActiveDocument.openTransaction("Write parameters") # prevent recomputing

        for i, arg in enumerate(args):

            if arg is not None:

                params.set(f"B{i+1}", str(arg))

        App.ActiveDocument.commitTransaction()


    def recompute(self):

        # Force all objects to recompute
        self._doc.recompute()

        for obj in self._doc.Objects:

            if hasattr(obj, "recompute"):

                obj.recompute()


    def __enter__(self):

        pass

    # todo: investigate best method to clean up; in a mean time will clean up manually
    '''
    # this is only called if obj invoked using 'with', hence __del__ is used
    def __exit__(self, exc_type, exc_value, traceback):

        if self._isClone and self._path is not None and os.path.exists(self._path):

            os.remove(self._path)

    # __del__ called on garbage collection, which might not happen immediatly
    def __del__(self, exc_type, exc_value, traceback):

        if self._isClone and self._path is not None and os.path.exists(self._path):

            os.remove(self._path)
    '''

    def destroy(self):

        self._file.close(self._doc)
        self._file.destroy()
        
    
    def getPath(self, name):

        # todo: why dont these work bellow class?
        DEFAULT_TEMPLATE_DIR = os.path.join(App.getUserAppDataDir(), 'Mod', 'Cubinets', 'freecad', 'Cubinets', 'templates')
        TEMPLATE_DIR = App.ParamGet("User parameter:BaseApp/Mod/Cubinets").GetString("TemplateFolder", DEFAULT_TEMPLATE_DIR)

        path = os.path.join(TEMPLATE_DIR, f"{name}.FCStd")

        return path


    def findSolid(self):

        for obj in self._doc.Objects:

            if hasattr(obj, "Shape") and not obj.Shape.isNull():

                return obj

        return None


    def findSheet(self):

        for obj in self._doc.Objects:

            if obj.TypeId == "Spreadsheet::Sheet":

                return obj

        return None


    # todo: fix this mess;
    # todo: extractor should really extract Std_Body containing Part::Box and Part::FeaturePython, so user could manipulate further
    def extractVisibleCubes(self):

        def is_visible(obj):
            try:
                return obj.ViewObject.Visibility
            except Exception:
                return False

        objs = []

        for obj in self._doc.Objects:

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


    def getCubinet(self):

        pass