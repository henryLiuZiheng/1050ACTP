from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
#from view.threads import WorkThread
from PyQt5.QtSql import *
#import mysql.connector
#import MySQLdb
import visa
import threading,time
from xlutils.copy import copy
import xlrd
import xlwt
import serial
import configparser
import serial.tools.list_ports
from multiprocessing import Process,Pool
from main_view import Ui_MainWindow
from TestFunction import OIP3_Parameter
from TestFunction import S_Parameter
from TestFunction import P1_Parameter
from TestFunction import NF_Parameter
from TestFunction import THD_Parameter
from TestFunction import waveTest_Parameter
from TestFunction import VoltOrCurr_Parameter




import sys
from db import pyMySql

str_ver = "V0.5T"
class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
    # 通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        #print("run 666")
        self._signal.emit("run 666")  # 信号发送

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.ser = serial.Serial()
        self.conf = configparser.ConfigParser()
        self.errDisplay.hide()
        self.successDisplay.hide()
        self.selectDirBT.clicked.connect(self.getIniFileDir)
        self.openCurrUartBT.clicked.connect(self.port_open)
        self.uartComFreshBT.clicked.connect(self.refresh)
        self.clearDebugBT.clicked.connect(self.clearDebug)


        # self.OIP3ComBox.setEnabled(False)
        # self.OIP3ComFresh.setEnabled(False)
        # self.OIP3ComOpen.setEnabled(False)
        # self.OIP3ConComander.setEnabled(False)
        #
        # self.S_DataComBox.setEnabled(False)
        # self.S_DataComFresh.setEnabled(False)
        # self.S_DataComOpen.setEnabled(False)
        # self.S_DataConComander.setEnabled(False)
        #
        # self.P1ComBox.setEnabled(False)
        # self.P1ComFresh.setEnabled(False)
        # self.P1ComOpen.setEnabled(False)
        # self.P1ConComander.setEnabled(False)
        #
        # self.NFComBox.setEnabled(False)
        # self.NFComFresh.setEnabled(False)
        # self.NFComOpen.setEnabled(False)
        # self.NFConComander.setEnabled(False)

        #self.testType.currentTextChanged.connect(self.testTypeEnable)
        self.dataLocation.currentTextChanged.connect(self.dataSavaType)
        self.selectTxtFile.clicked.connect(self.mySelectDir)
        self.pltBtn.clicked.connect(self.myFigureForTestData)


        # self.OIP3DevRefresh.clicked.connect(self.OIP3DevFresh)
        # self.conConfirmAct1.clicked.connect(self.OIP3FreqDevConfirm)
        # self.conConfirmAct2.clicked.connect(self.OIP3SignalDevConfirm)
        # self.OIP3CheckBox.clicked.connect(self.OIP3SPISetEnable)
        # self.setConfirmAct.clicked.connect(self.OIP3SettingConfirm)
        # self.setRefreshAct.clicked.connect(self.OIP3SettingFresh)
        #
        # self.S_DataDevRefresh.clicked.connect(self.S_DataDevFresh)
        # self.S_DataConConfirmAct.clicked.connect(self.S_DataDevConfirm)
        # self.S_DataCheckBox.clicked.connect(self.S_DataSPISetEnable)
        # self.S_DataSetConfirmAct.clicked.connect(self.S_DataSettingConfirm)
        # self.S_DataSetRefreshAct.clicked.connect(self.S_DataSettingFresh)
        #
        # self.P1DevRefresh.clicked.connect(self.P1DevFresh)
        # self.P1ConConfirmAct.clicked.connect(self.P1DevConfirm)
        # self.P1CheckBox.clicked.connect(self.P1SPISetEnable)
        # self.P1SetConfirmAct.clicked.connect(self.P1SettingConfirm)
        # self.P1SetRefreshAct.clicked.connect(self.P1SettingFresh)
        #
        # self.NFDevRefresh.clicked.connect(self.NFDevFresh)
        # self.NFConConfirmAct.clicked.connect(self.NFDevConfirm)
        # self.NFCheckBox.clicked.connect(self.NFSPISetEnable)
        # self.NFSetConfirmAct.clicked.connect(self.NFSettingConfirm)
        # self.NFSetRefreshAct.clicked.connect(self.NFSettingFresh)

        self.beginAction.clicked.connect(self.testBegin)
        self.upData2ServerFlag = False
        self.uartTestState = False

        self.OIP3Dev1Flag = False
        self.OIP3Dev2Flag = False
        self.OIP3SettingFlag = False

        self.S_DataDevFlag = False

        self.P1DevFlag = False

        self.testCondition = []

        self.imgName = ''

        self.debugView.appendPlainText('测试软件开启！')

        infomation = ["Current测试",'Voltage测试',"wavetest测试","S参数测试", "P1测试", "OIP3测试","NF测试","THD测试"]
        self.testType.addItems(infomation)
        self.testDate.setDate(QDate.currentDate())

        infomation = ["CW", "DW", "GW","F85","F55","0","27","55","125"]
        self.testTemp.addItems(infomation)

        infomation = ["本地TXT文件", "服务器"]
        self.dataLocation.addItems(infomation)
        #self.testTypeEnable()

    def myFigureForTestData(self):
        import numpy as np
        import matplotlib.pyplot as plt
        file = self.fileDir.text()
        testConditions = self.testCondition
        name = self.imgName


        strValueArray = []
        plt.figure()  # 定义一个图像窗口
        try:
            for line in open(file):
                cnt = 0
                x = np.array([])
                y = np.array([])
                if(line.find('@')>0):
                    temp = line.split('@')[1]
                    if(temp.find(';')>0):
                        temp = temp.split(';')[0]
                        if(temp.find(',')>0):
                            temp = temp.split(',')
                            for single in temp:
                                x = np.append(x, float(testConditions[cnt]))
                                if(float(single)>100):
                                    if(cnt > 0):
                                        y = np.append(y, y[cnt-1])
                                    else:
                                        y = np.append(y,float("0"))
                                else:
                                    y = np.append(y, float(single))
                                cnt = cnt + 1
                            print(x)
                            print(y)
                            plt.plot(x, y)  # 绘制曲线 y
            plt.grid(True, linestyle='-.')
            plt.title(name, fontsize=24)
            plt.xlabel('Frequency(Hz)', fontsize=14)
            plt.ylabel('Value(dBm)', fontsize=14)
            staticImgDir = str(file).replace('.txt', '.png')
            plt.savefig(staticImgDir)
        except BaseException:
            self.debugView.appendPlainText('画图出错，请检查数据记录txt文件')

    def mySelectDir(self):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.title("请选择数据保存的.txt文件")
        root.withdraw()

        Filepath = filedialog.askopenfilename(title=u'请选择数据保存的.txt文件',filetypes=[('TXT', '*.txt'), ('All Files', '*')])  # 获得选择好的文件
        if str(Filepath).find(".txt"):
            self.fileDir.setText(Filepath)
        else:
            self.debugView.appendPlainText('请选择正确TXT文件！')

    def getIniFileDir(self):
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()

        Filepath = filedialog.askopenfilename(title=u'请选择测试用例.ini文件',filetypes=[('ini', '*.ini'), ('All Files', '*')])  # 获得选择好的文件

        self.iniFileDir.setText(Filepath)
        try:
            self.conf.read(self.iniFileDir.text(), encoding="utf-8")
            productName = str(self.conf.get("Test Info", "productName"))  # 获取测试产品名称
            testType = str(self.conf.get("Test Info", "testType")) + "测试"  # 获取测试类型
            uartState = str(self.conf.get("Test Condition", "testUartRemotes"))  # 获取测试指令

            self.chipName.setText(productName)
            self.testType.setCurrentText(testType)

            if uartState == "无":
                self.uartComBox.hide()
                self.uartComFreshBT.hide()
                self.openCurrUartBT.hide()
                self.uartTestState = True

            else:
                self.uartComBox.show()
                self.uartComFreshBT.show()
                self.openCurrUartBT.show()
        except BaseException:
            pass
        else:
            QApplication.processEvents()

    def dataSavaType(self):
        if self.dataLocation.currentText() == "本地TXT文件":
            self.fileDir.setEnabled(True)
            self.selectTxtFile.setEnabled(True)
            self.upData2ServerFlag = False
            self.pltBtn.setEnabled(True)


        else:
            self.fileDir.setEnabled(False)
            self.selectTxtFile.setEnabled(False)
            self.upData2ServerFlag = True
            self.pltBtn.setEnabled(False)
        #self.testTypeEnable()

    def refresh(self):
        # 查询可用的串口
        try:
            plist = list(serial.tools.list_ports.comports())
            if len(plist) <= 0:
                print("未搜索到串口！")
            else:
                # 把所有的可用的串口输出到comboBox中去
                self.uartComBox.clear()

                for i in range(0, len(plist)):
                    plist_0 = list(plist[i])
                    #print(1)
                    self.uartComBox.addItem(str(plist_0[0]))
        except BaseException:
            print(1)

    def clearDebug(self):
        self.debugView.clear()

    def port_open(self):
        self.ser.port = self.uartComBox.currentText()
        self.ser.baudrate = 115200
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.parity = 'N'
        if(self.openCurrUartBT.text() == '打开串口'):
            try:
                self.ser.open()
                self.openCurrUartBT.setText('关闭串口')
                self.openCurrUartBT.setStyleSheet('color:red')
                self.debugView.appendPlainText('串口连接成功！')
                self.uartComFreshBT.setEnabled(False)
                self.uartComBox.setEnabled(False)
                self.uartTestState = True


            except BaseException:
                print(1)
                self.debugView.appendPlainText('此串口不能打开！')
        else:
            try:
                self.ser.close()
                self.openCurrUartBT.setText('打开串口')
                self.openCurrUartBT.setStyleSheet('color:black')
                self.debugView.appendPlainText('串口连接已关闭！')
                self.uartComFreshBT.setEnabled(True)
                self.uartComBox.setEnabled(True)
                self.uartTestState = False


            except BaseException:
                pass


