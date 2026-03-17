# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Cubinets addon.

import FreeCAD as App
from .Misc import Paths
from .Qt import QtWidgets

PARAM_PATH = "User parameter:BaseApp/Preferences/Mod/Cubinets"

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cabinet Workbench Settings")
        self.setMinimumWidth(420)

        self.params = App.ParamGet(PARAM_PATH)

        layout = QtWidgets.QVBoxLayout(self)

        # -------- Template folder --------
        folder_layout = QtWidgets.QHBoxLayout()

        self.folder_edit = QtWidgets.QLineEdit()
        self.folder_edit.setText(self.params.GetString("TemplateFolder",Paths['Templates']))

        browse_btn = QtWidgets.QPushButton("Browse…")
        # todo: check browse folder
        browse_btn.clicked.connect(self.browse_folder)

        folder_layout.addWidget(QtWidgets.QLabel("Template folder:"))
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(browse_btn)

        layout.addLayout(folder_layout)

        # -------- Cutlist settings --------
        # --- Radios ---

        plane = self.params.GetString("WorkingPlane", "xz")

        rb_xz = QtWidgets.QRadioButton("XZ (front)")
        rb_xy = QtWidgets.QRadioButton("XY (top)")
        #rb_yz = QtWidgets.QRadioButton("YZ (right)")

        self._map = {
            "xz": rb_xz,
            "xy": rb_xy,
            #"yz": rb_yz,
        }

        self._map.get(plane, rb_xz).setChecked(True)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(rb_xz)
        hbox.addWidget(rb_xy)
        #hbox.addWidget(rb_yz)

        group = QtWidgets.QGroupBox("Templates' Working Plane")
        group.setLayout(hbox)

        layout.addWidget(group)

        # checkbox
        self.sort_by_dimension_cb = QtWidgets.QCheckBox("Sort by dimension value (descending)")
            #In cutlist values will be sorted by size from max to min (eg.: 140 x 600 x 18 will be represented as 600 x 140 x 18). This may be usefull if your templates do not follow design convention."
        self.sort_by_dimension_cb.setChecked(
            self.params.GetBool("CutlistSortByDimension", False)
        )

        layout.addWidget(self.sort_by_dimension_cb)

        # checkbox
        self.group_by_thickness_cb = QtWidgets.QCheckBox(
            "Group cutlist by dimensions"
        )
        self.group_by_thickness_cb.setChecked(
            self.params.GetBool("CutlistGroupByThickness", True)
        )

        layout.addWidget(self.group_by_thickness_cb)

        # -------- Buttons --------
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def browse_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select template folder"
        )
        if folder:
            self.folder_edit.setText(folder)

    def get_plane(self):
        for plane, rb in self._map.items():
            if rb.isChecked():
                return plane
        return "xz"

    def accept(self):
        self.params.SetString("TemplateFolder", self.folder_edit.text())
        self.params.SetBool("CutlistGroupByThickness", self.group_by_thickness_cb.isChecked())
        self.params.SetBool("CutlistSortByDimension", self.sort_by_dimension_cb.isChecked())
        self.params.SetString("WorkingPlane", next(k for k, rb in self._map.items() if rb.isChecked()))
        super().accept()
