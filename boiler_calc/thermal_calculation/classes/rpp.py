import math
from . import newton_method
from . import new_water_steam
from pyXSteam.XSteam import XSteam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class RPP:
    def __init__(self, boiler, type, name, unknown, stat, tip_rpp,
                 Tpk, ql, tii, F, delta_P, nu_v, steam_number):
        self.ti = 1
        self.F = 1
        self.hi = 1
        self.Di = 1
        self.Dii = 1
        self.vii_topk = 1
        self.Qb = 0
        self.Br = 1
        self.Pi = 1
        self.Pii = 1
        self.Vpk = 1
        ##########################
        self.__boiler = boiler
        self.type = type
        self.name = name
        self.tip_rpp = tip_rpp
        self.tii = tii
        self.hii = math.nan
        self.F = F
        self.Tpk = Tpk
        self.ql = ql
        self.delta_P = delta_P
        self.nu_v = nu_v
        self.steam_number = steam_number
        self.unknown = unknown
        self.stat = stat
        self.all = ['hi', 'hii', 'F']
        self.varia = list(set(self.all) - set(self.unknown) - set(self.stat))

    def __q0gg(self):
        return 30

    def __q0pov(self):
        return 30

    def __Q_method(self, F):
        tip_rpp, ql, nu_v, Br, vii_topk, Tpk, Vpk =\
            self.tip_rpp, self.ql, self.nu_v, self.Br, self.vii_topk, self.Tpk, self.Vpk
        if tip_rpp == 'PT':
            Q = ql * nu_v * F / Br
        elif tip_rpp == 'GG':
            Q = self.__q0gg() * math.pow((vii_topk + 273 + Tpk + 273) / 2 / 1273, 2 ) * F / Br
        else: # PV
            snk = 3.6 * Vpk / F
            Q = self.__q0pov() * math.pow(snk / 2.8, 0.25) * math.pow((Tpk + 273) / 1273, 2) * F / Br
        return Q


    def __rppiter(self, argum):
        Pi, Pii, unknown, ti, tii, Br, Di = \
            self.Pi, self.Pii, self.unknown, self.ti, self.tii, self.Br, self.Di
        self.hi = hi = argum['hi']
        self.hii = hii = argum['hii']
        self.F = F = argum['F']

        prov_argum = {
            'hii' : 0
        }

        self.ti = ti = new_water_steam.eheatT(Pi, hi) if 'hi' in unknown else self.ti
            #WaterSteam.t_ph(Pi, hi) if 'hi' in unknown else ti
        self.tii = tii = new_water_steam.eheatT(Pii, hii) if 'hii' in unknown else self.tii
            #WaterSteam.t_ph(Pii, hii) if 'hii' in unknown else tii
        if self.F < 0:
            self.F = F = argum['F'] = 1 if 'F' in unknown else self.F
        Q = self.__Q_method(F)
        delta_rpp = Q * Br / Di
        prov_argum['hii'] = hi + delta_rpp

        self.ti, self.tii = ti, tii
        return prov_argum

    def __kornikpp(self):
        Pi, delta_P, Di, ti, tii, F, unknown, hi, hii, stat = \
            self.Pi, self.delta_P, self.Di, self.ti, self.tii, self.F, self.unknown, self.hi, self.hii, self.stat
        self.Pii = Pii = Pi - delta_P
        self.Dii = Dii = Di

        argum_temp = {
            'hi' : ti,
            'hii' : tii,
            'F' : F
        }

        newton_method.argum_nan(argum_temp)

        newton_method.argum_pre(unknown, argum_temp)

        self.ti = ti = argum_temp["hi"]
        self.tii = tii = argum_temp["hii"]
        self.F = F = argum_temp["F"]

        argum = {
            'hi' : new_water_steam.eheatHPT(Pi, ti)#WaterSteam.h_pt(Pi, ti)
            if 'hi' in unknown or math.isnan(hi) else hi,
            'hii' : new_water_steam.eheatHPT(Pii, tii)#WaterSteam.h_pt(Pii, tii)
            if 'hii' in unknown or math.isnan(hii) or 'hii' in stat else hii,
            'F' : F
        }

        newton_method.newton_method(self.__rppiter, argum, unknown)
        #self.hi, self.hii, self.F = argum.values()

    def poisk_korney(self):
        boiler = self.__boiler
        self.vii_topk = boiler.vii_topk
        self.Vpk = boiler.Vpk
        self.ql = boiler.ql
        self.Br = boiler.Br
        self.Tpk = boiler.v_pk
        self.__kornikpp()

