import os
import configparser
import sys
from PySide6 import QtWidgets, QtGui, QtCore  # Add QtCore import
from request import getOneRowWaiting, updateData, read_config
import socketio

# Custom QMenu subclass to keep the menu open after an action is clicked
class PersistentMenu(QtWidgets.QMenu):
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:  # Ensure QtCore.Qt is used
            action = self.activeAction()
            if action:
                action.triggered.emit()  # Emit the triggered signal of the action
            event.accept()

        else:
            super().mouseReleaseEvent(event)

# Your SystemTrayIcon class with modifications
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.menu = PersistentMenu(parent)
        self.setContextMenu(self.menu)
        self.activated.connect(self.onTrayIconActivated)
        self.sio = socketio.SimpleClient()
        self.sio.connect(read_config('URL'))

    def onTrayIconActivated(self):
        self.refreshMenu()

    def refreshMenu(self):
        self.menu.clear()
        self.menu.setStyleSheet("font-size: 24px")
        queueCustomer = getOneRowWaiting()

        if(len(queueCustomer.keys())==0):
            self.menu.addAction(f"No List")
        else:
            name, queueId, queueStatus = queueCustomer.get('name'), queueCustomer.get('queueId'), queueCustomer.get('queueStatus')
            self.menu.addAction(f"{name} {queueStatus}")
            next = self.menu.addAction(f'{ "Next" if queueStatus=="waiting" else "Finish"}')
            next.setIcon(QtGui.QIcon(f'assets/{ "next" if queueStatus=="waiting" else "finish"}.png'))
            next.triggered.connect(lambda n=name, q=queueId: self.sendRequest(n, q))
            if queueStatus=="ongoing":
                call = self.menu.addAction(f"Call {name}")
                call.setIcon(QtGui.QIcon("assets/notify.png"))
                call.triggered.connect(lambda n=name, q=queueId: self.alert(n,q))

        exit_ = self.menu.addAction("Exit")
        exit_.setIcon(QtGui.QIcon("assets/exit.png"))
        exit_.triggered.connect(lambda: sys.exit())

    def alert(self,name,queueId):
        print(f"Call {name} {queueId}")
        self.sio.emit('ping-request', {"name": name, "queueId": queueId})

    def sendRequest(self, name, queueId):
        message = updateData(queueId)
        self.refreshMenu()
        # notified("Update", message)

def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        tray_icon = SystemTrayIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "assets/systemTray.ico")))
        tray_icon.setVisible(True)
        tray_icon.showMessage('Welcome', read_config('CASHIER_NAME'))
        sys.exit(app.exec())
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
