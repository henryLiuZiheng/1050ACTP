class Interpreter(object):
    def __init__(self):
        self.stack = []
        #存储变量映射关系的字典变量
        self.environment = {}

#函数指针调用
def hwFunc1(x):
	print("hwFunc1 %s" %(x+1))

def hwFunc2(x):
	print("hwFunc2 %s" %(x+1))

 
 
funcSets={"func1":hwFunc1,"func2":hwFunc2}
funcSets["func1"](1)
