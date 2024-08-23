from PyQt6 import QtCore, QtGui, QtWidgets
import sys,chessMain,random,pickle,webbrowser,platform

#global variables
skinIndex = 0 #set to default skin
saveFilePath = ''
ospath =  '' if platform.system() == 'Darwin' else '.' #added to fix os relative path issue
def macToWindowsPath(path : str):
    return path.replace('/',chr(92)) if ospath == '.' else path #can't use '\' as literal error occurs 

class mainMenu(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setWindowTitle("SCACCHIRO - A New Experience Of Chess")
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.BackRound = QtWidgets.QLabel(self.centralwidget)
        self.BackRound.setGeometry(QtCore.QRect(-70, -70, 1431, 791))
        self.BackRound.setMinimumSize(QtCore.QSize(1280, 720))
        self.BackRound.setText("")
        self.BackRound.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/NewBackroundP.png")))
        self.BackRound.setObjectName("BackRound")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(640, -60, 651, 211))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/titleRedone.png")))
        self.label.setObjectName("label")
        self.NewGameButton = QtWidgets.QPushButton(self.centralwidget)
        self.NewGameButton.setGeometry(QtCore.QRect(10, 330, 191, 101))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.NewGameButton.setFont(font)
        self.NewGameButton.setObjectName("NewGameButton")
        self.ContinueGameButton = QtWidgets.QPushButton(self.centralwidget)
        self.ContinueGameButton.setGeometry(QtCore.QRect(10, 430, 191, 101))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(18)
        font.setItalic(True)
        self.ContinueGameButton.setFont(font)
        self.ContinueGameButton.setObjectName("ContinueGameButton")
        self.SkinButton = QtWidgets.QPushButton(self.centralwidget)
        self.SkinButton.setGeometry(QtCore.QRect(110, 530, 90, 101))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(24)
        self.SkinButton.setFont(font)
        self.SkinButton.setObjectName("SkinButton")
        self.TutButton = QtWidgets.QPushButton(self.centralwidget)
        self.TutButton.setGeometry(QtCore.QRect(10, 530, 90, 101))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(18)
        font.setItalic(True)
        self.TutButton.setFont(font)
        self.TutButton.setObjectName("TutButton")
        self.Leave = QtWidgets.QPushButton(self.centralwidget)
        self.Leave.setGeometry(QtCore.QRect(1200, 600, 75, 75))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(24)
        self.Leave.setFont(font)
        self.Leave.setObjectName("Leave")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        #changing the colour of push buttons to make more visisble
        self.NewGameButton.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid rgb(135,206,250)
            }""")
        self.ContinueGameButton.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid rgb(135,206,250)
            }""")
        self.TutButton.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid rgb(135,206,250)
            }""")
        self.SkinButton.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid rgb(135,206,250)
            }""")
        self.Leave.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid rgb(135,206,250)
            }""")
        #Button Functions
        self.NewGameButton.clicked.connect(self.newGameClicked)
        self.ContinueGameButton.clicked.connect(self.contGameClicked)
        self.SkinButton.clicked.connect(self.skinsPressed)
        self.TutButton.clicked.connect(self.tutPressed)
        self.Leave.clicked.connect(self.exitG)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.NewGameButton.setText(_translate("MainWindow", "New Game"))
        self.ContinueGameButton.setText(_translate("MainWindow", "Continue Game"))
        self.SkinButton.setText(_translate("MainWindow", "Skins"))
        self.TutButton.setText(_translate("MainWindow", "Tutorial"))
        self.Leave.setText(_translate("MainWindow", "Exit"))
    
    def newGameClicked(self):
        menus.setCurrentIndex(menus.currentIndex()+1)
    def contGameClicked(self):
        menus.setCurrentIndex(menus.currentIndex()+2)
    def skinsPressed(self):
        menus.setCurrentIndex(menus.currentIndex()+3)
    def tutPressed(self):
        webbrowser.open('https://youtu.be/7NdSL2iQsWA')
    def exitG(self):
        exit()


class newGameMenu(object):
    def setupUi(self, NewGameWindow):
        NewGameWindow.setObjectName("NewGameWindow")
        NewGameWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(NewGameWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.BackRound = QtWidgets.QLabel(self.centralwidget)
        self.BackRound.setGeometry(QtCore.QRect(-70, -70, 1431, 791))
        self.BackRound.setMinimumSize(QtCore.QSize(1280, 720))
        self.BackRound.setText("")
        self.BackRound.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/NewBackroundP.png")))
        self.BackRound.setObjectName("BackRound")
        self.NewGame = QtWidgets.QLabel(self.centralwidget)
        self.NewGame.setGeometry(QtCore.QRect(770, -30, 541, 151))
        self.NewGame.setText("")
        self.NewGame.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/NewGametxt.png")))
        self.NewGame.setScaledContents(True)
        self.NewGame.setObjectName("NewGame")
        self.General = QtWidgets.QLabel(self.centralwidget)
        self.General.setGeometry(QtCore.QRect(1090, 120, 171, 71))
        self.General.setText("")
        self.General.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/generaltxr.png")))
        self.General.setScaledContents(True)
        self.General.setObjectName("General")
        self.Timer = QtWidgets.QLabel(self.centralwidget)
        self.Timer.setGeometry(QtCore.QRect(1110, 220, 130, 60))
        self.Timer.setText("")
        self.Timer.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/timertxt.png")))
        self.Timer.setScaledContents(True)
        self.Timer.setObjectName("Timer")
        self.MoveLog = QtWidgets.QLabel(self.centralwidget)
        self.MoveLog.setGeometry(QtCore.QRect(1100, 320, 161, 60))
        self.MoveLog.setText("")
        self.MoveLog.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/movelog text.png")))
        self.MoveLog.setScaledContents(True)
        self.MoveLog.setObjectName("MoveLog")
        self.Abilities = QtWidgets.QLabel(self.centralwidget)
        self.Abilities.setGeometry(QtCore.QRect(30, 20, 171, 71))
        self.Abilities.setText("")
        self.Abilities.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/abilitiestxt.png")))
        self.Abilities.setScaledContents(True)
        self.Abilities.setObjectName("Abilities")
        self.Impervious = QtWidgets.QLabel(self.centralwidget)
        self.Impervious.setGeometry(QtCore.QRect(20, 100, 191, 91))
        self.Impervious.setText("")
        self.Impervious.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/impervious text.png")))
        self.Impervious.setScaledContents(True)
        self.Impervious.setObjectName("Impervious")
        self.Tether = QtWidgets.QLabel(self.centralwidget)
        self.Tether.setGeometry(QtCore.QRect(20, 220, 191, 81))
        self.Tether.setText("")
        self.Tether.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/tehtertct.png")))
        self.Tether.setScaledContents(True)
        self.Tether.setObjectName("Tether")
        self.Interchange = QtWidgets.QLabel(self.centralwidget)
        self.Interchange.setGeometry(QtCore.QRect(10, 330, 201, 91))
        self.Interchange.setText("")
        self.Interchange.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/interchangetxt.png")))
        self.Interchange.setScaledContents(True)
        self.Interchange.setObjectName("Interchange")
        self.Triumvirate = QtWidgets.QLabel(self.centralwidget)
        self.Triumvirate.setGeometry(QtCore.QRect(-10, 440, 261, 101))
        self.Triumvirate.setText("")
        self.Triumvirate.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/triumvirate.png")))
        self.Triumvirate.setScaledContents(True)
        self.Triumvirate.setObjectName("Triumvirate")
        self.cooldown = QtWidgets.QLabel(self.centralwidget)
        self.cooldown.setGeometry(QtCore.QRect(270, 30, 131, 51))
        self.cooldown.setText("")
        self.cooldown.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/cooldowntxt.png")))
        self.cooldown.setScaledContents(True)
        self.cooldown.setObjectName("cooldown")
        self.uses = QtWidgets.QLabel(self.centralwidget)
        self.uses.setGeometry(QtCore.QRect(480, 30, 81, 51))
        self.uses.setText("")
        self.uses.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/usestxt.png")))
        self.uses.setScaledContents(True)
        self.uses.setObjectName("uses")
        self.active = QtWidgets.QLabel(self.centralwidget)
        self.active.setGeometry(QtCore.QRect(630, 20, 130, 60))
        self.active.setText("")
        self.active.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/activetxt.png")))
        self.active.setScaledContents(True)
        self.active.setObjectName("active")
        self.impCool = QtWidgets.QSpinBox(self.centralwidget)
        self.impCool.setGeometry(QtCore.QRect(300, 130, 71, 31))
        self.impCool.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.impCool.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.impCool.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.impCool.setProperty("showGroupSeparator", False)
        self.impCool.setObjectName("impCool")
        self.impCool.setMinimum(1)
        self.impUse = QtWidgets.QSpinBox(self.centralwidget)
        self.impUse.setGeometry(QtCore.QRect(480, 130, 71, 31))
        self.impUse.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.impUse.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.impUse.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.impUse.setProperty("showGroupSeparator", False)
        self.impUse.setObjectName("impUse")
        self.impActive = QtWidgets.QSpinBox(self.centralwidget)
        self.impActive.setGeometry(QtCore.QRect(665, 130, 71, 31))
        self.impActive.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.impActive.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.impActive.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.impActive.setProperty("showGroupSeparator", False)
        self.impActive.setObjectName("impActive")
        self.tethCool = QtWidgets.QSpinBox(self.centralwidget)
        self.tethCool.setGeometry(QtCore.QRect(300, 250, 71, 31))
        self.tethCool.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tethCool.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.tethCool.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.tethCool.setProperty("showGroupSeparator", False)
        self.tethCool.setObjectName("tethCool")
        self.tethCool.setMinimum(1)
        self.tethUse = QtWidgets.QSpinBox(self.centralwidget)
        self.tethUse.setGeometry(QtCore.QRect(480, 250, 71, 31))
        self.tethUse.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tethUse.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.tethUse.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.tethUse.setProperty("showGroupSeparator", False)
        self.tethUse.setObjectName("tethUse")
        self.tethActive = QtWidgets.QSpinBox(self.centralwidget)
        self.tethActive.setGeometry(QtCore.QRect(665, 250, 71, 31))
        self.tethActive.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tethActive.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.tethActive.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.tethActive.setProperty("showGroupSeparator", False)
        self.tethActive.setObjectName("tethActive")
        self.intCool = QtWidgets.QSpinBox(self.centralwidget)
        self.intCool.setGeometry(QtCore.QRect(300, 360, 71, 31))
        self.intCool.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.intCool.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.intCool.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.intCool.setProperty("showGroupSeparator", False)
        self.intCool.setObjectName("intCool")
        self.intCool.setMinimum(1)
        self.intUses = QtWidgets.QSpinBox(self.centralwidget)
        self.intUses.setGeometry(QtCore.QRect(480, 360, 71, 31))
        self.intUses.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.intUses.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.intUses.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.intUses.setProperty("showGroupSeparator", False)
        self.intUses.setObjectName("intUses")
        self.triCool = QtWidgets.QSpinBox(self.centralwidget)
        self.triCool.setGeometry(QtCore.QRect(300, 480, 71, 31))
        self.triCool.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.triCool.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.triCool.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.triCool.setProperty("showGroupSeparator", False)
        self.triCool.setObjectName("triCool")
        self.triCool.setMinimum(1)
        self.triUses = QtWidgets.QSpinBox(self.centralwidget)
        self.triUses.setGeometry(QtCore.QRect(480, 480, 71, 31))
        self.triUses.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.triUses.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.PlusMinus)
        self.triUses.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.triUses.setProperty("showGroupSeparator", False)
        self.triUses.setObjectName("triUses")
        self.timerCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.timerCheck.setGeometry(QtCore.QRect(1080, 230, 21, 31))
        self.timerCheck.setText("")
        self.timerCheck.setIconSize(QtCore.QSize(32, 32))
        self.timerCheck.setChecked(False)
        self.timerCheck.setTristate(False)
        self.timerCheck.setObjectName("timerCheck")
        self.moveCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.moveCheck.setGeometry(QtCore.QRect(1080, 340, 87, 20))
        self.moveCheck.setText("")
        self.moveCheck.setObjectName("moveCheck")
        self.StartGameButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartGameButton.setGeometry(QtCore.QRect(1090, 580, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(24)
        font.setItalic(True)
        self.StartGameButton.setFont(font)
        self.StartGameButton.setMouseTracking(False)
        self.StartGameButton.setCheckable(False)
        self.StartGameButton.setChecked(False)
        self.StartGameButton.setObjectName("StartGameButton")
        self.DefaultSettings = QtWidgets.QPushButton(self.centralwidget)
        self.DefaultSettings.setGeometry(QtCore.QRect(140, 580, 171, 81))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(24)
        font.setItalic(True)
        self.DefaultSettings.setFont(font)
        self.DefaultSettings.setMouseTracking(False)
        self.DefaultSettings.setCheckable(False)
        self.DefaultSettings.setChecked(False)
        self.DefaultSettings.setObjectName("DefaultSettings")
        self.BackButton = QtWidgets.QPushButton(self.centralwidget)
        self.BackButton.setGeometry(QtCore.QRect(20, 580, 101, 81))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(24)
        self.BackButton.setFont(font)
        self.BackButton.setObjectName("BackButton")
        NewGameWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(NewGameWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 24))
        self.menubar.setObjectName("menubar")
        NewGameWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(NewGameWindow)
        self.statusbar.setObjectName("statusbar")
        NewGameWindow.setStatusBar(self.statusbar)
        
        #initialises all inputs to my recommended settings
        self.defaultPressed()

        #Changing backround of buttons
        self.StartGameButton.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid rgb(135,206,250)
            }""")
        self.BackButton.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid #DB6A6C
            }""")
        self.DefaultSettings.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid rgb(135,206,250)
            }""")
        #button signal connections
        self.DefaultSettings.clicked.connect(self.defaultPressed)
        self.BackButton.clicked.connect(self.backPressed)
        self.StartGameButton.clicked.connect(self.startGamePressed)
        
        self.retranslateUi(NewGameWindow)
        QtCore.QMetaObject.connectSlotsByName(NewGameWindow)

    def retranslateUi(self, NewGameWindow):
        _translate = QtCore.QCoreApplication.translate
        NewGameWindow.setWindowTitle(_translate("NewGameWindow", "SCACCHIRO - New Game"))
        self.StartGameButton.setText(_translate("NewGameWindow", "Start Game"))
        self.DefaultSettings.setText(_translate("NewGameWindow", "Default "))
        self.BackButton.setText(_translate("NewGameWindow", "Back"))
    
    def defaultPressed(self): #resets all inputs to my recommended settings
        self.impActive.setValue(4)
        self.impCool.setValue(10)
        self.impUse.setValue(5)
        self.tethActive.setValue(1)
        self.tethCool.setValue(10)
        self.tethUse.setValue(5)
        self.intCool.setValue(1)
        self.intUses.setValue(1)
        self.triCool.setValue(1)
        self.triUses.setValue(1)
        self.moveCheck.setChecked(True)
        self.timerCheck.setChecked(False)
    
    def backPressed(self):
        menus.setCurrentIndex(menus.currentIndex()-1)
    
    def startGamePressed(self):
        #grab values and states
        trueActive = [self.impActive.value(),self.tethActive.value()]
        trueCool = [self.impCool.value(),self.tethCool.value(),self.triCool.value(),self.intCool.value()]
        uses = [self.impUse.value(),self.tethUse.value(),self.triUses.value(),self.intUses.value()]
        ready = []
        for use in uses: #added due to tp21  | allows for disabling abilities
            ready.append(False) if use == 0 else ready.append(True) #creates ready list
        timerFlag = self.timerCheck.isChecked()
        logFlag = self.moveCheck.isChecked()
        #close main menu and initialise game
        menus.hide()
        chessMain.main(timerFlag,logFlag,skinIndex,None,trueActive,trueCool,uses,ready)
        #after exiting reopen windows
        menus.setCurrentIndex(menus.currentIndex()-1) #reopen on main page
        menus.show()
        


