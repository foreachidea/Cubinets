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

from spreadsheet.Row import Row
from spreadsheet.Column import Column
from spreadsheet.Cell import Cell
from spreadsheet.Address import Address

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