from . import new_water_steam
from pyXSteam.XSteam import XSteam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class T_sm:
    def __init__(self, boiler, type, name, unknown, stat, izvii, elem_number, elem_number_alter,
                 stream_number, stream_number_alter):
        self.vi_main = 1
        self.vi_alter = 1
        self.ti_main = 1
        self.ti_alter = 1
        self.ti_water_main = 1
        self.ti_water_alter = 1
        self.ti_air_main = 1
        self.ti_air_alter = 1
        self.vii = 1
        self.tii = 1
        self.tii_water = 1
        self.tii_air = 1
        self.Di_main = 1
        self.Di_alter = 1
        self.Dii = 1
        self.Gi_main = 1
        self.Gi_alter = 1
        self.Gii = 1
        self.Pi_water_main = 1
        self.Pi_water_alter = 1
        self.Pii_water = 1
        self.Pi_main = 1
        self.Pi_alter = 1
        self.Pii = 1
        self.Qlvh_main = 1
        self.Qlvh_alter = 1
        self.Qlvyh = 1
        self.hi_main = 1
        self.hi_alter = 1
        self.hii = 1
        self.Hi_main = 1
        self.Hi_alter = 1
        self.Hii = 1
        self.alfai_main = 0.1
        self.alfai_alter = 0.1
        self.alfaii = 1
        self.Bi_air_main = 1
        self.Bi_air_alter = 1
        self.Bii_air = 1
        self.Bi_main = 1
        self.Bi_alter = 1
        self.Bii = 1
        self.bettagvi_main = 0.1
        self.bettagvi_alter = 0.1
        self.bettagvii = 1
        self.hi_water_main = 1
        self.hi_water_alter = 1
        self.hi_air_main = 1
        self.hi_air_alter = 1
        self.hii_water = 1
        self.Hii_air = 1
        self.vc_rec = 0
        self.H_rec = 0
        ####################
        self.__boiler = boiler
        self.type = type
        self.name = name
        self.unknown = unknown
        self.stat = stat
        self.steam_number_main = elem_number
        self.water_number_main = elem_number
        self.air_number_main = elem_number
        self.gaz_number_main = elem_number
        self.steam_number_alter = elem_number_alter
        self.water_number_alter = elem_number_alter
        self.air_number_alter = elem_number_alter
        self.gaz_number_alter = elem_number_alter
        self.stream_number = stream_number
        self.stream_number_alter = stream_number_alter

        match type:
            case 'steam':
                all = ['hi', 'hi_alter', 'hii']
                tii = izvii
            case 'water':
                all = ["hi_water", "hi_water_alter", "hii_water"]
                tii_water = izvii
            case 'air':
                all = ["hi_air", "hi_air_alter", "hii_air"]
                tii_air = izvii
            case 'gaz':
                all = ["Hi", "Hi_alter", "Hii"]
                vii = izvii
            case _:
                all = []
        self.varia = list(set(all) - set(unknown) - set(stat))
        self.main_trakt = True

    @property
    def steam_number(self):
        if self.main_trakt == True:
            return self.steam_number_main
        else:
            return self.steam_number_alter

    @property
    def water_number(self):
        if self.main_trakt == True:
            return self.water_number_main
        else:
            return self.water_number_alter

    @property
    def air_number(self):
        if self.main_trakt == True:
            return self.air_number_main
        else:
            return self.air_number_alter

    @property
    def gaz_number(self):
        if self.main_trakt == True:
            return self.gaz_number_main
        else:
            return self.gaz_number_alter

    @property
    def vi(self):
        if self.main_trakt == True:
            return self.vi_main
        else:
            return self.vi_alter

    @vi.setter
    def vi(self, value):
        if self.main_trakt == True:
            self.vi_main = value
        else:
            self.vi_alter = value

    @property
    def ti(self):
        if self.main_trakt == True:
            return self.ti_main
        else:
            return self.ti_alter

    @ti.setter
    def ti(self, value):
        if self.main_trakt == True:
            self.ti_main = value
        else:
            self.ti_alter = value

    @property
    def ti_water(self):
        if self.main_trakt == True:
            return self.ti_water_main
        else:
            return self.ti_water_alter

    @ti_water.setter
    def ti_water(self, value):
        if self.main_trakt == True:
            self.ti_water_main = value
        else:
            self.ti_water_alter = value

    @property
    def ti_air(self):
        if self.main_trakt == True:
            return self.ti_air_main
        else:
            return self.ti_air_alter

    @ti_air.setter
    def ti_air(self, value):
        if self.main_trakt == True:
            self.ti_air_main = value
        else:
            self.ti_air_alter = value

    @property
    def Hi(self):
        if self.main_trakt == True:
            return self.Hi_main
        else:
            return self.Hi_alter

    @Hi.setter
    def Hi(self, value):
        if self.main_trakt == True:
            self.Hi_main = value
        else:
            self.Hi_alter = value

    @property
    def hi(self):
        if self.main_trakt == True:
            return self.hi_main
        else:
            return self.hi_alter

    @hi.setter
    def hi(self, value):
        if self.main_trakt == True:
            self.hi_main = value
        else:
            self.hi_alter = value

    @property
    def hi_water(self):
        if self.main_trakt == True:
            return self.hi_water_main
        else:
            return self.hi_water_alter

    @hi_water.setter
    def hi_water(self, value):
        if self.main_trakt == True:
            self.hi_water_main = value
        else:
            self.hi_water_alter = value

    @property
    def Hi_air(self):
        if self.main_trakt == True:
            return self.hi_air_main
        else:
            return self.hi_air_alter

    @Hi_air.setter
    def Hi_air(self, value):
        if self.main_trakt == True:
            self.hi_air_main = value
        else:
            self.hi_air_alter = value

    @property
    def Di(self):
        if self.main_trakt == True:
            return self.Di_main
        else:
            return self.Di_alter

    @Di.setter
    def Di(self, value):
        if self.main_trakt == True:
            self.Di_main = value
        else:
            self.Di_alter = value

    @property
    def Gi(self):
        if self.main_trakt == True:
            return self.Gi_main
        else:
            return self.Gi_alter

    @Gi.setter
    def Gi(self, value):
        if self.main_trakt == True:
            self.Gi_main = value
        else:
            self.Gi_alter = value

    @property
    def Pi(self):
        if self.main_trakt == True:
            return self.Pi_main
        else:
            return self.Pi_alter

    @Pi.setter
    def Pi(self, value):
        if self.main_trakt == True:
            self.Pi_main = value
        else:
            self.Pi_alter = value

    @property
    def Pi_water(self):
        if self.main_trakt == True:
            return self.Pi_water_main
        else:
            return self.Pi_water_alter

    @Pi_water.setter
    def Pi_water(self, value):
        if self.main_trakt == True:
            self.Pi_water_main = value
        else:
            self.Pi_water_alter = value

    @property
    def Qlvh(self):
        if self.main_trakt == True:
            return self.Qlvh_main
        else:
            return self.Qlvh_alter

    @Qlvh.setter
    def Qlvh(self, value):
        if self.main_trakt == True:
            self.Qlvh_main = value
        else:
            self.Qlvh_alter = value

    @property
    def alfai(self):
        if self.main_trakt == True:
            return self.alfai_main
        else:
            return self.alfai_alter

    @alfai.setter
    def alfai(self, value):
        if self.main_trakt == True:
            self.alfai_main = value
        else:
            self.alfai_alter = value

    @property
    def bettagvi(self):
        if self.main_trakt == True:
            return self.bettagvi_main
        else:
            return self.bettagvi_alter

    @bettagvi.setter
    def bettagvi(self, value):
        if self.main_trakt == True:
            self.bettagvi_main = value
        else:
            self.bettagvi_alter = value

    @property
    def Bi(self):
        if self.main_trakt == True:
            return self.Bi_main
        else:
            return self.Bi_alter

    @Bi.setter
    def Bi(self, value):
        if self.main_trakt == True:
            self.Bi_main = value
        else:
            self.Bi_alter = value

    @property
    def Bi_air(self):
        if self.main_trakt == True:
            return self.Bi_air_main
        else:
            return self.Bi_air_alter

    @Bi_air.setter
    def Bi_air(self, value):
        if self.main_trakt == True:
            self.Bi_air_main = value
        else:
            self.Bi_air_alter = value

    def __raschet_steam(self):
        self.Dii = self.Di_main + self.Di_alter
        self.Pii = (self.Pi_main * self.Di_main + self.Pi_alter * self.Di_alter) / (self.Di_main + self.Di_alter)
        self.hi_main = new_water_steam.eheatHPT(self.Pi_main, self.ti_main)
            #WaterSteam.h_pt(self.Pi_main, self.ti_main)
        self.hi_alter = new_water_steam.eheatHPT(self.Pi_alter, self.ti_alter)
            #WaterSteam.h_pt(self.Pi_alter, self.ti_alter)
        self.hii = (self.hi_main * self.Di_main + self.hi_alter * self.Di_alter) / (self.Di_main + self.Di_alter)
        self.tii = new_water_steam.eheatT(self.Pii, self.hii)
            #WaterSteam.t_ph(self.Pii, self.hii)

    def __raschet_water(self):
        self.Gii = self.Gi_main + self.Gi_alter
        self.Pii_water = (self.Pi_water_main * self.Gi_main + self.Pi_water_alter * self.Gi_alter) / (self.Gi_main + self.Gi_alter)
        self.hi_water_main = new_water_steam.eheatHPT(self.Pi_water_main, self.ti_water_main)
            #WaterSteam.h_pt(self.Pi_water_main, self.ti_water_main)
        self.hi_water_alter = new_water_steam.eheatHPT(self.Pi_water_alter, self.ti_water_alter)
            #WaterSteam.h_pt(self.Pi_water_alter, self.ti_water_alter)
        self.hii_water = (self.hi_water_main * self.Gi_main + self.hi_water_alter * self.Gi_alter) / (self.Gi_main + self.Gi_alter)
        self.tii_water = new_water_steam.eheatT(self.Pii_water, self.hii_water)
            #WaterSteam.t_ph(self.Pii_water, self.hii_water)

    def __raschet_air(self):
        self.Bii_air = self.Bi_air_main + self.Bi_air_alter
        self.hi_air_main = self.__boiler.HAIR(self.ti_air_main)
        self.hi_air_alter = self.__boiler.HAIR(self.ti_air_alter)
        self.bettagvii = (self.bettagvi_main * self.Bi_air_main + self.bettagvi_alter * self.Bi_air_alter) / (self.Bi_air_main + self.Bi_air_alter)
        self.Hii_air = (self.hi_air_main * self.Bi_air_main + self.hi_air_alter * self.Bi_air_alter) / (self.Bi_air_main + self.Bi_air_alter)
        self.tii_air = self.__boiler.tAIR(self.Hii_air)

    def __raschet_gaz(self):
        self.vc_rec = self.__boiler.vc_rec
        self.H_rec = self.__boiler.H_rec
        self.Bii = self.Bi_main + self.Bi_alter
        self.Qlvyh = (self.Qlvh_main * self.Bi_main + self.Qlvh_alter * self.Bi_alter) / (self.Bi_main + self.Bi_alter)
        self.Hi_main = self.__boiler.HGAZ(self.vi_main, self.alfai_main, self.vc_rec, self.H_rec)
        self.Hi_alter = self.__boiler.HGAZ(self.vi_alter, self.alfai_alter, self.vc_rec, self.H_rec)
        self.Hii = (self.Hi_main * self.Bi_main + self.Hi_alter * self.Bi_alter) / (self.Bi_main + self.Bi_alter)
        self.alfaii = (self.alfai_main * self.Bi_main + self.alfai_alter * self.Bi_alter) / (self.Bi_main + self.Bi_alter)
        self.vii = self.__boiler.vgaz(self.Hii, self.alfaii, self.vc_rec, self.H_rec)

    def poisk_korney(self):
        match self.type:
            case 'steam':
                self.__raschet_steam()
            case 'water':
                self.__raschet_water()
            case 'air':
                self.__raschet_air()
            case 'gaz':
                self.__raschet_gaz()
            case _:
                pass
