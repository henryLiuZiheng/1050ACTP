from Dev import BRJX_AT_LIB
import os

class S_Data:

    def __init__(self,deviceName):

        self.ATM = BRJX_AT_LIB.AutoTest('S_DATA',deviceName,deviceName)
        self.linkState = self.ATM.linkState
        self.savePath = ''
        self.usingState = False
        if self.linkState :
            if deviceName == 'ZVA40':
                self.savePath = 'x:\\'         #ZVA40映射为X盘

            if deviceName == 'ZVA50':
                self.savePath = 'z:\\'         #ZVA50映射为Z盘


    def mkdir(self,path):
        # 引入模块

        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")

        # 判断路径是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            print('success')

            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在

            return False

    def reFreshState(self):
        self.usingState = True

    def test_Start(self,TestConditions,chipName,testTemp,fileName):
        newTestConditions = TestConditions.split(',')
        if self.linkState == 1:

            spath = chipName+'\\'+testTemp
            path ='md '+ self.savePath+spath
            devPath = 'c:\\Users\\'+spath
            try:
                #os.system("net use z: \\"+self.savePath+"\\Users")
                os.system(path)
            except BaseException:
                print('已有映射')
            self.ATM.refreshDir(devPath)
            result = self.ATM.S_DATA(newTestConditions, fileName)
            return result
        else:
            result = ['err','未检测到测试仪表，请检查仪表连接情况！']
            return result