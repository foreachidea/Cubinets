# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

import freecad.Cubinets as module
from importlib.resources import as_file , files


resources = files(module) / 'Resources'

icons = resources / 'Icons'


def asIcon ( name : str ):

    file = name + '.svg'

    icon = icons / file

    with as_file(icon) as path:
        return str( path )