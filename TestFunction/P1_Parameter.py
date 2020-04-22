from Dev import BRJX_AT_LIB
from Dev import remoteGet


class P1:
    def __init__(self,deviceName):
        self.ATM = BRJX_AT_LIB.AutoTest('P1',deviceName,deviceName)
        self.linkState = self.ATM.linkState
        self.usingState = False

    def reFreshState(self):
        self.usingState = True

    def test_Start(self, TestConditions, AverCount, PowerStop):
        self.freeState = False
        newTestConditions = TestConditions.split(',')
        print(newTestConditions)

        if self.linkState == 1:
            return self.ATM.P1(newTestConditions, AverCount, PowerStop)
        else:
            result = ['err','未检测到测试仪表，请检查仪表连接情况！']
            return result
