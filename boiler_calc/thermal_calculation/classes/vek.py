from .abstract_conv_pov import *


class VEK(AbstractConvPov):
    def __init__(self, boiler, name, unknown, stat, tipdvizh, vii, tii, F, delta_P, fg, fi_pp,
            delta_alfa, ksi, n, s1, dn, A, m, gaz_number, water_number):
        super().__init__(boiler, name, unknown, stat, tipdvizh, vii, tii, F, delta_P, fg, fi_pp,
            delta_alfa, ksi, n, s1, dn, A, m, gaz_number)
        self.type = 'ВЭК'
        self.water_number = water_number
        self.all = all = {
            "Hi" : "Hi",
            "hi" : "hi_water",
            "Hii" : "Hii",
            "hii" : "hii_water",
            "F" : "F"
        }
        self.varia = varia = list(set(all.values()) - set(stat) - set(unknown))
        self.unknown_local = unknown_local = list(key for key, value in all.items() if value in unknown)

    ti_water = property(lambda self: self._AbstractConvPov__ti,
                  lambda self, value: setattr(self, '_AbstractConvPov__ti', value))
    tii_water = property(lambda self: self._AbstractConvPov__tii,
                   lambda self, value: setattr(self, '_AbstractConvPov__tii', value))
    hi_water = property(lambda self: self._AbstractConvPov__hi,
                  lambda self, value: setattr(self, '_AbstractConvPov__hi', value))
    hii_water = property(lambda self: self._AbstractConvPov__hii,
                   lambda self, value: setattr(self, '_AbstractConvPov__hii', value))
    Pi_water = property(lambda self: self._AbstractConvPov__Pi,
                  lambda self, value: setattr(self, '_AbstractConvPov__Pi', value))
    Pii_water = property(lambda self: self._AbstractConvPov__Pii,
                   lambda self, value: setattr(self, '_AbstractConvPov__Pii', value))
    Gi = property(lambda self: self._AbstractConvPov__Di,
                  lambda self, value: setattr(self, '_AbstractConvPov__Di', value))
    Gii = property(lambda self: self._AbstractConvPov__Dii,
                   lambda self, value: setattr(self, '_AbstractConvPov__Dii', value))

    def poisk_korney(self):
        super().poisk_korney()

