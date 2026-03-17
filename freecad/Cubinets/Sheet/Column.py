# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from .Type import Sheet


class Column:

    _label : str
    _self : Sheet
    
    def __init__(self, sheet: Sheet, label: str):

        self._sheet = sheet
        self._label = label


    def values(self, values):

        sheet = self._sheet._fc_sheet

        for i, value in enumerate(values, start = 1):

            if not value :
                continue

            sheet.set(f"{self._label}{i}", str(value))