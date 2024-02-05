import os, configparser, sys
from PySide6 import QtWidgets, QtGui
from request import getData, updateData
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

def notified(status, message):
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("assets/logo.png"), w)
    tray_icon.show()
    tray_icon.showMessage(status, message)

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip('Tooltip')

        self.menu = QtWidgets.QMenu(parent)

        exit_ = self.menu.addAction("Exit")
        exit_.setIcon(QtGui.QIcon("exit.png"))
        exit_.triggered.connect(lambda: sys.exit())

        self.setContextMenu(self.menu)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.refreshMenu()

    def refreshMenu(self):
        # Clear the existing menu
        self.menu.clear()

        # Add new items
        get = getData()
        if(len(get) == 0):
            open_app = self.menu.addAction(f"Empty")
            open_app.triggered.connect(lambda n="Empty", q="0": self.sendRequest(n, q))
            # open_app.hovered.connect(lambda: self.setHoverIcon(open_app, "assets/logo.png"))
        else:
            for item in get:
                name, queueId, queueStatus = item.get('name'), item.get('queueId'), item.get('queueStatus')
                if queueStatus == 'ongoing':
                    open_app = self.menu.addAction(f"{name} {queueStatus}")
                else:
                    open_app = self.menu.addAction(f"{name}")
                open_app.triggered.connect(lambda n=name, q=queueId: self.sendRequest(n, q))
                    # open_app.hovered.connect(lambda: self.setHoverIcon(open_app, "assets/logo.png"))

        # Add exit action back to the menu
        exit_ = self.menu.addAction("Exit")
        exit_.setIcon(QtGui.QIcon("assets/exit.png"))
        exit_.triggered.connect(lambda: sys.exit())

    def setHoverIcon(self, action, hover_icon_path):
        action.setIcon(QtGui.QIcon(hover_icon_path))

    def sendRequest(self, name, queueId):
        message = updateData(queueId)
        notified("Update", message)

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("assets/logo.png"), w)
    tray_icon.show()
    tray_icon.showMessage('Welcome',config.get('Configuration', 'CASHIER_NAME'))
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
