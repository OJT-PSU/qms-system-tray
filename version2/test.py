import os, configparser, sys
from PySide6 import QtWidgets, QtGui
from request import getOneRowWaiting, updateData

def read_config(key):
    config = configparser.ConfigParser()
    if getattr(sys, 'frozen', False):  # Check if running from PyInstaller bundle
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(__file__)  # Get the directory where the script is located

    config_file_path = os.path.join(exe_dir, 'config.ini')

    if os.path.exists(config_file_path):
        config.read(config_file_path)
        return config['Configuration'].get(key, None)
    else:

        raise FileNotFoundError("Config file config.ini not found.")

def notified(status, message):
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("logo.png"), w)
    tray_icon.show()
    tray_icon.showMessage(status, message)

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.currentQueueId = 0
        self.transactionType = ''
        self.setToolTip('QMS SYSTEM TRAY')

        self.menu = QtWidgets.QMenu(parent)
        self.setContextMenu(self.menu)
        self.activated.connect(self.onTrayIconActivated)
    
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
            next.setIcon(QtGui.QIcon(f'{ "next" if queueStatus=="waiting" else "finish"}.png'))
            next.triggered.connect(lambda n=name, q=queueId: self.sendRequest(n, q))
                
        exit_ = self.menu.addAction("Exit")
        exit_.setIcon(QtGui.QIcon("exit.png"))
        exit_.triggered.connect(lambda: sys.exit())

    def setHoverIcon(self, action, hover_icon_path):
        action.setIcon(QtGui.QIcon(hover_icon_path))

    def sendRequest(self, name, queueId):
        message = updateData(queueId)
        notified("Update", message)

def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        w = QtWidgets.QWidget()
        tray_icon = SystemTrayIcon(QtGui.QIcon(os.path.join(os.path.dirname(__file__), "systemTray.ico")), w)
        tray_icon.setVisible(True)
        tray_icon.showMessage('Welcome', read_config('CASHIER_NAME'))
        sys.exit(app.exec())
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()