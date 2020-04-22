from Dev import BRJX_AT_LIB
from Dev import remoteGet


class THD:
    def __init__(self,deviceName):
        self.ATM = BRJX_AT_LIB.AutoTest('THD',deviceName,deviceName)
        self.linkState = self.ATM.linkState
        self.usingState = False

    def reFreshState(self):
        self.usingState = True

    def test_Start(self, FreqData,FreqSpan):
        self.freeState = False


        if self.linkState == 1:
            return self.ATM.THD(FreqData,FreqSpan)
        else:
            result = ['err','未检测到测试仪表，请检查仪表连接情况！']
            return result