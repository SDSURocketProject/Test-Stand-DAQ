import sys
import os
import time
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
import socket
import subprocess
import paho.mqtt.client as mqtt

#sets up a log file in the directory the program is in.
logname = time.strftime("log/LC_ClientLog(%H_%M_%S).log", time.localtime())
logger = logging.getLogger("1")
logging.basicConfig(filename=logname, level=logging.DEBUG)

class Client(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowState(Qt.WindowMaximized)
		self.yGeom = QDesktopWidget().height()
		self.xGeom = QDesktopWidget().width()
		self.xScalar = (self.xGeom/1920)*2
		self.xCenter = self.xGeom/self.xScalar
		self.yCenter = self.yGeom/2
		self.client_settings = ClientSettings()
		self.initUI()
		self.MenuBar()
		self.Pictures()
		self.Labels()
		self.Buttons()
		self.show()


	def initUI(self):
		self.title = 'Test Stand'
		self.setWindowTitle(self.title)
		self.setWindowIcon(QIcon('pictures/icon.png'))
		# Set window background color
		self.setAutoFillBackground(True)
		p = self.palette()
		p.setColor(self.backgroundRole(), Qt.white)
		self.setPalette(p)

		# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

		# sets up the logging text box in the console

		self.logTextBox = QTextBrowser(self)
		self.font = QFont()
		self.font.setPointSize(12)
		self.logTextBox.setFont(self.font)
		self.logTextBox.setReadOnly(True)
		self.logTextBox.resize(400, 974)
		self.logTextBox.move(self.xCenter+560, 75)
		self.logTextBox.append("  =========Action Log=========")

		#Centers of Certain Objects, such as the test stand picture.
		self.testStandCenter = self.xCenter +290
		self.testStandDepth = self.yCenter - 480

		#Used to animate the Tanks, tough because the height function changes from the center of the picture.
		self.engineInit = 0
		self.engineInit_Move = 0
		self.tank_1_Init = 0
		self.tank_1_Init_Move = 0
		self.tank_2_Init = 0
		self.tank_2_Init_Move = 0


		#Initializing variables that will be used later in the program
		self.connection_status = False
		self.phidget_status = False
		self.loadcelltare = False
		self.arm_status = False
		self.HOST = "192.168.1.132"
		self.TOPIC_1 = "Valve_Commands"
		self.TOPIC_2 = "Valve_Readings"
		self.server_address = (self.HOST, 1883)
		self.voltlist = []


	def Labels(self):

		self.palettered = QPalette()
		self.palettered.setColor(QPalette.Foreground, Qt.red)

		self.paletteblack = QPalette()
		self.paletteblack.setColor(QPalette.Foreground, Qt.black)

		self.paletteblue = QPalette()
		self.paletteblue.setColor(QPalette.Foreground, Qt.blue)

		def createLabel(self, stext, smovex, smovey, sresizex, sresizey, sfontsize, storf, scolor):
			# makes code smaller, all the labels in the program
			slabel = QLabel(self)
			slabel.setText(stext)
			slabel.move(smovex, smovey)
			slabel.resize(sresizex, sresizey)
			slabel.setFont(QFont('Times', sfontsize, QFont.Bold, storf))
			slabel.setPalette(scolor)
			return slabel

		self.rocketlabel = createLabel(self, 'SDSU ROCKET PROJECT',0,25,500,50,20,True,self.paletteblack)
		self.teststandlabel = createLabel(self, 'TEST STAND',0,73,300,50,20,True,self.paletteblack)
		self.loadcelllabel = createLabel(self, '0',340,300,300,50,26,False,self.paletteblack)
		self.defineloadcell = createLabel(self, 'Load Cell Reading:',20,300,320,50,20,False,self.paletteblack)
		self.valves = createLabel(self, 'Valves:',235,375,300,50,20,False,self.paletteblack)
		self.breakwire = createLabel(self, 'BreakWire Reading: ',460,300,400,50,20,False,self.paletteblack)
		self.bwireread = createLabel(self, 'Connect',800,300,400,50,20,False,self.paletteblack)
		self.safteyread = createLabel(self, 'OFF',299,140,400,50,20,False,self.paletteblack)
		self.loadcellread = createLabel(self, 'OFF',299,215,400,50,20,False,self.paletteblack)

	def Pictures(self):

		def createPicture(self, spicture, smovex, smovey, sresizex, sresizey):
			# makes code smaller, all the pictures in the program
			# you have to save pictures to the pictures/ path in order to show
			pix = QLabel(self)
			pix.setPixmap(QPixmap('pictures/' + spicture))
			pix.resize(sresizex, sresizey)
			pix.move(smovex,smovey)
			return pix

		self.stand = createPicture(self,'stand.png',self.testStandCenter-350,self.testStandDepth,741,807)
		self.engine = createPicture(self,'Rocket_Engine.png',self.testStandCenter-40,self.testStandDepth + 750,80,186)
		self.engineHot = createPicture(self,'Rocket_Engine_Hot.png',self.testStandCenter-40,self.testStandDepth+843,80,0)
		self.load_cell = createPicture(self,'loadcell.png',self.testStandCenter-40,self.testStandDepth+740,80,87)
		self.tank1 = createPicture(self,'tank.png',self.testStandCenter-266,self.testStandDepth,171,711)
		self.tank2 = createPicture(self,'tank.png',self.testStandCenter+90,self.testStandDepth,171,711)
		self.blue = createPicture(self,'blue.png',self.testStandCenter-203,718,47,0)
		self.purple = createPicture(self,'purple.png',self.testStandCenter+90,718,47,0)
		self.redtopborder = createPicture(self,'red.png',0,25,1980,50)
		self.rocketlogo = createPicture(self,'rp2.png',self.testStandCenter-87.5,self.testStandDepth+95,175,91)
		self.box = createPicture(self,'box.png',0,73,215,50)
		self.border = createPicture(self,'border.png',13,431,564,159)
		self.border2 = createPicture(self,'border2.png',13,585,564,155)
		self.border3 = createPicture(self,'border2.png',13,735,564,155)
		self.border4 = createPicture(self,'border3.png',13,810,564,155)
		self.border5 = createPicture(self,'border.png',363,123,564,159)
		self.commandbreak = createPicture(self, 'break.png', 745, 560, 100, 10)
		#self.loxgauge = createPicture(self,'loxgauge.png',self.testStandCenter-570,self.testStandDepth+7,300,300)
		#self.ch4gauge = createPicture(self,'kerogauge.png',self.testStandCenter+260,self.testStandDepth+7,300,300)
		#self.heliumgauge = createPicture(self,'heliumgauge2.png',self.testStandCenter+260,self.testStandDepth+350,300,300)
		self.connectionsymbol = createPicture(self,'pingred.png',self.testStandCenter+40,self.testStandDepth,80,80)

	def Buttons(self):

		def createButton(self, stext, smovex, smovey, sresizex, sresizey, senabled, sfontsize, sfunction, sicon, siconx, sicony):
			# makes code smaller, all the labels in the program

			sbutton = QPushButton(stext, self)
			sbutton.move(smovex, smovey)
			sbutton.resize(sresizex, sresizey)
			sbutton.setEnabled(senabled)
			sbutton.setFont(sfontsize)
			sbutton.clicked.connect(sfunction)
			if stext == '':
				sbutton.setIcon(QIcon("pictures/"+sicon))
				sbutton.setIconSize(QSize(siconx, sicony))
			return sbutton


		#sets 4 different font sizes for the buttons created. Pick one.
		self.font2 = QFont()
		self.font2.setPointSize(18)
		self.font3 = QFont()
		self.font3.setPointSize(12)
		self.font4 = QFont()
		self.font4.setPointSize(36)
		self.font5 = QFont()
		self.font5.setPointSize(24)

		#Have to switch the True and False based on the states of the solenoids.... do that in the connect function, also have a read function that reads the states 
		#of the vents and displayes them/switches the buttons and labels
		self.connect_btn = createButton(self,'Connect',self.testStandCenter-120,self.testStandDepth+23,150,40,True,self.font5,self.connect_app,'icon.png',100,100)

		self.launch_btn = createButton(self,'Launch!',645,430,300,120,False,self.font4,self.mpv_open_app,'rp.png',200,200)

		self.saftey_btn = createButton(self,'Saftey',20,130,270,70,True,self.font5,self.saftey_app,'icon.png',100,100)

		self.abort_btn = createButton(self,"Abort :'(",660,590,270,70,False,self.font2,self.abort_app,'icon.png',100,100)

		self.lox_hi_open_btn = createButton(self,'LOX HI Open',20,440,270,70,True,self.font2,self.lox_hi_open_app,'icon.png',100,100)
		self.lox_hi_close_btn = createButton(self,'LOX HI Close',300,440,270,70,False,self.font2,self.lox_hi_close_app,'icon.png',100,100)

		self.meth_hi_open_btn = createButton(self,'CH4 HI Open',20,515,270,70,True,self.font2,self.meth_hi_open_app,'icon.png',100,100)
		self.meth_hi_close_btn = createButton(self,'CH4 HI Close',300,515,270,70,False,self.font2,self.meth_hi_close_app,'icon.png',100,100)

		self.meth_vent_open_btn = createButton(self,'CH4 Vent Open',20,590,270,70,True,self.font2,self.meth_vent_open_app,'icon.png',100,100)
		self.meth_vent_close_btn = createButton(self,'CH4 Vent Close',300,590,270,70,False,self.font2,self.meth_vent_close_app,'icon.png',100,100)

		self.lox_vent_open_btn = createButton(self,'LOX Vent Open',20,665,270,70,True,self.font2,self.lox_vent_open_app,'icon.png',100,100)
		self.lox_vent_close_btn = createButton(self,'LOX Vent Close',300,665,270,70,False,self.font2,self.lox_vent_close_app,'icon.png',100,100)

		self.meth_mpv_open_btn = createButton(self,'CH4 MPV Open',20,740,270,70,True,self.font2,self.meth_mpv_open_app,'icon.png',100,100)
		self.meth_mpv_close_btn = createButton(self,'CH4 MPV Close',300,740,270,70,False,self.font2,self.meth_mpv_close_app,'icon.png',100,100)

		self.lox_mpv_open_btn = createButton(self,'LOX MPV Open',20,815,270,70,True,self.font2,self.lox_mpv_open_app,'icon.png',100,100)	
		self.lox_mpv_close_btn = createButton(self,'LOX MPV Close',300,815,270,70,False,self.font2,self.lox_mpv_close_app,'icon.png',100,100)

		self.vents_open_btn = createButton(self,'Vents Open',20,890,270,70,True,self.font2,self.vents_open_app,'icon.png',100,100)  
		self.vents_close_btn = createButton(self,'Vents Close',300,890,270,70,False,self.font2,self.vents_close_app,'icon.png',100,100)

		#The labels on the vents buttons are backwards, but the apps and MQTT commands are right
		self.mpv_open_btn = createButton(self,'MPV Open',660,665,270,70,False,self.font2,self.mpv_open_app,'icon.png',100,100)
		self.mpv_close_btn = createButton(self,'MPV Close',660,740,270,70,False,self.font2,self.mpv_close_app,'icon.png',100,100)

		self.loadcell_btn = createButton(self,'Start Load Cell',20,205,270,70,True,self.font5,self.loadcell_app,'icon.png',100,100)
		#self.loadcell_tare_btn = createButton(self,'Tare Load Cell',5,290,270,70,True,self.font5,self.loadcelltare_app,'icon.png',100,100)

		self.ignitor_on_btn = createButton(self,'Ignitor On',370,205,270,70,False,self.font2,self.ignitor_on_app,'icon.png',100,100)
		self.ignitor_off_btn = createButton(self,'Ignitor Off',650,205,270,70,False,self.font2,self.ignitor_off_app,'icon.png',100,100)

		self.purge_open_btn = createButton(self,'Purge Open',370,130,270,70,True,self.font2,self.purge_open_app,'icon.png',100,100)
		self.purge_close_btn= createButton(self,'Purge Close',650,130,270,70,False,self.font2,self.purge_close_app,'icon.png',100,100)

		#self.so7_btn = createButton(self,'Solenoid 7 Open',660,740,270,70,True,self.font2,self.so7_app,'icon.png',100,100)
		#self.sc7_btn = createButton(self,'Solenoid 7 Close',660,815,270,70,False,self.font2,self.sc7_app,'icon.png',100,100)

	def lox_hi_open_app(self):
		if self.connection_status == True:
			logger.debug("Lox HI Open at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('lho')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def lox_hi_close_app(self):
		if self.connection_status == True:
			logger.debug("Lox HI Close at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('lhc')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def meth_hi_open_app(self):
		if self.connection_status == True:
			logger.debug("Methane HI Open at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('mho')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def meth_hi_close_app(self):
		if self.connection_status == True:
			logger.debug("Methane HI Close at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('mhc')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def meth_vent_open_app(self):
		if self.connection_status == True:
			logger.debug("Methane Vent Open at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('mvo')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def meth_vent_close_app(self):
		if self.connection_status == True:
			logger.debug("Methane Vent Close at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('mvc')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def lox_vent_open_app(self):
		if self.connection_status == True:
			logger.debug("Lox Vent Open at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('lvo')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def lox_vent_close_app(self):
		if self.connection_status == True:
			logger.debug("Lox Vent Close at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('lvc')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def meth_mpv_open_app(self):
		if self.connection_status == True:
			logger.debug("Methane MPV Open at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('mmo')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')			

	def meth_mpv_close_app(self):
		if self.connection_status == True:
			logger.debug("Methane MPV Close at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('mmc')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def lox_mpv_open_app(self):
		if self.connection_status == True:
			logger.debug("LOX MPV Open at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('lmo')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')	

	def lox_mpv_close_app(self):
		if self.connection_status == True:
			logger.debug("LOX MPV Close at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('lmc')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')		

	def purge_open_app(self):
		if self.connection_status == True:
			logger.debug("Purge Open at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('po')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def purge_close_app(self):
		if self.connection_status == True:
			logger.debug("Purge Close at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('pc')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def vents_open_app(self):
		if self.connection_status == True:
			logger.debug("Vents Open at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('vo')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def vents_close_app(self):
		if self.connection_status == True:
			logger.debug("Vents Close at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('vc')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def mpv_open_app(self):
		if self.connection_status == True:
			logger.debug("MPV Open at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('mo')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def mpv_close_app(self):
		if self.connection_status == True:
			logger.debug("MPV Close at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('mc')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def ignitor_on_app(self):
		if self.connection_status == True:
			logger.debug("Ignitor On at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('ion')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def ignitor_off_app(self):
		if self.connection_status == True:
			logger.debug("Ignitor Off at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('ioff')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def abort_app(self):
		if self.connection_status == True:
			logger.debug("Aborting at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('abort')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def so7_app(self):
		if self.connection_status == True:
			logger.debug(" at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('Ro7')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def sc7_app(self):
		if self.connection_status == True:
			logger.debug(" at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.send_info('Rc7')
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')

	def saftey_app(self):
		if self.connection_status == True:
			self.logTextBox.append("  >  Saftey Toggled!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			logger.debug("Saftey Toggled at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			if self.arm_status == False:
				self.launch_btn.setEnabled(True)
				self.ignitor_on_btn.setEnabled(True)
				self.mpv_open_btn.setEnabled(True)
				self.abort_btn.setEnabled(True)
				self.arm_status = True
			elif self.arm_status == True:
				self.launch_btn.setEnabled(False)
				self.ignitor_on_btn.setEnabled(False)
				self.mpv_open_btn.setEnabled(False)
				self.abort_btn.setEnabled(False)
				self.arm_status = False
		elif self.connection_status == False:
			QMessageBox.information(self, 'Connection Results', 'You are not connected, please connect and try again.')


	'''def loadcelltare_app(self):
		if self.loadcelltare = True:
			self.loadcell_app()
		else:
			QMessageBox.information(self, 'Tare Results', 'Cannot Tare a Load Cell That is Not Running')
			self.logTextBox.append("  >  Cannot Tare a Load Cell That is Not Running{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))'''

	def loadcell_app(self):

		def VoltageRatioInputAttached(e):
			print("Attached!")
			self.phidget_status = True

		def VoltageRatioInputDetached(e):
			print("Detached") 
			self.phidget_status = False

		def VoltageRatioChangeHandler(e, voltageRatio):
			try:
				voltageRatio = (877420*voltageRatio - self.voltavg)
				self.voltlist.append(voltageRatio)
				#print("VoltageRatio: %f" % voltageRatio)
				self.loadcelllabel.setText((str(voltageRatio))[0:6])
				logger.debug("                                                                                {} at {}".format(voltageRatio, time.asctime()))
			except:
				voltageRatio = (877420*voltageRatio)
				voltageZero.append(voltageRatio)
				#print("VoltageRatio: %f" % voltageRatio)
				self.loadcelllabel.setText(str(voltageRatio))

		def ErrorEvent(e, eCode, description):
			print("Error %i : %s" % (eCode, description))
		if self.phidget_status == False or self.loadcelltare == True:
			try:
				self.ch = VoltageRatioInput()
				self.ch.setOnErrorHandler(ErrorEvent)
				self.ch.setOnAttachHandler(VoltageRatioInputAttached)
				self.ch.setOnVoltageRatioChangeHandler(VoltageRatioChangeHandler)
				self.ch.openWaitForAttachment(1000)
				self.ch.setBridgeEnabled(1)
				voltageZero = []

				time.sleep(5)
				self.voltavg = float(sum(voltageZero)) / float(len(voltageZero))

				self.loadcelltare = False
			except PhidgetException as e:
				print("Phidget Exception %i: %s" % (e.code, e.details))
				self.loadcelllabel.setText("Error")
				self.logTextBox.append("  >  Phidget Not Found{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
				reply = QMessageBox.critical(self, "Phidget Results", "Couldn't connect to Phidget. Error is: \n{}: {}.\nMake sure Phidget is attached.".format(e.code, e.details),
														QMessageBox.Cancel | QMessageBox.Retry)
				if reply == QMessageBox.Cancel:
					self.logTextBox.append("  >  Phidget Canceled{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))
				elif reply == QMessageBox.Retry:
					self.logTextBox.append("  >  Retrying Phidget{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))
					self.loadcell_app()
		else:
			self.logTextBox.append("  >  Phidget already attached{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))

	def send_info(self,command):
		#Function that sends commands to server and listens for some responses
		'''
		#########RELAYS###########
		relay 1: LOX HI VALVE
		relay 2: METH HI VALVE
		relay 3: METH VENT VALVE
		relay 4: LOX VENT VALVE
		relay 5: METH MPV
		relay 6: LOX MPV
		relay 7: Nothing
		relay 8: PURGE
		'''
		if command == 'lho':
			message = b'LOX_HI_open'
			logger.debug("LOX HI Open at {}".format(time.asctime()))
		elif command == 'lhc':
			message = b'LOX_HI_close'
			logger.debug("LOX HI Close at {}".format(time.asctime()))
		elif command == 'mho':
			message = b'METH_HI_open'
			logger.debug("METH HI Open at {}".format(time.asctime()))
		elif command == 'mhc':
			message = b'METH_HI_close'
			logger.debug("METH HI Close at {}".format(time.asctime()))
		elif command == 'mvo':
			message = b'METH_VENT_open'
			logger.debug("METH Vent Open at {}".format(time.asctime()))
		elif command == 'mvc':
			message = b'METH_VENT_close'
			logger.debug("METH Vent Close at {}".format(time.asctime()))
		elif command == 'lvo':
			message = b'LOX_VENT_open'
			logger.debug("LOX Vent Open at {}".format(time.asctime()))
		elif command == 'lvc':
			message = b'LOX_VENT_close'
			logger.debug("LOX Vent Close at {}".format(time.asctime()))
		elif command == 'mmo':
			message = b'METH_MPV_open'
			logger.debug("METH MPV Open at {}".format(time.asctime()))
		elif command == 'mmc':
			message = b'METH_MPV_close'
			logger.debug("METH MPV Close at {}".format(time.asctime()))
		elif command == 'lmo':
			message = b'LOX_MPV_open'
			logger.debug("LOX MPV Open at {}".format(time.asctime()))
		elif command == 'lmc':
			message = b'LOX_MPV_close'
			logger.debug("LOX MPV Close at {}".format(time.asctime()))
		elif command == 'po':
			message = b'PURGE_open'
			logger.debug("Purge Open at {}".format(time.asctime()))
		elif command == 'pc':
			message = b'PURGE_close'
			logger.debug("Purge Close at {}".format(time.asctime()))
		elif command == 'vo':
			message = b'VENTS_open'
			logger.debug("Vents Open at {}".format(time.asctime()))
		elif command == 'vc':
			message = b'VENTS_close'
			logger.debug("Vents Close at {}".format(time.asctime()))
		elif command == 'mo':
			message = b'MAIN_open'
			logger.debug("Main Open at {}".format(time.asctime()))
		elif command == 'mc':
			message = b'MAIN_close'
			logger.debug("Main Close at {}".format(time.asctime()))
		elif command == 'ion':
			message = b'IGNITE_on'
			logger.debug("Ignitor On at {}".format(time.asctime()))
		elif command == 'ioff':
			message = b'IGNITE_off'
			logger.debug("Ignitor Off at {}".format(time.asctime()))
		elif command == 'abort':
			message = b'abort'
			logger.debug("aborting at {}".format(time.asctime()))
		elif command == 'Ro7':
			message = b'relay7_open'
			logger.debug(" at {}".format(time.asctime()))
		elif command == 'Rc7':
			message = b'relay7_close'
			logger.debug(" at {}".format(time.asctime()))

		print('publishing: {}'.format(message))
		self.client.publish(self.TOPIC_1,message)

	def get_info(self, data):
		print(data)
		# Receives information from the server and switches the label based on what the client is given
		'''
		#########RELAYS###########
		relay 1: LOX HI VALVE
		relay 2: METH HI VALVE
		relay 3: METH VENT VALVE
		relay 4: LOX VENT VALVE
		relay 5: METH MPV
		relay 6: LOX MPV
		relay 7: Nothing
		relay 8: PURGE
		'''
		if 'LOXHIOPEN' in data:
			logger.debug("LOX HI OPEN at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  LOX HI OPEN!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.lox_hi_open_btn.setEnabled(False)
			self.lox_hi_close_btn.setEnabled(True)

		elif 'METHHIOPEN' in data:
			logger.debug("METH HI OPEN at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  METH HI OPEN!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.meth_hi_open_btn.setEnabled(False)
			self.meth_hi_close_btn.setEnabled(True)

		elif 'METHVENTOPEN' in data:
			logger.debug("METH VENT OPEN at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  METH VENT OPEN!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.meth_vent_open_btn.setEnabled(False)
			self.meth_vent_close_btn.setEnabled(True)

		elif 'LOXVENTOPEN' in data:
			logger.debug("LOX VENT OPEN at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  LOX VENT OPEN!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.lox_vent_open_btn.setEnabled(False)
			self.lox_vent_close_btn.setEnabled(True)

		elif 'METHMPVOPEN' in data:
			logger.debug("METH MPV OPEN at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  METH MPV OPEN!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.meth_mpv_open_btn.setEnabled(False)
			self.meth_mpv_close_btn.setEnabled(True)

		elif 'LOXMPVOPEN' in data:
			logger.debug("LOX MPV OPEN at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  LOX MPV OPEN!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.lox_mpv_open_btn.setEnabled(False)
			self.lox_mpv_close_btn.setEnabled(True)

		elif 'PURGEOPEN' in data:
			logger.debug("PURGE OPEN at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  PURGE OPEN!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.purge_open_btn.setEnabled(False)
			self.purge_close_btn.setEnabled(True)

		elif 'VENTSOPEN' in data:
			logger.debug("VENTS OPEN at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  VENTS OPEN!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.vents_open_btn.setEnabled(False)
			self.vents_close_btn.setEnabled(True)
			self.meth_vent_open_btn.setEnabled(False)
			self.meth_vent_close_btn.setEnabled(True)
			self.lox_vent_open_btn.setEnabled(False)
			self.lox_vent_close_btn.setEnabled(True)

		elif 'MAINOPEN' in data:
			logger.debug("MAIN OPEN at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  MAIN OPEN!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.mpv_open_btn.setEnabled(False)
			self.mpv_close_btn.setEnabled(True)
			self.meth_mpv_open_btn.setEnabled(False)
			self.meth_mpv_close_btn.setEnabled(True)
			self.lox_mpv_open_btn.setEnabled(False)
			self.lox_mpv_close_btn.setEnabled(True)

		elif 'IGNITEON' in data:
			logger.debug("IGNITOR ON at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  IGNITOR ON!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.ignitor_on_btn.setEnabled(False)
			self.ignitor_off_btn.setEnabled(True)

		elif 'R7ON' in data:
			logger.debug("Relay_7_ON at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  Relay 7 ON!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.so7_btn.setEnabled(False)
			self.sc7_btn.setEnabled(True)

		elif 'LOXHICLOSE' in data:
			logger.debug("LOX HI CLOSE at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  LOX HI CLOSE!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.lox_hi_open_btn.setEnabled(True)
			self.lox_hi_close_btn.setEnabled(False)

		elif 'METHHICLOSE' in data:
			logger.debug("METH HI CLOSE at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  METH HI CLOSE!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.meth_hi_open_btn.setEnabled(True)
			self.meth_hi_close_btn.setEnabled(False)

		elif 'METHVENTCLOSE' in data:
			logger.debug("METH VENT CLOSE at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  METH VENT CLOSE!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.meth_vent_open_btn.setEnabled(True)
			self.meth_vent_close_btn.setEnabled(False)

		elif 'LOXVENTCLOSE' in data:
			logger.debug("LOX VENT CLOSE at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  LOX VENT CLOSE!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.lox_vent_open_btn.setEnabled(True)
			self.lox_vent_close_btn.setEnabled(False)

		elif 'METHMPVCLOSE' in data:
			logger.debug("METH MPV CLOSE at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  METH MPV CLOSE!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.meth_mpv_open_btn.setEnabled(True)
			self.meth_mpv_close_btn.setEnabled(False)

		elif 'LOXMPVCLOSE' in data:
			logger.debug("LOX MPV CLOSE at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  LOX MPV CLOSE!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.lox_mpv_open_btn.setEnabled(True)
			self.lox_mpv_close_btn.setEnabled(False)

		elif 'PURGECLOSE' in data:
			logger.debug("PURGE CLOSE at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  PURGE CLOSE!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.purge_open_btn.setEnabled(True)
			self.purge_close_btn.setEnabled(False)

		elif 'VENTSCLOSE' in data:
			logger.debug("VENTS CLOSE at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  VENTS CLOSE!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.vents_open_btn.setEnabled(True)
			self.vents_close_btn.setEnabled(False)
			self.meth_vent_open_btn.setEnabled(True)
			self.meth_vent_close_btn.setEnabled(False)
			self.lox_vent_open_btn.setEnabled(True)
			self.lox_vent_close_btn.setEnabled(False)

		elif 'MAINCLOSE' in data:
			logger.debug("MAIN CLOSE at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  MAIN CLOSE!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.mpv_open_btn.setEnabled(True)
			self.mpv_close_btn.setEnabled(False)
			self.meth_mpv_open_btn.setEnabled(True)
			self.meth_mpv_close_btn.setEnabled(False)
			self.lox_mpv_open_btn.setEnabled(True)
			self.lox_mpv_close_btn.setEnabled(False)

		elif 'IGNITEOFF' in data:
			logger.debug("IGNITOR OFF at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  IGNITOR OFF!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.ignitor_on_btn.setEnabled(True)
			self.ignitor_off_btn.setEnabled(False)

		elif 'ABORT' in data:
			logger.debug("ABORTED at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  ABORTED!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.mpv_open_btn.setEnabled(True)
			self.mpv_close_btn.setEnabled(False)
			self.meth_mpv_open_btn.setEnabled(True)
			self.meth_mpv_close_btn.setEnabled(False)
			self.lox_mpv_open_btn.setEnabled(True)
			self.lox_mpv_close_btn.setEnabled(False)
			self.vents_open_btn.setEnabled(False)
			self.vents_close_btn.setEnabled(True)
			self.meth_vent_open_btn.setEnabled(False)
			self.meth_vent_close_btn.setEnabled(True)
			self.lox_vent_open_btn.setEnabled(False)
			self.lox_vent_close_btn.setEnabled(True)
			self.meth_hi_open_btn.setEnabled(True)
			self.meth_hi_close_btn.setEnabled(False)
			self.lox_hi_open_btn.setEnabled(True)
			self.lox_hi_close_btn.setEnabled(False)

		elif 'R7OFF' in data:
			logger.debug("Relay_7_OFF at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  Relay 7 OFF!{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			self.so7_btn.setEnabled(True)
			self.sc7_btn.setEnabled(False)


	def paintEvent(self, e):

		# sets up the "paint brush" in order to use the drawLines function

		qp = QPainter()
		qp.begin(self)
		self.drawLines(qp)
		qp.end()

	def drawLines(self, qp):

		# draws the lines found in the program

		pen = QPen(Qt.black, 4, Qt.SolidLine)
		qp.setPen(pen)
		qp.drawLine(20, 375, 950, 375)
		#qp.drawLine(self.testStandCenter+178, self.testStandDepth+30, self.testStandCenter+210, self.testStandDepth+10)
		#qp.drawLine(self.testStandCenter+210, self.testStandDepth+10, self.testStandCenter+420, self.testStandDepth+10)
		#qp.drawLine(self.testStandCenter-178, self.testStandDepth+30, self.testStandCenter-210, self.testStandDepth+10)
		#qp.drawLine(self.testStandCenter-210, self.testStandDepth+10, self.testStandCenter-420, self.testStandDepth+10)

		#qp.drawLine(self.testStandCenter+178, self.testStandDepth+29, 950, 100)
		#qp.drawLine(307.5, 260, 307.5, 730)


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

	def on_connect(self, client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		self.error = rc
		self.connectionsymbol.setPixmap(QPixmap('pictures/pinggreen.png'))
		self.client.subscribe(self.TOPIC_2)
		#self.client.publish(self.TOPIC_1,b'give_states')
		return self.error

	def on_disconnect(client, userdata,rc=0):
		self.logTextBox.append("  >  Connection Lost...{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
		self.connectionsymbol.setPixmap(QPixmap('pictures/pingred.png'))
		self.client.loop_stop()

	def on_message(self, client, userdata, msg):
		print(str(msg.payload))
		self.get_info(str(msg.payload))

	def connect_app(self):

		self.logTextBox.append("  >  Connecting...{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))

		try:
			self.client = mqtt.Client()
			self.client.on_connect = self.on_connect
			self.client.on_message = self.on_message
			#self.client.on_publish = self.on_publish
			self.client.on_disconnect = self.on_disconnect
			self.client.connect(self.HOST, 1883, 60)
			QMessageBox.information(self, 'Connection Results', 'Socket Successfully Bound.\nClick "Read Statuses " to start')
			self.connection_status = True
			self.logTextBox.append("  >  Connected{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			#self.connectionsymbol.setPixmap(QPixmap('pictures/pinggreen.png'))
			logger.debug("Connection Successful at {}".format(time.asctime()))
			self.client.loop_start()

		except:
			logger.debug("Connection Unsuccessful at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			self.logTextBox.append("  >  Connection Unsuccessful{}".format(time.strftime("\t     -\t(%H:%M:%S)", time.localtime())))
			reply = QMessageBox.critical(self, "Connection Results", "Couldn't connect to {} at {}.\nMake sure server is listening.".format(self.server_address[0],self.server_address[1]),
													QMessageBox.Cancel | QMessageBox.Retry)
			if reply == QMessageBox.Cancel:
				self.logTextBox.append("  >  Connection Canceled{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))
			elif reply == QMessageBox.Retry:
				self.logTextBox.append("  >  Retrying Connection{}".format(time.strftime(" -\t(%H:%M:%S)", time.localtime())))
				self.connect_app()


	def close_app(self):
		# exits GUI
		self.logTextBox.append(">  Exiting...{}".format(time.strftime("\t-           (%H:%M:%S)", time.localtime())))
		choice = QMessageBox.question(self, "Confirmation.", "Are you sure you want to exit?",
												QMessageBox.Yes | QMessageBox.No)
		if choice == QMessageBox.Yes:
			print("System Closed")
			logger.debug("Application Exited at {}".format(time.strftime("(%H:%M:%S)", time.localtime())))
			sys.exit()
		else:
			self.logTextBox.append("> Exit Stopped{}".format(time.strftime("\t-         (%H:%M:%S)", time.localtime())))

	def animations(self,data):

		if data == "engine_up" and self.engineInit <= 186:
			self.engineInit += 9.3
			self.engineInit_Move += 9.3/2
			self.engineHot.move(self.testStandCenter-40,self.testStandDepth+843-self.engineInit_Move)
			self.engineHot.resize(80, self.engineInit)
			#self.engineHot.move(685, engineInit_move)
		elif data == "engine_down" and self.engineInit >= 9.3:
			self.engineInit -= 9.3
			self.engineInit_Move -= 9.3/2
			self.engineHot.resize(80, self.engineInit)
			self.engineHot.move(self.testStandCenter-40,self.testStandDepth+843-self.engineInit_Move)
		elif data == "tank_1_up" and self.tank_1_Init <= 1212:
			if self.tank_1_Init == 1212:
				self.blue.setPixmap(QPixmap('pictures/green.png'))
			self.tank_1_Init += 12
			self.tank_1_Init_Move += 12/2
			self.blue.move(self.testStandCenter-203, self.testStandDepth+668-self.tank_1_Init_Move)
			self.blue.resize(47, self.tank_1_Init)
		elif data == "tank_1_down" and self.tank_1_Init >= 12:
			if self.tank_1_Init <= 1224:
				self.blue.setPixmap(QPixmap('pictures/blue.png'))
			self.tank_1_Init -= 12
			self.tank_1_Init_Move -= 12/2
			self.blue.move(self.testStandCenter-203, self.testStandDepth+668-self.tank_1_Init_Move)
			self.blue.resize(47, self.tank_1_Init)
		elif data == "tank_2_up" and self.tank_2_Init <= 1212:
			if self.tank_2_Init == 1212:
				self.purple.setPixmap(QPixmap('pictures/green.png'))
			self.tank_2_Init += 12
			self.tank_2_Init_Move += 12/2
			self.purple.move(self.testStandCenter+153, self.testStandDepth+668-self.tank_2_Init_Move)
			self.purple.resize(47, self.tank_2_Init)
		elif data == "tank_2_down" and self.tank_2_Init >= 12:
			if self.tank_2_Init <= 1224:
				self.purple.setPixmap(QPixmap('pictures/purple.png'))
			self.tank_2_Init -= 12
			self.tank_2_Init_Move -= 12/2
			self.purple.move(self.testStandCenter+153, self.testStandDepth+668-self.tank_2_Init_Move)
			self.purple.resize(47, self.tank_2_Init)


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





'''self.toggle_1 = createButton(self,'',100,200,100,100,True,self.font5,self.toggler_1,'icon.png',100,100)
		self.toggle_2 = createButton(self,'',100,320,100,100,True,self.font5,self.toggler_2,'icon.png',100,100)
		self.toggle_3 = createButton(self,'',100,500,100,100,True,self.font5,self.toggler_3,'icon.png',100,100)
		self.toggle_4 = createButton(self,'',100,630,100,100,True,self.font5,self.toggler_4,'icon.png',100,100)
		self.toggle_5 = createButton(self,'',220,350,100,100,True,self.font5,self.toggler_5,'icon.png',100,100)
		self.toggle_6 = createButton(self,'',220,480,100,100,True,self.font5,self.toggler_6,'icon.png',100,100)
		#toggle_5 = createButton(self,'Toggle_2',400,70,290,170,True,self.font5,self.toggler_2,'',100,100)
		#toggle_6 = createButton(self,'Toggle_3',700,70,290,170,True,self.font5,self.toggler_3,'icon.png',100,100)

		#self.toggle_1.setStyleSheet("background-color: white")

	def toggler_1(self):
		#s.send(b'relay_1')
		self.animations("engine_up")

	def toggler_2(self):
		#s.send(b'relay_2')
		self.animations("engine_down")

	def toggler_3(self):
		#s.send(b'relay_3')
		self.animations("tank_1_up")

	def toggler_4(self):
		#s.send(b'relay_3')
		self.animations("tank_1_down")

	def toggler_5(self):
		#s.send(b'relay_3')
		self.animations("tank_2_up")

	def toggler_6(self):
		#s.send(b'relay_3')
		self.animations("tank_2_down")'''