from tempfile import NamedTemporaryFile
import os

from sublime_plugin import TextCommand
from .utils.error_handler import catch_errors
from .utils.mixins import NimLimeMixin
from .utils.idetools import Idetools


class GotodefCommand(TextCommand, NimLimeMixin):

    @catch_errors
    def run(self, edit):
        filename = self.view.file_name()
        sels = self.view.sel()

        if filename is None or not filename.endswith(".nim"):
            return

        for sel in sels:
            pos = self.view.rowcol(sel.begin())
            line = pos[0] + 1
            col = pos[1]

            Idetools.lookup(self, True, filename, line, col)