import os
import sys
from PySide6 import QtWidgets, QtGui
from request import getData, updateData

def notified(status,message):
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon.png"), w)
    tray_icon.show()
    tray_icon.showMessage(status, message)
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip('Tooltip')

        menu = QtWidgets.QMenu(parent)
        # get = getData()
        # for item in get:
        #     name, queueId = item.get('name'), item.get('queueId')
        #     open_app = menu.addAction(f"{name} {queueId}")
        #     open_app.triggered.connect(lambda n=name, q=queueId: self.sendRequest(n, q))
        #     open_app.hovered.connect(lambda: self.setHoverIcon(open_app, "icon.png"))
        exit_ = menu.addAction("Exit")
        exit_.setIcon(QtGui.QIcon("exit.png"))
        exit_.triggered.connect(lambda: sys.exit())

        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self,reason):
        print('clicked')
    def setHoverIcon(self, action, hover_icon_path):
        action.setIcon(QtGui.QIcon(hover_icon_path))

    def sendRequest(self, name, queueId):
        print(f"Opening Notepad for {name} with Queue ID {queueId}")
        message = updateData(queueId)
        notified("Update", message)
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon.png"), w)
    tray_icon.show()
    tray_icon.showMessage('Title', 'Description')
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