class Ui_ContinueGameMenu(object):
    def setupUi(self, ContinueGameMenu):
        ContinueGameMenu.setObjectName("ContinueGameMenu")
        ContinueGameMenu.resize(1280, 720)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ContinueGameMenu.sizePolicy().hasHeightForWidth())
        ContinueGameMenu.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(ContinueGameMenu)
        self.centralwidget.setObjectName("centralwidget")
        self.BackRound = QtWidgets.QLabel(self.centralwidget)
        self.BackRound.setGeometry(QtCore.QRect(-70, -70, 1431, 791))
        self.BackRound.setMinimumSize(QtCore.QSize(1280, 720))
        self.BackRound.setText("")
        self.BackRound.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/NewBackroundP.png")))
        self.BackRound.setObjectName("BackRound")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(730, -30, 571, 131))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/continueGame.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(1160, 590, 121, 91))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(24)
        self.backButton.setFont(font)
        self.backButton.setObjectName("backButton")
        self.contStarttGame = QtWidgets.QPushButton(self.centralwidget)
        self.contStarttGame.setGeometry(QtCore.QRect(0, 590, 241, 91))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(36)
        self.contStarttGame.setFont(font)
        self.contStarttGame.setObjectName("contStarttGame")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 300, 1011, 81))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(36)
        self.lineEdit.setFont(font)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.browse = QtWidgets.QPushButton(self.centralwidget)
        self.browse.setGeometry(QtCore.QRect(1100, 300, 151, 81))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(24)
        self.browse.setFont(font)
        self.browse.setObjectName("browse")
        ContinueGameMenu.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ContinueGameMenu)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 24))
        self.menubar.setObjectName("menubar")
        ContinueGameMenu.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ContinueGameMenu)
        self.statusbar.setObjectName("statusbar")
        ContinueGameMenu.setStatusBar(self.statusbar)

        self.retranslateUi(ContinueGameMenu)
        QtCore.QMetaObject.connectSlotsByName(ContinueGameMenu)

        #updating style of buttons & textbox
        self.contStarttGame.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid rgb(135,206,250)
            }""")
        self.browse.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid rgb(135,206,250)
            }""")
        self.backButton.setStyleSheet("""QPushButton {
            background-color : rgba(0,0,000,130); color: white;
            }
            QPushButton:hover {
            border : 3px solid #DB6A6C
            }""")
        self.lineEdit.setStyleSheet("""QLineEdit {
            background-color : rgba(0,0,000,130); color: white;
            }
            QLineEdit {
            border : 1px solid rgb(135,206,250)
            }""")
        
        #Button signal connections
        self.browse.clicked.connect(self.browsePressed)
        self.backButton.clicked.connect(self.backPressed)
        self.contStarttGame.clicked.connect(self.conPressed)


    def retranslateUi(self, ContinueGameMenu):
        _translate = QtCore.QCoreApplication.translate
        ContinueGameMenu.setWindowTitle(_translate("ContinueGameMenu", "ContinueGame"))
        self.backButton.setText(_translate("ContinueGameMenu", "Back"))
        self.contStarttGame.setText(_translate("ContinueGameMenu", "Start Game"))
        self.lineEdit.setText(_translate("ContinueGameMenu", "Filepath"))
        self.lineEdit.setPlaceholderText(_translate("ContinueGameMenu", "Filepath"))
        self.browse.setText(_translate("ContinueGameMenu", "Browse"))
    
    def browsePressed(self):
        global saveFilePath
        fileName = QtWidgets.QFileDialog.getOpenFileName(caption='Open SaveFile', filter='(*.savefile)') #opens file explorer and allows user to select a file to open |defensinve design only allowing savefiles to be selected
        saveFilePath = fileName[0]
        self.lineEdit.setText(saveFilePath) #the first element in fileName is the path of the file.

    def backPressed(self):
        menus.setCurrentIndex(menus.currentIndex()-2)
    
    def conPressed(self):
        if saveFilePath == '':
            self.lineEdit.setText('No File Selected') #defensive design
        else:
            with open(saveFilePath,"rb") as file: #open file
                loadedGs,timerFlg,logFlg,timeObj = tuple(pickle.load(file)) #load objects from file
            file.close()
            menus.hide()
            chessMain.main(timerFlg,logFlg,skinIndex,loadedGs,timer=timeObj) #pass into main and resume game 
            menus.setCurrentIndex(menus.currentIndex()-2) #go back to main menu
            menus.show() #reshow UI when game closes





