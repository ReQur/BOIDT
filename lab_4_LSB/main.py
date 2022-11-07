from lsb import LSB

_lsb = LSB(measure=1)
_lsb.encode('./misc/DSC_0163.bmp', './misc/message.txt')
print(_lsb.decode('./misc/DSC_0163-encoded.bmp'))

