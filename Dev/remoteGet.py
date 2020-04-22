import visa
import time

#日期：2019年08月24日
#版本：V1.0
#制作人：刘子恒

#罗德矢量网络分析仪
class ZVA:
    #
    def __init__(self,devName,savePath):
        self.filePath = savePath

        if(devName == 'ZVB8'):
            self.tcp_addr = 'TCPIP0::192.168.1.18::inst0::INSTR'
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1

        if(devName == 'ZVA40'):
            self.tcp_addr = 'TCPIP0::192.168.1.20::inst0::INSTR'
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1


        if(devName == 'ZVA50'):
            self.tcp_addr = 'TCPIP0::192.168.1.15::inst0::INSTR'
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1

    #S参数测试方法，设置POWIN（输入功率）、STARTFREQ（起始频点）、STOPFREQ（终止频点）、FILENAME（s2p文件名称）参数，
    # 返回值0：s2p文件保存成功，其余返回值详见错误代码表
    def S_data_save(self, POWERIN, STARTFREQ, STOPFREQ, FILENAME):
        lines =['SYST:DISP:UPD ON@',
                'SENS1:SWE:TYPE LIN@',
                'SENS1:FREQ:STAR STARTFREQ@',
                'SENS1:FREQ:STOP STOPFREQ@',
                'SOUR1:POW POWERIN@',
                '延迟500ms@',
                "CALC1:PAR:SDEF 'Trc1','S21'@",
                "DISP:WIND1:STAT ON;:DISP:WIND1:TRAC1:FEED 'Trc1'@",
                "CALC1:PAR:SDEF 'Trc2','S11'@",
                "DISP:WIND1:STAT ON;:DISP:WIND1:TRAC2:FEED 'Trc2'@",
                "CALC1:PAR:SDEF 'Trc3','S12'@",
                "DISP:WIND1:STAT ON;:DISP:WIND1:TRAC3:FEED 'Trc3'@",
                "CALC1:PAR:SDEF 'Trc4','S22'@",
                "DISP:WIND1:STAT ON;:DISP:WIND1:TRAC4:FEED 'Trc4'@",
                '延迟500ms@',
                'MMEM:STOR:TRAC:CHAN ALL,FILEPATH@']
        #FILEPATH = "'"+self.filePath+'\\'+FILENAME +'.s2p'+"'"
        FILEPATH = "'Traces\\" + FILENAME + '.s2p' + "'"
        for line in lines:
            if(line.find('@')>0):
                instr = line[:line.index('@')]
                if(instr.find('?')<0):
                    if(instr == '延迟500ms'):
                        time.sleep(0.5)
                    else:
                        instr = instr.replace('POWERIN', POWERIN)
                        instr = instr.replace('STARTFREQ', STARTFREQ)
                        instr = instr.replace('STOPFREQ', STOPFREQ)
                        instr = instr.replace('FILEPATH', FILEPATH)
                        print(instr)
                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return -1
        return 0

    #P-1测试方法，设置AVERCOUNT（平均采样次数）、POWERSTOP（截至功率）、CWFREQ（待测频点）参数，
    # 返回值为'<port_In>,<port_Out>'：代表输入1dB压缩点和输出1dB压缩点，其余返回值详见错误代码表
    def P1_data(self, AVERCOUNT, POWERSTOP, CWFREQ):
        lines =['SYST:DISP:UPD ON@',
                "CALC1:PAR:DEL 'Trc2'@",
                "CALC1:PAR:DEL 'Trc3'@",
                "CALC1:PAR:DEL 'Trc4'@",
                'SENS1:SWE:TYPE POW@',
                'SENS1:AVER:COUN AVERCOUNT@',
                'SENS1:AVER ON@',
                "DIAG:SERV:RFP ON@",
                "SENS1:FREQ:CW CWFREQ@",
                "延迟100ms@",
                "SOUR1:POW:STOP POWERSTOP@",
                "延迟100ms@",
                "CALC1:STAT:NLIN:COMP:LEV 1.000000E+0@",
                '延迟100ms@',
                'CALC1:STAT:NLIN:COMP:RES?@',
                'DIAG:SERV:RFP OFF@']

        for line in lines:
            if(line.find('@')>0):
                instr = line[:line.index('@')]
                if(instr.find('?')<0):
                    if(instr == '延迟100ms'):
                        time.sleep(0.3)
                    else:
                        instr = instr.replace('AVERCOUNT', AVERCOUNT)
                        instr = instr.replace('CWFREQ', CWFREQ)
                        instr = instr.replace('POWERSTOP', POWERSTOP)
                        try:
                            print(instr)
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return -2

    #频段内最大增益点测试方法，设置AVERCOUNT（平均采样次数）、STARTFREQ（起始频点）、STOPFREQ（终止频点）参数，
    # 返回值为'<freq>,<mag>'：最大增益对应频率和最大增益值，其余返回值详见错误代码表
    def mark_max_data(self,AVERCOUNT,STARTFREQ,STOPFREQ):
        lines = ['SYST:DISP:UPD ON@',
                 'SENS1:SWE:TYPE LIN@',
                 'SENS1:AVER:COUN AVERCOUNT@',
                 'SENS1:AVER ON@',
                 "SENS1:FREQ:STAR STARTFREQ@",
                 "SENS1:FREQ:STOP STOPFREQ@",
                 "延迟100ms@",
                 "CALC1:MARK1 OFF@",
                 "延迟100ms@",
                 "CALC1:MARK1 ON@",
                 "延迟100ms@",
                 "CALC1:MARK1:FUNC:EXEC MAX@",
                 '延迟100ms@',
                 'CALC1:MARK1:FUNC:RES?@']

        for line in lines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.1)
                    else:
                        instr = instr.replace('AVERCOUNT', AVERCOUNT)
                        instr = instr.replace('STARTFREQ', STARTFREQ)
                        instr = instr.replace('STOPFREQ', STOPFREQ)

                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return '-2:remote指令错误，请设置合适参数'
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return '-3:请求矢网返回数据超时'

    #通过MARK点获取频点对应Value
    def mark_data(self, **kwargs):
        strParams = ["ch", "markPoint", "freqData","status"]
        for strParam in strParams:
            try:
                if type(kwargs[strParam]) != str:
                    kwargs[strParam] = str(kwargs[strParam])
            except BaseException:
                return "-3:缺少" + strParam + "参数"
        lines = [
            "CALC" + kwargs["ch"] + ":MARK" + kwargs["markPoint"]+" "+kwargs["status"]+"@",
            "CALC" + kwargs["ch"] + ":MARK" + kwargs["markPoint"]+":X "+kwargs["freqData"]+"@",
            '延迟100ms@',
            "CALC" + kwargs["ch"] + ":MARK" + kwargs["markPoint"]+":Y?@"
        ]

        for line in lines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.2)
                    else:
                        try:
                            print(instr)
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                        return self.instance.query(instr)
                    except BaseException:
                        return -2

    #添加trace
    def add_ch(self,**kwargs):
        strParams = ["window","ch","testType","dataType","trac","traceName","traceType"]
        for strParam in strParams:
            try:
                if type(kwargs[strParam]) != str:
                    kwargs[strParam] = str(kwargs[strParam])
            except BaseException:
                return "-3:缺少"+strParam+"参数"
        lines =[
            "CALC" + kwargs["ch"] + ":PAR:SDEF " + "'" + kwargs["traceName"] + "'" + "," + "'" + kwargs[
                "traceType"] + "'" + "@",
            "DISP:WIND"+kwargs["window"]+":STAT ON;:DISP:WIND"+kwargs["window"]+":TRAC"+kwargs["trac"]+":FEED '"+kwargs["traceName"]+"'@",
            "SENS"+kwargs["ch"]+":SWE:TYPE "+kwargs["testType"]+"@",
            "CALC"+kwargs["ch"]+":FORM "+kwargs["dataType"]+"@"
        ]

        for line in lines:
            if(line.find('@')>0):
                instr = line[:line.index('@')]
                if(instr.find('?')<0):
                    if(instr == '延迟100ms'):
                        time.sleep(0.3)
                    else:
                        try:
                            print(instr)
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return -2
        return 0

    #删除频道及trace
    def delete_ch(self,ch):
        if type(ch) != str:
            ch = str(ch)
        lines =[
            "CALC"+ch+":PAR:DEL:CALL@"
        ]

        for line in lines:
            if(line.find('@')>0):
                instr = line[:line.index('@')]
                if(instr.find('?')<0):
                    if(instr == '延迟100ms'):
                        time.sleep(0.3)
                    else:
                        try:
                            print(instr)
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return -2
        return 0

