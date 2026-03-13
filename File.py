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