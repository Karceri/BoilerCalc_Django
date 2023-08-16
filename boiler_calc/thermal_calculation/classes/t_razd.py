

class T_razd:
    def __init__(self, boiler, type, name, unknown, stat, elem_number, rD_main, rD_alter,
                 stream_number, stream_number_alter):
        self.vi = 1
        self.ti = 1
        self.ti_air = 1
        self.ti_water = 1
        self.vii = 1
        self.tii = 1
        self.tii_air = 1
        self.tii_water = 1
        self.Pi = 1
        self.Pii = 1
        self.Qlvh = 1
        self.Qlvyh_main = 1
        self.Qlvyh_alter = 1
        self.Di = 1
        self.Dii_main = 1
        self.Dii_alter = 1
        self.Gi = 1
        self.Gii_main = 1
        self.Gii_alter = 1
        self.alfai = 1
        self.alfaii = 1
        self.bettagvi = 1
        self.bettagvii = 1
        self.Pi_water = 1
        self.Pii_water = 1
        self.Bi = 1
        self.Bii_main = 1
        self.Bii_alter = 1
        self.Bi_air = 1
        self.Bii_air_main = 1
        self.Bii_air_alter = 1
        self.Hi = 1
        self.hi = 1
        self.Hi_air = 1
        self.hi_water = 1
        self.Hii = 1
        self.hii = 1
        self.Hii_air = 1
        self.hii_water = 1
        #######################
        self.__boiler = boiler
        self.type = type
        self.name = name
        self.unknown = unknown
        self.stat = stat
        self.steam_number = elem_number if type == 'steam' else 0
        self.water_number = elem_number if type == 'water' else 0
        self.air_number = elem_number if type == 'air' else 0
        self.gaz_number = elem_number if type == 'gaz' else 0
        self.rD_main = rD_main
        self.rD_alter = rD_alter
        self.stream_number = stream_number
        self.stream_number_alter = stream_number_alter
        match type:
            case 'steam':
                all = ['hi', 'hii']
            case 'water':
                all = ['hi_water', 'hii_water']
            case 'air':
                all = ['hi_air', 'hii_air']
            case 'gaz':
                all = ['Hi', 'Hii']
            case _:
                all = []
        self.varia = list(set(all) - set(unknown) - set(stat))
        self.main_trakt = True

    @property
    def Dii(self):
        if self.main_trakt == True:
            return self.Dii_main
        else:
            return self.Dii_alter

    @Dii.setter
    def Dii(self, value):
        if self.main_trakt == True:
            self.Dii_main = value
        else:
            self.Dii_alter = value

    @property
    def Gii(self):
        if self.main_trakt == True:
            return self.Gii_main
        else:
            return self.Gii_alter

    @Gii.setter
    def Gii(self, value):
        if self.main_trakt == True:
            self.Gii_main = value
        else:
            self.Gii_alter = value

    @property
    def Qlvyh(self):
        if self.main_trakt == True:
            return self.Qlvyh_main
        else:
            return self.Qlvyh_alter

    @property
    def Bii(self):
        if self.main_trakt == True:
            return self.Bii_main
        else:
            return self.Bii_alter

    @Bii.setter
    def Bii(self, value):
        if self.main_trakt == True:
            self.Bii_main = value
        else:
            self.Bii_alter = value

    @property
    def Bii_air(self):
        if self.main_trakt == True:
            return self.Bii_air_main
        else:
            return self.Bii_air_alter

    @Bii_air.setter
    def Bii_air(self, value):
        if self.main_trakt == True:
            self.Bii_air_main = value
        else:
            self.Bii_air_alter = value

    def __raschet_steam(self):
        self.Dii_main = self.Di * self.rD_main
        self.Dii_alter = self.Di * self.rD_alter
        self.Pii = self.Pi
        self.tii = self.ti
        self.hii = self.hi

    def __raschet_water(self):
        self.Gii_main = self.Gi * self.rD_main
        self.Gii_alter = self.Gi * self.rD_alter
        self.Pii_water = self.Pi_water
        self.tii_water = self.ti_water
        self.hii_water = self.hi_water

    def __raschet_air(self):
        self.Bii_air_main = self.Bi_air * self.rD_main
        self.Bii_air_alter = self.Bi_air * self.rD_alter
        self.tii_air = self.ti_air
        self.Hii_air = self.Hi_air
        self.bettagvii = self.bettagvi

    def __raschet_gaz(self):
        self.Bii_main = self.Bi * self.rD_main
        self.Bii_alter = self.Bi * self.rD_alter
        self.alfaii = self.alfai
        self.vii = self.vi
        self.Hii = self.Hi
        self.Qlvyh_main = self.Qlvh * self.rD_main
        self.Qlvyh_alter = self.Qlvh * self.rD_alter

    def poisk_korney(self):
        match self.type:
            case 'steam':
                self.__raschet_steam()
            case 'water':
                self.__raschet_water()
            case 'air':
                self.__raschet_air()
            case 'gaz':
                self.__raschet_gaz()
            case _:
                pass
