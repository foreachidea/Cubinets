# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from .Address import Address
from .Type import Sheet


class Row:

    _sheet : Sheet
    _index : int

    def __init__(self, sheet: Sheet, index: int):

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