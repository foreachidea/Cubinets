# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from .Type import Sheet

class Cell:

    _address : str
    _sheet : Sheet

    def __init__(self, sheet: Sheet, address: str):
        
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