#罗德频谱仪系列
class RSFSx:
    #
    def __init__(self,devName):
        self.linkState = 0
        if(devName == 'FSWP'):
            self.tcp_addr = 'TCPIP0::192.168.1.80::inst0::INSTR'
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1

        if(devName == 'FSV'):
            self.tcp_addr = 'TCPIP0::192.168.1.81::inst0::INSTR'
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1

    def IM3_Pfund_data(self,CENTERFREQ, SPANFREQ):
        lines = ['SYST:DISP:UPD ON@',
                 'INST SAN@',
                 'FREQ:CENT CENTERFREQ@',
                 'FREQ:SPAN SPANFREQ@',
                 'CALC1:MARK1 ON@',
                 '延迟100ms@',
                 'CALC1:MARK1:TRAC 1@',
                 '延迟100ms@',
                 'CALC1:MARK1:X '+str(int(CENTERFREQ)+1500000)+'@',
                 '延迟100ms@',
                 'CALC1:MARK1:Y?@',
                 #IM3
                 '延迟100ms@',
                 'CALC1:MARK2 ON@',
                 '延迟100ms@',
                 'CALC1:MARK2:TRAC 1@',
                 '延迟100ms@',
                 'CALC1:MARK2:X '+str(int(CENTERFREQ)+500000)+'@',
                 '延迟100ms@',
                 'CALC1:MARK2:Y?@']
                 #Pfund


        data = []
        for line in lines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.1)
                    else:
                        instr = instr.replace('CENTERFREQ', CENTERFREQ)
                        instr = instr.replace('SPANFREQ', SPANFREQ)
                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return -1 #连接关系出错
                else:
                    if(instr.find('MARK1') >= 0):
                        try:
                            data.append(self.instance.query(instr))
                        except BaseException:
                            return -2  #测试结果出错
                    if(instr.find('MARK2') >= 0):
                        try:
                            data.append(self.instance.query(instr))
                        except BaseException:
                            return -2   #测试结果出错
        return data

    def noise_figure(self,FREQSTART, FREQSTOP,SWEEPPOINT,AVERAGE,ENRTABLE, LOSSINPUTTABLE, LOSSOUTPUTTABLE, SWEEPTIME):
        outData = []
        lines = [#'延迟100ms@',
                 'SYST:DISP:UPD ON@'
                 'FREQ:STAR FREQSTART@',#20MHz
                 #'延迟100ms@',
                 'FREQ:STOP FREQSTOP@',#2000MHz
                 #'延迟100ms@',
                 #'CONF:FREQ:SING@',
                 'SWE:POIN SWEEPPOINT@',
                 #'FREQ:LIST:DATA FREQTABLE@'
                 #'INIT:CONT OFF',
                 'CORR:ENR:MODE TABL@',
                 'CORR:ENR:MEAS:TABL:DATA ENRTABLE@',#1MHZ,10,2MHZ,12
                 'CORR:LOSS:INP:MODE TABL@',
                 'CORR:LOSS:INP:TABL LOSSINPUTTABLE@',#1MHz,10,2MHz,12
                 'CORR:LOSS:OUTP:MODE TABL@',
                 'CORR:LOSS:OUTP:TABL LOSSOUTPUTTABLE@',#1MHz,10,2MHz,12
                 #'CORR ON@',
                 'SWE:COUN AVERAGE@'
                 'SWE:TIME SWEEPTIME@',#0.1s
                 'CONF:LIST:SING@',
                 'INIT:CONT OFF@',
                 'INIT:IMM@',
                 '延迟100ms@',
                 #'CONF:LIST:SING@',

                 #'CONF:ARR:MEM2 ONCE@',
                 'FETC:ARR:NOIS:FIG?@']
                 #'FETC:ARR:NOIS:GAIN?@']

                 #Mark

        for line in lines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                print(instr)
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        delayTime = (float(SWEEPPOINT)*float(AVERAGE))*(float(SWEEPTIME.replace("s",""))+0.05)+3
                        print(delayTime)

                        time.sleep(delayTime)
                    else:
                        instr = instr.replace('FREQSTART', FREQSTART)
                        instr = instr.replace('FREQSTOP', FREQSTOP)
                        instr = instr.replace('SWEEPPOINT', SWEEPPOINT)
                        instr = instr.replace('ENRTABLE', ENRTABLE)
                        instr = instr.replace('LOSSINPUTTABLE', LOSSINPUTTABLE)
                        instr = instr.replace('LOSSOUTPUTTABLE', LOSSOUTPUTTABLE)
                        instr = instr.replace('AVERAGE', AVERAGE)



                        instr = instr.replace('SWEEPTIME', SWEEPTIME)
                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    if(instr.find('FIG')>0):
                        try:
                            temp = str(self.instance.query(instr))
                            print(temp)
                            #outData.append(temp)
                            outData = str(temp)
                        except BaseException:
                            return -2
                    if(instr.find('GAIN')>0):
                        try:
                            temp = str(self.instance.query(instr))
                            outData.append(temp)
                        except BaseException:
                            return -2
        return outData


    def mark_data(self,CENTERFREQ, SPANFREQ):
        lines = ['SYST:DISP:UPD ON@',
                 'INST SAN@',
                 'FREQ:CENT CENTERFREQ@',
                 'FREQ:SPAN SPANFREQ@',
                 '延迟100ms@',
                 'CALC1:MARK1 ON@',
                 '延迟100ms@',
                 'CALC1:MARK1:TRAC 1@',
                 '延迟100ms@',
                 'CALC1:MARK1:X CENTERFREQ@',
                 '延迟100ms@',
                 'CALC1:MARK1:Y?@']
                 #Mark
        rm1 = visa.ResourceManager()
        try:
            instance = rm1.open_resource(self.tcp_addr)
        except BaseException:
            return '-1：连接矢网超时'
        for line in lines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.1)
                    else:
                        instr = instr.replace('CENTERFREQ', str(CENTERFREQ))
                        instr = instr.replace('SPANFREQ', str(SPANFREQ))
                        try:
                            instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    if(instr.find('MARK1') > 0):
                        try:
                            temp = str(instance.query(instr))
                            return temp
                        except BaseException:
                            return -2

