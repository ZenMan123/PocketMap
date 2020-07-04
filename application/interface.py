from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(
            "#tell_button, #choose_button, #cities_button, #countries_button, #lakes_button, #lucky_button, #monuments_button, #mountains_button, #rivers_button, #waterfalls_button {\n"
            "    color: orange; \n"
            "    font-family: comic sans ms;\n"
            "     background-color: #151719; \n"
            "    border-style: solid; \n"
            "    border-color: white;\n"
            "    border-width: 2px;\n"
            "    border-radius: 7px;\n"
            "    \n"
            "}\n"
            "\n"
            "#tell_button:hover, #choose_button:hover, #cities_button:hover, #countries_button:hover, #lakes_button:hover, #lucky_button:hover, #monuments_button:hover, #mountains_button:hover, #rivers_button:hover, #waterfalls_button:hover\n"
            " {\n"
            "    background-color: #99ffcc;\n"
            "    color: blue;\n"
            "}\n"
            "\n"
            "\n"
            "#tell_button:pressed, #choose_button:pressed, #cities_button:pressed, #countries_button:pressed, #lakes_button:pressed, #lucky_button:pressed, #monuments_button:pressed, #mountains_button:pressed, #rivers_button:pressed, #waterfalls_button:pressed\n"
            " {\n"
            "    background-color: white;\n"
            "}\n"
            "\n"
            "#objects {\n"
            "    font-weight: bold;\n"
            "    color: #8AA8BD;\n"
            "    font-size: 16px;\n"
            "    border: 5px solid white;\n"
            "    border-radius: 10px;\n"
            "}\n"
            "\n"
            "\n"
            "#title {\n"
            "    color: orange;\n"
            "    font-size: 40px;\n"
            "    font-family: \'Century\';\n"
            "}\n"
            "#choose {\n"
            "    color: #ffffff;\n"
            "    font-family: ‘Lato’;\n"
            "    font-size: 20px;\n"
            "}\n"
            "\n"
            "QMainWindow {\n"
            "    background-color: #161a1f;\n"
            "}\n"
            "\n"
            "\n"
            "\n"
            "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(1500, 30, 291, 56))
        font = QtGui.QFont()
        font.setFamily("Century")
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setStyleSheet("")
        self.title.setObjectName("title")
        self.choose = QtWidgets.QLabel(self.centralwidget)
        self.choose.setGeometry(QtCore.QRect(1320, 125, 361, 41))
        font = QtGui.QFont()
        font.setFamily("‘Lato’")
        font.setPointSize(-1)
        self.choose.setFont(font)
        self.choose.setStyleSheet("")
        self.choose.setObjectName("choose")
        self.objects = QtWidgets.QComboBox(self.centralwidget)
        self.objects.setGeometry(QtCore.QRect(1690, 125, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setWeight(75)
        self.objects.setFont(font)
        self.objects.setStyleSheet("")
        self.objects.setEditable(True)
        self.objects.setCurrentText("")
        self.objects.setObjectName("objects")
        self.tell_button = QtWidgets.QPushButton(self.centralwidget)
        self.tell_button.setGeometry(QtCore.QRect(1550, 190, 141, 41))
        font = QtGui.QFont()
        font.setFamily("comic sans ms")
        font.setPointSize(15)
        self.tell_button.setFont(font)
        self.tell_button.setStyleSheet("")
        self.tell_button.setObjectName("tell_button")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(1370, 240, 501, 411))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.choose_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("comic sans ms")
        font.setPointSize(15)
        self.choose_button.setFont(font)
        self.choose_button.setStyleSheet("")
        self.choose_button.setObjectName("choose_button")
        self.gridLayout.addWidget(self.choose_button, 0, 0, 1, 1)
        self.countries_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("comic sans ms")
        font.setPointSize(15)
        self.countries_button.setFont(font)
        self.countries_button.setStyleSheet("")
        self.countries_button.setObjectName("countries_button")
        self.gridLayout.addWidget(self.countries_button, 0, 1, 1, 1)
        self.lakes_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("comic sans ms")
        font.setPointSize(15)
        self.lakes_button.setFont(font)
        self.lakes_button.setStyleSheet("")
        self.lakes_button.setObjectName("lakes_button")
        self.gridLayout.addWidget(self.lakes_button, 1, 1, 1, 1)
        self.monuments_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("comic sans ms")
        font.setPointSize(15)
        self.monuments_button.setFont(font)
        self.monuments_button.setStyleSheet("")
        self.monuments_button.setObjectName("monuments_button")
        self.gridLayout.addWidget(self.monuments_button, 2, 1, 1, 1)
        self.rivers_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("comic sans ms")
        font.setPointSize(15)
        self.rivers_button.setFont(font)
        self.rivers_button.setStyleSheet("")
        self.rivers_button.setObjectName("rivers_button")
        self.gridLayout.addWidget(self.rivers_button, 1, 0, 1, 1)
        self.waterfalls_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("comic sans ms")
        font.setPointSize(15)
        self.waterfalls_button.setFont(font)
        self.waterfalls_button.setStyleSheet("")
        self.waterfalls_button.setObjectName("waterfalls_button")
        self.gridLayout.addWidget(self.waterfalls_button, 2, 0, 1, 1)
        self.cities_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("comic sans ms")
        font.setPointSize(15)
        self.cities_button.setFont(font)
        self.cities_button.setStyleSheet("")
        self.cities_button.setObjectName("cities_button")
        self.gridLayout.addWidget(self.cities_button, 0, 2, 1, 1)
        self.mountains_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("comic sans ms")
        font.setPointSize(15)
        self.mountains_button.setFont(font)
        self.mountains_button.setStyleSheet("")
        self.mountains_button.setObjectName("mountains_button")
        self.gridLayout.addWidget(self.mountains_button, 1, 2, 1, 1)
        self.lucky_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("comic sans ms")
        font.setPointSize(15)
        self.lucky_button.setFont(font)
        self.lucky_button.setStyleSheet("")
        self.lucky_button.setObjectName("lucky_button")
        self.gridLayout.addWidget(self.lucky_button, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title.setText(_translate("MainWindow", "POCKET MAP"))
        self.choose.setText(_translate("MainWindow", "Выберите географический объект:"))
        self.tell_button.setText(_translate("MainWindow", "Рассказать"))
        self.choose_button.setText(_translate("MainWindow", "Избранное"))
        self.countries_button.setText(_translate("MainWindow", "Страны"))
        self.lakes_button.setText(_translate("MainWindow", "Озёра"))
        self.monuments_button.setText(_translate("MainWindow", "Памятники"))
        self.rivers_button.setText(_translate("MainWindow", "Реки"))
        self.waterfalls_button.setText(_translate("MainWindow", "Водопады"))
        self.cities_button.setText(_translate("MainWindow", "Города"))
        self.mountains_button.setText(_translate("MainWindow", "Горы"))
        self.lucky_button.setText(_translate("MainWindow", "Мне повезёт!"))
