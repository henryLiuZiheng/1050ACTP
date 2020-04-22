import visa
tcp_addr = ""
rm1 = visa.ResourceManager()
ZVB8Instr = rm1.open_resource(self.tcp_addr)