#罗德信号源系列
class RSRFSin:
    def __init__(self,devName):
        self.linkState = 0

        if(devName == 'SMW200A'):
            self.tcp_addr = 'TCPIP0::192.168.1.120::inst0::INSTR'
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1

        if(devName == 'SMF'):
            self.tcp_addr = 'TCPIP0::ZVA50-50-100364::inst0::INSTR'
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1

    def RFout(self,RFFREQ, POWVALUE, IQSTATE, RFOUTSTATE):
        lines = ['SOUR1:FREQ RFFREQ@',
                 'SOUR1:POW POWVALUE@',
                 ':SOUR1:IQ:STAT IQSTATE@',
                 'OUTP1 RFOUTSTATE@']

        for line in lines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.1)
                    else:
                        instr = instr.replace('RFFREQ', RFFREQ)
                        instr = instr.replace('POWVALUE', POWVALUE)
                        instr = instr.replace('IQSTATE', IQSTATE)
                        instr = instr.replace('RFOUTSTATE', RFOUTSTATE)
                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return -2
#罗德示波器系列
class RSRTMosc:
    def __init__(self,devName):
        self.linkState = 0

        if(devName == 'RTM1054'):
            self.tcp_addr = 'TCPIP0::192.168.1.91::inst0::INSTR'#地址为192.168.1.91
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1
    outdata = []
    def config(self,**kwargs):
        comlines = [
                 'TIMebase:SCALe scaleTime@',
                 'TIMebase:POSition timePosition@',
                 'CHANnel1:STATe CH1State@',
                 'CHANnel2:STATe CH2State@',
                 'CHANnel3:STATe CH3State@',
                 'CHANnel4:STATe CH4State@'
                 ]

        ChannelsSetlines = []
        if kwargs["CH1State"] == "ON":
            ChannelsSetlines.append("CHANnel1:SCALe "+str(kwargs["CH1DIV"])+"@")
            ChannelsSetlines.append("CHANnel1:OFFSet "+str(kwargs["CH1offset"])+"@")
            ChannelsSetlines.append("MEASurement1:SOURce CH1@")
            ChannelsSetlines.append("MEASurement1:ENABle ON@")
            ChannelsSetlines.append("MEASurement1:STATistics:ENABle ON@")
        else:
            ChannelsSetlines.append("MEASurement1:ENABle OFF@")


        if kwargs["CH2State"] == "ON":
            ChannelsSetlines.append("CHANnel2:SCALe "+str(kwargs["CH2DIV"])+"@")
            ChannelsSetlines.append("CHANnel2:OFFSet "+str(kwargs["CH2offset"])+"@")
            ChannelsSetlines.append("MEASurement2:SOURce CH2@")
            ChannelsSetlines.append("MEASurement2:ENABle ON@")
            ChannelsSetlines.append("MEASurement2:STATistics:ENABle ON@")
        else:
            ChannelsSetlines.append("MEASurement2:ENABle OFF@")

        if kwargs["CH3State"] == "ON":
            ChannelsSetlines.append("CHANnel3:SCALe "+str(kwargs["CH3DIV"])+"@")
            ChannelsSetlines.append("CHANnel3:OFFSet "+str(kwargs["CH3offset"])+"@")
            ChannelsSetlines.append("MEASurement3:SOURce CH3@")
            ChannelsSetlines.append("MEASurement3:ENABle ON@")
            ChannelsSetlines.append("MEASurement3:STATistics:ENABle ON@")
        else:
            ChannelsSetlines.append("MEASurement3:ENABle OFF@")

        if kwargs["CH4State"] == "ON":
            ChannelsSetlines.append("CHANnel4:SCALe "+str(kwargs["CH4DIV"])+"@")
            ChannelsSetlines.append("CHANnel4:OFFSet "+str(kwargs["CH4offset"])+"@")
            ChannelsSetlines.append("MEASurement4:SOURce CH4@")
            ChannelsSetlines.append("MEASurement4:ENABle ON@")
            ChannelsSetlines.append("MEASurement4:STATistics:ENABle ON@")
        else:
            ChannelsSetlines.append("MEASurement4:ENABle OFF@")

        triglines = [
            'TRIGger:A:SOURce ' + kwargs["TriggerSourc"]+'@',
            'TRIGger:A:MODE ' + str(kwargs["TriggerMode"])+'@'
        ]
        if kwargs["TriggerSourc"] == 'CH1':
            triglines.append("TRIGger:A:LEVel1:VALue "+str(kwargs["TriggerLevel"])+"@")
        if kwargs["TriggerSourc"] == 'CH2':
            triglines.append("TRIGger:A:LEVel2:VALue "+str(kwargs["TriggerLevel"])+"@")
        if kwargs["TriggerSourc"] == 'CH3':
            triglines.append("TRIGger:A:LEVel3:VALue "+str(kwargs["TriggerLevel"])+"@")
        if kwargs["TriggerSourc"] == 'CH4':
            triglines.append("TRIGger:A:LEVel4:VALue "+str(kwargs["TriggerLevel"])+"@")


        savelines = [
            'MMEM:MDIR "/USB_FRONT/' + kwargs["saveDirName"]+'"@',
            'MMEM:CDIR "/USB_FRONT/' + kwargs["saveDirName"] + '"@',
            'HCOP:DEST "MMEM"@',
            'HCOP:LANG PNG@',
            'HCOP:COL:SCH COL@',
            'MMEM:NAME "'+ kwargs["saveFileName"] + '"@',
            'HCOP:IMM@',
            '延迟10000ms@',
            'CHANnel1:DATA:XINCrement?@',
            '延迟1000ms@',
            'CHANnel1:DATA?@'
        ]

        for line in comlines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.1)
                    else:
                        instr = instr.replace('scaleTime', str(kwargs["scaleTime"]))
                        instr = instr.replace('timePosition', str(kwargs["timePosition"]))
                        instr = instr.replace('CH1State', str(kwargs["CH1State"]))
                        instr = instr.replace('CH2State', str(kwargs["CH2State"]))
                        instr = instr.replace('CH3State', str(kwargs["CH3State"]))
                        instr = instr.replace('CH4State', str(kwargs["CH4State"]))

                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                        self.instance.query(instr)
                    except BaseException:
                        return -2

        for line in triglines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.1)
                    else:
                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return -2

        for line in ChannelsSetlines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.1)
                    else:
                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return -2
        time.sleep(float(kwargs["waitTimeBeforeSaving"]))
        data = []
        for line in savelines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (line.find('ms') > 0):
                        a = instr.replace('延迟','')
                        b = a.replace('ms','')
                        print(b)
                        print(float(b)/1000)
                        time.sleep((float(b)/1000))
                    else:
                        try:
                            self.instance.write(instr)
                            print(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       data.append(self.instance.query(instr))
                    except BaseException:
                        return -2
        return data

#是德科技3446X系列（数字万用表）
class KeySightDigit:
    def __init__(self,devName):
        self.linkState = 0

        if(devName == '数字万用表1'):
            self.tcp_addr = '34461A_1'#地址为192.168.1.91
            rm1 = visa.ResourceManager()
            try:
                print(4)
                self.instance = rm1.open_resource(self.tcp_addr)
                print(5)

            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1

    def getValue(self,**kwargs):
        outData = 0
        getlines = [
            '延迟500ms@',
            ':FUNC "' + kwargs["testMode"]+'"@',
            ':' + kwargs["testMode"] + ':RANG:AUTO ON@',
            ':SAMP:COUN 1@',
            ':TRIG:SOUR IMM@',
            ':READ?@'
        ]
        for line in getlines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟500ms'):
                        time.sleep(0.5)
                    else:
                        try:
                            print(instr)
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                        outData = self.instance.query(instr)
                    except BaseException:
                        return -2
        return outData


class comFun:
    def __init__(self,strType):
        self.flag = strType

    def flaotOrintAll(self,a):
        if(self.flag == 'float'):
            temp = 0
            if(a.find('-')>=0):
                try:
                    temp =0 - float(a.replace('-',''))
                except BaseException:
                   print( 'float转换错误')
            else:
                try:
                    temp = float(a)
                except BaseException:
                    print('float转换错误')
            return temp

        if(self.flag == 'int'):
            temp = 0
            if (a.find('-') >= 0):
                try:
                    temp = 0 - int(a.replace('-', ''))
                except BaseException:
                    print('int转换错误')
            else:
                try:
                    temp = int(a)
                except BaseException:
                    print('int转换错误')
            return temp

