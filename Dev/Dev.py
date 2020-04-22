class Dev(object):
    def __init__(self, Name = "", ConnectType = 0):
        self.Name = Name
        self.ConnectType = ConnectType
        print("dev init:", self.Name)
		
    def print_dev(self):
        print("dev name:", self.Name)