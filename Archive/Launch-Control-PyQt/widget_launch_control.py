import sys
import time
import logging
import threading
import socket
import subprocess
from datetime import datetime
from PyQt5 import QtCore, QtWidgets, QtGui, Qt, QtMultimedia

server_IP = '192.168.0.21'  # This is the IP of the ESB Pi. It is a static IP.
port = 5002
BUFF = 1024

logname = time.strftime("log/LC_ClientLog(%H_%M_%S).log", time.localtime())
logger = logging.getLogger("")
logging.basicConfig(filename=logname, level=logging.DEBUG)

# Get a Timer Reset button. Also Maybe link the abort button to the countdown timer.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class LaunchControl(QtWidgets.QWidget):
    def __init__(self):

        # initializes the Geometry and the overall window

        super().__init__()

        self.server_address = (server_IP,port)
        self.connection_status = False

        self.init_ui()

    def init_ui(self):

        # initializes the GUI with the pictures found in the pictures folder.

        self.palettered = QtGui.QPalette()
        self.palettered.setColor(QtGui.QPalette.Foreground, QtCore.Qt.red)

        self.paletteblack = QtGui.QPalette()
        self.paletteblack.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)

        self.paletteblue = QtGui.QPalette()
        self.paletteblue.setColor(QtGui.QPalette.Foreground, QtCore.Qt.blue)

        # initial values
        self.kdata = "Open"
        self.mdata = "Open"
        self.ldata = "Open"
        self.bdata = "Intact"

        # time_thread = threading.Thread(target = self.get_time)
        # time_thread.start()

        self.server_address = (server_IP, port)
        self.connection_status = False  # initialzing to a false connection state
        self.arm_status = False

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        #grid.addWidget(self.serial_feed, tl_vertical_grid_pos, tl_hor_grid_pos, vertical_grid_length_min, hor_grid_width_min

        def createLabel(self, stext, smovex, smovey, sresizex, sresizey, sfontsize, storf, scolor):
            # makes code smaller, all the labels in the program

            slabel = QtWidgets.QLabel(self)
            slabel.setText(stext)
            slabel.move(smovex, smovey)
            slabel.resize(sresizex, sresizey)
            slabel.setFont(QtGui.QFont('Times', sfontsize, QtGui.QFont.Bold, storf))
            slabel.setPalette(scolor)

        def createPicture(self, spicture, smovex, smovey, sresizex, sresizey):
            # makes code smaller, all the pictures in the program
            # you have to save pictures to the pictures/ path in order to show

            pix = QtWidgets.QLabel(self)
            pix.setPixmap(QtGui.QPixmap('pictures/' + spicture))
            pix.move(smovex, smovey)
            pix.resize(sresizex, sresizey)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Pictures

        #All of the Pictures that change states.

        self.statusbreakred = QtWidgets.QLabel(self)
        self.statusbreakred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusbreakred.move(500, 335)
        self.statusbreakred.resize(380, 48)

        self.statusmainred = QtWidgets.QLabel(self)
        self.statusmainred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusmainred.move(500, 390)
        self.statusmainred.resize(380, 48)

        self.statusloxred = QtWidgets.QLabel(self)
        self.statusloxred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusloxred.move(500, 445)
        self.statusloxred.resize(380, 48)

        self.statuskerored = QtWidgets.QLabel(self)
        self.statuskerored.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statuskerored.move(500, 500)
        self.statuskerored.resize(380, 48)

        self.statusignitorred = QtWidgets.QLabel(self)
        self.statusignitorred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statusignitorred.move(500, 555)
        self.statusignitorred.resize(380, 48)

        self.statussafteyred = QtWidgets.QLabel(self)
        self.statussafteyred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statussafteyred.move(500, 610)
        self.statussafteyred.resize(380, 48)

        self.statushgpscolor = QtWidgets.QLabel(self)
        self.statushgpscolor.setPixmap(QtGui.QPixmap('pictures/statred.png'))
        self.statushgpscolor.move(500, 665)
        self.statushgpscolor.resize(380, 48)

        # def createPicture(self, spicture, smovex, smovey, sresizex, sresizey):

        whitetoolbar = createPicture(self, 'white.png', 0, 0, 1200, 80)
        whitebackground = createPicture(self, 'white2.png', 800, 0, 750, 700)
        redstripetoolbar = createPicture(self, 'red.png', 0, 45, 1200, 20)
        blackbottom = createPicture(self, 'black.png', 0, 740, 1200, 150)
        blacklogoback = createPicture(self, 'black2.png', 745, 65, 60, 675)
        sdsulogo = createPicture(self, 'sdsu2.png', 10, 750, 100, 79)
        redlogounderline = createPicture(self, 'red2.png', 770, 785, 350, 5)
        whitebtnborder = createPicture(self, 'black3.png', 320, 165, 400, 13)
        statrborder = createPicture(self, 'rborder.png', 675, 280, 50, 450)
        statlborder = createPicture(self, 'lborder.png', 315, 280, 50, 450)
        buttonrborder = createPicture(self, 'rborder.png', 250, 280, 50, 450)
        buttonlborder = createPicture(self, 'lborder.png', 20, 280, 50, 450)
        statusboxbreak = createPicture(self, 'statusborder.png', 330, 335, 380, 48)
        statusboxmain = createPicture(self, 'statusborder.png', 330, 390, 380, 48)
        statusboxlox = createPicture(self, 'statusborder.png', 330, 445, 380, 48)
        statusboxkero = createPicture(self, 'statusborder.png', 330, 500, 380, 48)
        statusboxignitor = createPicture(self, 'statusborder.png', 330, 555, 380, 48)
        statusboxsaftey = createPicture(self, 'statusborder.png', 330, 610, 380, 48)
        statusboxhgps = createPicture(self, 'statusborder.png', 330, 665, 380, 48)
        rocketlogo = createPicture(self, 'rocket2.png', 1030, 740, 150, 150)
        redstripetoolbar = createPicture(self, 'red.png', 0, 740, 1200, 5)
        commandbreak = createPicture(self, 'break.png', 110, 285, 100, 10)
        statusbreak = createPicture(self, 'break.png', 470, 285, 100, 10)
        buttonbreak = createPicture(self, 'break.png', 470, 156, 100, 10)
        buttonbreak2 = createPicture(self, 'break.png', 470, 177, 100, 10)
        blackpoint = createPicture(self, 'redpoint.png', 298, 212, 10, 10)
        blackpoint2 = createPicture(self, 'redpoint.png', 298, 112, 10, 10)
        blackpoint3 = createPicture(self, 'redpoint.png', 515, 112, 10, 10)
        blackpoint4 = createPicture(self, 'redpoint.png', 515, 212, 10, 10)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Labels

        # def createLabel(self, stext, smovex, smovey, sresizex, sresizey, sfontsize, storf, scolor):

        self.mainlabel = createLabel(self, 'LAUNCH CONTROL', 10, 0, 500, 50, 24, True, self.paletteblack)
        self.rocketlabel = createLabel(self, 'SDSU ROCKET PROJECT', 780, 740, 500, 50, 20, True, self.palettered)
        self.buttonlabel = createLabel(self, 'Commands:', 90, 230, 800, 80, 13, True, self.paletteblack)
        self.statuslabel = createLabel(self, 'Readings:', 465, 230, 800, 80, 13, True, self.paletteblack)
        self.connectionlabel = createLabel(self, 'Connection:', 985, 10, 500, 50, 9, False, self.paletteblue)
        self.breakwirelabel = createLabel(self, 'Breakwire Status', 340, 335, 500, 50, 12, False, self.paletteblue)
        self.mainValvelabel = createLabel(self, 'Main Propellant Valve', 338, 390, 500, 50, 10, False, self.paletteblue)
        self.loxValvelabel = createLabel(self, 'Lox Vent Valve', 340, 445, 500, 50, 12, False, self.paletteblue)
        self.keroValvelabel = createLabel(self, 'Kero Vent Valve', 340, 500, 500, 50, 12, False, self.paletteblue)
        self.ignitorstatuslabel = createLabel(self, 'Ignitor Status', 340, 555, 500, 50, 12, False, self.paletteblue)
        self.safteystatus = createLabel(self, 'Saftey Status', 340, 610, 500, 50, 12, False, self.paletteblue)
        self.hgpsstatuslabel = createLabel(self, 'HGPS', 340, 665, 500, 50, 12, False, self.paletteblue)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # All of the labels that change states.

        self.connectionstatus = QtWidgets.QLabel(self)
        self.connectionstatus.setText('Not Connected')
        self.connectionstatus.move(1080, 10)
        self.connectionstatus.resize(500, 50)
        self.connectionstatus.setFont(QtGui.QFont('Times', 9, QtGui.QFont.Bold, False))
        self.connectionstatus.setPalette(self.paletteblue)

        self.breakwirechange = QtWidgets.QLabel(self)
        self.breakwirechange.setText('Intact')
        self.breakwirechange.move(590, 335)
        self.breakwirechange.resize(500, 50)
        self.breakwirechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.breakwirechange.setPalette(self.paletteblack)

        self.mainValvechange = QtWidgets.QLabel(self)
        self.mainValvechange.setText('Open')
        self.mainValvechange.move(595, 390)
        self.mainValvechange.resize(500, 50)
        self.mainValvechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.mainValvechange.setPalette(self.paletteblack)

        self.loxValvechange = QtWidgets.QLabel(self)
        self.loxValvechange.setText('Open')
        self.loxValvechange.move(595, 445)
        self.loxValvechange.resize(500, 50)
        self.loxValvechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.loxValvechange.setPalette(self.paletteblack)

        self.keroValvechange = QtWidgets.QLabel(self)
        self.keroValvechange.setText('Open')
        self.keroValvechange.move(595, 500)
        self.keroValvechange.resize(500, 50)
        self.keroValvechange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.keroValvechange.setPalette(self.paletteblack)

        self.ignitorstatuschange = QtWidgets.QLabel(self)
        self.ignitorstatuschange.setText('Not Lit')
        self.ignitorstatuschange.move(590, 555)
        self.ignitorstatuschange.resize(500, 50)
        self.ignitorstatuschange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.ignitorstatuschange.setPalette(self.paletteblack)

        self.safteystatuschange = QtWidgets.QLabel(self)
        self.safteystatuschange.setText('Disarmed')
        self.safteystatuschange.move(550, 610)
        self.safteystatuschange.resize(500, 50)
        self.safteystatuschange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.safteystatuschange.setPalette(self.paletteblack)

        self.hgpsstatuschange = QtWidgets.QLabel(self)
        self.hgpsstatuschange.setText('Off')
        self.hgpsstatuschange.move(600, 665)
        self.hgpsstatuschange.resize(500, 50)
        self.hgpsstatuschange.setFont(QtGui.QFont('Times', 18, QtGui.QFont.Bold, False))
        self.hgpsstatuschange.setPalette(self.paletteblack)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # sets up the logging text box in the console

        self.logTextBox = QtWidgets.QTextBrowser(self)
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.logTextBox.setFont(self.font)
        self.logTextBox.setReadOnly(True)
        self.logTextBox.resize(400, 675)
        self.logTextBox.move(800, 65)
        self.logTextBox.append("  =========Action Log=========")

        timerbackground = createPicture(self, 'timerback.png', 635, 0, 300, 39)

        self.timert = QtWidgets.QLabel(self)
        self.timert.setText("Countdown: ")
        self.timert.move(670, -18)
        self.timert.resize(200, 50)
        self.timert.setFont(QtGui.QFont('Times', 8, QtGui.QFont.Bold, True))

        self.timeup = -60
        self.timert = QtWidgets.QLabel(self)
        self.timert.setText("-60")
        self.timert.move(845, -10)
        self.timert.resize(100, 50)
        self.timert.setFont(QtGui.QFont('Times', 20, QtGui.QFont.Bold, False))

        self.timerT = QtWidgets.QLabel(self)
        self.timerT.setText("T")
        self.timerT.move(800, -10)
        self.timerT.resize(100, 50)
        self.timerT.setFont(QtGui.QFont('Times', 20, QtGui.QFont.Bold, False))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        """color = QtGui.QColor(0,0,0)

        fontColor = QtWidgets.QAction('Font bg Color', self)
        fontColor.triggered.connect(self.color_picker)

        self.toolbar.addAction(fontColor)

        Figuring out how to color"""
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.setLayout(grid)
        self.homeButtons()
        self.show()

    # self.Time()


    def homeButtons(self):

        # Sets up buttons found in the program

        self.font2 = QtGui.QFont()
        self.font2.setPointSize(18)
        self.font3 = QtGui.QFont()
        self.font3.setPointSize(12)
        self.font4 = QtGui.QFont()
        self.font4.setPointSize(10)
        self.font5 = QtGui.QFont()
        self.font5.setPointSize(24)

        self.launchBtn = QtWidgets.QPushButton("Launch!", self)
        self.launchBtn.resize(290, 170)
        self.launchBtn.move(5, 70)
        self.launchBtn.setEnabled(False)
        self.launchBtn.setFont(self.font5)
        self.launchBtn.clicked.connect(self.launch_app)

        self.igniteBtn = QtWidgets.QPushButton("Ignite!", self)
        self.igniteBtn.resize(203, 85)
        self.igniteBtn.move(310, 70)
        self.igniteBtn.setEnabled(False)
        self.igniteBtn.setFont(self.font3)
        self.igniteBtn.clicked.connect(self.ignite_app)

        self.igniteoffBtn = QtWidgets.QPushButton("Ignitor Off!", self)
        self.igniteoffBtn.resize(203, 53)
        self.igniteoffBtn.move(310, 187)
        self.igniteoffBtn.setEnabled(False)
        self.igniteoffBtn.setFont(self.font3)
        self.igniteoffBtn.clicked.connect(self.igniteoff_app)

        self.abortBtn = QtWidgets.QPushButton("Abort!", self)
        self.abortBtn.resize(203, 85)
        self.abortBtn.move(528, 70)
        self.abortBtn.setEnabled(False)
        self.abortBtn.setFont(self.font3)
        self.abortBtn.clicked.connect(self.abort_app)

        self.ping_serverBtn = QtWidgets.QPushButton("Connect", self)
        self.ping_serverBtn.resize(240, 60)
        self.ping_serverBtn.move(40, 295)
        self.ping_serverBtn.setFont(self.font3)
        self.ping_serverBtn.clicked.connect(self.connect_app)

        self.open_ventsBtn = QtWidgets.QPushButton("Open Vents", self)
        self.open_ventsBtn.resize(240, 60)
        self.open_ventsBtn.move(40, 355)
        self.open_ventsBtn.setFont(self.font3)
        self.open_ventsBtn.clicked.connect(self.openvents_app)

        self.close_ventsBtn = QtWidgets.QPushButton("Close Vents", self)
        self.close_ventsBtn.resize(240, 60)
        self.close_ventsBtn.move(40, 415)
        self.close_ventsBtn.setFont(self.font3)
        self.close_ventsBtn.clicked.connect(self.closevents_app)

        self.close_mainBtn = QtWidgets.QPushButton("Close Main", self)
        self.close_mainBtn.resize(240, 60)
        self.close_mainBtn.move(40, 475)
        self.close_mainBtn.setFont(self.font3)
        self.close_mainBtn.clicked.connect(self.closemain_app)

        self.hgpsonBtn = QtWidgets.QPushButton("HGPS On", self)
        self.hgpsonBtn.resize(240, 60)
        self.hgpsonBtn.move(40, 535)
        self.hgpsonBtn.setFont(self.font3)
        self.hgpsonBtn.clicked.connect(self.hgpson_app)

        self.hgpsoffBtn = QtWidgets.QPushButton("HGPS Off", self)
        self.hgpsoffBtn.resize(240, 60)
        self.hgpsoffBtn.move(40, 595)
        self.hgpsoffBtn.setFont(self.font3)
        self.hgpsoffBtn.clicked.connect(self.hgpsoff_app)

        self.safteyBtn = QtWidgets.QPushButton("Toggle Saftey", self)
        self.safteyBtn.resize(240, 60)
        self.safteyBtn.move(40, 655)
        self.safteyBtn.setFont(self.font3)
        self.safteyBtn.clicked.connect(self.saftey_app)

        self.bstronBtn = QtWidgets.QPushButton("Boosters On", self)
        self.bstronBtn.resize(102, 53)
        self.bstronBtn.move(528, 187)
        self.bstronBtn.setFont(self.font4)
        self.bstronBtn.setEnabled(False)
        self.bstronBtn.clicked.connect(self.boosterson_app)

        self.bstroffBtn = QtWidgets.QPushButton("Boosters Off", self)
        self.bstroffBtn.resize(102, 53)
        self.bstroffBtn.move(633, 187)
        self.bstroffBtn.setFont(self.font4)
        self.bstroffBtn.setEnabled(False)
        self.bstroffBtn.clicked.connect(self.boostersoff_app)

        self.statusBtn = QtWidgets.QPushButton("Read Statuses", self)
        self.statusBtn.resize(350, 35)
        self.statusBtn.move(345, 295)
        self.statusBtn.setFont(self.font3)
        self.statusBtn.clicked.connect(self.read_app)

        self.timeBtn = QtWidgets.QPushButton("Start", self)
        self.timeBtn.move(668, 15)
        self.timeBtn.resize(125, 20)
        self.timeBtn.setEnabled(False)
        self.timeBtn.clicked.connect(self.timer1)

        self.pingBtn = QtWidgets.QPushButton("Ping Server", self)
        self.pingBtn.move(1070, 0)
        self.pingBtn.resize(125, 25)
        self.pingBtn.clicked.connect(self.ping_app)

    def paintEvent(self, e):

        # sets up the "paint brush" in order to use the drawLines function

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        self.drawLines2(qp)
        qp.end()

    def drawLines(self, qp):

        # draws the red lines found in the program

        pen = QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(20, 250, 725, 250)
        qp.drawLine(307.5, 260, 307.5, 730)
        #qp.drawLine(320, 190, 410, 190)

    # qp.drawLine(330,400,710,400)
    # qp.drawLine(20,205,325,205)
    # qp.drawLine(240,265,240,305)

    def drawLines2(self, qp):  # (not being used currently)

        # draws the black lines found in the program

        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)

    def timer0(self):
        self.timeup += 1
        self.timert.setText(str(self.timeup))
        if self.timeup >= 1:
            self.timerT.setText("T+")
        if self.timeup == 0:
            QtMultimedia.QSound.play('sounds/beep.wav')

    def timer1(self):
        self.logTextBox.append("  >  Timer Started!{}".format(time.strftime("   -\t(%H:%M:%S)", time.localtime())))
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer0)
        self.timer.start(1000)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # This is where the functions are for the buttons and toolbar

    def launch_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  Launching!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Launching at {}".format(time.asctime()))
            self.send_info('L')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def read_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  Reading{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Reading at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

            self.infotimer = QtCore.QTimer()
            self.infotimer.timeout.connect(self.get_info)
            self.infotimer.setInterval(200)
            self.infotimer.start()
            self.logTextBox.append(" > Starting Get Info Timer{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Started Get Info Timer at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))

        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def ignite_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  Igniting!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Igniting at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('Ig')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def igniteoff_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  Ignitor Off!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Ignitor Off at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('IO')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def boosterson_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  Boosters On{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Boosters On at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('BL')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def boostersoff_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  Boosters Off{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Boosters Off at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('BO')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')
        
    def abort_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  Aborting!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Aborting at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('A')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')


    def connect_app(self):

        self.logTextBox.append("  >  Connecting...{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))

        try:
            self.s = socket.create_connection(self.server_address,timeout = 1.5)
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'Socket Successfully Bound.\nClick "Read Statuses " to start')
            self.connection_status = True
            self.connectionstatus.setText('Connected')
            self.logTextBox.append("  >  Connected{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Connection Successful at {}".format(time.asctime()))

        except socket.error as e:
            logger.debug("Connection Unsuccessful at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            reply = QtWidgets.QMessageBox.critical(self, "Connection Results", "Couldn't connect to {} at {}. Error is: \n{}.\nMake sure server is listening.".format(self.server_address[0],self.server_address[1],e),
                                                    QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Retry)
            if reply == QtWidgets.QMessageBox.Cancel:
                self.logTextBox.append("  >  Connection Canceled{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))
            elif reply == QtWidgets.QMessageBox.Retry:
                self.connect_app()


    def openvents_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  Vents Opened{}".format(time.strftime("    -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Vents Opened at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('VO')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def closevents_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  Vents Closed{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Vents Closed at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('VC')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def closemain_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  Main Propellant Valve Closed{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("Main Closed at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('MC')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def hgpson_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  HGPS turned ON{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("HGPS ON at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('HGPS_On')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def hgpsoff_app(self):

        if self.connection_status == True:
            self.logTextBox.append("  >  HGPS turned OFF{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
            logger.debug("HGPS OFF at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            self.send_info('HGPS_Off')
        elif self.connection_status == False:
            QtWidgets.QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

    def saftey_app(self):

        if self.connection_status == True:
            if self.arm_status == False:
                self.igniteBtn.setEnabled(True)
                self.launchBtn.setEnabled(True)
                self.abortBtn.setEnabled(True)
                self.timeBtn.setEnabled(True)
                self.igniteoffBtn.setEnabled(True)
                self.bstroffBtn.setEnabled(True)
                self.bstronBtn.setEnabled(True)
                self.safteystatuschange.setText('Armed')
                self.statussafteyred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                self.logTextBox.append("  >  Saftey Toggled{}".format(time.strftime("   -\t(%H:%M:%S)", time.localtime())))
                self.arm_status = True

            elif self.arm_status == True:
                self.igniteBtn.setEnabled(False)
                self.launchBtn.setEnabled(False)
                self.abortBtn.setEnabled(False)
                self.timeBtn.setEnabled(False)
                self.igniteoffBtn.setEnabled(False)
                self.bstronBtn.setEnabled(False)
                self.bstroffBtn.setEnabled(False)
                self.safteystatuschange.setText('Disarmed')
                self.statussafteyred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                self.logTextBox.append("  >  Saftey Toggled{}".format(time.strftime("   -\t(%H:%M:%S)", time.localtime())))
                self.arm_status = False

        elif self.connection_status == False:
            logger.debug("Connection Error, Safety will not toggle unless client is connected to server at {}".format(time.asctime()))
            reply = QtWidgets.QMessageBox.critical(self, 'Connection Error', 'Safety will not toggle unless client is connected to server',
                                                    QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Retry)
            if reply == QtWidgets.QMessageBox.Cancel:
                self.logTextBox.append("  >  Saftey Canceled{}".format(time.strftime("       -\t(%H:%M:%S)", time.localtime())))
            elif reply == QtWidgets.QMessageBox.Retry:
                self.saftey_app()

    def ping_app(self):

        QtWidgets.QMessageBox.information(self, '', 'Pinging...')
        #response = subprocess.call(["ping", server_IP,"-c1", "-W1","-q"])
        response = subprocess.call("ping {} -n 1 -w 1".format(server_IP)) #This is Windows syntax.
        logger.debug("Pinging Server at {}".format(time.asctime()))
        self.logTextBox.append("  >  Pinging Server{}".format(time.strftime("    -\t(%H:%M:%S)", time.localtime())))

        if response == 0:
            QtWidgets.QMessageBox.information(self, 'Ping Results', 'Ping to {} sucessful!\nGo ahead and connect.'.format(server_IP))
            logger.debug("Ping_Sucessful at {}".format(time.asctime()))
            self.logTextBox.append("  >  Pinging Successful{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))
        else:
            QtWidgets.QMessageBox.information(self, 'Ping Results', "Ping to {} unsucessful!\nCheck the IP you're connecting to, or if server is online.".format(server_IP))
            logger.debug("Ping_Unsucessful at {}".format(time.asctime()))
            self.logTextBox.append("  >  Pinging Unsucessful{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))

    def send_info(self,command):

        if command == 'MO':
            message = b'main_open'
            logger.debug("main_open at {}".format(time.asctime()))
        elif command == 'MC':
            message = b'main_close'
            logger.debug("main_close at {}".format(time.asctime()))
        elif command == 'VO':
            message = b'vents_open'
            logger.debug("vents_open at {}".format(time.asctime()))
        elif command == 'VC':
            message = b'vents_close'
            logger.debug("vents_close at {}".format(time.asctime()))
        elif command == 'L':
            message = b'launch'
            logger.debug("launch at {}".format(time.asctime()))
        elif command == 'A':
            message = b'abort'
            logger.debug("abort at {}".format(time.asctime()))
        elif command == "Ig":
            message = b"ign1_on"
            logger.debug("ign1_on at {}".format(time.asctime()))
        elif command == "IO":
            message = b"ign1_off"
            logger.debug("ign1_off at {}".format(time.asctime()))
        elif command =='HGPS_On':
            message = b"ign2_on"
            logger.debug("HGPS_On at {}".format(time.asctime()))
        elif command == 'HGPS_Off':
            message = b'ign2_off'
            logger.debug("HGPS_Off at {}".format(time.asctime()))
        elif command == "BL":
            message = b'boosters_lit'
            logger.debug("Boosters On at {}".format(time.asctime()))
        elif command == "BO":
            message = b'boosters_off'
            logger.debug("Boosters Off at {}".format(time.asctime()))

        self.s.send(message)
        data = self.s.recv(BUFF)
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        if data.decode("utf-8") == 'Ignitor 1 Lit':
            time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            self.statusignitorred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
            self.ignitorstatuschange.setText('Lit af')
            logging.info("Ignitor 1 lit: {}".format(time_now))
            logger.debug("Ignitor_1_lit at {}".format(time.asctime()))

        elif data.decode("utf-8") == 'Ignitor 1 Off':
            self.statusignitorred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
            self.ignitorstatuschange.setText('Not Lit')
            logger.debug("Ignitor_1_Off at {}".format(time.asctime()))

        elif data.decode("utf-8") == 'Ignitor 2 Lit':
            self.statushgpscolor.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
            self.hgpsstatuschange.setText('On')
            logger.debug("HGPS On at {}".format(time.asctime()))

        elif data.decode("utf-8") == 'Ignitor 2 Off':
            self.statushgpscolor.setPixmap(QtGui.QPixmap('pictures/statred.png'))
            self.hgpsstatuschange.setText('Off')
            logger.debug("HGPS Off at {}".format(time.asctime()))

        elif data.decode("utf-8") == 'Boosters Lit':
            #self.statushgpscolor.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
            #self.hgpsstatuschange.setText('On')
            logger.debug("Boosters Lit at {}".format(time.asctime()))

        elif data.decode("utf-8") == 'Boosters Off':
            #self.statushgpscolor.setPixmap(QtGui.QPixmap('pictures/statred.png'))
            #self.hgpsstatuschange.setText('Off')
            logger.debug("Boosters Off at {}".format(time.asctime()))

    def switch_label(self,label):

        #These statements change the status of the labels
        if label == 'bwire':
            if self.breakwirechange.text() == 'Intact':
                self.statusbreakred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                self.breakwirechange.setText('Broken')
                logger.debug("bwire_Broken at {}".format(time.asctime()))
            elif self.breakwirechange.text() == 'Broken':
                self.statusbreakred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                self.breakwirechange.setText('Intact')
                logger.debug("bwire_Intact at {}".format(time.asctime()))

        if label == 'main':
            if self.mainValvechange.text() == 'Open':
                self.statusmainred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                self.mainValvechange.setText('Closed')
                logger.debug("main_Closed at {}".format(time.asctime()))
            elif self.mainValvechange.text() == 'Closed':
                self.statusmainred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                self.mainValvechange.setText('Open')
                logger.debug("main_Open at {}".format(time.asctime()))

        if label == 'kero':
            if self.keroValvechange.text() == 'Open':
                self.statuskerored.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                self.keroValvechange.setText('Closed')
                logger.debug("kero_Closed at {}".format(time.asctime()))
            elif self.keroValvechange.text() == 'Closed':
                self.statuskerored.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                self.keroValvechange.setText('Open')
                logger.debug("kero_Open at {}".format(time.asctime()))

        if label == 'lox':
            if self.loxValvechange.text() == 'Open':
                self.statusloxred.setPixmap(QtGui.QPixmap('pictures/statgreen.png'))
                self.loxValvechange.setText('Closed')
                logger.debug("lox_Closed at {}".format(time.asctime()))
            elif self.loxValvechange.text() == 'Closed':
                self.statusloxred.setPixmap(QtGui.QPixmap('pictures/statred.png'))
                self.loxValvechange.setText('Open')
                logger.debug("lox_Open at {}".format(time.asctime()))

    def get_info(self):

        try:
            self.s.send(b'bwire_status')
            self.bdata = self.s.recv(BUFF)

            self.s.send(b'main_status')
            self.mdata = self.s.recv(BUFF)

            self.s.send(b'kero_status')
            self.kdata = self.s.recv(BUFF)

            self.s.send(b'LOX_status')
            self.ldata = self.s.recv(BUFF)

        except (socket.error,AttributeError) as err:
            time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
            logging.error("{},{}".format(time_now,err))
            logger.debug("{},{}".format(time_now,err))

        #The following if statements call the label to be changed only if the server sends a message that contradicts the current status of the label 
        if self.bdata.decode("utf-8") != self.breakwirechange.text():
            self.switch_label("bwire")
            print("Break Wire Changed:")
            print(self.bdata)
            logger.debug("bwire_status of {} at {}".format(str(self.bdata),time.asctime()))

        if self.mdata.decode("utf-8") != self.mainValvechange.text():
            self.switch_label('main')
            print("Main Changed")
            print(self.mdata)
            logger.debug("main_status of {} at {}".format(str(self.mdata),time.asctime()))

        if self.kdata.decode("utf-8") != self.keroValvechange.text():
            self.switch_label('kero')
            print("Kero Changed")
            print(self.kdata)
            logger.debug("kero_status of {} at {}".format(str(self.kdata),time.asctime()))

        if self.ldata.decode("utf-8") != self.loxValvechange.text():
            self.switch_label('lox')
            print("Lox Changed")
            print(self.ldata)
            logger.debug("lox_status of {} at {}".format(str(self.ldata),time.asctime()))


    def close_app(self):
        # exits GUI
        self.logTextBox.append(">  Exiting...{}".format(time.strftime("\t-           (%H:%M:%S)", time.localtime())))
        choice = QtWidgets.QMessageBox.question(self, "Confirmation.", "Are you sure you want to exit?", 
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            print("System Closed")
            logger.debug("Application Exited at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
            sys.exit()
        else:
            self.logTextBox.append("> Exit Stopped{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))


