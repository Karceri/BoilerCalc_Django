import math
from pyXSteam.XSteam import XSteam
from . import new_water_steam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class Closing_point:
    def __init__(self, boiler, type, name, text, izv, unknown, stat, elem_number,
                 bettagvi, P, Rash, B_set):
        self.vi = 1
        self.ti = 1
        self.ti_water = 1
        self.ti_air = 1
        self.Hi = 1
        self.hi = 1
        self.hi_water = 1
        self.Hi_air = 1
        self.Hii = 1
        self.hii = 1
        self.hii_water = 1
        self.Hii_air = 1
        self.Qlvh = 1
        self.Qlvyh = 1
        self.alfai = 1
        self.alfaii = 1
        self.Q_stvpr = 1
        self.bettagvii = 1
        self.Bi_air = 1
        self.Bii_air = 1
        self.Qb = 0
        ##################################
        self.__boiler = boiler
        self.type = type
        self.name = name
        self.text = text
        self.vii = izv if type == 'НачалоГазТ' else 0
        self.tii = izv if type == 'НачалоПарТ' else 0
        self.tii_water = izv if type == 'НачалоВодТ' else 0
        self.tii_air = izv if type == 'НачалоВоздТ' else 0
        self.bettagvi = bettagvi
        self.steam_number = elem_number
        self.water_number = elem_number
        self.air_number = elem_number
        self.gaz_number = elem_number
        self.__n_Qb = -1
        self.unknown = unknown
        self.stat = stat
        if B_set == 'Задается':
            self.__B_set = True
        else:
            self.__B_set = False

        match type:
            case 'КонецПарВторТ':
                self.all = ['hi']
                self.Pi = P
                self.Di = Rash
            case 'КонецПарПервТ':
                self.all = ['hi']
                self.Pi = P
                self.Di = Rash
            case 'НачалоПарТ':
                self.all = ['hii']
                self.Pii = P
                self.Dii = Rash
            case 'КонецВодТ':
                self.all = ['hi_water']
                self.Pi_water = P
                self.Gi = Rash
            case 'НачалоВодТ':
                self.all = ['hii_water']
                self.Pii_water = P
                self.Gii = Rash
            case 'КонецВоздТ':
                self.all = ['hi_air']
            case 'НачалоВоздТ':
                self.all = ['hii_air']
            case 'КонецГазТ':
                self.all = ['Hi']
                self.Bi = Rash
            case 'НачалоГазТ':
                self.all = ['Hii']
                self.Bii = Rash
            case _:
                pass
        self.varia = list(set(self.all) - set(unknown) - set(stat))

    def __raschet_begin_gaz(self):
        boiler, B_set, Bii = self.__boiler, self.__B_set, self.Bii
        self.Hii = boiler.HGAZ(self.vii, 1.2, 0, 0)
        if B_set == True:
            boiler.B_set = B_set
            boiler.Br = Bii
        else:
            self.Bii = boiler.Br

    def __raschet_end_gaz(self):
        boiler, alfai, vi, Hi = self.__boiler, self.alfai, self.vi, self.Hi
        boiler.alfa_uhg = alfai
        boiler.vuhg = vi
        boiler.Huhg = Hi

    def __raschet_begin_steam(self):
        boiler, text, Pii, tii, Dii, n_Qb = self.__boiler, self.text, self.Pii, self.tii, self.Dii, self.__n_Qb
        if 'СторВпр' in text:
            self.hii = hii = new_water_steam.eheatHPT(Pii, tii)
                #WaterSteam.h_pt(Pii, tii)
            self.Q_stvpr = Q_stvpr = Dii * (boiler.hvt_ii - hii)
            if n_Qb == -1:
                boiler.Q_stvpr.append(Q_stvpr)
                self.__n_Qb = len(boiler.Q_stvpr) - 1
            else:
                boiler.Q_stvpr[n_Qb] = Q_stvpr

    def __raschet_end_steam_second(self):
        boiler = self.__boiler
        boiler.Dvt = self.Di
        boiler.tvt_ii = self.ti
        boiler.hvt_ii = self.hi

    def __raschet_end_steam_first(self):
        boiler = self.__boiler
        boiler.Dpe = self.Di
        boiler.tpe = self.ti
        boiler.hpe = self.hi

    def __raschet_begin_water(self):
        boiler, text = self.__boiler, self.text
        self.hii_water = new_water_steam.eheatHPT(self.Pii_water, self.tii_water)
            #WaterSteam.h_pt(self.Pii_water, self.tii_water)
        if 'ВодТ' in text:
            boiler.Gpv = self.Gii
            boiler.Ppv = self.Pii_water
            boiler.tpv = self.tii_water
            boiler.hpv = self.hii_water

    def __raschet_end_water(self):
        pass

    def __raschet_begin_air(self):
        boiler = self.__boiler
        self.bettagvii = self.bettagvi
        self.Br = Br = boiler.Br
        if math.isnan(Br):
            self.Br = Br = 20
        self.Bii_air = Br * self.bettagvii
        boiler.thv = self.tii_air
        self.Hii_air = boiler.HAIR(self.tii_air)
        boiler.Hhv0 = self.Hii_air

    def __raschet_end_air(self):
        boiler = self.__boiler
        boiler.tgv = self.ti_air
        boiler.Hgv = self.Hi_air

    def poisk_korney(self):
        match self.type:
            case 'НачалоГазТ':
                self.__raschet_begin_gaz()
            case 'КонецГазТ':
                self.__raschet_end_gaz()
            case 'НачалоПарТ':
                self.__raschet_begin_steam()
            case 'КонецПарПервТ':
                self.__raschet_end_steam_first()
            case 'КонецПарВторТ':
                self.__raschet_end_steam_second()
            case 'НачалоВодТ':
                self.__raschet_begin_water()
            case 'КонецВодТ':
                self.__raschet_end_water()
            case 'НачалоВоздТ':
                self.__raschet_begin_air()
            case 'КонецВоздТ':
                self.__raschet_end_air()
            case _:
                pass

