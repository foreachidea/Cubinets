# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon for FreeCAD.

import FreeCAD as App
import os
import shutil

class File:

    def __init__(self, path):

        self._path = path
        self._isClone = False


    def open(self):

        if self.isOpen():
            
            # clone template file if it's opened by user  
            self._path = self.clone(self._path)
            self._isClone = True

        doc = App.openDocument(self._path, hidden=True)

        return doc


    def close(self, doc):

        App.closeDocument(doc.Name)

    
    def destroy(self):

        if self._isClone and self._path is not None and os.path.exists(self._path):

            os.remove(path)


    def isOpen(self):

        # todo: review results of these operations, are they required at all? can this be done in getPath?
        path = os.path.abspath(self._path)
        path = os.path.normpath(path)
        path = os.path.normcase(path)

        for openedTemplate in App.listDocuments().values():

            if not openedTemplate.FileName:

                continue  # skip unsaved docs

            openedTemplatePath = os.path.normpath(openedTemplate.FileName)
            openedTemplatePath = os.path.normcase(openedTemplatePath)

            if openedTemplatePath == path:

                #return openedTemplate
                return True

        return False


    def randomHex(self, bytes = 8):

        byteString = random.randbytes(bytes)
        randomHex = byteString.hex()

        return randomHex


    def clone(self):

        randPrefix = randomHex()
        dest = App.getTempPath() + f"{randPrefix}_" + os.path.basename(self._path)
        dest = os.path.normpath(dest)
        dest = os.path.normcase(dest)
                    
        shutil.copy(path, dest, follow_symlinks=True)

        return dest