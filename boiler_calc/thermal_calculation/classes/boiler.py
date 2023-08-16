import math, numpy as np, pdb
from .exceptions import *


# Теплоемкость продуктов сгорания при сжигании твердых, жидких и газообразных топлив cг кДж/(м3К), при температуре 2200 °С
def cgaz_method(tip, Wp):
    if tip == 'solid':
        res = 1.71 + 4.2 * Wp * 1E-2
    elif tip == 'liquid':
        res = 1.693
    else: # 'gaseous'
        res = 1.685
    return res


# Теоретическая энтальпия газов при температуре 2200 °C
def H0GAZ2200(VGAZ0, cgaz):
    res = 2200 * VGAZ0 * cgaz
    return res


# Теоретическая энтальпия воздуха, кДж/кг, при температуре 2200 °С
def H0AIR2200(VAIR0):
    res = 3403 * VAIR0
    return res


# Энтальпии газов при температуре 2200°C и избытке воздуха alfa
def HGAZ2200(VGAZ0, alfa, VAIR0, cgaz):
    HGAZ0 = H0GAZ2200(VGAZ0, cgaz)
    HAIR0 = H0AIR2200(VAIR0)
    H = HGAZ0 + (alfa - 1) * HAIR0
    return H


# Подпрограмма по расчету энтальпии газов
def HGAZ(vgaz, VGAZ0, alfa, VAIR0, cgaz):
    H2200 = HGAZ2200(VGAZ0, alfa, VAIR0, cgaz)
    if vgaz <= 1150:
        H = H2200 * vgaz / (2695 - 0.3 * vgaz)
    else: # vgaz > 1150
        H = H2200 * (vgaz / 2050 - 0.075)
    return H


# Определение температуры газов
def vgaz(H, VGAZ0, alfa, VAIR0, cgaz):
    H2200 = HGAZ2200(VGAZ0, alfa, VAIR0, cgaz)
    if H / H2200 <= 0.5:
        vgaz = 2695 * ((H / H2200) / (1 + 0.3 * H / H2200))
    else: # HGAZ/HGAZ2200 > 0.5
        vgaz = 2050 * (H / H2200 + 0.075)
    return vgaz


# При известной температуре воздуха tв
def HAIR_method(bettaAIR, VAIR0, tAIR):
    HAIR0 = H0AIR2200(VAIR0)
    H = bettaAIR * HAIR0 * tAIR / (2610 - 0.25 * tAIR)
    return H


# При известной энтальпии воздуха Hв
def tAIR_method(bettaAIR, VAIR0, HAIR):
    HAIR0 = H0AIR2200(VAIR0)
    t = 2610 * HAIR / (bettaAIR * HAIR0 + 0.25 * HAIR)
    return t


