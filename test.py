import os
import sys
from PySide6 import QtWidgets, QtGui


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip('Tooltip')

        menu = QtWidgets.QMenu(parent)

        open_app = menu.addAction("Open Notepad")
        open_app.triggered.connect(self.open_notepad)
        open_app.hovered.connect(lambda: self.setHoverIcon(open_app, "icon.png"))

        exit_ = menu.addAction("Exit")
        exit_.setIcon(QtGui.QIcon("exit.png"))
        exit_.triggered.connect(lambda: sys.exit())

        self.setContextMenu(menu)


    def setHoverIcon(self, action, hover_icon_path):
        action.setIcon(QtGui.QIcon(hover_icon_path))

    def open_notepad(self):
        os.system('notepad')

    def open_calc(self):
        os.system('calc')


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon.png"), w)
    tray_icon.show()
    tray_icon.showMessage('Title', 'Description')
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
