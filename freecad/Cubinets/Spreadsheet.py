# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from .spreadsheet import Address , Column , Cell , Row


class Spreadsheet:

    def __init__(self, fc_sheet):

        self._fc_sheet = fc_sheet
    

    def row(self, index: int) -> 'Row':

        return Row(self, index)


    def rows(self, start = 1):

        for i in range(start, self.rowCount() + 1):

            yield self.row(i)
    

    def column(self, label: str) -> 'Column':

        return Column(self, label)


    def cell(self, address: str) -> 'Cell':

        return Cell(self, address)
        

    def rowCount(self):

        usedRange = self._fc_sheet.getUsedRange()

        if not usedRange:

            return 0

        lastCellAddress = usedRange[1]
        index = int(''.join(filter(str.isdigit, lastCellAddress)))

        return index


    def columnCount(self):

        usedRange = self._fc_sheet.getUsedRange()
        
        if not usedRange:

            return 0

        lastCellAddress = usedRange[1]

        label = Address.extractLabel(lastCellAddress)
        index = Address.labelToIndex(label)

        return index