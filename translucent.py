#!/usr/bin/python

import sys, re

class Color(object):

    def __init__(self, inp, alpha=1):
        self.alpha = alpha
        if type(inp) is str:
            if re.match(r'^#\d{3}$', inp):
                inp = '#' + inp[1] * 2 + inp[2] * 2 + inp[3] * 2
            if re.match(r'^#\d{6}$', inp):
                self._data = (int(inp[1:2], 16),
                              int(inp[3:4], 16),
                              int(inp[5:6], 16))
            if re.match(r'^\d{1,3}\s*,\s*\d{1,3}\s*,\s*\d{1,3}\s*$', inp):
                self._data = tuple([int(a) for a in inp.split(',')])
        else:
            self._data = inp

    def translucent(self, alpha):
        bg = 255
        newcolor = [unmix(x, bg, alpha) for x in self._data]
        return self.__class__(newcolor)

    def hex(self):
        cleaned_data = [int(round(x)) for x in self._data]
        for i in range(len(cleaned_data)):
            if cleaned_data[i] > 255:
                cleaned_data[i] = 255
            elif cleaned_data[i] < 0:
                cleaned_data[i] = 0
        output = '#' + ''.join([('0' + '{0:X}'.format(x))[-2:] for x in cleaned_data])
        return output

    def __repr__(self):
        return 'Color(' + self.hex() + ')'
        #return 'Color' + str(self._data)

def unmix(composite, bg, alpha):
    top = (composite - (1 - alpha) * bg) / alpha
    return top

if __name__ == '__main__':
    color = Color(sys.argv[1])
    alpha = float(sys.argv[2])
    if alpha > 1 or alpha < 0:
        raise Exception('Alpha must be between 0 & 1.')
    print 'COLOR:', color
    print 'ALPHA:', alpha
    print 'TRANSLUCENT:', color.translucent(alpha)
