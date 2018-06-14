import sys
import time


class ProcessBar():
    def __init__(self):
        pass

    def show(self):
        for i in range(100):
            k = i + 1
            str = '='*(i//2 - 1) + '>' + ' '*((100-k)//2)
            sys.stdout.write('\r'+str+'[%s%%]'%(i+1))
            sys.stdout.flush()
            time.sleep(0.1)


