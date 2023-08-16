from pyXSteam.XSteam import XSteam
from . import new_water_steam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class Drum:
    def __init__(self, boiler, steam_number, water_number, Gpr, name):
        self.ti = 0
        self.tii = 1
        self.Pb = 138
        self.Di = 100
        self.Dii = 100
        self.hi = 0
        self.hii = 1
        self.hii_water = 0
        self.tii_water = 0
        self.Pi = 1
        self.Pii_water = 1
        self.Qb = 0
        self.type = 'Барабан'
        ####################
        self.__boiler = boiler
        self.name= name
        self.Gpr = Gpr
        self.steam_number = steam_number
        self.water_number = water_number
        self.unknown = []
        self.all = ['hii', 'hi_water']
        self.stat = ['hii']
        self.varia = list(set(self.all) - set(self.unknown) - set(self.stat))

    ti_water = property(lambda self: self.ti, lambda self, value: setattr(self, 'ti', value))
    hi_water = property(lambda self: self.hi, lambda self, value: setattr(self, 'hi', value))
    Pii = property(lambda self: self.Pb, lambda self, value: setattr(self, 'Pb', value))
    Pi_water = property(lambda self: self.Pb, lambda self, value: setattr(self, 'Pb', value))
    Gi = property(lambda self: self.Di, lambda self, value: setattr(self, 'Di', value))
    Gii = property(lambda self: self.Dii, lambda self, value: setattr(self, 'Dii', value))

    def poisk_korney(self):
        boiler = self.__boiler
        self.Dii =  self.Di
        boiler.Pb = self.Pb
        self.tii = new_water_steam.eheatTs(self.Pb)
            #WaterSteam.tsat_p(self.Pb)
        self.hii_water = new_water_steam.eheatH1(self.tii)
            #WaterSteam.hL_t(self.tii)
        self.hii = new_water_steam.eheatH11(self.tii)
            #WaterSteam.hV_t(self.tii)
        boiler.Gpr = self.Gpr
        boiler.hkip = self.hii_water