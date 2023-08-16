import math
from pyXSteam.XSteam import XSteam
from . import new_water_steam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class CVD:
    def __init__(self, boiler, name, rD_main, rD_alter, Pii_alter, kpd_noi, tii_alter, steam_number,
                 stream_number, stream_number_alter):
        self.Di = 1
        self.Dii_main = 1
        self.Dii_alter = 1
        self.S = 1
        self.Pi = 1
        self.Pii_main = 1
        self.ti = 1
        self.tii_main = 1
        self.hi = 1
        self.hii_main = 1
        self.hii_alter = 1
        self.hii_alter_teor = 1
        self.H = 1
        self.Qb = 0
        self.type = 'ЦВД'
        ####################
        self.__boiler = boiler
        self.name = name
        self.rD_main = rD_main
        self.rD_alter = rD_alter
        self.Pii_alter = Pii_alter
        self.tii_alter = tii_alter
        self.kpd_noi = kpd_noi
        self.steam_number = steam_number
        self.stream_number = stream_number
        self.stream_number_alter = stream_number_alter
        self.varia = ['hi']
        self.main_trakt = True

    @property
    def tii(self):
        if self.main_trakt == True:
            return self.tii_main
        else:
            return self.tii_alter

    @tii.setter
    def tii(self, value):
        if self.main_trakt == True:
            self.tii_main = value
        else:
            self.tii_alter = value

    @property
    def hii(self):
        if self.main_trakt == True:
            return self.hii_main
        else:
            return self.hii_alter

    @hii.setter
    def hii(self, value):
        if self.main_trakt == True:
            self.hii_main = value
        else:
            self.hii_alter = value

    @property
    def Dii(self):
        if self.main_trakt == True:
            return self.Dii_main
        else:
            return self.Dii_alter

    @Dii.setter
    def Dii(self, value):
        if self.main_trakt == True:
            self.Dii_main = value
        else:
            self.Dii_alter = value

    @property
    def Pii(self):
        if self.main_trakt == True:
            return self.Pii_main
        else:
            return self.Pii_alter

    @Pii.setter
    def Pii(self, value):
        if self.main_trakt == True:
            self.Pii_main = value
        else:
            self.Pii_alter = value

    def __raschet(self):
        self.Pii_main = self.Pi
        self.tii_main = self.ti
        self.hii_main = self.hi
        self.Dii_main = self.Di * self.rD_main
        self.Dii_alter = self.Di * self.rD_alter
        self.hii_alter = new_water_steam.eheatHPT(self.Pii_alter, self.tii_alter)
            #WaterSteam.h_pt(self.Pii_alter, self.tii_alter)

    def poisk_korney(self):
        self.__raschet()
        self.__boiler.tvt_i = self.tii_alter
        self.__boiler.hvt_i = self.hii_alter
