# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

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