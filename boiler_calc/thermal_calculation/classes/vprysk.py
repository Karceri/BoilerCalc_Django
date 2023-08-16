import math
from . import newton_method, new_water_steam
from pyXSteam.XSteam import XSteam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class Vprysk:
    def __init__(self, boiler, type, name, unknown, stat,
            tii, Gvpr, steam_number, steam_number_alter, stream_number, stream_number_alter):
        self.ti_local = 100
        self.hi_local = 100
        self.Di_local = 25
        self.Dii = 25
        self.Qb = 0
        self.Gvpr = 1
        self.tkip = 100
        self.hkip = 100
        self.Pi_local = 10
        self.Pii = 10
        self.Pvpr = 10
        #################
        self.boiler = boiler
        self.type = type
        self.name = name
        self.tii = tii
        self.hii = math.nan
        self.Gvpr = Gvpr
        self.steam_number_local = steam_number
        self.steam_number_alter = steam_number_alter
        self.stream_number = stream_number
        self.stream_number_alter = stream_number_alter
        self.unknown = unknown
        self.stat = stat
        self.all = all = ['hi', 'hii']
        self.varia = list(set(all) - set(unknown) - set(stat))
        self.main_trakt = True

    @property
    def steam_number(self):
        if self.main_trakt == True:
            return self.steam_number_local
        else:
            return self.steam_number_alter

    @property
    def ti(self):
        if self.main_trakt == True:
            return self.ti_local
        else:
            return self.tkip

    @ti.setter
    def ti(self, value):
        if self.main_trakt == True:
            self.ti_local = value
        else:
            self.tkip = value

    @property
    def hi(self):
        if self.main_trakt == True:
            return self.hi_local
        else:
            return self.hkip

    @hi.setter
    def hi(self, value):
        if self.main_trakt == True:
            self.hi_local = value
        else:
            self.hkip = value

    @property
    def Pi(self):
        if self.main_trakt == True:
            return self.Pi_local
        else:
            return self.Pvpr

    @Pi.setter
    def Pi(self, value):
        if self.main_trakt == True:
            self.Pi_local = value
        else:
            self.Pvpr = value

    @property
    def Di(self):
        if self.main_trakt == True:
            return self.Di_local
        else:
            return self.Gvpr

    @Di.setter
    def Di(self, value):
        if self.main_trakt == True:
            self.Di_local = value
        else:
            self.Gvpr = value

    def __vpr_iter(self, argum):
        Pi, Pii, unknown, ti, tii, Gvpr, Di, hkip = \
            self.Pi_local, self.Pii, self.unknown, self.ti_local, self.tii, self.Gvpr, self.Di_local, self.hkip

        self.hi_local = hi = argum['hi']
        self.hii = hii = argum['hii']

        prov_argum = {
            'hii' : 0
        }
        self.ti_local = ti = new_water_steam.eheatT(Pi, hi) if 'hi' in unknown else self.ti_local
            #WaterSteam.t_ph(Pi, hi) if 'hi' in unknown else ti
        self.tii = tii = new_water_steam.eheatT(Pii, hii) if 'hii' in unknown else self.tii
            #WaterSteam.t_ph(Pii, hii) if 'hii' in unknown else tii
        delta_vpr = Gvpr / Di * (hi - hkip)
        prov_argum['hii'] = hi - delta_vpr

        self.Pi_local, self.Pii, self.unknown, self.ti_local, self.tii, self.Gvpr, self.Di_local, self.hkip = \
            Pi, Pii, unknown, ti, tii, Gvpr, Di, hkip
        return prov_argum

    def __vpr(self):
        Pi, Di, Gvpr, tkip, ti, tii, unknown, hi, hii = \
            self.Pi_local, self.Di_local, self.Gvpr, self.tkip, self.ti_local, self.tii, self.unknown, self.hi_local, self.hii

        self.Pii = Pii = Pi
        self.Dii = Dii = Di + Gvpr
        self.hkip = hkip = new_water_steam.eheatH1(tkip)
            #WaterSteam.hL_t(tkip)

        argum_temp = {
            'hi' : ti,
            'hii' : tii,
        }

        newton_method.argum_nan(argum_temp)

        newton_method.argum_pre(unknown, argum_temp)

        self.ti_local = ti = argum_temp["hi"]
        self.tii = tii = argum_temp["hii"]

        argum = {
            'hi' : new_water_steam.eheatHPT(Pi, ti) #WaterSteam.h_pt(Pi, ti)
            if 'hi' in unknown or math.isnan(hi) else hi,
            'hii' : new_water_steam.eheatHPT(Pii, tii) #WaterSteam.h_pt(Pii, tii)
            if 'hii' in unknown or math.isnan(hii) else hii,
        }

        newton_method.newton_method(self.__vpr_iter, argum, unknown)

        #self.hi_local, self.hii, = argum.values()

    def poisk_korney(self):
        self.__vpr()






