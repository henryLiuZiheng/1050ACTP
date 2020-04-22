from Dev import remoteGet as newRemoteGet
import math


class AutoTest:
    def __init__(self,TestType, DeviceNa1, DeviceNa2):
        self.equipmentNum = 0
        #选择测试指标类型
        if(TestType == 'P1'):
            self.equipmentNum = 1                                #设备数查询标识
            self.ZVADevice = DeviceNa1                           #选择设备名
            self.ZVA = newRemoteGet.ZVA(self.ZVADevice,'c:\\Users\\594')   #创建ZVA类对象
            self.linkState = self.ZVA.linkState                  #查询连接情况并赋值

        if(TestType == 'S_DATA'):
            self.equipmentNum = 1                                 #设备数查询标识
            self.ZVADevice = DeviceNa1                            #选择设备名
            self.ZVA = newRemoteGet.ZVA(self.ZVADevice,'c:\\Users\\594')    #创建ZVA类对象
            self.linkState = self.ZVA.linkState                   #查询连接情况并赋值

        if(TestType == 'IP3'):
            self.equipmentNum = 2                                 #设备数查询标识
            self.RfDevice = DeviceNa1                             #选择信号源设备名
            self.FSxDevice = DeviceNa2                            #选择频谱仪设备名
            self.FSWP = newRemoteGet.RSFSx(self.FSxDevice)           #创建频谱仪类对象s
            self.SMW = newRemoteGet.RSRFSin(self.RfDevice)           #创建信号源类对象
            #print(self.FSWP.linkState)
            print(self.SMW.linkState)

            if(self.FSWP.linkState&self.SMW.linkState):           #查询两台设备连接情况并赋值（同时连接成功才认为仪表连接成功）
                self.linkState = 1
            else:
                self.linkState = 0

        if (TestType == 'NF'):
            self.equipmentNum = 1  # 设备数查询标识
            self.FSxDevice = DeviceNa1  # 选择设备名
            self.FSWP = newRemoteGet.RSFSx(self.FSxDevice)  # 创建频谱仪类对象
            self.linkState = self.FSWP.linkState  # 查询连接情况并赋值

        if (TestType == 'THD'):
            self.equipmentNum = 1  # 设备数查询标识
            self.FSxDevice = DeviceNa1  # 选择设备名
            self.FSWP = newRemoteGet.RSFSx(self.FSxDevice)  # 创建频谱仪类对象
            self.linkState = self.FSWP.linkState  # 查询连接情况并赋值

        if (TestType == 'wavetest'):
            str_dict = {'scaleTime': 0.1,
                        'timePosition': 0.001,

                        'CH1State':"ON",
                        'CH1DIV':0.1,
                        'CH1offset':0,

                        'CH2State':"ON",
                        'CH2DIV':0.1,
                        'CH2offset':0,

                        'CH3State': "OFF",

                        'CH4State': "OFF",

                        'TriggerSourc':'CH1',
                        'TriggerLevel':0,
                        'TriggerMode':'AUTO',

                        'saveDirName':'LZH/BR9281',
                        'saveFileName':'br92813',

                        'waitTimeBeforeSaving':10

                        }
            self.confStruct = str_dict
            self.equipmentNum = 1  # 设备数查询标识
            self.RTMDevice = DeviceNa1  # 选择设备名
            self.RTM = newRemoteGet.RSRTMosc(self.RTMDevice)  # 创建频谱仪类对象
            self.linkState = self.RTM.linkState  # 查询连接情况并赋值

        if (TestType == 'VoltOrCurr'):
            print(2)
            self.equipmentNum = 1  # 设备数查询标识
            self.DigitDevice = DeviceNa1  # 选择设备名
            self.DIGIVoltAndCurr = newRemoteGet.KeySightDigit(self.DigitDevice)  # 创建频谱仪类对象
            print(3)

            self.linkState = self.DIGIVoltAndCurr.linkState  # 查询连接情况并赋值
    #P1测试模块
    #输入：1、测试频点条件
    #      2、平均次数值
    #      3、输入功率设置
    #输出：P1浮点数类型记录数组
    def P1(self, TestConditions, AverCount, PowerStop):                              #P1测试函数
        P1 = ['success']                                                             #创建P1装载数组（浮点数类型）
        P1temps = []                                                                 #创建P1装载数组（字符串类型）
        myFloat = newRemoteGet.comFun('float')                                          #创建类型转换类对象为字符串转浮点数类型
        for testCondition in TestConditions:                                         #根据测试条件进行循环测试
            P1DATA = self.ZVA.P1_data(AverCount, PowerStop, testCondition)
            if (P1DATA == -1):
                P1 = ['err', '指令错误，请设置合理配置参数']
                return P1
            if (P1DATA == -2):
                P1 = ['err', '请求数据超时，请检查连接情况']
                return P1
            try:
                strP1DATA = str(P1DATA).split(',')
                fP1Data = myFloat.flaotOrintAll(strP1DATA[1])  # 装载浮点数类型P1
                P1.append(fP1Data)
            except BaseException:
                print('float转换错误')

        print(P1)                                                                    #输出P1测试数组
        return P1

    #S参数文件保存测试模块
    #输入：1、测试频点条件
    #      2、待保存文件名
    def S_DATA(self,TestConditions, FileName):                                                      #S参数测试函数
        S_Data = ['success']
        vnaDataState = self.ZVA.S_data_save(TestConditions[0], TestConditions[1], TestConditions[2], FileName)     #直接调用一次S参数保存函数，保存文件类型为.s2p格式；保存路径设置有待商议
        if (vnaDataState == -1):
            S_Data = ['err', '指令错误，请设置合理配置参数']
            return S_Data
        else:
            S_Data = ['success', '.s2p文件数据已保存到仪器c:\\\\Rohde&Schwarz\\\\Nwa\\\\Traces 路径下']
            return S_Data
    #IP3测试模块
    #输入：1、测试频点条件
    #      2、环境线损记录数组
    #      3、频率Span值
    #      4、信号源功率输出保护门限
    #输出：IP3浮点数类型记录数组
    def IP3(self, TestConditions, SignalLosses,PoutData, SpanFreq, PowerLimTh):              #IP3测试函数
        signalLevel = -15                                                           #设置初始信号源输出功率
        IP3 = ['success']                                                           #创建IP3浮点数类型数组

        myFloat = newRemoteGet.comFun('float')                                         #创建类型转换类对象为字符串转浮点数类型
        reCnt = 0                                                                   #设置信号源功率调整次数上限
        n = 0                                                                       #创建数组索引
        for signalLoss in SignalLosses:                                             #按照数据库线损值进行测试
            flag = True                                                             #设置信号源功率调整开关为开
            while (flag):                                                           #只要Flag为真则重复调整
                SignalState = self.SMW.RFout(TestConditions[n], str(signalLevel), 'ON', 'ON')     #使能信号源双音信号输出（注意：在开启测试前，请配置好信号源双音设置）
                FSWPDATA = self.FSWP.IM3_Pfund_data(TestConditions[n], SpanFreq)    #获取IM3和Pfund数值（FSWPDATA[0]为IM3数据，FSWPDATA[1]为Pfund数据）
                if ((FSWPDATA == -1)|(SignalState == -1)):
                    IP3 = ['err','指令错误，请设置合理配置参数']
                    return IP3
                if ((FSWPDATA == -2)|(SignalState == -2)):
                    IP3 = ['err','请求数据超时，请检查连接情况']
                    return IP3
                try:
                    IM3 = myFloat.flaotOrintAll(FSWPDATA[0].replace('\\n', ''))    #装载浮点数类型IM3数据用于后面程序输出IP3
                    Pfund = myFloat.flaotOrintAll(FSWPDATA[1].replace('\\n', ''))  #装载浮点数类型Pfund数据用于后面程序调整信号源输出功率
                except BaseException:
                    print('float转换错误')
                else:
                    add = myFloat.flaotOrintAll(signalLoss)+myFloat.flaotOrintAll(PoutData) - Pfund                #得到对应频率下Pfund与线损差值
                    print(add)
                    if (abs(add) <= 0.01):                                         #判断Pfund与线损差值情况
                        flag = False                                               #若Pfund与线损差值小于0.01dBm以内，则认为信号源功率调整完毕，关闭信号源调整开关
                        reCnt = 0                                                  #调整次数清零
                        IP3.append(((Pfund-IM3) / 2))                                     #添加一次IP3数据
                    else:
                        signalLevel = signalLevel + add                            #若Pfund与线损差值大于0.01dBm，则重新计算signalLevel值
                        if (signalLevel >= PowerLimTh):                            #判断signalLevel值是否大于信号源输出功率保护门限
                            flag = False
                            reCnt = 0                                              #调整次数清零
                            IP3 = ['err', '超过功率保护，请确认环境，设置合适阈值']   #若signalLevel值大于信号源输出功率保护门限，则报警，并关闭信号源调整开关
                            return IP3

                        else:
                            flag = True                                            #若signalLevel值小于或等于信号源输出功率保护门限，则继续进行调整
                        if (reCnt > 4):                                            #判断当前频点下，信号源调整次数
                            print('精度大于0.01')                                 #若大于4次，则添加一次IP3数据，并告知点整精度大于0.01
                            IP3.append(((Pfund-IM3) / 2))
                            flag = False
                            reCnt = 0
                reCnt = reCnt + 1                                                  #信号源调整次数加1
            n = n + 1                                                              #测试条件索引加1
        self.SMW.RFout('1000000000', '-15', 'ON', 'OFF')                           #测试结束，关闭信号源输出，并将设置为1G，-15dBm
        print(IP3)                                                                 #输出IP3浮点数类型数组
        return IP3


    def NOISE_FIGURE(self,FreqStart,FreqStop,sweepPoint,average,EnrTable,LossInputTable,LossOutputTable,SweepTime):
        myFloat = newRemoteGet.comFun('float')  # 创建类型转换类对象为字符串转浮点数类型
        NF = ["success"]
        outdata = self.FSWP.noise_figure(FreqStart,FreqStop,sweepPoint,average,EnrTable,LossInputTable,LossOutputTable,SweepTime)
        print(outdata)
        #noiseFigureAndGain = outdata[0].replace('\n','')+';'+outdata[1].replace('\n','')
        #noiseFigure = str(outdata).replace('\n','')
        if (outdata == -1):
            NF = ['err', '指令错误，请设置合理配置参数']
            return NF
        if (outdata == -2):
            NF = ['err','请求数据超时，请检查连接情况']
            return NF
        #print(outdata)
        noiseFigure = outdata.split(',')
        for outdataTemp in noiseFigure:
            NF.append(myFloat.flaotOrintAll(outdataTemp))
        return NF

    def THD(self,FreqData,FreqSpan):
        THD = ["success"]
        myFloat = newRemoteGet.comFun('float')  # 创建类型转换类对象为字符串转浮点数类型
        try:
            #print(self.FSWP.mark_data( FreqData * 1, FreqSpan ))

            V1 = myFloat.flaotOrintAll(self.FSWP.mark_data( FreqData * 1, FreqSpan ))
            V2 = myFloat.flaotOrintAll(self.FSWP.mark_data( FreqData * 2, FreqSpan ))
            V3 = myFloat.flaotOrintAll(self.FSWP.mark_data( FreqData * 3, FreqSpan ))
            V4 = myFloat.flaotOrintAll(self.FSWP.mark_data( FreqData * 4, FreqSpan ))
            V5 = myFloat.flaotOrintAll(self.FSWP.mark_data( FreqData * 5, FreqSpan ))
            V6 = myFloat.flaotOrintAll(self.FSWP.mark_data( FreqData * 6, FreqSpan ))
            temp = (V2 * V2) + (V3 * V3) + (V4 * V4) + (V5 * V5) + (V6 * V6)
            temp = temp/abs(V1)
            temp = temp ** 0.5
            THD_out = 20 * math.log(10,temp)
            THD.append(THD_out)
            THD.append(V1)
            THD.append(V2)
            THD.append(V3)
            THD.append(V4)
            THD.append(V5)
            THD.append(V6)
        except BaseException:
            THD = ['err','数据处理错误']
        return THD

    def wavetest(self,**config):
        waveOutData = ["success"]
        try:
            configData = self.confStruct
            waveOutData.append(self.RTM.config(**config))
        except BaseException:
            waveOutData = ["err","示波器配置出错"]

        return waveOutData

    def getVoltOrCurr(self,**config):
        Data = ["success"]
        try:
            temp = self.DIGIVoltAndCurr.getValue(**config)
            Data.append(temp)
        except BaseException:
            Data = ["err","万用表配置错误"]

        return Data

    def refreshDir(self,path):
        self.ZVA.filePath = path