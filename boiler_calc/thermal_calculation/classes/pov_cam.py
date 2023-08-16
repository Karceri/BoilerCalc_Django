

class Pov_cam:
    def __init__(self, boiler, name, gaz_number, unknown, stat, Vpk):
        self.vi = 1
        self.vii = 1
        self.Qlvh = 1
        self.Qlvyh = 1
        self.Qb = 0
        self.alfai = 1
        self.alfaii = 1
        self.Bi = 1
        self.Bii = 1
        self.Hii = 1
        self.Hi = 1
        self.type = 'Поворотная камера'
        #####################
        self.__boiler = boiler
        self.name = name
        self.gaz_number = gaz_number
        self.unknown = unknown
        self.stat = stat
        self.Vpk = Vpk
        self.all = ['Hi', 'Hii']
        self.varia = list(set(self.all) - set(self.unknown) - set(self.stat))

    def poisk_korney(self):
        boiler = self.__boiler
        self.vii =  self.vi
        self.Hii = self.Hi
        self.Qlvyh = self.Qlvh
        self.alfaii= self.alfai
        self.Bii = self.Bi
        boiler.v_pk = self.vii
        boiler.Vpk = self.Vpk
