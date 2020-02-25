#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#@FileName    :translate.py
#@Dscription    :
#@Time    :2020/02/25 16:56:17
#@Author    :stranger



import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pyperclip
import pyautogui
import random
import json
from http import client
from hashlib import md5
from urllib.parse import quote
fromLang = 'auto'
# enter your secretkey
appid = '' 
# enter your secretkey
secretKey = '' 
preurl = '/api/trans/vip/translate'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(558, 331)
        MainWindow.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)#window Placement
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input = QtWidgets.QTextBrowser(self.centralwidget)
        self.input.setObjectName("input")
        self.horizontalLayout.addWidget(self.input)
        self.output = QtWidgets.QTextBrowser(self.centralwidget)
        self.output.setObjectName("output")
        self.horizontalLayout.addWidget(self.output)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.translate = QtWidgets.QPushButton(self.centralwidget)
        self.translate.setObjectName("translate")
        self.verticalLayout.addWidget(self.translate)
        self.translate.clicked.connect(self.pushButton_click)#按钮操作
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 558, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "translate tool"))
        self.translate.setText(_translate("MainWindow", "翻译"))


    def getsentence(self):
        #pyautogui.hotkey('ctrl', 'c')
        sentence = pyperclip.paste()
        try:
            sentence = sentence.replace('\n', ' ')
            return sentence
        except:
            return sentence

    def gettrans(self,currentData):
        if currentData[0] >= u'\u4e00' and currentData[0] <=u'\u9fa5':
            toLang = 'en'
        else:
            toLang = 'zh'

        salt = random.randint(32768, 65536)
        sign = appid+currentData+str(salt)+secretKey
        m1 = md5(sign.encode(encoding='utf-8'))
        sign = m1.hexdigest()
        myurl = preurl+'?appid='+appid+'&q='+ quote(currentData)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
        try:
            httpClient = client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            result = response.read()
            result = json.loads(result)['trans_result'][0]['dst']
        except:
            result = 'Non-networked'
        finally:
            if httpClient:
                httpClient.close()
        return result

    def pushButton_click(self):
        sentence=self.getsentence()
        self.input.setPlainText(sentence)
        self.output.setPlainText(self.gettrans(sentence))

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())