#     def testTypeEnable(self):
#
#         self.OIP3SettingFlag = False
#         self.OIP3Dev1Flag = False
#         self.OIP3Dev2Flag = False
#         self.S_DataDevFlag = False
#         self.S_DataSettingFlag = False
#         self.P1DevFlag = False
#         self.P1SettingFlag = False
#         self.NFDevFlag = False
#         self.NFSettingFlag = False
#
#
#         self.OIP3FreqDev.setEnabled(False)
#         self.OIP3SignalDev.setEnabled(False)
#         self.conConfirmAct1.setEnabled(False)
#         self.conConfirmAct2.setEnabled(False)
#         self.OIP3DevRefresh.setEnabled(False)
#         self.sweepBW.setEnabled(False)
#         self.signalProtect.setEnabled(False)
#         self.OIP3TestCondition.setEnabled(False)
#         self.OIP3LossValue.setEnabled(False)
#         self.setConfirmAct.setEnabled(False)
#         self.setRefreshAct.setEnabled(False)
#
#         self.S_DataDev.setEnabled(False)
#         self.S_DataConConfirmAct.setEnabled(False)
#         self.S_DataDevRefresh.setEnabled(False)
#         self.powerInData.setEnabled(False)
#         self.startFreqData.setEnabled(False)
#         self.stopFreqData.setEnabled(False)
#         self.S_DataSetConfirmAct.setEnabled(False)
#         self.S_DataSetRefreshAct.setEnabled(False)
#
#         self.P1Dev.setEnabled(False)
#         self.P1ConConfirmAct.setEnabled(False)
#         self.P1DevRefresh.setEnabled(False)
#         self.P1AverData.setEnabled(False)
#         self.P1PowerStopData.setEnabled(False)
#         self.P1TestCondition.setEnabled(False)
#         self.P1SetConfirmAct.setEnabled(False)
#         self.P1SetRefreshAct.setEnabled(False)
#
#         self.NFDev.setEnabled(False)
#         self.NFConConfirmAct.setEnabled(False)
#         self.NFDevRefresh.setEnabled(False)
#         self.NFStartFreq.setEnabled(False)
#         self.NFStopFreq.setEnabled(False)
#         self.NFSweepTime.setEnabled(False)
#         self.NFTestCondition.setEnabled(False)
#         self.NFENRTab.setEnabled(False)
#         self.NFINTab.setEnabled(False)
#         self.NFOUTTab.setEnabled(False)
#         self.NFSetConfirmAct.setEnabled(False)
#         self.NFSetRefreshAct.setEnabled(False)
#
#         if self.testType.currentText() == "S参数测试" :
#             self.S_DataDev.setEnabled(True)
#             self.S_DataConConfirmAct.setEnabled(True)
#             self.S_DataDevRefresh.setEnabled(True)
#             self.powerInData.setEnabled(True)
#             self.startFreqData.setEnabled(True)
#             self.stopFreqData.setEnabled(True)
#             self.S_DataSetConfirmAct.setEnabled(True)
#             self.S_DataSetRefreshAct.setEnabled(True)
#             self.pltBtn.setEnabled(False)
#
#
#         if self.testType.currentText() == "P1测试":
#             self.P1Dev.setEnabled(True)
#             self.P1ConConfirmAct.setEnabled(True)
#             self.P1DevRefresh.setEnabled(True)
#             self.P1AverData.setEnabled(True)
#             self.P1PowerStopData.setEnabled(True)
#             self.P1TestCondition.setEnabled(True)
#             self.P1SetConfirmAct.setEnabled(True)
#             self.P1SetRefreshAct.setEnabled(True)
#             self.pltBtn.setEnabled(True)
#
#
#         if self.testType.currentText() == "OIP3测试":
#             self.OIP3FreqDev.setEnabled(True)
#             self.OIP3SignalDev.setEnabled(True)
#             self.conConfirmAct1.setEnabled(True)
#             self.conConfirmAct2.setEnabled(True)
#             self.OIP3DevRefresh.setEnabled(True)
#             self.sweepBW.setEnabled(True)
#             self.signalProtect.setEnabled(True)
#             self.OIP3TestCondition.setEnabled(True)
#             self.OIP3LossValue.setEnabled(True)
#             self.setConfirmAct.setEnabled(True)
#             self.setRefreshAct.setEnabled(True)
#             self.pltBtn.setEnabled(True)
#
#
#         if self.testType.currentText() == "NF测试":
#             self.NFDev.setEnabled(True)
#             self.NFConConfirmAct.setEnabled(True)
#             self.NFDevRefresh.setEnabled(True)
#             self.NFStartFreq.setEnabled(True)
#             self.NFStopFreq.setEnabled(True)
#             self.NFSweepTime.setEnabled(True)
#             self.NFTestCondition.setEnabled(True)
#             self.NFENRTab.setEnabled(True)
#             self.NFINTab.setEnabled(True)
#             self.NFOUTTab.setEnabled(True)
#             self.NFSetConfirmAct.setEnabled(True)
#             self.NFSetRefreshAct.setEnabled(True)
#             self.pltBtn.setEnabled(True)
#
#
#     #OIP3 Configure Fun :
#     def OIP3DevFresh(self):
#         self.OIP3Dev1Flag = False
#         self.OIP3Dev2Flag = False
#         self.OIP3SettingFlag = False
#         self.OIP3FreqDev.clear()
#         self.OIP3SignalDev.clear()
#         self.OIP3FreqDev.setEnabled(True)
#         self.OIP3SignalDev.setEnabled(True)
#         self.conConfirmAct1.setEnabled(True)
#         self.conConfirmAct2.setEnabled(True)
#         resManage = visa.ResourceManager()
#         reslists = resManage.list_resources()
#         for reslist in reslists:
#             print(reslist)
#             if str(reslist) == 'TCPIP0::192.168.1.81::inst0::INSTR':
#                 self.OIP3FreqDev.addItem('FSV')
#             if str(reslist) == 'TCPIP0::FSWP26-101228::inst0::INSTR':
#                 self.OIP3FreqDev.addItem('FSWP')
#             if str(reslist) == 'TCPIP0::192.168.1.120::inst0::INSTR':
#                 self.OIP3SignalDev.addItem('SMW200A')
#
#     def OIP3FreqDevConfirm(self):
#         self.OIP3Dev1Flag = True
#         self.OIP3FreqDev.setEnabled(False)
#         self.conConfirmAct1.setEnabled(False)
#
#     def OIP3SignalDevConfirm(self):
#         self.OIP3Dev2Flag = True
#         self.OIP3SignalDev.setEnabled(False)
#         self.conConfirmAct2.setEnabled(False)
#
#     def OIP3SPISetEnable(self):
#         if self.OIP3CheckBox.isChecked() :
#             self.OIP3ComBox.setEnabled(True)
#             self.OIP3ComFresh.setEnabled(True)
#             self.OIP3ComOpen.setEnabled(True)
#             self.OIP3ConComander.setEnabled(True)
#         else:
#             self.OIP3ComBox.setEnabled(False)
#             self.OIP3ComFresh.setEnabled(False)
#             self.OIP3ComOpen.setEnabled(False)
#             self.OIP3ConComander.setEnabled(False)
#
#     def OIP3SettingConfirm(self):
#         self.OIP3SettingFlag = True
#
#         self.sweepBW.setEnabled(False)
#         self.signalProtect.setEnabled(False)
#         self.OIP3TestCondition.setEnabled(False)
#         self.OIP3LossValue.setEnabled(False)
#         self.setConfirmAct.setEnabled(False)
#
#     def OIP3SettingFresh(self):
#         self.sweepBW.setEnabled(True)
#         self.signalProtect.setEnabled(True)
#         self.OIP3TestCondition.setEnabled(True)
#         self.OIP3LossValue.setEnabled(True)
#         self.setConfirmAct.setEnabled(True)
#
#
# ###################################
#
#
#
#     # S_Data Configure Fun :
#     def S_DataDevFresh(self):
#         self.S_DataSettingFlag = False
#         self.S_DataDev.clear()
#         self.S_DataDev.setEnabled(True)
#         self.S_DataConConfirmAct.setEnabled(True)
#         resManage = visa.ResourceManager()
#         reslists = resManage.list_resources()
#         for reslist in reslists:
#             if str(reslist) == 'TCPIP0::192.168.1.15::inst0::INSTR':
#                 self.S_DataDev.addItem('ZVA50')
#
#
#     def S_DataDevConfirm(self):
#         self.S_DataDevFlag = True
#         self.S_DataDev.setEnabled(False)
#         self.S_DataConConfirmAct.setEnabled(False)
#
#     def S_DataSPISetEnable(self):
#         if self.S_DataCheckBox.isChecked():
#             self.S_DataComBox.setEnabled(True)
#             self.S_DataComFresh.setEnabled(True)
#             self.S_DataComOpen.setEnabled(True)
#             self.S_DataConComander.setEnabled(True)
#         else:
#             self.S_DataComBox.setEnabled(False)
#             self.S_DataComFresh.setEnabled(False)
#             self.S_DataComOpen.setEnabled(False)
#             self.S_DataConComander.setEnabled(False)
#
#     def S_DataSettingConfirm(self):
#         self.S_DataSettingFlag = True
#
#         self.powerInData.setEnabled(False)
#         self.startFreqData.setEnabled(False)
#         self.stopFreqData.setEnabled(False)
#         self.S_DataSetConfirmAct.setEnabled(False)
#
#     def S_DataSettingFresh(self):
#         self.powerInData.setEnabled(True)
#         self.startFreqData.setEnabled(True)
#         self.stopFreqData.setEnabled(True)
#         self.S_DataSetConfirmAct.setEnabled(True)
#
# ###################################
#
#     # P1 Configure Fun :
#     def P1DevFresh(self):
#         self.P1DevFlag = False
#         self.P1SettingFlag = False
#         self.P1Dev.clear()
#         self.P1Dev.setEnabled(True)
#         self.P1ConConfirmAct.setEnabled(True)
#         resManage = visa.ResourceManager()
#         reslists = resManage.list_resources()
#         self.P1Dev.addItem('ZVA50')
#         for reslist in reslists:
#             print(reslist)
#             for reslist in reslists:
#                 if str(reslist) == 'TCPIP0::192.168.1.15::inst0::INSTR':
#                     self.P1Dev.addItem('ZVA50')
#
#     def P1DevConfirm(self):
#         self.P1DevFlag = True
#         self.P1Dev.setEnabled(False)
#         self.P1ConConfirmAct.setEnabled(False)
#
#     def P1SPISetEnable(self):
#         if self.P1CheckBox.isChecked():
#             self.P1ComBox.setEnabled(True)
#             self.P1ComFresh.setEnabled(True)
#             self.P1ComOpen.setEnabled(True)
#             self.P1ConComander.setEnabled(True)
#         else:
#             self.P1ComBox.setEnabled(False)
#             self.P1ComFresh.setEnabled(False)
#             self.P1ComOpen.setEnabled(False)
#             self.P1ConComander.setEnabled(False)
#
#     def P1SettingConfirm(self):
#         self.P1SettingFlag = True
#
#         self.P1AverData.setEnabled(False)
#         self.P1PowerStopData.setEnabled(False)
#         self.P1TestCondition.setEnabled(False)
#         self.P1SetConfirmAct.setEnabled(False)
#
#     def P1SettingFresh(self):
#         self.P1SettingFlag = False
#
#         self.P1AverData.setEnabled(True)
#         self.P1PowerStopData.setEnabled(True)
#         self.P1TestCondition.setEnabled(True)
#         self.P1SetConfirmAct.setEnabled(True)
#
# ###################################
#     # NF Configure Fun :
#     def NFDevFresh(self):
#         self.NFDevFlag = False
#         self.NFSettingFlag = False
#         self.NFDev.clear()
#         self.NFDev.setEnabled(True)
#         self.NFConConfirmAct.setEnabled(True)
#         resManage = visa.ResourceManager()
#         reslists = resManage.list_resources()
#         for reslist in reslists:
#             print(reslist)
#             for reslist in reslists:
#                 if str(reslist) == 'TCPIP0::192.168.1.81::inst0::INSTR':
#                     self.NFDev.addItem('FSV')
#
#     def NFDevConfirm(self):
#         self.NFDevFlag = True
#         self.NFDev.setEnabled(False)
#         self.NFConConfirmAct.setEnabled(False)
#
#     def NFSPISetEnable(self):
#         if self.NFCheckBox.isChecked():
#             self.NFComBox.setEnabled(True)
#             self.NFComFresh.setEnabled(True)
#             self.NFComOpen.setEnabled(True)
#             self.NFConComander.setEnabled(True)
#         else:
#             self.NFComBox.setEnabled(False)
#             self.NFComFresh.setEnabled(False)
#             self.NFComOpen.setEnabled(False)
#             self.NFConComander.setEnabled(False)
#
#     def NFSettingConfirm(self):
#         self.NFSettingFlag = True
#
#         self.NFStartFreq.setEnabled(False)
#         self.NFStopFreq.setEnabled(False)
#         self.NFSweepTime.setEnabled(False)
#         self.NFTestCondition.setEnabled(False)
#         self.NFENRTab.setEnabled(False)
#         self.NFINTab.setEnabled(False)
#         self.NFOUTTab.setEnabled(False)
#         self.NFSetConfirmAct.setEnabled(False)
#
#     def NFSettingFresh(self):
#
#         self.NFSettingFlag = False
#         self.NFStartFreq.setEnabled(True)
#         self.NFStopFreq.setEnabled(True)
#         self.NFSweepTime.setEnabled(True)
#         self.NFTestCondition.setEnabled(True)
#         self.NFENRTab.setEnabled(True)
#         self.NFINTab.setEnabled(True)
#         self.NFOUTTab.setEnabled(True)
#         self.NFSetConfirmAct.setEnabled(True)

    ###################################




    def testBegin(self):
        HOSTIP = '192.168.1.4'  #用于云测试保存数据时候用，本地保存可忽略该参数
        print("func success")
        if (self.chipNum.text() == "")|(self.chipName.text() == ""):
            self.debugView.appendPlainText("请输入当前测试芯片名称和序号！")
        else:
            if self.uartTestState:
                self.beginAction.setEnabled(False)
                if self.testType.currentText() == 'OIP3测试':
                    #if self.OIP3Dev1Flag :
                    if True:
                        #if self.OIP3Dev2Flag:
                        if True:
                            #if self.OIP3SettingFlag:
                            if True:
                                upDataBuf = []


                                self.chipName.setEnabled(False)
                                self.testType.setEnabled(False)
                                self.testTemp.setEnabled(False)
                                self.testerNum.setEnabled(False)
                                self.testDate.setEnabled(False)
                                self.testDate.setDate(QDate.currentDate())

                                testDevName1 = str(self.conf.get("Test Info", "deviceName1"))  # 获取信号源使用仪表
                                testDevName2 = str(self.conf.get("Test Info", "deviceName2"))  # 获取频谱仪使用仪表
                                testUartRemotes = str(self.conf.get("Test Condition", "testUartRemotes"))  # 获取测试uart指令
                                testFreqPoints = str(self.conf.get("Test Condition", "testFreqPoints"))  # 获取详细测试频点
                                poutSafeTh = str(self.conf.get("Test Condition", "poutSafeTh"))  # 获取信号源输出额定功率
                                poutSetValue = str(self.conf.get("Test Condition", "poutSetValue"))  # 设置输出功率值（ex：在某某功率下的OIP3）
                                spanFreq = str(self.conf.get("Test Condition", "spanFreq"))  # 获取平均点数
                                OIP3LossSetValue = str(self.conf.get("Test Condition", "lossSetValue"))  # 获取频点对应线损
                                OIP3HighTh = str(self.conf.get("Test Condition", "OIP3ValueHighTh"))  # 获取平均点数
                                OIP3LowTh = str(self.conf.get("Test Condition", "OIP3ValueLowTh"))  # 获取频点对应线损
                                testTime = len(testFreqPoints.split(','))
                                self.debugView.appendPlainText('OIP3测试开始，预计需要'+str(testTime)+'秒，'+'请等待···')
                                self.errDisplay.hide()
                                self.successDisplay.hide()
                                self.stateDisplay.setText('测试中')
                                QApplication.processEvents()
                                newOIP3Test = OIP3_Parameter.IP3(testDevName1,testDevName2)
                                result = newOIP3Test.test_Start(testFreqPoints,OIP3LossSetValue,poutSetValue,spanFreq,poutSafeTh)
                                if result[0] == 'err':
                                    self.debugView.appendPlainText(result[1])
                                    QApplication.processEvents()
                                if result[0] == 'success':
                                    temp = self.testTemp.currentText()
                                    tableName = self.chipName.text() + 'OIP3' +temp + self.chipNum.text()
                                    tableName = tableName.replace(' ','')
                                    self.imgName = tableName
                                    print(tableName)

                                    conditions = testFreqPoints.split(',')
                                    for single in result[1:]:
                                        upDataBuf.append(float(single)+float(poutSetValue))
                                    #upDataBuf = float(result[1:])+float(poutSetValue)
                                    print(upDataBuf)

                                    self.testCondition = conditions
                                    self.debugView.appendPlainText(str(conditions))
                                    self.debugView.appendPlainText(str(upDataBuf))
                                    cnt = 0
                                    self.stateDisplay.setText('通过')
                                    self.successDisplay.show()
                                    for singleData in upDataBuf:
                                        if ((float(singleData)<float(OIP3LowTh))|(float(singleData)>float(OIP3HighTh))):
                                            content ='注意：'+ str(conditions[cnt])+'Hz频率下的OIP3值：'+str(singleData)+'dBm 超过警戒限定'
                                            self.debugView.appendPlainText(content)
                                            self.stateDisplay.setText('错误')
                                            self.successDisplay.hide()
                                            self.errDisplay.show()
                                            cnt = cnt + 1

                                            QApplication.processEvents()

                                    QApplication.processEvents()
                                    print(1)
                                    if self.upData2ServerFlag:
                                        try:
                                            myDB = pyMySql.MySqlDataBase(HOSTIP, "root", "liuziheng1", "TESTDB")
                                            myDB.upDataOriData(tableName,conditions,upDataBuf)
                                            myDB.pyInsertDataToTestType('myactp_testtype',self.chipName.text(),temp,'OIP3')
                                            myDB.pyInsertDataToChipInfo('myactp_chipinfo',self.chipName.text(),temp,'OIP3',self.chipNum.text())
                                        except BaseException:
                                            self.debugView.appendPlainText('数据库连接失败')
                                            QApplication.processEvents()
                                    else:
                                        try:
                                            temp = str(upDataBuf).replace('[','')
                                            temp = temp.replace(']','')
                                            temp = self.chipNum.text()+'@'+temp+';'+self.testDate.text()+'['+self.testerNum.text()+']'+'\n'
                                            newFilePath = self.fileDir.text()
                                            file_handle = open(newFilePath, mode='a')
                                            file_handle.write(temp)
                                        except BaseException:
                                            self.debugView.appendPlainText('老哥，请确认是否是TXT文件 = =''')
                                            QApplication.processEvents()

                                #self.debugView.appendPlainText(tableName)
                                QApplication.processEvents()
                                self.chipName.setEnabled(True)
                                self.testType.setEnabled(True)
                                self.testTemp.setEnabled(True)
                                self.testerNum.setEnabled(True)
                                self.testDate.setEnabled(True)
                            else:
                                self.debugView.appendPlainText('未确认参数配置，请确认！')
                        else:
                            self.debugView.appendPlainText('未确认连接信号源，请确认！')
                    else:
                        self.debugView.appendPlainText('未确认连接频谱仪，请确认！')

                if self.testType.currentText() == 'S参数测试':
                    #if self.S_DataDevFlag:
                    if True:
                        temp = self.testTemp.currentText()
                        tableName = self.chipName.text() + 'S_DATA' + temp + self.chipNum.text()
                        tableName = tableName.replace(' ', '')
                        #if self.S_DataSettingFlag:
                        if True:
                            upDataBuf = []

                            testDevName = str(self.conf.get("Test Info", "deviceName"))  # 获取使用仪表
                            testUartRemotes = str(self.conf.get("Test Condition", "testUartRemotes"))# 获取测试uart指令
                            startFreq = str(self.conf.get("Test Condition", "startFreq"))  # 获取起始测试频点
                            stopFreq = str(self.conf.get("Test Condition", "stopFreq"))  # 获取结束测试频点
                            inputPower = str(self.conf.get("Test Condition", "inputPower"))  # 获取仪表输出信号功率大小

                            self.debugView.appendPlainText('S参数测试开始，请等待···')
                            self.chipName.setEnabled(False)
                            self.testType.setEnabled(False)
                            self.testTemp.setEnabled(False)
                            self.testerNum.setEnabled(False)
                            self.testDate.setEnabled(False)
                            self.testDate.setDate(QDate.currentDate())
                            QApplication.processEvents()
                            newS_DataTest = S_Parameter.S_Data(testDevName)
                            testConditions = inputPower + ',' + startFreq + ',' + stopFreq
                            result = newS_DataTest.test_Start(testConditions,self.chipName.text(),temp,tableName)
                            if result[0] == 'err':
                                self.debugView.appendPlainText(result[1])
                                QApplication.processEvents()
                            if result[0] == 'success':
                                self.debugView.appendPlainText(str(result[1]))
                                QApplication.processEvents()
                                #myDB = pyMySql.MySqlDataBase(HOSTIP, "root", "liuziheng1", "TESTDB")
                                #myDB.upDataOriData(tableName,conditions,upDataBuf)
                                if self.upData2ServerFlag:
                                    try:
                                        myDB = pyMySql.MySqlDataBase(HOSTIP, "root", "liuziheng1", "TESTDB")
                                        print(1)
                                        myDB.pyInsertDataToTestType('myactp_testtype', self.chipName.text(), temp, 'S_DATA')
                                        myDB.pyInsertDataToChipInfo('myactp_chipinfo', self.chipName.text(), temp, 'S_DATA', self.chipNum.text())
                                    except BaseException:
                                        self.debugView.appendPlainText('数据库连接失败')
                                        QApplication.processEvents()


                                print(1)
                            self.debugView.appendPlainText(tableName)
                            QApplication.processEvents()
                            self.chipName.setEnabled(True)
                            self.testType.setEnabled(True)
                            self.testTemp.setEnabled(True)
                            self.testerNum.setEnabled(True)
                            self.testDate.setEnabled(True)
                        else:
                            self.debugView.appendPlainText('未确认参数配置，请确认！')
                    else:
                        self.debugView.appendPlainText('未确认连接矢网，请确认！')

                if self.testType.currentText() == 'P1测试':
                    #if self.P1DevFlag:
                    if True:
                        #if self.P1SettingFlag:
                        if True:
                            upDataBuf = []


                            self.chipName.setEnabled(False)
                            self.testType.setEnabled(False)
                            self.testTemp.setEnabled(False)
                            self.testerNum.setEnabled(False)
                            self.testDate.setEnabled(False)
                            self.testDate.setDate(QDate.currentDate())


                            testDevName = str(self.conf.get("Test Info", "deviceName"))  # 获取使用仪表
                            testUartRemotes = str(self.conf.get("Test Condition", "testUartRemotes"))# 获取测试uart指令
                            testFreqPoints = str(self.conf.get("Test Condition", "testFreqPoints"))  # 获取详细测试频点
                            P1AverPoint = str(self.conf.get("Test Condition", "averagePoints"))  # 获取平均点数
                            P1StopValue = str(self.conf.get("Test Condition", "sotpPowerValue"))  # 获取平均点数
                            P1LossSetValue = str(self.conf.get("Test Condition", "lossSetValue"))  # 获取频点对应线损
                            P1HighTh = str(self.conf.get("Test Condition", "p1ValueHighTh"))  # 获取平均点数
                            P1LowTh = str(self.conf.get("Test Condition", "p1ValueLowTh"))  # 获取频点对应线损

                            testTime = len(testFreqPoints.split(','))/2
                            self.debugView.appendPlainText('P1测试开始，预计需要'+str(testTime)+'秒，'+'请等待···')
                            self.errDisplay.hide()
                            self.successDisplay.hide()
                            self.stateDisplay.setText('测试中')
                            QApplication.processEvents()
                            newP1Test = P1_Parameter.P1(testDevName)

                            result = newP1Test.test_Start(testFreqPoints,P1AverPoint,P1StopValue)
                            if result[0] == 'err':
                                self.debugView.appendPlainText(result[1])
                                QApplication.processEvents()
                            if result[0] == 'success':
                                temp = self.testTemp.currentText()
                                tableName = self.chipName.text() + 'P1' +temp + self.chipNum.text()
                                tableName = tableName.replace(' ','')
                                self.imgName = tableName

                                print(tableName)
                                conditions = testFreqPoints.split(',')
                                upDataBuf = result[1:]
                                print(upDataBuf)
                                lossCnt = 0
                                if P1LossSetValue == "无":
                                    upDataBuf = result[1:]
                                else:
                                    newSignalLosses = P1LossSetValue.split(',')
                                    print(newSignalLosses)
                                    for upData in upDataBuf:
                                        print(upData)
                                        upDataBuf[lossCnt] = upData + float(newSignalLosses[lossCnt])
                                        lossCnt = lossCnt + 1
                                print(2)
                                self.testCondition = conditions

                                self.debugView.appendPlainText(str(conditions))
                                self.debugView.appendPlainText(str(upDataBuf))
                                cnt = 0
                                self.stateDisplay.setText('通过')
                                self.successDisplay.show()
                                for singleData in upDataBuf:
                                    if ((float(singleData) < float(P1LowTh)) | (float(singleData) > float(P1HighTh))):
                                        content = '注意：' + str(conditions[cnt]) + 'Hz频率下的P1值：' + str(singleData) + 'dBm 超过限定'
                                        self.debugView.appendPlainText(content)
                                        self.stateDisplay.setText('错误')
                                        self.successDisplay.hide()
                                        self.errDisplay.show()
                                        cnt = cnt+1

                                        QApplication.processEvents()
                                QApplication.processEvents()
                                print(1)
                                if self.upData2ServerFlag:
                                    try:
                                        myDB = pyMySql.MySqlDataBase(HOSTIP, "root", "liuziheng1", "TESTDB")
                                        myDB.upDataOriData(tableName,conditions,upDataBuf)
                                        myDB.pyInsertDataToTestType('myactp_testtype',self.chipName.text(),temp,'P1')
                                        myDB.pyInsertDataToChipInfo('myactp_chipinfo',self.chipName.text(),temp,'P1',self.chipNum.text())
                                    except BaseException:
                                        self.debugView.appendPlainText('数据库连接失败')
                                        QApplication.processEvents()
                                else:
                                    try:
                                        temp = str(upDataBuf).replace('[', '')
                                        temp = temp.replace(']', '')
                                        temp = self.chipNum.text() + '@' + temp + ';' + self.testDate.text() + '[' + self.testerNum.text() + ']' + '\n'
                                        newFilePath = self.fileDir.text()
                                        file_handle = open(newFilePath, mode='a')
                                        file_handle.write(temp)
                                    except BaseException:
                                        self.debugView.appendPlainText('老哥，请确认是否是TXT文件 = =''')
                                        QApplication.processEvents()
                            #self.debugView.appendPlainText(tableName)
                            QApplication.processEvents()
                            self.chipName.setEnabled(True)
                            self.testType.setEnabled(True)
                            self.testTemp.setEnabled(True)
                            self.testerNum.setEnabled(True)
                            self.testDate.setEnabled(True)
                        else:
                            self.debugView.appendPlainText('未确认参数配置，请确认！')
                    else:
                        self.debugView.appendPlainText('未确认连接矢网，请确认！')

                if self.testType.currentText() == 'NF测试':
                    #if self.NFDevFlag:
                    if True:
                        #if self.NFSettingFlag:
                        if True:
                            upDataBuf = []
                            print(1)
                            testDevName = str(self.conf.get("Test Info", "deviceName"))  # 获取使用仪表
                            testUartRemotes = str(self.conf.get("Test Condition", "testUartRemotes"))# 获取测试uart指令
                            #testFreqPoints = str(self.conf.get("Test Condition", "testFreqPoints"))  # 获取详细测试频点
                            startFreq = str(self.conf.get("Test Condition", "startFreq"))  # 获取平均点数
                            stopFreq = str(self.conf.get("Test Condition", "stopFreq"))  # 获取平均点数
                            enrSetTable = str(self.conf.get("Test Condition", "enrSetTable"))  # 获取频点对应线损
                            inLossSetValue = str(self.conf.get("Test Condition", "inLossSetValue"))  # 获取频点对应线损
                            outLossSetValue = str(self.conf.get("Test Condition", "outLossSetValue"))  # 获取频点对应线损
                            NFSweepTime = str(self.conf.get("Test Condition", "sweepTime"))  # 获取平均点数
                            NFSweepPoints = str(self.conf.get("Test Condition", "sweepPoints"))  # 获取平均点数
                            NFAverage = str(self.conf.get("Test Condition", "average"))  # 获取平均点数
                            NFHighTh = str(self.conf.get("Test Condition", "NFValueHighTh"))  # 获取平均点数
                            NFLowTh = str(self.conf.get("Test Condition", "NFValueLowTh"))  # 获取频点对应线损
                            print(1)
                            FSTAR = startFreq
                            FSTOP = stopFreq
                            ENRTAB = enrSetTable
                            if inLossSetValue == "无":
                                LOSSINTAB = ""
                            else:
                                LOSSINTAB = inLossSetValue

                            if outLossSetValue == "无":
                                LOSSOUTTAB = ""
                            else:
                                LOSSOUTTAB = outLossSetValue

                            SWEEPTIME = NFSweepTime + 's'
                            SWEEPPOINT = NFSweepPoints
                            #FREQTABLE = testFreqPoints
                            AVERAGE = NFAverage
                            self.debugView.appendPlainText('NF测试开始，预计需要' + str(round(int(SWEEPPOINT)*int(AVERAGE)*(float(NFSweepTime)+0.05))) + '秒，' + '请等待···')
                            self.errDisplay.hide()
                            self.successDisplay.hide()
                            self.stateDisplay.setText('测试中')

                            self.chipName.setEnabled(False)
                            self.testType.setEnabled(False)
                            self.testTemp.setEnabled(False)
                            self.testerNum.setEnabled(False)
                            self.testDate.setEnabled(False)
                            self.testDate.setDate(QDate.currentDate())
                            QApplication.processEvents()
                            newNFTest = NF_Parameter.NF(testDevName)
                            print(1)
                            result = newNFTest.test_Start(FSTAR, FSTOP, SWEEPPOINT,AVERAGE,ENRTAB, LOSSINTAB,LOSSOUTTAB, SWEEPTIME)
                            if result[0] == 'err':
                                self.debugView.appendPlainText(result[1])
                                QApplication.processEvents()
                            if result[0] == 'success':
                                fStart = float(str(FSTAR).replace('MHz','000000'))
                                NFtemp = fStart
                                fStop = float(str(FSTOP).replace('MHz','000000'))
                                stepFreq = (fStop - fStart)/(int(SWEEPPOINT)-1)
                                freqTable = [float(fStart)]
                                for i in range(int(SWEEPPOINT)-1):
                                    NFtemp = NFtemp + stepFreq
                                    freqTable.append(str(NFtemp))
                                conditions = freqTable
                                self.testCondition = conditions

                                temp = self.testTemp.currentText()
                                tableName = self.chipName.text() + 'NF' + temp + self.chipNum.text()
                                tableName = tableName.replace(' ', '')
                                self.imgName = tableName

                                print(tableName)
                                upDataBuf = result[1:]

                                self.debugView.appendPlainText(str(upDataBuf))
                                cnt = 0
                                self.stateDisplay.setText('通过')
                                self.successDisplay.show()
                                print('right')
                                for singleData in upDataBuf:
                                    if ((float(singleData) < float(NFLowTh)) | (float(singleData) > float(NFHighTh))):
                                        print('right1')

                                        content = '注意：' + str(conditions[cnt]) + 'Hz频率下的NF值：' + str(singleData) + 'dBm 超过限定'
                                        self.debugView.appendPlainText(content)
                                        print('right1')

                                        self.stateDisplay.setText('错误')
                                        print('right2')

                                        self.successDisplay.hide()
                                        self.errDisplay.show()
                                        cnt = cnt+1
                                        QApplication.processEvents()

                                QApplication.processEvents()

                                print(conditions)
                                if self.upData2ServerFlag:
                                    try:
                                        myDB = pyMySql.MySqlDataBase("localhost", "root", "liuziheng1", "TESTDB")
                                        myDB.upDataOriData(tableName, conditions, upDataBuf)
                                        myDB.pyInsertDataToTestType('myactp_testtype', self.chipName.text(), temp, 'NF')
                                        myDB.pyInsertDataToChipInfo('myactp_chipinfo', self.chipName.text(), temp, 'NF',self.chipNum.text())
                                    except BaseException:
                                        self.debugView.appendPlainText('数据库连接失败')
                                        QApplication.processEvents()
                                else:
                                    try:
                                        temp = str(upDataBuf).replace('[', '')
                                        temp = temp.replace(']', '')
                                        temp = self.chipNum.text() + '@' + temp + ';' + self.testDate.text() + '[' + self.testerNum.text() + ']' + '\n'
                                        newFilePath = self.fileDir.text()
                                        file_handle = open(newFilePath, mode='a')
                                        file_handle.write(temp)
                                        newChipNum = int(self.chipNum.text()) + 1
                                        self.chipNum.setText(str(newChipNum))
                                    except BaseException:
                                        self.debugView.appendPlainText('老哥，请确认是否是TXT文件 = =''')
                                        QApplication.processEvents()

                            # self.debugView.appendPlainText(tableName)
                            QApplication.processEvents()
                            self.chipName.setEnabled(True)
                            self.testType.setEnabled(True)
                            self.testTemp.setEnabled(True)
                            self.testerNum.setEnabled(True)
                            self.testDate.setEnabled(True)
                        else:
                            self.debugView.appendPlainText('未确认参数配置，请确认！')
                    else:
                        self.debugView.appendPlainText('未确认连接矢网，请确认！')

                if self.testType.currentText() == 'THD测试':

                    productName = str(self.conf.get("Test Info", "productName"))#获取测试产品名称
                    testType = str(self.conf.get("Test Info", "testType"))+"测试"#获取测试类型

                    testUartRemotes = str(self.conf.get("Test Condition", "testUartRemotes")).split(",")#获取测试uart指令
                    testFreqPoints = str(self.conf.get("Test Condition", "testFreqPoints")).split(",")#获取详细测试频点
                    testFreqSpan = str(self.conf.get("Test Condition", "testFreqSpan"))#获取测试频率带宽显示设置


                    print(productName)
                    print(testUartRemotes)
                    if productName == self.chipName.text():
                        if testType == self.testType.currentText():
                            newTHDTest = THD_Parameter.THD('FSV')
                            temp = 0
                            outData = []
                            for testUartRemote in testUartRemotes:
                                if testUartRemotes[0] != "无":
                                    print(testUartRemote)
                                    testUartRemote = (testUartRemote + '\r\n').encode('utf-8')
                                    num = self.ser.write(testUartRemote)
                                result = newTHDTest.test_Start(float(testFreqPoints[temp]),float(testFreqSpan))
                                if result[0] == 'err':
                                    self.debugView.appendPlainText(result[1])
                                    QApplication.processEvents()
                                    break
                                if result[0] == 'success':
                                    print(result)
                                    self.debugView.appendPlainText("THD:"+str(result[1])+" 条件:"+str(testUartRemote))
                                    QApplication.processEvents()
                                    outData = result[1:]
                                    outData.append(str(testUartRemote))
                                    temp = temp + 1
                                    strTemp = str(outData).replace('[', '')
                                    strTemp = strTemp.replace(']', '')
                                    strTemp = strTemp.replace("'", '')
                                    strTemp = strTemp.replace(",", '\t')
                                    strTemp = self.chipNum.text() + '\t' + strTemp + '\t' + self.testDate.text() + '\t' + self.testerNum.text() + '\n'
                                    newFilePath = self.fileDir.text()
                                    try:
                                        file_handle = open(newFilePath, mode='a')
                                        file_handle.write(strTemp)
                                    except:
                                        self.debugView.appendPlainText("保存路径错误！")
                        else:
                            self.debugView.appendPlainText("检测到测试用例中测试类型设置不匹配！")
                    else:
                        self.debugView.appendPlainText("检测到测试用例中测试产品设置不匹配！")

                if self.testType.currentText() == 'wavetest测试':
                    productName = str(self.conf.get("Test Info", "productName"))#获取测试产品名称
                    testType = str(self.conf.get("Test Info", "testType"))+"测试"#获取测试类型

                    testUartRemotes = str(self.conf.get("Test Condition", "testUartRemotes")).split(",")#获取测试uart指令
                    print(testUartRemotes)
                    config = {'scaleTime': str(self.conf.get("Test Condition", "scaleTime")),
                                'timePosition': str(self.conf.get("Test Condition", "timePosition")),

                                'CH1State': str(self.conf.get("Test Condition", "CH1State")),
                                'CH1DIV': str(self.conf.get("Test Condition", "CH1DIV")),
                                'CH1offset': str(self.conf.get("Test Condition", "CH1offset")),

                                'CH2State': str(self.conf.get("Test Condition", "CH2State")),
                                'CH2DIV': str(self.conf.get("Test Condition", "CH2DIV")),
                                'CH2offset': str(self.conf.get("Test Condition", "CH2offset")),

                                'CH3State': str(self.conf.get("Test Condition", "CH3State")),
                                'CH3DIV': str(self.conf.get("Test Condition", "CH3DIV")),
                                'CH3offset': str(self.conf.get("Test Condition", "CH3offset")),

                                'CH4State': str(self.conf.get("Test Condition", "CH4State")),
                                'CH4DIV': str(self.conf.get("Test Condition", "CH4DIV")),
                                'CH4offset': str(self.conf.get("Test Condition", "CH4offset")),

                                'TriggerSourc':str(self.conf.get("Test Condition", "TriggerSourc")),
                                'TriggerLevel':str(self.conf.get("Test Condition", "TriggerLevel")),
                                'TriggerMode':str(self.conf.get("Test Condition", "TriggerMode")),

                                'saveDirName':'test',
                                'saveFileName':'test',#此处注意RS示波器存储文件名字符串不能超过8个

                                'waitTimeBeforeSaving':float(str(self.conf.get("Test Condition", "waitTimeBeforeSaving")))

                                }


                    if productName == self.chipName.text():
                        if testType == self.testType.currentText():
                            newwavetestTest = waveTest_Parameter.wavetest('RTM1054')
                            config["saveDirName"] = self.chipName.text()
                            print(config["saveDirName"])
                            if testUartRemotes[0] != "无":
                                typeStr = str(self.conf.get("Test Condition", "remotesType"))
                                in_put = ("all set ct="+typeStr + '\r\n').encode('utf-8')
                                num = self.ser.write(in_put)
                                time.sleep(1)
                            temp = 0
                            for testUartRemote in testUartRemotes:
                                config["saveFileName"] = self.chipNum.text()+str(temp)
                                print(config["saveFileName"])
                                if testUartRemotes[0] != "无":
                                    print(testUartRemote)
                                    testUartRemote = (testUartRemote + '\r\n').encode('utf-8')
                                    num = self.ser.write(testUartRemote)
                                    print(num)
                                result = newwavetestTest.test_Start(**config)
                                if result[0] == 'err':
                                    self.debugView.appendPlainText(result[1])
                                    QApplication.processEvents()
                                    break
                                if result[0] == 'success':
                                    print(result[1])
                                    temp = temp + 1
                        else:
                            self.debugView.appendPlainText("检测到测试用例中测试类型设置不匹配！")
                    else:
                        self.debugView.appendPlainText("检测到测试用例中测试产品设置不匹配！")

                if self.testType.currentText() == 'Voltage测试':
                    productName = str(self.conf.get("Test Info", "productName"))#获取测试产品名称
                    testType = str(self.conf.get("Test Info", "testType"))+"测试"#获取测试类型

                    testUartRemotes = str(self.conf.get("Test Condition", "testUartRemotes")).split(",")#获取测试uart指令
                    print(testUartRemotes)
                    config = {'testMode': str(self.conf.get("Test Condition", "testMode"))
                                }


                    if productName == self.chipName.text():
                        if testType == self.testType.currentText():
                            newVoltageTest = VoltOrCurr_Parameter.getValue('数字万用表1')
                            temp = 0
                            outData = []
                            for testUartRemote in testUartRemotes:
                                if testUartRemotes[0] != "无":
                                    print(testUartRemote)
                                    testUartRemote = (testUartRemote + '\r\n').encode('utf-8')
                                    num = self.ser.write(testUartRemote)
                                result = newVoltageTest.test_Start(**config)
                                if result[0] == 'err':
                                    self.debugView.appendPlainText(result[1])
                                    QApplication.processEvents()
                                    break
                                if result[0] == 'success':
                                    print(result)
                                    outData.append(str(result[1]).replace("\n",""))
                                    self.debugView.appendPlainText("电压值："+str(result[1]).replace("\n","")+"V:已保存！")

                                    QApplication.processEvents()
                                    temp = temp + 1
                            strTemp = str(outData).replace('[', '')
                            strTemp = strTemp.replace(']', '')
                            strTemp = strTemp.replace("'", '')
                            strTemp = strTemp.replace(",", '\t')
                            strTemp = self.chipNum.text() + '\t' + strTemp + '\t' + self.testDate.text() + '\t' + self.testerNum.text() + '\n'
                            newFilePath = self.fileDir.text()
                            try:
                                file_handle = open(newFilePath, mode='a')
                                file_handle.write(strTemp)
                            except:
                                self.debugView.appendPlainText("保存路径错误！")


                        else:
                            self.debugView.appendPlainText("检测到测试用例中测试类型设置不匹配！")
                    else:
                        self.debugView.appendPlainText("检测到测试用例中测试产品设置不匹配！")

                if self.testType.currentText() == 'Current测试':
                    productName = str(self.conf.get("Test Info", "productName"))#获取测试产品名称
                    testType = str(self.conf.get("Test Info", "testType"))+"测试"#获取测试类型

                    testUartRemotes = str(self.conf.get("Test Condition", "testUartRemotes")).split(",")#获取测试uart指令
                    print(testUartRemotes)
                    config = {'testMode': str(self.conf.get("Test Condition", "testMode"))}
                    print(config)

                    if productName == self.chipName.text():
                        if testType == self.testType.currentText():
                            newTemp = VoltOrCurr_Parameter
                            newVoltageTest = newTemp.getValue('数字万用表1')
                            temp = 0
                            outData = []
                            for testUartRemote in testUartRemotes:
                                if testUartRemotes[0] != "无":
                                    print(testUartRemote)
                                    testUartRemote = (testUartRemote + '\r\n').encode('utf-8')
                                    num = self.ser.write(testUartRemote)
                                result = newVoltageTest.test_Start(**config)
                                if result[0] == 'err':
                                    self.debugView.appendPlainText(result[1])
                                    QApplication.processEvents()
                                    break
                                if result[0] == 'success':
                                    print(result)
                                    outData.append(str(result[1]).replace("\n", ""))
                                    self.debugView.appendPlainText("电流值："+str(result[1]).replace("\n","")+"A:已保存！")
                                    QApplication.processEvents()

                                    temp = temp + 1
                            strTemp = str(outData).replace('[', '')
                            strTemp = strTemp.replace(']', '')
                            strTemp = strTemp.replace("'", '')
                            strTemp = strTemp.replace(",", '\t')
                            strTemp = self.chipNum.text() + '\t' + strTemp + '\t' + self.testDate.text() + '\t' + self.testerNum.text() + '\n'
                            newFilePath = self.fileDir.text()
                            try:
                                file_handle = open(newFilePath, mode='a')
                                file_handle.write(strTemp)
                            except:
                                self.debugView.appendPlainText("保存路径错误！")


                        else:
                            self.debugView.appendPlainText("检测到测试用例中测试类型设置不匹配！")
                    else:
                        self.debugView.appendPlainText("检测到测试用例中测试产品设置不匹配！")

                try:
                    self.chipNum.setText(str(int(self.chipNum.text())+1))
                except BaseException:
                    self.debugView.appendPlainText("芯片序号设置错误！")
                self.beginAction.setEnabled(True)
            else:
                if str(self.iniFileDir.text()).find("ini")>0:
                    self.debugView.appendPlainText("请连接串口！")
                else:
                    self.debugView.appendPlainText("请导入正确测试用例！")


    def newTest(self):
        self.th = WorkThread(ip='192.168.1.1', port=4000)
        self.th.finishSignal.connect(self.button_finish)
        # t= threading.Thread(target=self.testBegin(),args=(111,112))#创建线程
        # t.start()


# self.work1 = work(1)
# self.work1.start()

        # self.daq = Process(target=self.Read_data())
        # print("thread success")
        # pool = Pool(processes = 3)
        # pool.apply_async(self.testBegin,(1,))
        # #pool.apply_async(self.testBegin,(2,))
        # pool.close()
        #self.thread = Runthread()  # 创建线程
        #self.thread._signal.connect(self.testBegin)  # 连接信号
        #self.thread.start()  # 开始线程



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setWindowTitle("自动测试系统客户端"+str_ver)
    mainWindow.label.setText(str_ver)
    mainWindow.show()
    sys.exit(app.exec_())
