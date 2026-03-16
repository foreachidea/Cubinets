# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from typing import TYPE_CHECKING

if TYPE_CHECKING:

    from Spreadsheet import Spreadsheet

class Cell:

    def __init__(self, sheet: 'Spreadsheet', address: str):
        
        self._sheet = sheet
        self._address = address


    def value(self, default = None):

        try:

            value = self._sheet._fc_sheet.get(self._address)

        except (RuntimeError, ValueError):

            return default

        if value in (None, ''):

            return default

        return value