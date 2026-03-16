# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon for FreeCAD.

from .Address import Address
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from Spreadsheet import Spreadsheet


class Row:

    def __init__(self, sheet: 'Spreadsheet', index: int):

        self._sheet = sheet
        self._index = index


    def __iter__(self):

        yield from self.values()


    def values(self):

        values = []
        columnCount = self._sheet.columnCount()

        for i in range(1, columnCount + 1):

            label = Address.indexToLabel(i)
            address = f"{label}{self._index}"
            value = self._sheet.cell(address).value()
            values.append(value)
        
        return values