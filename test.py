import os, configparser, sys
from PySide6 import QtWidgets, QtGui
from request import getOneRowWaiting, updateData
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
        self.currentQueueId = 0
        self.setToolTip('QMS SYSTEM TRAY')

        self.menu = QtWidgets.QMenu(parent)
        self.setContextMenu(self.menu)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        # if reason == QtWidgets.QSystemTrayIcon.Trigger:
        self.refreshMenu()

    def refreshMenu(self):
        # Clear the existing menu
        self.menu.clear()
        self.menu.setStyleSheet("font-size: 24px")
        # Add new items
        queueCustomer = getOneRowWaiting('payment')
        if(len(queueCustomer.keys())==0):
            self.menu.addAction(f"No List")
        else:
            name, queueId, queueStatus = queueCustomer.get('name'), queueCustomer.get('queueId'), queueCustomer.get('queueStatus')
            self.menu.addAction(f"{name} {queueStatus}")
            # open_app.triggered.connect(lambda n=name, q=queueId: self.sendRequest(n, q))
            # open_app.hovered.connect(lambda: self.setHoverIcon(open_app, "assets/logo.png"))
            # Add exit action back to the menu
            next = self.menu.addAction(f'{ "Next" if queueStatus=="waiting" else "Finish"}')
            next.setIcon(QtGui.QIcon(f'assets/{ "next" if queueStatus=="waiting" else "finish"}.png'))
            next.triggered.connect(lambda n=name, q=queueId: self.sendRequest(n, q))
                
        # self.menu.setStyleSheet(open("style.css", "r").read())
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
