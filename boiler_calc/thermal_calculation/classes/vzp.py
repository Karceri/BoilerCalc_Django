import math
from . import newton_method
from pyXSteam.XSteam import XSteam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class VZP:
    def __init__(self, boiler, type, name, unknown, stat, tipdvizh, vii, tii, F, fg, fi_pp,
                 delta_alfa, ksi0, delta_ksi, wg, wp, air_number, gaz_number):
        self.vi = 1
        self.ti = 1
        self.Hi = 1
        self.hi = 1
        self.k = 0
        self.deltat = 0
        self.Qb = 0
        self.Br = 1
        self.Pi = 1
        self.Pii = 1
        self.Bi_air = 1
        self.Bii_air = 1
        self.fi = 1
        self.bettagvii = 1
        self.bettagvi = 1
        self.Qlvh = 1
        self.Ql = 1
        self.Qlvyh = 1
        self.alfai = 1
        self.alfaii = 1
        self.vc_rec = 0
        self.H_rec = 0
        self.Vg = 1
        ##########################
        self.boiler = boiler
        self.type = type
        self.name = name
        self.unknown = unknown
        self.tipdvizh = tipdvizh
        self.vii = vii
        self.tii = tii
        self.Hii = math.nan
        self.hii = math.nan
        self.F = F
        self.fg = fg
        self.fi_pp = fi_pp
        self.ksi0 = ksi0
        self.delta_ksi = delta_ksi
        self.wg = wg
        self.wp = wp
        self.air_number = air_number
        self.gaz_number = gaz_number
        self.delta_alfa = delta_alfa
        self.stat = stat
        self.all = all = {
            'Hi' : 'Hi',
            'hi' : 'hi_air',
            'Hii' : 'Hii',
            'hii' : 'hii_air',
            'F' : 'F',
        }
        self.varia = varia = list(set(all.values()) - set(stat) - set(unknown))
        self.unknown_local = unknown_local = list(key for key, value in all.items() if value in unknown)

    Bi = property(lambda self: self.Br, lambda self, value: setattr(self, 'Br', value))
    Bii = property(lambda self: self.Br, lambda self, value: setattr(self, 'Br', value))
    Hi_air = property(lambda self: self.hi, lambda self, value: setattr(self, 'hi', value))
    Hii_air = property(lambda self: self.hii, lambda self, value: setattr(self, 'hii', value))
    ti_air = property(lambda self: self.ti, lambda self, value: setattr(self, 'ti', value))
    tii_air = property(lambda self: self.tii, lambda self, value: setattr(self, 'tii', value))

    def __Qb_method(self):

        self.Qb = self.k * self.deltat * self.F / 1000

    def __k_method(self, wg, wp):
        ksi = self.ksi0 + self.delta_ksi
        k = 3 * ksi * math.pow(wg + 0.5 * wp, 0.8)
        return k

    def __vzpiter(self, argum):
        boiler, alfai, vc_rec, H_rec, unknown, vi, ti, alfaii, vii, tii, unknown_local, tipdvizh,\
            wg, wp, delta_alfa, Br, fi, Ql, bettagvii = \
            self.boiler, self.alfai, self.vc_rec, self.H_rec, self.unknown, self.vi, self.ti, self.alfaii,\
            self.vii, self.tii, self.unknown_local, self.tipdvizh, self.wg, self.wp, self.delta_alfa, self.Br,\
            self.fi, self.Ql, self.bettagvii

        access = False
        self.Hi = Hi = argum['Hi']
        self.Hii = Hii = argum['Hii']
        self.hi = hi = argum["hi_air"]
        self.hii = hii = argum["hii_air"]
        self.F = F = argum["F"]

        prov_argum = {
            'Hii' : 0,
            'hii_air' : 0,
        }
        self.vi = vi = boiler.vgaz(Hi, alfai, vc_rec, H_rec) if 'Hi' in unknown else self.vi
        self.ti = ti = boiler.tAIR(hi) if 'hi_air' in unknown else self.ti
        self.vii = vii = boiler.vgaz(Hii, alfaii, vc_rec, H_rec) if 'Hii' in unknown else self.vii
        self.tii = tii = boiler.tAIR(hii) if 'hii_air' in unknown else self.tii

        self.vi, self.ti, self.vii, self.tii, access = vi, ti, vii, tii, access = newton_method.restrictions(unknown_local, tipdvizh, access, vi, ti, vii, tii)
        if access == True:
            self.Hi = Hi = argum['Hi'] = boiler.HGAZ(vi, alfai, vc_rec, H_rec) if 'Hi' in unknown else self.Hi
            self.Hii = Hii = argum['Hii'] = boiler.HGAZ(vii, alfaii, vc_rec, H_rec) if 'Hii' in unknown else self.Hii
            self.hi = hi = argum['hi_air'] = boiler.HAIR(ti) if 'hi_air' in unknown else self.hi
            self.hii = hii = argum['hii_air'] = boiler.HAIR(tii) if 'hii_air' in unknown else self.hii

        k = self.__k_method(wg, wp)
        deltat = boiler.tempnap(tipdvizh, vi, ti, vii, tii)
        Hpris = boiler.HAIR((ti + tii) / 2)
        prov_argum["Hii"] = Hi + delta_alfa * Hpris - k * F * deltat / (Br * 1000 * fi)
        prov_argum["hii_air"] = hi + ((k * F * deltat) / (Br * 1000) + Ql) / (bettagvii + delta_alfa / 2)

        self.vi, self.ti, self.vii, self.tii, self.k, self.deltat = vi, ti, vii, tii, k, deltat

        return prov_argum

    def __kornivzp(self):
        boiler, bettagvi, delta_alfa, Bi_air, Qlvh, fi_pp, alfai, vi, ti, vii, tii, F, unknown, vc_rec, \
        H_rec, Hi, hi, Hii, hii = \
            self.boiler, self.bettagvi, self.delta_alfa, self.Bi_air, self.Qlvh, self.fi_pp, self.alfai, \
            self.vi, self.ti, self.vii, self.tii, self.F, self.unknown, self.vc_rec, self.H_rec, \
            self.Hi, self.hi, self.Hii, self.hii

        self.bettagvii = bettagvii = bettagvi - delta_alfa
        self.Bii_air = Bii_air = Bi_air
        self.Qlvyh = Qlvyh = Qlvh * (1 - fi_pp)
        self.Ql = Ql = Qlvh - Qlvyh
        self.alfaii = alfaii = alfai + delta_alfa

        argum_temp = {
            'Hi' : vi,
            'hi_air': ti,
            'Hii': vii,
            'hii_air': tii,
            'F': F,
        }

        newton_method.argum_nan(argum_temp)

        newton_method.argum_pre(unknown, argum_temp)

        self.vi = vi = argum_temp["Hi"]
        self.ti = ti = argum_temp["hi_air"]
        self.vii = vii = argum_temp["Hii"]
        self.tii = tii = argum_temp["hii_air"]
        self.F = F = argum_temp["F"]

        argum = {
            'Hi' : boiler.HGAZ(vi, alfai, vc_rec, H_rec) if 'Hi' in unknown or math.isnan(Hi) else Hi,
            'hi_air' : boiler.HAIR(ti) if 'hi_air' in unknown or math.isnan(hi) else hi,
            'Hii' : boiler.HGAZ(vii, alfaii, vc_rec, H_rec) if 'Hii' in unknown or math.isnan(Hii) else Hii,
            'hii_air': boiler.HAIR(tii) if 'hii_air' in unknown or math.isnan(hii) else hii,
            'F' : F,
        }

        newton_method.newton_method(self.__vzpiter, argum, unknown)
        #self.Hi, self.hi, self.Hii, self.hii, self.F = argum.values()

    def poisk_korney(self):
        Br, boiler, alfai, delta_alfa = self.Br, self.boiler, self.alfai, self.delta_alfa
        if math.isnan(Br):
            self.Br = 20
        self.vc_rec = boiler.vc_rec
        self.H_rec= boiler.H_rec
        self.Vg = boiler.Vg(alfai + delta_alfa / 2, boiler.Vg_rec)
        self.fi = boiler.fi
        self.__kornivzp()
        self.__Qb_method()

