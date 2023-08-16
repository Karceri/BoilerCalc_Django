import math
from . import newton_method
from . import new_water_steam
from pyXSteam.XSteam import XSteam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class Shirm_pov:
    def __init__(self, boiler, type, name, text, unknown, stat, tipdvizh, vii, tii, F, delta_P, fg, fi_pp,
            delta_alfa, steam_number, gaz_number):
        self.vi = 500
        self.Hi = 500
        self.Qlvh = 100
        self.Ql = 100
        self.alfai = 1
        self.alfaii = 1
        self.x_dryii = 0
        self.x_dryi = 0
        self.wg = 5
        self.Qlvyh = 100
        self.Qb = 0
        self.vc_rec = 0
        self.H_rec = 0
        self.Vg = 5
        self.fi = 1
        self.Hhv0 = 100
        self.k = 0
        self.deltat = 0
        self.Di = 25
        self.Dii = 25
        self.__Br = 25
        self.Pi = 1
        self.Pii = 1
        self.ti = 1
        self.hi = 1
        ############################
        self.__boiler = boiler
        self.type = type
        self.name = name
        self.text = text
        self.tipdvizh = tipdvizh
        self.vii = vii
        self.Hii = math.nan
        self.tii = tii
        self.hii = math.nan
        self.F = F
        self.delta_P = delta_P
        self.fg = fg
        self.fi_pp = fi_pp
        self.delta_alfa = delta_alfa
        self.__n_Qb = -1
        self.unknown = unknown
        self.stat = stat
        self.steam_number = steam_number
        self.gaz_number = gaz_number
        self.all = {
            "Hi" : "Hi",
            "hi" : "hi",
            "Hii" : "Hii",
            "hii" : "hii",
            "F" : "F",
        }
        self.varia = list(set(self.all.values()) - set(stat) - set(unknown))
        self.unknown_local = list(key for key, value in self.all.items() if value in unknown)

    Bi = property(lambda self: self.__Br,
                  lambda self, value: setattr(self, '_Shirm_pov__Br', value))
    Bii = property(lambda self: self.__Br,
                   lambda self, value: setattr(self, '_Shirm_pov__Br', value))

    def __Qb_method(self):
        k, deltat, F, boiler, n_Qb = self.k, self.deltat, self.F, self.__boiler, self.__n_Qb

        Qb = k * deltat * F / 1000
        if n_Qb == -1:
            boiler.Qb.append(Qb)
            self.__n_Qb = len(boiler.Qb) - 1
        else:
            boiler.Qb[n_Qb] = Qb
        return Qb

    def __k_method(self, wg, vii):
        A = 40; n = 0.5
        k = A * (vii + 273) / 1400 * (1 + 0.4 * math.pow(wg / 7, n))
        return k

    def __shpp_iter(self, argum):
        all, boiler, alfai, alfaii, vc_rec, H_rec, unknown, vi, vii, ti, tii, Pi, Pii, unknown_local, tipdvizh, \
        Vg, fg, Br, fi, delta_alfa, Hhv0, Di, Ql \
            = self.all, self.__boiler, self.alfai, self.alfaii, self.vc_rec, self.H_rec, self.unknown,\
              self.vi, self.vii, self.ti, self.tii, self.Pi, self.Pii, self.unknown_local,\
              self.tipdvizh, self.Vg, self.fg, self.__Br, self.fi, self.delta_alfa, self.Hhv0, self.Di, \
              self.Ql

        access = False
        self.Hi = Hi = argum['Hi']
        self.Hii = Hii = argum['Hii']
        self.hi = hi = argum['hi']
        self.hii = hii = argum['hii']
        self.F = F = argum['F']

        prov_argum = { all['Hii'] : 0,
                       all['hii'] : 0, }

        self.vi = vi = boiler.vgaz(Hi, alfai, vc_rec, H_rec) if 'Hi' in unknown else self.vi
        self.ti = ti = new_water_steam.eheatT(Pi, hi) if 'hi' in unknown else self.ti
            #WaterSteam.t_ph(Pi, hi) if 'hi' in unknown else ti
        x_dryi = new_water_steam.eheatXPH(Pi, hi)
            #WaterSteam.x_ph(Pi, hi)
        self.vii = vii = boiler.vgaz(Hii, alfaii, vc_rec, H_rec) if 'Hii' in unknown else self.vii
        self.tii = tii = new_water_steam.eheatT(Pii, hii) if 'hii' in unknown else self.tii
            #WaterSteam.t_ph(Pii, hii) if 'hii' in unknown else tii
        x_dryii = new_water_steam.eheatXPH(Pii, hii)
            #WaterSteam.x_ph(Pii, hii)

        self.vi, self.ti, self.vii, self.tii, access = vi, ti, vii, tii, access = newton_method.restrictions(unknown_local, tipdvizh, access, vi, ti, vii, tii)
        if access == True:
            self.Hi = Hi = argum['Hi'] = boiler.HGAZ(vi, alfai, vc_rec, H_rec) if 'Hi' in unknown else self.Hi
            self.Hii = Hii = argum['Hii'] = boiler.HGAZ(vii, alfaii, vc_rec, H_rec) if 'Hii' in unknown else self.Hii
            self.hi = hi = argum["hi"] = new_water_steam.eheatHPT(Pi, ti) if 'hi' in unknown else self.hi
                #WaterSteam.h_pt(Pi, ti) if 'hi' in unknown else hi
            self.hii = hii = argum["hii"] = new_water_steam.eheatHPT(Pii, tii) if 'hii' in unknown else self.hii
                #WaterSteam.h_pt(Pii, tii) if 'hii' in unknown else hii

        wg = boiler.wg(Vg, vi, vii, fg, Br)
        k = self.__k_method(wg, vii)

        if x_dryii > 0 and x_dryii < 1:
            tkip = new_water_steam.eheatTs(Pii)
                #WaterSteam.tsat_p(Pii)
            hkip = new_water_steam.eheatH1(tkip)
                #WaterSteam.hL_t(tkip)
            Qbvek = fi * (Hi - Hii + delta_alfa * Hhv0)
            tusl = tkip + (hii - hkip) / 8.4
            Q1 = (hkip - hi) * Di / Br
            Hpr = Hii + Q1 / fi - delta_alfa * Hhv0
            vpr = boiler.vgaz(Hpr, alfaii, vc_rec, H_rec)
            Q2 = Qbvek - Q1
            deltat = boiler.tempnap_average(tipdvizh, vi, ti, vii, tusl, vpr, tkip, Q1, Q2)
        else:
            deltat = boiler.tempnap(tipdvizh, vi, ti, vii, tii)

        prov_argum["Hii"] = Hi + delta_alfa * Hhv0 - k * F * deltat / (Br * 1000 * fi)
        prov_argum["hii"] = (k * F * deltat / (Br * 1000) + Ql) * Br / Di + hi

        self.vi, self.ti, self.vii, self.tii, self.x_dryi, self.x_dryii, self.k, self.wg, self.deltat \
            = vi, ti, vii, tii ,x_dryi, x_dryii, k, wg, deltat
        return prov_argum

    def __solution(self):
        all, vi, ti, vii, tii, F, unknown, boiler, stat, alfai, Pi, vc_rec, H_rec, Hi, Hii, hi, hii = \
            self.all, self.vi, self.ti, self.vii, self.tii, self.F, self.unknown, self.__boiler, \
            self.stat, self.alfai, self.Pi, self.vc_rec, self.H_rec, self.Hi, self.Hii, self.hi, \
            self.hii,

        self.alfaii = alfaii = alfai + self.delta_alfa
        self.Pii = Pii = Pi - self.delta_P
        self.Qlvyh = self.Qlvh * (1 - self.fi_pp)
        self.Ql = self.Qlvh - self.Qlvyh
        self.Dii = self.Di

        argum_temp = {
            "Hi" : vi,
            "hi" : ti,
            "Hii" : vii,
            "hii" : tii,
            "F" : F
        }

        newton_method.argum_nan(argum_temp)

        newton_method.argum_pre(unknown, argum_temp)

        self.vi = vi = argum_temp["Hi"]
        self.ti = ti = argum_temp["hi"]
        self.vii = vii = argum_temp["Hii"]
        self.tii = tii = argum_temp["hii"]
        self.F = F = argum_temp["F"]

        argum = {
            "Hi" : boiler.HGAZ(vi, alfai, vc_rec, H_rec) if "Hi" in unknown or math.isnan(Hi) else Hi,
            "hi" : new_water_steam.eheatHPT(Pi, ti) #WaterSteam.h_pt(Pi, ti)
            if "hi" in unknown or math.isnan(hi) else hi,
            "Hii" : boiler.HGAZ(vii, alfaii, vc_rec, H_rec) if "Hii" in unknown or math.isnan(Hii) else Hii,
            "hii" : new_water_steam.eheatHPT(Pii, tii) #WaterSteam.h_pt(Pii, tii)
            if "hii" in unknown or math.isnan(hii) or all["hii"] in stat else hii,
            "F" : F
        }

        newton_method.newton_method(self.__shpp_iter, argum, unknown)
        #self.Hi, self.hi, self.Hii, self.hii, self.F = argum.values()

    def poisk_korney(self):
        boiler, alfai, delta_alfa = self.__boiler, self.alfai, self.delta_alfa

        if math.isnan(self.__Br):
            self.__Br = 20
        self.vc_rec = boiler.vc_rec
        self.Vg = boiler.Vg(alfai + delta_alfa / 2, boiler.Vg_rec)
        self.fi = boiler.fi
        self.Hhv0 = boiler.Hhv0
        self.H_rec = boiler.H_rec
        self.__solution()
        self.Qb = self.__Qb_method()

