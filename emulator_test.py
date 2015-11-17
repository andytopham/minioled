#!/usr/bin/python
# Master for dummy oled testing.

import uoled_emulator
import time

print 'Starting'
display = uoled_emulator.Uoled_Emulator()
display.writerow(1, '012345678901234567890')
display.writerow(2, 'Row2')
display.writerow(3, 'Row3')
display.writerow(4, 'Row4')
time.sleep(5)

