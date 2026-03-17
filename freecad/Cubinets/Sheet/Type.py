# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

from typing import TYPE_CHECKING , Protocol , Any

if TYPE_CHECKING:
    from .Cell import Cell


class Sheet ( Protocol ):

    _fc_sheet : Any

    def columnCount ( self ) -> int :
        ...

    def cell ( self , address : str ) -> 'Cell' :
        ...