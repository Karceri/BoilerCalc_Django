from abc import ABC, abstractmethod
from . import newton_method
from . import new_water_steam
import math
from pyXSteam.XSteam import XSteam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class AbstractConvPov(ABC):
    def __init__(self, boiler, name, unknown, stat, tipdvizh, vii, tii, F, delta_P, fg, fi_pp,
            delta_alfa, ksi, n, s1, dn, A, m, gaz_number):
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
        self.type = None
        self.all = None
        self.varia = None
        self.unknown_local = None
        self.k = 0
        self.deltat = 0
        self.__Di = 25
        self.__Dii = 25
        self.__Br = 25
        self.__Pi = 1
        self.__Pii = 1
        self.__ti = 1
        self.__hi = 1
        ############################
        self.__boiler = boiler
        self.name = name
        self.unknown = unknown
        self.stat = stat
        self.tipdvizh = tipdvizh
        self.vii = vii
        self.Hii = math.nan
        self.__tii = tii
        self.__hii = math.nan
        self.F = F
        self.delta_P = delta_P
        self.fg = fg
        self.fi_pp = fi_pp
        self.delta_alfa = delta_alfa
        self.ksi = ksi
        self.n = n
        self.s1 = s1
        self.dn = dn
        self.A = A
        self.m = m
        self.__n_Qb = -1
        self.gaz_number = gaz_number

    Bi = property(lambda self: self.__Br,
                  lambda self, value: setattr(self, '_AbstractConvPov__Br', value))
    Bii = property(lambda self: self.__Br,
                  lambda self, value: setattr(self, '_AbstractConvPov__Br', value))

    def __Qb_method(self):
        k, deltat, F, boiler, n_Qb = self.k, self.deltat, self.F, self.__boiler, self.__n_Qb

        Qb = k * deltat * F / 1000
        if n_Qb == -1:
            boiler.Qb.append(Qb)
            self.__n_Qb = len(boiler.Qb) - 1
        else:
            boiler.Qb[n_Qb] = Qb
        return Qb

    def __k_method(self, wg):
        s1, dn, ksi, A, n, m = self.s1, self.dn, self.ksi, self.A, self.n, self.m

        sigma1 = s1 / dn
        k = 0.86 * ksi * A * math.pow(wg / 9, n) * math.pow(32 / dn, 0.35) * math.pow(sigma1 / 2.5, 0.15 * m)
        return k

    def __conv_iter(self, argum):
        all, boiler, alfai, alfaii, vc_rec, H_rec, unknown, vi, vii, ti, tii, Pi, Pii, unknown_local, tipdvizh, \
        Vg, fg, Br, fi, delta_alfa, Hhv0, Di, Ql \
            = self.all, self.__boiler, self.alfai, self.alfaii, self.vc_rec, self.H_rec, self.unknown,\
              self.vi, self.vii, self.__ti, self.__tii, self.__Pi, self.__Pii, self.unknown_local,\
              self.tipdvizh, self.Vg, self.fg, self.__Br, self.fi, self.delta_alfa, self.Hhv0, self.__Di, \
              self.Ql

        access = False
        self.Hi = Hi = argum[all['Hi']]
        self.Hii = Hii = argum[all['Hii']]
        self.__hi = hi = argum[all['hi']]
        self.__hii = hii = argum[all['hii']]
        self.F = F = argum[all['F']]

        prov_argum = { all['Hii'] : 0,
                       all['hii'] : 0 }

        self.vi = vi = boiler.vgaz(Hi, alfai, vc_rec, H_rec) if all['Hi'] in unknown else self.vi
        self.__ti = ti = new_water_steam.eheatT(Pi, hi) if all['hi'] in unknown else self.__ti
        #WaterSteam.t_ph(Pi, hi) if all['hi'] in unknown else ti
        x_dryi = new_water_steam.eheatXPH(Pi, hi)
        #WaterSteam.x_ph(Pi, hi)
        self.vii = vii = boiler.vgaz(Hii, alfaii, vc_rec, H_rec) if all['Hii'] in unknown else self.vii
        self.__tii = tii = new_water_steam.eheatT(Pii, hii) if all['hii'] in unknown else self.__tii
        #WaterSteam.t_ph(Pii, hii) if all['hii'] in unknown else tii
        x_dryii = new_water_steam.eheatXPH(Pii, hii)
        #WaterSteam.x_ph(Pii, hii)

        self.vi, self.__ti, self.vii, self.__tii, access = vi, ti, vii, tii, access = newton_method.restrictions(unknown_local, tipdvizh, access, vi, ti, vii, tii)
        if access == True:
            self.Hi = Hi = argum[all['Hi']] = boiler.HGAZ(vi, alfai, vc_rec, H_rec) if all['Hi'] in unknown else self.Hi
            self.Hii = Hii = argum[all['Hii']] = boiler.HGAZ(vii, alfaii, vc_rec, H_rec) if all['Hii'] in unknown else self.Hii
            self.__hi = hi = argum[all["hi"]] = new_water_steam.eheatHPT(Pi, ti) if all['hi'] in unknown else self.__hi
            #WaterSteam.h_pt(Pi, ti) if all['hi'] in unknown else hi
            self.__hii = hii = argum[all["hii"]] = new_water_steam.eheatHPT(Pii, tii) if all['hii'] in unknown else self.__hii
            #WaterSteam.h_pt(Pii, tii) if all['hii'] in unknown else hii

        wg = boiler.wg(Vg, vi, vii, fg, Br)
        k = self.__k_method(wg)

        if x_dryii > 0 and x_dryii < 1:
            tkip = new_water_steam.eheatTs(Pii)#WaterSteam.tsat_p(Pii)
            hkip = new_water_steam.eheatH1(tkip)#WaterSteam.hL_t(tkip)
            Qbvek = fi * (Hi - Hii + delta_alfa * Hhv0)
            tusl = tkip + (hii - hkip) / 8.4
            Q1 = (hkip - hi) * Di / Br
            Hpr = Hii + Q1 / fi - delta_alfa * Hhv0
            vpr = boiler.vgaz(Hpr, alfaii, vc_rec, H_rec)
            Q2 = Qbvek - Q1
            deltat = boiler.tempnap_average(tipdvizh, vi, ti, vii, tusl, vpr, tkip, Q1, Q2)
        else:
            deltat = boiler.tempnap(tipdvizh, vi, ti, vii, tii)

        prov_argum[all["Hii"]] = Hi + delta_alfa * Hhv0 - k * F * deltat / (Br * 1000 * fi)
        prov_argum[all["hii"]] = (k * F * deltat / (Br * 1000) + Ql) * Br / Di + hi

        self.vi, self.__ti, self.vii, self.__tii, self.x_dryi, self.x_dryii, self.k, self.wg, self.deltat \
            = vi, ti, vii, tii ,x_dryi, x_dryii, k, wg, deltat
        return prov_argum

    def __solution(self):
        all, vi, ti, vii, tii, F, unknown, boiler, stat, alfai, Pi, vc_rec, H_rec, Hi, Hii, hi, hii = \
            self.all, self.vi, self.__ti, self.vii, self.__tii, self.F, self.unknown, self.__boiler, \
            self.stat, self.alfai, self.__Pi, self.vc_rec, self.H_rec, self.Hi, self.Hii, self.__hi, \
            self.__hii,

        self.alfaii = alfaii = alfai + self.delta_alfa
        self.__Pii = Pii = Pi - self.delta_P
        self.Qlvyh = self.Qlvh * (1 - self.fi_pp)
        self.Ql = self.Qlvh - self.Qlvyh
        self.__Dii = self.__Di

        argum_temp = {
            all["Hi"] : vi,
            all["hi"] : ti,
            all["Hii"] : vii,
            all["hii"] : tii,
            all["F"] : F
        }

        newton_method.argum_nan(argum_temp)

        newton_method.argum_pre(unknown, argum_temp)

        self.vi = vi = argum_temp[all["Hi"]]
        self.__ti = ti = argum_temp[all["hi"]]
        self.vii = vii = argum_temp[all["Hii"]]
        self.__tii = tii = argum_temp[all["hii"]]
        self.F = F = argum_temp[all["F"]]

        argum = {
            all["Hi"] : boiler.HGAZ(vi, alfai, vc_rec, H_rec) if all["Hi"] in unknown or math.isnan(Hi) else Hi,
            all["hi"] : new_water_steam.eheatHPT(Pi, ti)#WaterSteam.h_pt(Pi, ti)
            if all["hi"] in unknown or math.isnan(hi) else hi,
            all["Hii"] : boiler.HGAZ(vii, alfaii, vc_rec, H_rec) if all["Hii"] in unknown or math.isnan(Hii) else Hii,
            all["hii"] : new_water_steam.eheatHPT(Pii, tii)#WaterSteam.h_pt(Pii, tii)
            if all["hii"] in unknown or math.isnan(hii) or all["hii"] in stat
                else hii,
            all["F"] : F
        }

        newton_method.newton_method(self.__conv_iter, argum, unknown)
        #self.Hi, self.__hi, self.Hii, self.__hii, self.F = argum.values()

    @abstractmethod
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


