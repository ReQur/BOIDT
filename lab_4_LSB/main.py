from PIL import Image
import numpy as np

import lsb
from converter import bit_acii_generator, merge_bits_to_ascii

nums = list(bit_acii_generator('./message.txt'))
print(merge_bits_to_ascii(nums))
# lsb.encode('./DSC_0163.bmp', './message.txt')
print(lsb.decode('./DSC_0163-encoded.bmp'))




