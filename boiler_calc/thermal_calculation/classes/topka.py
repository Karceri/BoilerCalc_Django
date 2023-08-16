import math
from . import newton_method
from pyXSteam.XSteam import XSteam
WaterSteam = XSteam(XSteam.UNIT_SYSTEM_MKS)


class SingleZoneTopka:
    def __init__(self, boiler, name, unknown, stat, Ffst, Fzst, Fbok, Fvok, bt, ht, hg, Vt,
                 ksi, x, delta_alfa, alfaii, gaz_number, air_number, gaz_number_alter, stream_number_alter):
        self.vi_main = 1
        self.vi_rec = 1
        self.ti = 1
        self.ti_water = 1
        self.ti_air = 1
        self.F = 1
        self.vii = 1
        self.tii = 1
        self.tii_water = 1
        self.tii_air = 1
        self.Hi_main = 1
        self.Hi_rec = 0
        self.H_rec = 0
        self.hi = 1
        self.hi_water = 1
        self.Hi_air = 1
        self.Hii = 1
        self.hii = 1
        self.hii_water = 1
        self.Hii_air = 1
        self.Di = 1
        self.Dii = 1
        self.Br_main = 1
        self.Br_rec = 0
        self.fi = 1
        self.bettagvi = 1
        self.t1 = 1
        self.Hhv0 = 1
        self.alfapl = 1
        self.q3 = 1
        self.q4 = 1
        self.q6 = 1
        self.delta_alfa = 1
        self.Qlvyh = 1
        self.alfai_main = 1
        self.alfai_rec = 0
        self.alfaii = 1
        self.tgv = 1
        self.Ql = 1
        self.Bi_air = 1
        self.Bii_air = 1
        self.ql = 1
        self.r_rec = 0
        self.vc_rec = 0
        self.Qrr = 1
        self.Vg_rec = 0
        self.Br = 1
        self.Bug = 1
        self.M = 1
        self.Vg = 1
        self.rv = 1
        self.Vt = 1
        self.ksi = 1
        self.x = 1

        ###########################
        self.__boiler = boiler
        self.type = 'Топка однозонная'
        self.name = name
        self.Ffst = Ffst
        self.Fzst = Fzst
        self.Fbok = Fbok
        self.Fvok = Fvok
        self.bt = bt
        self.ht = ht
        self.hg = hg
        self.Vt = Vt
        self.ksi = ksi
        self.x = x
        self.n_Qb = -1
        self.air_number = air_number
        self.gaz_number_main = gaz_number
        self.gaz_number_alter = gaz_number_alter
        self.stream_number_alter = stream_number_alter
        self.delta_alfa = delta_alfa
        self.unknown = unknown
        self.stat = stat
        all = ['Hi', 'Hii', 'hi_air']
        self.varia = list(set(all) - set(unknown) - set(stat))
        self.main_trakt = True

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
            return self.vi_rec

    @vi.setter
    def vi(self, value):
        if self.main_trakt == True:
            self.vi_main = value
        else:
            self.vi_rec = value

    @property
    def Hi(self):
        if self.main_trakt == True:
            return self.Hi_main
        else:
            return self.Hi_rec

    @Hi.setter
    def Hi(self, value):
        if self.main_trakt == True:
            self.Hi_main = value
        else:
            self.Hi_rec = value

    @property
    def alfai(self):
        if self.main_trakt == True:
            return self.alfai_main
        else:
            return self.alfai_rec

    @alfai.setter
    def alfai(self, value):
        if self.main_trakt == True:
            self.alfai_main = value
        else:
            self.alfai_rec = value

    @property
    def Bi(self):
        if self.main_trakt == True:
            return self.Br_main
        else:
            return self.Br_rec

    @Bi.setter
    def Bi(self, value):
        if self.main_trakt == True:
            self.Br_main = value
        else:
            self.Br_rec = value

    Gi = property(lambda self: self.Di,
                  lambda self, value: setattr(self, 'Di', value))
    Gii = property(lambda self: self.Dii,
                   lambda self, value: setattr(self, 'Dii', value))

    Bii = property(lambda self: self.Br,
                    lambda self, value: setattr(self, 'Br', value))



    def __Br_method(self, Br_main, Br_rec):
        return Br_main + Br_rec

    def __Vg_rec_method(self, r_rec, Vg_rec):
        if math.isnan(Vg_rec):
            Vg_rec = 0
        return r_rec * self.__boiler.Vg(self.alfai_rec, Vg_rec)

    def __vc_rec_method(self, r_rec, Hi_rec, vi_rec):
        vc_rec = r_rec * Hi_rec / vi_rec
        if math.isnan(vc_rec):
            vc_rec = 0
        return vc_rec

    def __r_rec_method(self):
        r_rec = self.Br_rec / self.Br_main
        if math.isnan(r_rec):
            r_rec = 0
        return r_rec

    def __H_rec_method(self, r_rec, Hi_rec):
        H_rec = r_rec * Hi_rec
        if math.isnan(H_rec):
            H_rec = 0
        return H_rec

    def __alfagor_func(self):
        return self.alfaii - self.delta_alfa

    def __bettagv_func(self):
        return self.alfaii - self.delta_alfa - self.alfapl

    def __QB_method(self):
        return self.bettagvi * self.Hi_air + (self.delta_alfa + self.alfapl) * self.Hhv0

    def __Fsum(self):
        return self.Ffst + self.Fzst + 2 * self.Fbok + self.Fvok

    def __Qt_method(self, QB):
        return self.Qrr * ((100 - self.q3 - self.q4 - self.q6) / (100 - self.q4)) + self.__boiler.Qf + QB + self.H_rec

    def Ql_method(self, Qt, Hii):
        self.Ql = (Qt - Hii) * self.fi
        QlBr = self.Ql * self.Br
        if self.n_Qb == -1:
            self.__boiler.Qb.append(QlBr)
            self.n_Qb = len(self.__boiler.Qb) - 1
        else:
            self.__boiler.Qb[self.n_Qb] = QlBr
        return self.Ql

    def ql_method(self, Ql, Hii):
        hi = 0.98
        self.ql = ql = self.Br * Ql / (self.__Fsum() * hi)
        return ql

    def Qlvyh_method(self, ql, Hii):
        tettabetta= 0.8
        res = 1100 / self.vii * tettabetta * ql * self.Fvok / self.Br
        return res

    def __iter(self, argum):
        boiler, alfai, alfaii, vc_rec, H_rec, unknown, vi, vii, ti, tii, \
        Vg, Br, fi, delta_alfa, Hhv0, Di, Ql, Vt, Vg_rec, alfai_rec, r_rec, hg ,ht, x, ksi \
            = self.__boiler, self.alfai_main, self.alfaii, self.vc_rec, self.H_rec, self.unknown, \
              self.vi_main, self.vii, self.ti, self.tii, \
              self.Vg, self.Br, self.fi, self.delta_alfa, self.Hhv0, self.Di, \
              self.Ql, self.Vt, self.Vg_rec, self.alfai_rec, self.r_rec, self.hg, self.ht, self.x, self.ksi

        self.Hi_main = Hi = argum['Hi']
        self.Hii = Hii = argum['Hii']

        prov_argum = {
            'Hii' : 0
        }

        self.vi_main = vi = boiler.vgaz(Hi, alfai, vc_rec, H_rec) if 'Hi' in unknown else self.vi_main
        self.vii = vii = boiler.vgaz(Hii, alfaii, vc_rec, H_rec) if 'Hii' in unknown else self.vii
        va = vi
        Qt = Hi
        cvcp = (Qt - Hii) / (va - vii)
        Ta = va + 273.15
        St = 3.6 * Vt / self.__Fsum()
        p = 0.1
        Vg = boiler.Vg(alfaii, Vg_rec)
        Vh2o = boiler.Vh20(alfaii)
        Gg = boiler.Gg(alfaii, alfai_rec, r_rec)
        rRO2 = boiler.rRO2(Vg)
        rH2O = boiler.rH20(Vh2o, Vg)
        Muzl = boiler.Muzl(Gg)
        Kzl = boiler.Kzl_Muzl(vii, Muzl, St)
        rn = boiler.rn(rH2O, rRO2)
        Kg = boiler.Kg(St, vii, rH2O, rn)
        K = boiler.K(Kg, rn, Kzl)
        Bug = boiler.Bu(K, St, p)
        Bupriv = 1.6 * math.log((1.4 * math.pow(Bug, 2) + Bug + 2) / (1.4 * math.pow(Bug, 2) - Bug + 2))
        Xt = hg / ht
        rv = Vg / (boiler.Vn20 + boiler.Vro2)
        M = 0.46 * (1 - 0.4 * Xt) * math.pow(rv, 0.3333)
        fiekr = x * ksi
        vtiiprov = Ta / (1 + M * math.pow(Bupriv, 0.3) *
                         math.pow(((5.67E-11 * fiekr * self.__Fsum() * math.pow(Ta, 3)) /
                                   (fi * Br * cvcp)), 0.6)) - 273.15
        prov_argum["Hii"] = boiler.HGAZ(vtiiprov, alfaii, vc_rec, H_rec)

        self.alfai_main, self.alfaii, self.vc_rec, self.H_rec, self.unknown, self.vi_main, self.vii, self.ti, self.tii, \
        self.Vg, self.Br, self.fi, self.delta_alfa, self.Hhv0, self.Di, \
        self.Ql, self.Vt, self.Vg_rec, self.alfai_rec, self.r_rec, self.hg, self.ht, self.x, self.ksi = \
            alfai, alfaii, vc_rec, H_rec, unknown, vi, vii, ti, tii, \
        Vg, Br, fi, delta_alfa, Hhv0, Di, Ql, Vt, Vg_rec, alfai_rec, r_rec, hg, ht, x, ksi
        return prov_argum

    def __solution(self):
        boiler, ti_air, bettagvi, delta_alfa, alfapl, Br_main, Vg_rec, Hi_rec, vi_rec, unknown, t1, vii, Hii = \
            self.__boiler, self.ti_air, self.bettagvi, self.delta_alfa, self.alfapl, self.Br_main, self.Vg_rec,\
            self.Hi_rec, self.vi_rec, self.unknown, self.t1, self.vii, self.Hii

        if math.isnan(ti_air):
            self.ti_air = ti_air = 350
        self.tgv = tgv = ti_air
        self.Hi_air = hi_air = boiler.HAIR(tgv)
        self.alfai_main = alfai = self.__alfagor_func()
        self.alfaii = alfaii = bettagvi + delta_alfa + alfapl
        self.Br = Br = Br_main
        if math.isnan(Br):
            self.Br = Br = 20
        self.r_rec = r_rec = self.__r_rec_method()
        self.Vg_rec = Vg_rec = self.__Vg_rec_method(r_rec, Vg_rec)
        self.H_rec = H_rec = self.__H_rec_method(r_rec, Hi_rec)
        self.vc_rec = vc_rec = self.__vc_rec_method(r_rec, Hi_rec, vi_rec)
        self.QB = QB = self.__QB_method()
        self.Hi_main = Hi = self.__Qt_method(QB)
        self.vi_main = vi = boiler.vgaz(Hi, alfai, vc_rec, H_rec)
        self.vii = vii = t1 - 50 if "Hii" in unknown else vii

        argum_temp = {
            'Hi' : vi,
            'Hii' : vii,
        }

        argum = {
            'Hi' : boiler.HGAZ(vi, alfai, vc_rec, H_rec) if "Hi" in unknown or math.isnan(Hi) else Hi,
            'Hii': boiler.HGAZ(vii, alfaii, vc_rec, H_rec) if "Hii" in unknown or math.isnan(Hii) else Hii,
        }

        newton_method.newton_method(self.__iter, argum, unknown)

        #Hi, Hii = self.Hi_main, self.Hii = argum.values()

        self.Ql = Ql = self.Ql_method(self.Hi_main, self.Hii)
        self.ql = ql = self.ql_method(Ql, self.Hii)
        self.Qlvyh = self.Qlvyh_method(ql, self.Hii)

    def poisk_korney(self):
        boiler = self.__boiler
        self.fi = boiler.fi
        self.t1 = boiler.t1
        self.Hhv0 = boiler.Hhv0
        self.alfapl = boiler.alfapl
        self.Qrr = boiler.Qrr
        self.q3 = boiler.q3
        self.q4 = boiler.q4
        self.q6 = boiler.q6

        self.__solution()

        boiler.r_rec = self.r_rec
        boiler.Vg_rec = self.Vg_rec
        boiler.H_rec = self.H_rec
        boiler.vc_rec = self.vc_rec
        boiler.tgv = self.tgv
        boiler.Hgv = self.Hi_air
        boiler.bettagv = self.bettagvi
        boiler.ql = self.ql
        boiler.vii_topk = self.vii








