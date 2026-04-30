# AI Editor - Copyright (C) 2026 Kalpit
#
# This file is part of AI Editor.
#
# AI Editor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AI Editor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AI Editor.  If not, see <https://www.gnu.org/licenses/>.
from version import __version__
from PySide6.QtWidgets import QApplication
import sys
from widget import Widget

app = QApplication(sys.argv)

widget = Widget()
widget.show()

app.exec()