import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QTextBrowser, QBoxLayout, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QObject, pyqtSignal


class RadioTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()


        self.serial_feed.append('Feature Not Yet Implemented')
        self.coms_status.append('Currently Testing Qt Signaling in this Text Browser, hit connect to test')


    def initUI(self):
        serial_feed_label = QLabel('Serial Feed')
        coms_status_label = QLabel('Status')

        self.serial_feed = QTextBrowser()
        self.coms_status = QTextBrowser()
        self.serial_options = SerialOptions()

        self.serial_options.connect_push.connect(self.connect_clicked_signal)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(serial_feed_label, 1, 0)
        grid.addWidget(self.serial_feed, 1, 1, 20, 24)

        grid.addWidget(self.serial_options, 1, 26, 20, 24)
        #grid.addWidget(self.serial_feed, tl_vertical_grid_pos, tl_hor_grid_pos, vertical_grid_length_min, hor_grid_width_min

        grid.addWidget(coms_status_label, 21, 0)
        grid.addWidget(self.coms_status, 21, 1, 20, 50)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()

    def connect_clicked_signal(self):
        self.coms_status.append("Connect Signaled Successfuly from Seperate Widget")








class SerialOptions(QWidget):
    connect_push = pyqtSignal()

    def __init__(self):
        super().__init__()


        main_box = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        self.setting_popup = SerialSettings()


        button_settings = QPushButton("Settings", self)
        button_connect = QPushButton("Connect", self)


        button_settings.clicked.connect(self.setting_popup.show)
        button_connect.clicked.connect(self.connect_push.emit)


        hbox1.addWidget(button_settings)
        hbox1.addWidget(button_connect)


        main_box.addLayout(hbox1)
        #main_box.addLayout(hbox2)

        self.setLayout(main_box)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.setting_popup.close()



class SerialSettings(QWidget):
    def __init__(self):
        super().__init__()

        self.title = 'Serial Settings'
        self.left = 50
        self.top = 50
        self.width = 300
        self.height = 500

        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('pictures/settings.png'))
        self.setFixedSize(300, 500)





