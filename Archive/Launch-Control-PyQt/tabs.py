from PyQt5.QtWidgets import QWidget, QPushButton, QTabWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSlot
#from widget_start import Start
from widget_launch_control import LaunchControl
from widget_coms import RadioTab


class TabManager(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.tabs = QTabWidget()

        #Init Tabs
        self.launch_control = LaunchControl()
        self.radio = RadioTab()
        #self.start_page = Start(self)
        #self.tab_name = customWidget()

        #Connect Tabs
        #self.tabs.addTab(self.start_page, "Start")
        self.tabs.addTab(self.launch_control, "Launch Control")
        self.tabs.addTab(self.radio, "Radio")

        #Add tabs to widget

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
            print("\n")
            for currentQTableWidgetItem in self.tableWidget.selectedItems():
                print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())