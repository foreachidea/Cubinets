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

from .Address import Address
from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from Spreadsheet import Spreadsheet


class Column:
    
    def __init__(self, sheet: 'Spreadsheet', label: str):

        self._sheet = sheet
        self._label = label


    def values(self, values):

        for i, value in enumerate(values, start = 1):

            if value is not None:

                self.sheet._fc_sheet.set(f"{self._label}{i}", str(value))