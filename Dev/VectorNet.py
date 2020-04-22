from Dev import Dev

class VectorNet(Dev):
    def __init__(self, Name = "", ConnectType = 0,t=0):  # 先继承，在重构
        super().__init__(Name, ConnectType)
        self.t = t

test = VectorNet(Name="vect1",ConnectType = 0,t=0)
print("aa")
test.print_dev()