class Boiler:
    def __init__(self, mark, tip, Wr, Ar, Sr, Cr, Hr, Nr, Or, vg, Qnr, klo, t1, t2, t3,
                 Dnom, aun, q3, q4):
        self.Dpe = 100
        self.Gpv = 100
        self.Ppe = 138
        self.Ppv = 138
        self.Pb = 138
        self.tpe = 545
        self.tpv = 200
        self.tgv = 300
        self.thv = 30
        self.vuhg = 150
        self.alfat = 1
        self.v_pk = 600
        self.Br = 30
        self.B = 30
        self.bettagv = 1
        self.Vair0 = 5
        self.Vn20 = 1
        self.Vro2 = 1
        self.Vh2o0 = 1
        self.Vg0 = 1
        self.Ap = 1
        self.Wp = 1
        self.Huhg = 450
        self.Hhv0 = 150
        self.Hgv = 1000
        self.q6 = 0.3
        self.q5 = 0.3
        self.fi = 0.3
        self.alfa_uhg = 1.25
        self.q2 = 6
        self.kpd = 90
        self.hpe = 3500
        self.hpv = 1700
        self.hkip = 2500
        self.Gpr = 0
        self.Kk = 0
        self.abs_Q = 0
        self.rel_Q = 0
        self.Dvt = 100
        self.tvt_i = 300
        self.tvt_ii = 545
        self.hvt_i = 3000
        self.hvt_ii = 3500
        self.Vpk = 1000
        self.vii_topk = 1000
        self.ql = 500
        self.vc_rec = 0
        self.Qrr = 0
        self.Qvvn = 0
        self.Qf = 0
        self.Qtl = 0
        self.Qkrb = 0
        self.k = 0
        self.Vg_rec = 0
        self.H_rec = 0
        self.r_rec = 0
        self.B_set = False
        self.n_iter = 0
        ####################
        self.Qb = []
        self.Q_stvpr = []
        self.mark = mark
        self.tip = tip
        self.Wr = Wr
        self.Ar = Ar
        self.Sr = Sr
        self.Cr = Cr
        self.Hr = Hr
        self.Nr = Nr
        self.Or = Or
        self.vg = vg
        self.Qnr = Qnr
        self.klo = klo
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.Dnom = Dnom
        self.aun = aun
        self.q3 = q3
        self.q4 = q4
        self.alfapl = 0.06
        self.d_zl = 16

    #Pb = property(lambda self: self.__Pb, lambda self, value: setattr(self, '_Boiler__Pb', value))
    #Qnr = property(lambda self: self.__Qnr)

    def poisk_korney(self):
        self.Vair0 = Vair0 = self.__Vair0_method()
        self.Vn20 = Vn20 = self.__Vn20_method(Vair0)
        self.Vro2 = Vro2 = self.__Vro2_method()
        self.Vh2o0 = Vh2o0 = self.__Vh2o0_method(Vair0)
        self.Vg0 = Vg0 = self.__Vg0_method(Vro2, Vn20, Vh2o0)
        self.Qrr = Qrr = self.__Qrr_method()
        self.Ap = Ap = self.__Ap_method()
        self.Wp = Wp = self.__Wp_method()
        self.q6 = q6 = self.__q6_method(Qrr)
        self.q5 = q5 = self.__q5_method()
        self.q2 = q2 = self.__q2_method(Qrr)
        self.kpd = kpd = self.__kpd_method(q2, q5, q6)
        self.fi = fi = self.__fi_method(q5, kpd)
        if self.B_set == False:
            self.B = B = self.__B_method(kpd, Qrr)
            self.Br = Br = self.__Br_method(B)
        self.Kk = Kk = self.__Kk_method()
        self.abc_Q = abc_Q = self.__abs_Q_method(Qrr, kpd, self.B)
        self.rel_Q = rel_Q = self.__rel_Q_method(abc_Q, Qrr, self.B)

    def __Qrr_method(self):  # Располагаемое тепло
        Qtl, Qkrb, k = self.Qtl, self.Qkrb, self.k
        res = self.Qnr + Qtl + (1 - k) * Qkrb
        return res

    def __abs_Q_method(self, Qrr, kpd, B): # Абсолютная величина невязки
        res = B * (Qrr * kpd / 100 + self.Qvvn + self.Qf) - sum(self.Qb)
        return res

    def __rel_Q_method(self, abs_Q, Qrr, B): # Относительная величина невязки
        res = math.fabs(abs_Q) / (Qrr * B) * 100
        return res

    def __Vair0_method(self):  # Теоретический объем воздуха
        res = 0.0889 * (self.Cr + 0.375 * self.Sr) + 0.265 * self.Hr - 0.0333 * self.Or
        return res

    def __Vn20_method(self, Vair0):  # Объем азота
        res = 0.79 * Vair0 + 0.8 * self.Nr / 100
        return res

    def __Vro2_method(self):  # Объем трехатомных газов
        res = 1.866 * (self.Cr + 0.375 * self.Sr) / 100
        return res

    def __Vh2o0_method(self, Vair0):  # Объем водяных паров
        res = 0.111 * self.Hr + 0.0124 * self.Wr + 0.0161 * Vair0
        return res

    def __Vg0_method(self, Vro2, Vn20, Vh2o0):  # Объем дымовых газов
        res = Vro2 + Vn20 + Vh2o0
        return res

    def __Ap_method(self):  # Приведенная зольность
        res = self.Ar * 1000 / self.Qnr
        return res

    def __Wp_method(self):  # Приведенная влажность
        res = self.Wr * 1000 / self.Qnr
        return res

    def __q6_method(self, Qrr):  # Потеря с физическим теплом шлака
        if self.t3 == 0:
            tshl = 1500
            ctshl = 1800
        else:
            if self.t3 > 1350:
                ctshl = 560
            else:
                tshl = self.t3 + 100
                cshl = 1.1 + 0.2 * (tshl - 1300) / 400
                ctshl = cshl * tshl
        res = (1 - self.aun) * self.Ar * ctshl / Qrr
        return res

    def __q5_method(self):  # Потеря теплоты от наружного охлаждения
        q5n = math.pow(60 / self.Dnom, 0.5) / math.log10(self.Dnom)
        res = q5n * self.Dnom / (self.Gpv - self.Gpr)
        return res

    def __q2_method(self, Qrr): # Потеря теплоты с уходящим газами
        try:
            res = ((1 - self.r_rec) * self.Huhg - self.alfa_uhg * self.Hhv0) * (100 - self.q4) / Qrr
        except: #if math.isnan(res):
            res = 10
        return res

    def __kpd_method(self, q2, q5, q6): # КПД
        res = 100 - q2 - self.q3 - self.q4 - q5 - q6
        return res

    def __fi_method(self, q5, kpd): # Коэффициент сохранения тепла
        res = 1 - q5 / (kpd + q5)
        return res

    def __B_method(self, kpd, Qrr): # Полный расход топлива
        res = ((self.Gpv - self.Gpr) * (self.hpe - self.hpv) + self.Dvt * (self.hvt_ii - self.hvt_i) +
               self.Gpr * (self.hkip - self.hpv) + sum(self.Q_stvpr)) / (Qrr * kpd / 100 + self.Qvvn + self.Qf)
        return res

    def __Br_method(self, B): # Расчетный расход топлива
        res = B * (1 - self.q4 / 100)
        return res

    def Vh20(self, alfa_average): # Объем водяных паров
        res = self.Vh2o0 + 0.0161 * (alfa_average - 1) * self.Vair0
        return res

    def Vg(self, alfa_average, Vgrec): # Полный объем газов
        res = self.Vg0 + 1.016 * (alfa_average - 1) * self.Vair0 + Vgrec
        return res

    def rRO2(self, Vg): # Объемная доля трехатомных газов
        res = self.Vro2 / Vg
        return res

    def rH20(self, Vh2O, Vg): # Объемная доля водяных паров
        res = Vh2O / Vg
        return res

    def rn(self, rH2O, rRO2): # Суммарная объемная доля
        res = rH2O + rRO2
        return res

    def Gg(self, alfa_average, alfa_otb, r): # Масса дымовых газов
        alfa_otb = 0 if math.isnan(alfa_otb) else alfa_otb
        r = 0 if math.isnan(r) else r
        res = (1 - 0.01 * self.Ar) * (1 + r) + 1.306 * (alfa_average + alfa_otb * r) * self.Vair0
        return res

    def Muzl(self, Gg): # Концентрация золовых частиц
        res = self.Ar * self.aun / (100 * Gg)
        return res

    def __Kk_method(self): # Коэфициент ослабления
        if self.mark == 'Антрацит' or self.mark == 'Полуантрацит' or self.mark == 'Тощий':
            return 1
        else:
            return 0.5

    def Kg(self, Stsh, vii, rH2O, rn): # Коэффициент поглощения лучей газовой фазой
        res = ((7.8 + 16 * rH2O) / math.sqrt(rn * Stsh) - 1) * (1 - 0.37 * (vii + 273.15) / 1000)
        return res

    def Kzl_Muzl(self, vii, Muzl, s): # Коэффициент ослабления лучей взвешенными в топочной среде частицами
        res = 1E4 * 0.75 / math.pow(vii + 273.15, 0.6667) * Muzl / (1 + 1.2 * Muzl * s)
        return res

    def K(self, Kg, rn, Kzl_Muzl): # Коэффициент поглощения
        res = Kg * rn + Kzl_Muzl + self.Kk
        return res

    def Bu(self, K, Stsh, p): # Критерий Буггера
        res = K * p * Stsh
        return res

    def at(self, Bu): # Степень черноты
        res = 1 - math.exp(-Bu)
        return res

    def HGAZ(self, v, alfa, vc_rec, H_rec): # Энтальпия газа
        cgaz = cgaz_method(self.tip, self.Wp)
        H = HGAZ(v, self.Vg0, alfa, self.Vair0, cgaz)
        if vc_rec != 0:
            n = 0
            eps = 0.000001
            v_out_rec = v + 50
            H_out_rec = HGAZ(v_out_rec, self.Vg0, alfa, self.Vair0, cgaz)
            H = H_out_rec + H_rec
            vc = H_out_rec / v_out_rec + vc_rec
            v_prov = H / vc
            while math.fabs(v_prov - v) > eps:
                H_out_rec_eps = HGAZ(v_out_rec + eps, self.Vg0, alfa, self.Vair0, cgaz)
                H_eps = H_out_rec_eps + H_rec
                vc_eps = H_out_rec / v_out_rec + vc_rec
                v_prov_eps = H_eps / vc_eps
                v_proizv = ((v_prov_eps - v) - (v_prov - v)) / eps
                v_out_rec = v_out_rec - (v_prov - v) / v_proizv

                H_out_rec = HGAZ(v_out_rec, self.Vg0, alfa, self.Vair0, cgaz)
                H = H_out_rec + H_rec
                vc = H_out_rec / v_out_rec + vc_rec
                v_prov = H / vc
                n += 1
                if n > 1000:
                    break
        return H

    def vgaz(self, H, alfa, vc_rec, H_rec):
        cgaz = cgaz_method(self.tip, self.Wp)
        v = vgaz(H - H_rec, self.Vg0, alfa, self.Vair0, cgaz)
        if vc_rec != 0:
            v = H / ((H - H_rec) / v + vc_rec)
        return v

    def HAIR(self, t):
        res = HAIR_method(1, self.Vair0, t)
        return res

    def tAIR(self, H):
        res = tAIR_method(1, self.Vair0, H)
        return res

    def tempnap(self, tipdvizh, vi, ti, vii, tii):
        if tipdvizh == 'Прямоток':
            deltatb = vi - ti
            deltatm = vii - tii
        else: # Противоток
            if ((vi - tii) > (vii - ti)):
                deltatb = vi - tii
                deltatm = vii - ti
            else: # (vi - tii) < (vii - ti)
                deltatb = vii - ti
                deltatm = vi - tii
        temp_nap = (deltatb - deltatm) / math.log(deltatb / deltatm)
        return temp_nap

    def tempnap_average(self, tipdvizh, vi, ti, vii, tii, vpr, tkip, Q1, Q2):
        deltat1 = self.tempnap(tipdvizh, vpr, ti, vii, tkip)
        deltat2 = self.tempnap(tipdvizh, vi, tkip, vpr, tii)
        deltat = (Q1 + Q2) / (Q1 / deltat1 + Q2 / deltat2)
        return deltat

    def wg(self, Vg, vi, vii, fg, Br):
        wg = Br * Vg * ((vi + vii) / 2 + 273) / (fg * 273)
        return wg
