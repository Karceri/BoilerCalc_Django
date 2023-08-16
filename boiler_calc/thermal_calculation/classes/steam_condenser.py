import math
from . import newton_method, new_water_steam
from pyXSteam.XSteam import XSteam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class SteamCondenser:
    def __init__(self, boiler, type, name, unknown, stat, tii, tii_water, steam_number, water_number):
        self.ti = 1
        self.ti_water = 1
        self.hi = 1
        self.hi_water = 1
        self.Di = 1
        self.Dii = 1
        self.Gi = 1
        self.Gii = 1
        self.Qb = 0
        self.Pi = 1
        self.Pii = 1
        self.Pi_water = 1
        self.Pii_water = 1
        self.x_dryi = 0
        self.x_dryii = 0
        ########################
        self.__boiler = boiler
        self.type = type
        self.name = name
        self.unknown = unknown
        self.tii = tii
        self.tii_water = tii_water
        self.hii = math.nan
        self.hii_water = math.nan
        self.steam_number = steam_number
        self.water_number = water_number
        self.stat = stat
        self.all = ['hi', 'hi_water', 'hii', 'hii_water']
        self.varia = list(set(self.all) - set(unknown) - set(stat))

    def __iter(self, argum):
        Pi, Pii, unknown, ti, tii, ti_water, tii_water, Dii, Gii = \
            self.Pi, self.Pii, self.unknown, self.ti, self.tii, self.ti_water, self.tii_water, \
            self.Dii, self.Gii
        self.hi = hi = argum['hi']
        self.hii = hii = argum['hii']
        self.hi_water = hi_water = argum['hi_water']
        self.hii_water = hii_water = argum['hii_water']

        prov_argum = {
            'hii_water' : 0
        }

        self.ti_water = ti_water = new_water_steam.eheatT(Pi, hi_water) if 'hi_water' in unknown else self.ti_water
            #WaterSteam.t_ph(Pi, hi_water) if 'hi_water' in unknown else ti_water
        x_dryi = new_water_steam.eheatXPH(Pi, hi_water)
            #WaterSteam.x_ph(Pi, hi_water)
        self.tii_water = tii_water = new_water_steam.eheatT(Pii, hii_water) if 'hii_water' in unknown else self.tii_water
            #WaterSteam.t_ph(Pii, hii_water) if 'hii_water' in unknown else tii_water
        x_dryii = new_water_steam.eheatXPH(Pii, hii_water)
            #WaterSteam.x_ph(Pii, hii_water)
        prov_argum['hii_water'] = hi_water + Dii * (hi - hii) / Gii

        self.ti, self.tii, self.ti_water, self.tii_water = ti, tii, ti_water, tii_water
        return prov_argum

    def __solution(self):
        Pi, Pi_water, Di, Gi, ti, tii, ti_water, tii_water, unknown, hi, hii, hi_water, hii_water, stat = \
            self.Pi, self.Pi_water, self.Di, self.Gi, self.ti, self.tii, self.ti_water, self.tii_water, \
            self.unknown, self.hi, self.hii, self.hi_water, self.hii_water, self.stat

        self.Dii = Dii = Di
        self.Gii = Gii = Gi
        self.Pii = Pii = Pi
        self.Pii_water = Pii_water = Pi_water
        self.tii = tii = ti

        argum_temp = {
            'hi' : ti,
            'hi_water': ti_water,
            'hii' : tii,
            'hii_water': tii_water,
        }

        newton_method.argum_nan(argum_temp)

        newton_method.argum_pre(unknown, argum_temp)

        self.ti = ti = argum_temp["hi"]
        self.ti_water  = ti_water = argum_temp["hi_water"]
        self.tii = tii = argum_temp["hii"]
        self.tii_water = tii_water = argum_temp["hii_water"]

        argum = {
            'hi' : new_water_steam.eheatH11(ti) #WaterSteam.hV_t(ti)
            if 'hi' in unknown or math.isnan(hi) else hi,
            'hii' : new_water_steam.eheatH1(tii) #WaterSteam.hL_t(tii)
            if 'hii' in unknown or math.isnan(hii) else hii,
            'hi_water': new_water_steam.eheatHPT(Pi, ti_water) #WaterSteam.h_pt(Pi, ti_water)
            if 'hi_water' in unknown or math.isnan(hi_water) else hi_water,
            'hii_water': new_water_steam.eheatHPT(Pii, tii_water) #WaterSteam.h_pt(Pii, tii_water)
            if 'hii_water' in unknown or math.isnan(hii_water) else hii_water,
        }

        newton_method.newton_method(self.__iter, argum, unknown)
        #self.hi, self.hii, self.hi_water, self.hii_water = argum.values()

    def poisk_korney(self):
        self.__solution()
