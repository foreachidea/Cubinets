import FreeCAD as App
import FreeCADGui as Gui

from PySide import QtGui, QtCore


class Freezer:
    """
    UI/Document freeze controller.

    Profiles:
        - geometry
        - io
        - light

    Supports:
        - Nested usage (reference counted)
        - Modal progress dialog (UI locking)
        - Optional cancel
        - Auto transaction handling
        - Headless progress updates
        - Debug logging

    Example usage:

    # geometry
    with UIFreezer(profile="geometry", steps=100, cancel=False) as f:
        for i in range(100):
            obj = App.ActiveDocument.addObject("Part::Box", f"Box_{i}")
            obj.Length = 10
            f.update(i, f"Creating box {i}")

    # filescan
    with UIFreezer(profile="io", steps=len(files), cancel=True) as f:
        for i, path in enumerate(files):

            if f.cancel_requested():
                break

            scan_file(path)
            f.update(i, f"Scanning {path}")

    # light mode
    with UIFreezer(profile="light"):
        parse_spreadsheet()


    # nesting example
    files = ["a.step", "b.step", "c.step"]

        with UIFreezer(profile="geometry", steps=3) as outer:

            for i, file in enumerate(files):

                # Nested IO operation
                with UIFreezer(profile="io", steps=100, cancel=True) as inner:

                    for p in range(100):

                        if inner.cancel_requested():
                            return  # safely exits

                        # simulate scan
                        inner.update(p, f"Scanning {file} : {p}%")

                # Geometry creation after IO
                obj = App.ActiveDocument.addObject("Part::Box", f"Box_{i}")
                obj.Length = 10

                outer.update(i, f"Created object {i}")



    todo: investigate freeze gui update
    Gui.updateGui = False
    # do work
    Gui.updateGui = True

    """

    # --- Class-level depth tracking ---
    _depth = 0
    _active_instance = None

    # -------------------------------------------------------------
    # INITIALIZATION
    # -------------------------------------------------------------
    def __init__(self,
                 profile="geometry",
                 steps=None,
                 cancel=False,
                 transaction="auto",
                 custom=None,
                 debug=False):

        self.profile = profile
        self.steps = steps
        self.cancel = cancel
        self.transaction_mode = transaction
        self.custom = custom or {}
        self.debug = debug

        self.doc = App.ActiveDocument
        self.view = Gui.ActiveDocument.ActiveView if Gui.ActiveDocument else None
        self.mw = Gui.getMainWindow()

        self._progress = None
        self._transaction_opened = False
        # in current version  i believe recompute must be called explicitly...
        self._recompute_suspended = False
        self._view_frozen = False
        self._cursor_set = False

        self._configure_profile()

    # -------------------------------------------------------------
    # PROFILE CONFIGURATION
    # -------------------------------------------------------------
    def _configure_profile(self):
        """Set behavior based on profile."""
        base = {
            "cursor": True,
            "modal": False,
            "suspend_recompute": False,
            "freeze_view": False,
            "transaction": False
        }

        if self.profile == "geometry":
            base.update({
                "modal": True,
                "suspend_recompute": True,
                "freeze_view": True,
                "transaction": True
            })

        elif self.profile == "io":
            base.update({
                "modal": True
            })

        elif self.profile == "light":
            base.update({
                "modal": False
            })

        # Override with atomic custom settings
        base.update(self.custom)
        self.config = base

    # -------------------------------------------------------------
    # ENTER
    # -------------------------------------------------------------
    def __enter__(self):
        Freezer._depth += 1

        if self.debug:
            App.Console.PrintMessage(f"[Freezer] Enter '{self.profile}' depth={Freezer._depth}\n")

        # If nested, do nothing except allow status updates
        if Freezer._depth > 1:
            return self

        Freezer._active_instance = self

        try:
            self._apply_freeze()
        except Exception as e:
            App.Console.PrintError(f"[Freezer] Freeze error: {e}\n")

        return self

    # -------------------------------------------------------------
    # EXIT
    # -------------------------------------------------------------
    def __exit__(self, exc_type, exc_val, exc_tb):
        Freezer._depth -= 1

        if self.debug:
            App.Console.PrintMessage(
                f"[Freezer] Exit '{self.profile}' depth={Freezer._depth}\n"
            )

        # Only restore on outermost exit
        if Freezer._depth == 0:
            try:
                self._restore()
            except Exception as e:
                App.Console.PrintError(f"[Freezer] Restore error: {e}\n")

            Freezer._active_instance = None

        # Do not suppress exceptions
        return False

    # -------------------------------------------------------------
    # APPLY FREEZE
    # -------------------------------------------------------------
    def _apply_freeze(self):

        # Busy cursor
        if self.config["cursor"]:
            QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            self._cursor_set = True

        # Modal progress dialog (UI lock)
        if self.config["modal"]:
            maximum = self.steps if self.steps is not None else 0

            self._progress = QtGui.QProgressDialog(
                "Processing...",
                "Cancel" if self.cancel else None,
                0,
                maximum,
                self.mw
            )

            self._progress.setWindowModality(QtCore.Qt.WindowModal)
            self._progress.setMinimumDuration(0)
            self._progress.setValue(0)
            self._progress.show()

        # Suspend recompute
        #if self.config["suspend_recompute"] and self.doc:
        #    self.doc.suspendRecompute()
        #    self._recompute_suspended = True
        self._recompute_suspended = True

        # Freeze 3D view redraw
        if self.config["freeze_view"] and self.view:
            self.view.setUpdatesEnabled(False)
            self._view_frozen = True

        # Transaction handling
        # todo: check this logic, expand here
        if self.config["transaction"] and self.doc:
            if self.transaction_mode == "auto":
                # Only open if none active
                self.doc.openTransaction("Freezer Operation")
                self._transaction_opened = True
            elif self.transaction_mode is True:
                self.doc.openTransaction("Freezer Operation")
                self._transaction_opened = True

        QtGui.QApplication.processEvents()

    # -------------------------------------------------------------
    # RESTORE
    # -------------------------------------------------------------
    def _restore(self):

        # Resume recompute
        if self._recompute_suspended and self.doc:
            #self.doc.resumeRecompute()
            self.doc.recompute()

        # Restore view
        if self._view_frozen and self.view:
            self.view.setUpdatesEnabled(True)

        # Commit transaction
        if self._transaction_opened and self.doc:
            self.doc.commitTransaction()

        # Close progress dialog
        if self._progress:
            self._progress.close()
            self._progress = None

        # Restore cursor
        if self._cursor_set:
            QtGui.QApplication.restoreOverrideCursor()

        QtGui.QApplication.processEvents()

    # -------------------------------------------------------------
    # PUBLIC API
    # -------------------------------------------------------------
    def update(self, value=None, text=None):
        """
        Update progress safely.
        Can be called from headless supervision loop.
        """

        if Freezer._active_instance != self:
            return

        if self._progress:
            if value is not None:
                self._progress.setValue(value)
            if text:
                self._progress.setLabelText(text)

            QtGui.QApplication.processEvents()

    def set_status(self, text):
        if self._progress:
            self._progress.setLabelText(text)
            QtGui.QApplication.processEvents()

    def cancel_requested(self):
        if self._progress and self.cancel:
            return self._progress.wasCanceled()
        return False
