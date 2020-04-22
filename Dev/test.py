import visa
import time
import os, sys

def test_GPIB():
    dev_list = list()
    resManage = visa.ResourceManager()
    reslists = resManage.list_resources()
    print(repr(reslists))
    #devname = reslists[4]
    #ins = resManage.open_resource(devname)
    #meas = ins.write('MEAS:VOLT:DC? 10, MAX')
    #meas = ins.write('*IDN?')
    for reslist in reslists:
        try:
            ins = resManage.open_resource(reslist)
            meas = ins.query('*IDN?')
            strlists = meas.split(",", 2)
            print("%s is %s %s" % (reslist, strlists[0], strlists[1]))
            dev_str = strlists[0] + " " + strlists[1]
            dev_list.append(dev_str)
            #yield dev_str
            
            
            return dev_list
        except:
            print(reslist)

devlis = test_GPIB()
#aa = dict.fromkeys(devlis, reslists)
print(devlis)

def test():
    dev_list2 = list()
