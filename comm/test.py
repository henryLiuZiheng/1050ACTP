import os
import numpy as np
x = open('z:\BR9175\CW\BR9175S_DATACW1Ch1.s2p')
y = x.readlines()
mm = 0
temp = []
for line in y:
    mm = mm+1
    if mm > 5:
        line = line.strip()
        line = line.split('  ')
        temp.append(line)
print(temp)
temp = np.array(temp)
temp = np.delete(temp, 1, axis=1)
print(temp)
Z = complex(a[cnt], b[cnt])
ZZ.append(Z)
cnt = cnt + 1
am = np.abs(ZZ)
ph = np.angle(ZZ)