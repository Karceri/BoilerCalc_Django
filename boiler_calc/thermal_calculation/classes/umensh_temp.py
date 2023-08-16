import math
from . import newton_method
from pyXSteam.XSteam import XSteam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class UmenshTemp:
    def __init__(self, boiler, name, gaz_number, unknown, stat, delta_v):
        self.vi = 1
        self.vii = 1
        self.Qlvh = 1
        self.Qlvyh = 1
        self.alfai = 1
        self.alfaii = 1
        self.Bi = 1
        self.Bii = 1
        self.Hi = 1
        self.Hii = 1
        self.Qb = 1
        #########################
        self.__boiler = boiler
        self.type = 'УменьшТемпГаза'
        self.name = name
        self.n_Qb = -1
        self.gaz_number = gaz_number
        self.unknown = unknown
        self.stat = stat
        self.delta_v = delta_v
        all = ['Hi', 'Hii']
        self.varia = list(set(all) - set(unknown) - set(stat))

    def __Qb_method(self):
        boiler, n_Qb, Hi, Hii, Bii = self.__boiler, self.n_Qb, self.Hi, self.Hii, self.Bii

        self.Qb = Qb = (Hi - Hii) * Bii
        if n_Qb == -1:
            boiler.Qb.append(Qb)
            self.n_Qb = len(boiler.Qb) - 1
        else:
            boiler.Qb[n_Qb] = Qb

    def poisk_korney(self):
        boiler, vi, delta_v, alfai, Qlvh, Bi = \
            self.__boiler, self.vi, self.delta_v, self.alfai, self.Qlvh, self.Bi

        self.vii = vii = vi - delta_v
        self.alfaii = alfaii = alfai
        self.Hii = boiler.HGAZ(vii, alfaii, boiler.vc_rec, boiler.H_rec)
        self.Qlvyh = Qlvh
        self.Bii = Bi
        self.__Qb_method()
