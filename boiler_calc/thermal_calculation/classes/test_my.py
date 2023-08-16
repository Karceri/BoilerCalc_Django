'''from abc import ABC, abstractmethod


class AbstractConvPov(ABC):
    def __init__(self, boiler, name):
        self.__boiler = boiler
        self.name = name
        self.arg = {
            'name' : name
        }

    #name = property(lambda self: self.__name)

    @abstractmethod
    def poisk_korney(self):
        self.Br = 20


class kpp(AbstractConvPov):
    def __init__(self, boiler, name):
        super().__init__(boiler, name)
        #self.name = 'xxxx'
        arg = self.arg
        arg['name'] = 'xxxx'

    #name = property(lambda self: self._AbstractConvPov__name,
    #              lambda self, value: setattr(self, '_AbstractConvPov__name', value))

    def poisk_korney(self):
        super().poisk_korney()


ww = kpp('1', '1')
ww.name = '2w2'
print(ww.arg)'''


# def CreateLists(count):
#     lists = []
#     for i in range(count):
#         lists.append(None)
#         lists[i] = []
#     return lists

#lists = []


#lists.extend([[]] * 5)
#lists = CreateLists(5)


import new_water_steam, numpy as np
from pyXSteam.XSteam import XSteam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)
import math

class s:
    def __init__(self):
        self.elem_par = {'h': 3,
                    'w': 5,
                    't': 1}

    # Bi = property(lambda self: self.elem_par['h'], lambda self, value: setattr(self, 'elem_par[\'h\']', value))

    @property
    def Bi(self):
        return self.elem_par['h']

    @Bi.setter
    def Bi(self, value):
        self.elem_par['h'] = value


elem_par = {'h' : 3,
            'w' : 5,
            't' : 1}


#elem_par = sorted(elem_par, key=lambda o: o)
# x = new_water_steam.eheatT(26.6, math.nan)

a = s()
a.Bi = 45
x = a.Bi

print(x)









