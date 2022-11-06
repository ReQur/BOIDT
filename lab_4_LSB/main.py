from lsb import LSB

_lsb = LSB()
_lsb.encode('./DSC_0163.bmp', './message.txt')
print(_lsb.decode('./DSC_0163-encoded.bmp'))






