

class Calorifer:
    def __init__(self, boiler, type, name, unknown, stat, tii, air_number):
        self.Bi_air = 1
        self.Bii_air = 1
        self.bettagvi = 1
        self.bettagvii = 1
        self.Hi_air = 1
        self.Hii_air = 1
        self.Qvvn = 0
        self.ti_air = 1
        self.Qb = 0
        ######################
        self.__boiler = boiler
        self.type = type
        self.name = name
        self.unknown = unknown
        self.stat = stat
        self.tii_air = tii
        self.air_number = air_number
        self.all = ['hi_air', 'hii_air']
        self.varia = list(set(self.all) - set(stat) - set(unknown))

    def __Qvvn_method(self):
        return (self.Hii_air - self.Hi_air) * self.bettagvii

    def poisk_korney(self):
        self.bettagvii = self.bettagvi
        self.Bii_air = self.Bi_air
        self.Hii_air = self.__boiler.HAIR(self.tii_air)
        self.Qvvn = self.__Qvvn_method()
        self.__boiler.Qvvn = self.Qvvn

