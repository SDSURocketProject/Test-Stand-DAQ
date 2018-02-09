import sys
import time
import logging
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QWidget, QLabel, QLineEdit, QVBoxLayout, QMessageBox, QPushButton, QStackedWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon,QPixmap,QFont
from tabs import TabManager

class Client(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(325,40,1300,1000)
        self.title = 'Launch Control Client'
        self.setFixedSize(1225,950)

        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('pictures/icon.png'))
        #self.setFixedSize(1030, 800)

        self.client_settings = ClientSettings()

        self.table_widget = TabManager(self)
        self.setCentralWidget(self.table_widget)

        self.MenuBar()
        #self.ToolBar()
        self.show()

        """def ToolBar(self):

        # Sets up the tool bar found right below the Menu. Has usefull applications.
        # Not being used

        homeAction = QAction(QIcon('pictures/home.png'), 'Home', self)
        #homeAction.triggered.connect(self.close_application)

        launchAction = QAction(QIcon('pictures/rocket.png'), 'Launch Control', self)
        # launchAction.triggered.connect(self.close_application)

        exitAction = QAction(QIcon('pictures/exit.png'), 'Exit', self)
        exitAction.triggered.connect(self.close_app)

        settingAction = QAction(QIcon('pictures/settings.png'), 'Settings', self)
        settingAction.triggered.connect(self.client_settings.show)
        
        connectionAction = QAction(QIcon('pictures/connection.png'), 'Connections', self)
        # connectionAction.triggered.connect(self.close_application)

        graphAction = QAction(QIcon('pictures/graph.png'), 'Graphs', self)
        # graphAction.triggered.connect(self.close_application)


        self.toolBar = self.addToolBar("Launch Window")
        self.toolBar.addAction(homeAction)
        self.toolBar.addAction(launchAction)
        self.toolBar.addAction(graphAction)
        self.toolBar.addAction(connectionAction)
        self.toolBar.addAction(settingAction)
        self.toolBar.addAction(exitAction)"""

    def MenuBar(self):

        # Sets up File and About on top left of page. Most Functions are not completed yet.
 
        settingAction = QAction(QIcon('pictures/settings.png'), '&Settings', self)
        settingAction.setShortcut('Ctrl+S')
        settingAction.setStatusTip("Doesn't Work Right Now")
        settingAction.triggered.connect(self.client_settings.call_window)

        exitAction = QAction(QIcon('pictures/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(self.close_app)

        helpAction = QAction(QIcon('pictures/help.png'), '&Help', self)
        helpAction.setShortcut('Ctrl+H')
        helpAction.setStatusTip("Doesn't Wort Right Now")
        # helpAction.triggered.connect(QtWidgets.)

        aboutAction = QAction(QIcon('pictures/about.png'), '&About', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.setStatusTip("Doesn't Work Right Now")
        # aboutAction.triggered.connect(QtWidgets.)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        aboutMenu = menubar.addMenu('&About')
        fileMenu.addAction(settingAction)
        fileMenu.addAction(exitAction)
        aboutMenu.addAction(helpAction)
        aboutMenu.addAction(aboutAction)

    def close_app(self):
        # exits GUI
        #self.logTextBox.append(">  Exiting...{}".format(time.strftime("\t-           (%H:%M:%S)", time.localtime())))
        choice = QMessageBox.question(self, "Confirmation.", "Are you sure you want to exit?",
                                                QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("System Closed")
            logger.debug("Application Exited at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            sys.exit()
        else:
            pass
            #self.logTextBox.append("> Exit Stopped{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))


class ClientSettings(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'Client Settings'
        self.left = 50
        self.top = 50
        self.width = 500
        self.height = 500

        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('pictures/settings.png'))
        self.setFixedSize(500, 500)

        self.log_folder_label = QLabel('Log Folder:', self)
        self.log_folder_label.move(10,10)
        self.log_folder_field = QLineEdit(self)
        self.log_folder_field.move(10,30)

        self.time_folder_label = QLabel('Time:', self)
        self.time_folder_label.move(10,60)
        self.time_folder_field = QLineEdit(self)
        self.time_folder_field.move(10,80)


        self.settings_init()

    def call_window(self):
        #This functioned is called everytime the window is opened so that
        #settings init is called to reload whatever settings are saved in config
        self.settings_init()
        self.show()

    def settings_init(self):
        #Unfinished
        #Would load current setting from config
        self.log_folder_field.setText('log')
        self.time_folder_field.setText(str(10))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Client()
    sys.exit(app.exec_())
