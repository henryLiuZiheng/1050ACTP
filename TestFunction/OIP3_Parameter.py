from Dev import BRJX_AT_LIB
from Dev import remoteGet


class IP3:
    def __init__(self, deviceName1,deviceName2):#仪器1为信号源 ， 仪器2为频谱仪
        self.ATM = BRJX_AT_LIB.AutoTest('IP3', deviceName1, deviceName2)
        self.linkState = self.ATM.linkState
        self.freeState = True

    def reFreshState(self):
        self.freeState = True

    def test_Start(self, TestConditions, SignalLosses,PoutData, SpanFreq, PowerLimTh):
        self.freeState = False
        newTestConditions = TestConditions.split(',')
        newSignalLosses = SignalLosses.split(',')


        if self.linkState == 1:
            return self.ATM.IP3(newTestConditions, newSignalLosses,PoutData, SpanFreq, float(PowerLimTh))
        else:
            result = ['err','未检测到测试仪表，请检查仪表连接情况！']
            return result