class SkinMenu(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.BackRound = QtWidgets.QLabel(self.centralwidget)
        self.BackRound.setGeometry(QtCore.QRect(-70, -70, 1431, 791))
        self.BackRound.setMinimumSize(QtCore.QSize(1280, 720))
        self.BackRound.setText("")
        self.BackRound.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/NewBackroundP.png")))
        self.BackRound.setObjectName("BackRound")
        self.SelectSkin = QtWidgets.QLabel(self.centralwidget)
        self.SelectSkin.setGeometry(QtCore.QRect(830, -20, 471, 131))
        self.SelectSkin.setText("")
        self.SelectSkin.setPixmap(QtGui.QPixmap( macToWindowsPath("./ReqImgs/selectSkin.png")))
        self.SelectSkin.setScaledContents(True)
        self.SelectSkin.setObjectName("SelectSkin")
        self.chooseSkin = QtWidgets.QComboBox(self.centralwidget)
        self.chooseSkin.setGeometry(QtCore.QRect(100, 320, 381, 61))
        self.chooseSkin.setStyleSheet("QComboBox{\n"
        "background-color : rgba(0,0,000,130);\n"
        "border : 1px solid rgb(135,206,250); color: white;\n"
        "}\n"
        "QListView{\n"
        "font-size: 13px;\n"
        "background-color : rgba(0,0,000,130);\n"
        "}\n"
        "\n"
        "QListViewItem{\n"
        "padding-left: 10px\n"
        "backround-color : rgb(135,206,250)\n"
        "}\n"
        "QListView:item:hover{\n"
        "backround-color :  #fff;\n"
        "}")
        self.chooseSkin.setObjectName("chooseSkin")
        self.chooseSkin.addItem("")
        self.PreviewBox = QtWidgets.QLabel(self.centralwidget)
        self.PreviewBox.setGeometry(QtCore.QRect(620, 100, 500, 500))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(36)
        self.PreviewBox.setFont(font)
        self.PreviewBox.setStyleSheet("QLabel{\n"
        "background-color : rgba(0,0,000,130);\n"
        "border : 1px solid rgb(135,206,250);\n"
        "}\n"
        "")
        self.PreviewBox.setObjectName("PreviewBox")
        self.Random = QtWidgets.QPushButton(self.centralwidget)
        self.Random.setGeometry(QtCore.QRect(10, 570, 210, 101))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(24)
        self.Random.setFont(font)
        self.Random.setStyleSheet("QPushButton {\n"
        "        background-color : rgba(0,0,000,130); color: white;\n"
        "        }\n"
        "        QPushButton:hover {\n"
        "        border : 3px solid rgb(135,206,250)\n"
        "        }")
        self.Random.setObjectName("Random")
        self.BackButton = QtWidgets.QPushButton(self.centralwidget)
        self.BackButton.setGeometry(QtCore.QRect(1170, 570, 105, 101))
        font = QtGui.QFont()
        font.setFamily("Connection II")
        font.setPointSize(24)
        self.BackButton.setFont(font)
        self.BackButton.setStyleSheet("QPushButton {\n"
        "        background-color : rgba(0,0,000,130); color: white;\n"
        "        }\n"
        "        QPushButton:hover {\n"
        "        border : 3px solid #DB6A6C\n"
        "        }")
        self.BackButton.setObjectName("BackButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #appearance updates
        self.chooseSkin.addItem('Pixel')
        self.chooseSkin.addItem('Madware')
        self.PreviewBox.setPixmap(QtGui.QPixmap("./Skins/Previews/default.png"))
        #button and combobox signal connections
        self.chooseSkin.currentIndexChanged.connect(self.skinChanged)
        self.BackButton.clicked.connect(self.backPressed)
        self.Random.clicked.connect(self.randomPressed)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.chooseSkin.setItemText(0, _translate("MainWindow", "Default"))
        self.Random.setText(_translate("MainWindow", "Random"))
        self.BackButton.setText(_translate("MainWindow", "Back"))
    
    def skinChanged(self):
        global skinIndex
        indTofName = {0:'default',1 : 'Pixel',2:'Madware'} #converts from index of the combobox to the filenamme of the image required
        skinIndex = self.chooseSkin.currentIndex()
        name = indTofName[skinIndex]
        self.PreviewBox.setPixmap(QtGui.QPixmap(f"./Skins/Previews/{name}.png"))
    
    def backPressed(self):
        menus.setCurrentIndex(menus.currentIndex()-3)
    
    def randomPressed(self):
        self.chooseSkin.setCurrentIndex(random.randint(0,2))












def main():
    global menus,app,windows
    app = QtWidgets.QApplication(sys.argv)
    menuClasses = [mainMenu(),newGameMenu(),Ui_ContinueGameMenu(),SkinMenu()] 
    windows = [QtWidgets.QMainWindow() for _ in range(len(menuClasses))] #creates instances of the main window
    menus = QtWidgets.QStackedWidget()
    menus.setFixedHeight(720)
    menus.setFixedWidth(1280)
    for x in range(len(menuClasses)): # applies the contents of each class to their respective window in order
        menuClasses[x].setupUi(windows[x])
    for window in windows: # adds each window to the stacked widget
        menus.addWidget(window)
    menus.show()
    sys.exit(app.exec())

def openFolder():
    browser = QtWidgets.QFileDialog()#opens file explorer and allows user to a save path
    #browser.setFileMode(QtWidgets.QFileDialog.FileMode.Directory) #set to only open directories
    browser.setAcceptMode(QtWidgets.QFileDialog.AcceptMode.AcceptSave)
    filePath = browser.getSaveFileName(caption='Save File To') #open
    if filePath:
        return filePath[0] #the first element in fileName is the path of the folder.
    else:
        return None #if cancel is pressed
if __name__ == "__main__":
    main()
