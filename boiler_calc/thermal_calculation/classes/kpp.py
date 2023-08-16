from .abstract_conv_pov import *


class KPP(AbstractConvPov):
    def __init__(self, boiler, name, unknown, stat, tipdvizh, vii, tii, F, delta_P, fg, fi_pp,
            delta_alfa, ksi, n, s1, dn, A, m, gaz_number, steam_number):
        super().__init__(boiler, name, unknown, stat, tipdvizh, vii, tii, F, delta_P, fg, fi_pp,
            delta_alfa, ksi, n, s1, dn, A, m, gaz_number)
        self.type = 'КПП'
        self.steam_number = steam_number
        self.all = all = {
            "Hi" : "Hi",
            "hi" : "hi",
            "Hii" : "Hii",
            "hii" : "hii",
            "F" : "F"
        }
        self.varia = varia = list(set(all.values()) - set(stat) - set(unknown))
        self.unknown_local = unknown_local = list(key for key, value in all.items() if value in unknown)

    ti = property(lambda self: self._AbstractConvPov__ti,
                  lambda self, value: setattr(self, '_AbstractConvPov__ti', value))
    tii = property(lambda self: self._AbstractConvPov__tii,
                  lambda self, value: setattr(self, '_AbstractConvPov__tii', value))
    hi = property(lambda self: self._AbstractConvPov__hi,
                  lambda self, value: setattr(self, '_AbstractConvPov__hi', value))
    hii = property(lambda self: self._AbstractConvPov__hii,
                  lambda self, value: setattr(self, '_AbstractConvPov__hii', value))
    Pi = property(lambda self: self._AbstractConvPov__Pi,
                  lambda self, value: setattr(self, '_AbstractConvPov__Pi', value))
    Pii = property(lambda self: self._AbstractConvPov__Pii,
                   lambda self, value: setattr(self, '_AbstractConvPov__Pii', value))
    Di = property(lambda self: self._AbstractConvPov__Di,
                  lambda self, value: setattr(self, '_AbstractConvPov__Di', value))
    Dii = property(lambda self: self._AbstractConvPov__Dii,
                   lambda self, value: setattr(self, '_AbstractConvPov__Dii', value))

    def poisk_korney(self):
        super().poisk_korney()

