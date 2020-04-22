from Dev import BRJX_AT_LIB
from Dev import remoteGet


class NF:
    def __init__(self,deviceName):
        self.ATM = BRJX_AT_LIB.AutoTest('NF',deviceName,deviceName)
        self.linkState = self.ATM.linkState
        self.usingState = False

    def reFreshState(self):
        self.usingState = True

    def test_Start(self, FreqStart, FreqStop, sweepPoint,average,EnrTable,LossInputTable,LossOutputTable,SweepTime):
        self.freeState = False
        if self.linkState == 1:
            #FreqStart,FreqStop,sweepPoint,EnrTable,LossInputTable,LossOutputTable,SweepTime
            return self.ATM.NOISE_FIGURE(FreqStart, FreqStop, sweepPoint,average,EnrTable,LossInputTable,LossOutputTable,SweepTime)
        else:
            result = ['err','未检测到测试仪表，请检查仪表连接情况！']
            return result
