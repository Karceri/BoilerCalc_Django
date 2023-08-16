import win32com.client, os, pythoncom, shutil, math, pdb
from win32com.client import constants
from .boiler import *
from .kpp import *
from .vek import *
from .closing_points import *
from .cvd import *
from .calorifer import *
from .drum import *
from .pov_cam import *
from .rpp import *
from .shirm_povs import *
from .steam_condenser import *
from .t_razd import *
from .t_sm import *
from .topka import *
from .umensh_temp import *
from .vprysk import *
from .vzp import *
from . import recognition_entry


file_path = r"C:\Users\Konstantin\Desktop\ТПЕ-216 — заводской.vsdm"
fuel = 'Ирша-Бородинское 2Б, Р'
mark = ''; tip = ''
Wr = 0; Ar = 0; Sr = 0; Cr = 0; Hr = 0; Nr = 0; Or = 0; vg = 0; Qnr = 0; klo = 0
t1 = 0; t2 = 0; t3 = 0
Dnom = 186.11; aun = 0.95; q3 = 0; q4 = 0.5
eps = 0.001

single_zone_topkas = []
drums = []
pov_cams = []
rpps = []
shirm_povs = []
kpps = []
veks = []
vzps = []
vprysks = []
closing_points = []
t_razds = []
t_sms = []
steam_condensers = []
cvds = []
calorifers = []
umensh_temps = []

all_elems = []
#elem_par = []
#elem_water = []
#elem_air = []
#elem_gaz = []


def read_visio():
    appVisio = win32com.client.Dispatch("Visio.Application", pythoncom.CoInitialize())
    doc = appVisio.Documents.Add(file_path)
    calculate(appVisio)
    #q = steamTable.h_pt(140, 815)
    #for shape in appVisio.ActivePage.Shapes:


def copy_visio():
    destinationFilePath = r"C:\Users\Konstantin\Documents\PycharmProjects\BoilerCalc_Django\boiler_calc\media\data.vsdm"
    shutil.copy2(file_path, destinationFilePath)
    appVisio = win32com.client.Dispatch("Visio.Application", pythoncom.CoInitialize())
    doc = appVisio.Documents.Add(destinationFilePath)
    appVisio.ActivePage.PageSheet.DeleteSection(243)
    appVisio.ActivePage.PageSheet.DeleteSection(242)

    for shape in appVisio.ActivePage.Shapes:
        shape.DeleteSection(243)
        shape.DeleteSection(242)
        found_elem = next((elem for elem in all_elems if elem.name == shape.Name), None)
        if found_elem != None:
            data(found_elem, shape)
    doc.SaveAs(destinationFilePath)
    appVisio.Visible = 1


def fuel_method():
    global mark, tip, Wr, Ar, Sr, Cr, Hr, Nr, Or, vg, Qnr, klo, t1, t2, t3
    if fuel == 'Ирша-Бородинское 2Б, Р':
        mark = "Бурый"; tip = "solid"
        Wr = 33; Ar = 7.4; Sr = 0.2; Cr = 42.6; Hr = 3; Nr = 0.6; Or = 13.2; vg = 47; Qnr = 15280; klo = 1.15
        t1 = 1180; t2 = 1210; t3 = 1230
    elif fuel == 'Назаровское 2Б, Р':
        mark = "Бурый"; tip = "solid"
        Wr = 39; Ar = 7.9; Sr = 0.4; Cr = 37.2; Hr = 2.5; Nr = 0.5; Or = 12.5; vg = 47; Qnr = 12850; klo = 1
        t1 = 1200; t2 = 1220; t3 = 1240
    elif fuel == 'Березовское 2Б, Р':
        mark = "Бурый"; tip = "solid"
        Wr = 33; Ar = 4.7; Sr = 0.2; Cr = 44.2; Hr = 3.1; Nr = 0.4; Or = 14.4; vg = 48; Qnr = 15660; klo = 1.3
        t1 = 1270; t2 = 1290; t3 = 1310
    elif fuel == 'Челябинский 3Б, Р':
        mark = "Бурый"; tip = "solid"
        Wr = 17; Ar = 35.7; Sr = 0.8; Cr = 33.6; Hr = 2.5; Nr = 0.9; Or = 9.5; vg = 44; Qnr = 12560; klo = 1.3
        t1 = 1180; t2 = 1370; t3 = 1450
    elif fuel == 'Кузнецкий Г, Р, СШ':
        mark = "Каменный"; tip = "solid"
        Wr = 8.5; Ar = 16.9; Sr = 0.4; Cr = 60.1; Hr = 4.2; Nr = 2.0; Or = 7.9; vg = 39.5; Qnr = 23570; klo = 1.2
        t1 = 1170; t2 = 1300; t3 = 1390


def data(elem_trakt, shape):
    name = elem_trakt.name
    type = elem_trakt.type
    if type == 'КПП':
        item = next((elem for elem in kpps if elem.name == name), None)
        if item != None:
            recognition_entry.output_data(item, shape)
    else:
        pass


def calculate(appVisio):
    fuel_method()
    boiler = Boiler(mark, tip, Wr, Ar, Sr, Cr, Hr, Nr, Or, vg, Qnr, klo, t1, t2, t3, Dnom, aun, q3, q4)
    count_stream_steam = appVisio.ActivePage.PageSheet.Cells("Prop.num_stream_steam").ResultInt(32, 0)
    count_stream_water = appVisio.ActivePage.PageSheet.Cells("Prop.num_stream_water").ResultInt(32, 0)
    count_stream_air = appVisio.ActivePage.PageSheet.Cells("Prop.num_stream_air").ResultInt(32, 0)
    count_stream_gaz = appVisio.ActivePage.PageSheet.Cells("Prop.num_stream_gaz").ResultInt(32, 0)

    #elem_par.extend([] for e in range(count_stream_steam))
    #elem_water.extend([] for e in range(count_stream_water))
    #elem_air.extend([] for e in range(count_stream_air))
    #elem_gaz.extend([] for e in range(count_stream_gaz))

    global elem_par, elem_water, elem_air, elem_gaz

    elem_par = [[] for e in range(count_stream_steam)]
    elem_gaz = [[] for e in range(count_stream_gaz)]
    elem_water = [[] for e in range(count_stream_water)]
    elem_air = [[] for e in range(count_stream_air)]

    numP = [0 for e in range(count_stream_steam)]
    numG = [0 for e in range(count_stream_gaz)]
    numW = [0 for e in range(count_stream_water)]
    numA = [0 for e in range(count_stream_air)]

    for shape in appVisio.ActivePage.Shapes:
        if shape.CellExists('Prop.class', 0) == -1:
            match shape.Cells('Prop.class').ResultStr(231):
                case 'КПП':
                    recognition_entry.RaspoznKPP(shape, boiler, elem_par, elem_gaz, kpps, all_elems)
                case 'ВЭК':
                    recognition_entry.RaspoznVEK(shape, boiler, elem_water, elem_gaz, veks, all_elems)
                case 'ШирмПов':
                    recognition_entry.RaspoznShirmPov(shape, boiler, elem_par, elem_gaz, shirm_povs, all_elems)
                case 'РПП':
                    recognition_entry.RaspoznRPP(shape, boiler, elem_par, rpps, all_elems)
                case 'ВЗП':
                    recognition_entry.RaspoznVZP(shape, boiler, elem_air, elem_gaz, vzps, all_elems)
                case 'ЗамыкающаяТочка':
                    recognition_entry.RaspoznClosingPoint(shape, boiler, elem_air, elem_gaz, elem_water,
                                                          elem_par, closing_points, all_elems)
                case 'Впрыск':
                    recognition_entry.RaspoznVprysk(shape, boiler, elem_par, vprysks, all_elems)
                case 'Барабан':
                    recognition_entry.RaspoznDrum(shape, boiler, elem_par, elem_water, drums, all_elems)
                case 'Топка':
                    recognition_entry.RaspoznTopka(shape, boiler, elem_air, elem_gaz, single_zone_topkas, all_elems)
                case 'ПоворотнаяКамера':
                    recognition_entry.RaspoznPovCam(shape, boiler, elem_gaz, pov_cams, all_elems)
                case 'ТочкаРазделения':
                    recognition_entry.RaspoznTRazd(shape, boiler, elem_air, elem_gaz, elem_water, elem_par,
                                                   t_razds, all_elems)
                case 'ТочкаСмешения':
                    recognition_entry.RaspoznTSm(shape, boiler, elem_air, elem_gaz, elem_water, elem_par,
                                                 t_sms, all_elems)
                case 'КонденсаторПара':
                    recognition_entry.RaspoznSteamCondencer(shape, boiler, elem_par, elem_water,
                                                            steam_condensers, all_elems)
                case 'ЦВД':
                    recognition_entry.RaspoznCVD(shape, boiler, elem_par, cvds, all_elems)
                case 'Калорифер':
                    recognition_entry.RaspoznCalorifer(shape, boiler, elem_air, calorifers, all_elems)
                case 'УменьшТемпГаза':
                    recognition_entry.RaspoznUmenshTemp(shape, boiler, elem_gaz, umensh_temps, all_elems)
                case _:
                    pass
    usl_vii = True
    usl_tii = True
    usl_tii_water = True
    usl_tii_air = True

    for i in range(len(elem_par)):
        item_vprs = [e for e in vprysks if e.stream_number_alter == i + 1]
        for item in item_vprs:
            item.main_trakt = False
        items = [e for e in t_sms if e.stream_number_alter == i + 1]
        for item in items:
            item.main_trakt = False
        elem_par[i] = sorted(elem_par[i], key=lambda o: o.steam_number)
        numP[i] = len(elem_par[i])
        for item in items:
            item.main_trakt = True
        for item in item_vprs:
            item.main_trakt = True

    for i in range(len(elem_water)):
        items = [e for e in t_sms if e.stream_number_alter == i + 1]
        for item in items:
            item.main_trakt = False
        elem_water[i] = sorted(elem_water[i], key=lambda o: o.water_number)
        numW[i] = len(elem_water[i])
        for item in items:
            item.main_trakt = True

    for i in range(len(elem_air)):
        items = [e for e in t_sms if e.stream_number_alter == i + 1]
        for item in items:
            item.main_trakt = False
        elem_air[i] = sorted(elem_air[i], key=lambda o: o.air_number)
        numA[i] = len(elem_air[i])
        for item in items:
            item.main_trakt = True

    for i in range(len(elem_gaz)):
        items = [e for e in t_sms if e.stream_number_alter == i + 1]
        for item in items:
            item.main_trakt = False
        items_topka = [e for e in single_zone_topkas if e.stream_number_alter == i + 1]
        for item in items_topka:
            item.main_trakt = False
        elem_gaz[i] = sorted(elem_gaz[i], key=lambda o: o.gaz_number)
        numG[i] = len(elem_gaz[i])
        for item in items:
            item.main_trakt = True
        for item in items_topka:
            item.main_trakt = True

    n = 0
    vii_prediter = [[]] * len(elem_gaz)
    for i in range(len(elem_gaz)):
        vii_prediter[i] = [None] * numG[i]
    tii_prediter = [[]] * len(elem_par)
    for i in range(len(elem_par)):
        tii_prediter[i] = [None] * numP[i]
    tii_water_prediter = [[]] * len(elem_water)
    for i in range(len(elem_water)):
        tii_water_prediter[i] = [None] * numW[i]
    tii_air_prediter = [[]] * len(elem_air)
    for i in range(len(elem_air)):
        tii_air_prediter[i] = [None] * numA[i]

    while usl_vii or usl_tii or usl_tii_water or usl_tii_air or n <= 2:
        boiler.poisk_korney()
        for item in elem_par:
            iter_par(item)

        for i in range(len(elem_par)):
            items = [e for e in cvds if e.stream_number_alter == i + 1]
            for item in items:
                item.main_trakt = False
            for j in range(numP[i]):
                tii_prediter[i][j] = elem_par[i][j].tii
            for item in items:
                item.main_trakt = True

        for item in elem_water:
            iter_water(item)

        for i in range(len(elem_water)):
            for j in range(numW[i]):
                tii_water_prediter[i][j] = elem_water[i][j].tii_water

        for item in elem_air:
            iter_air(item)

        for i in range(len(elem_air)):
            for j in range(numA[i]):
                tii_air_prediter[i][j] = elem_air[i][j].tii_air

        for item in elem_gaz:
            iter_gaz(item)

        for i in range(len(elem_gaz)):
            for j in range(numG[i]):
                vii_prediter[i][j] = elem_gaz[i][j].vii

        every = 0
        for i in range(len(elem_par)):
            items = [e for e in cvds if e.stream_number_alter == i + 1]
            for item in items:
                item.main_trakt = False
            for j in range(numP[i]):
                nan = False
                if math.isnan(elem_par[i][j].tii) and math.isnan(tii_prediter[i][j]):
                    nan = True
                if math.fabs(elem_par[i][j].tii - tii_prediter[i][j]) < eps or nan:
                    every += 1
            ad = sum(numP)
            usl_tii = False if every == sum(numP) else True
            for item in items:
                item.main_trakt = True
        every = 0
        for i in range(len(elem_water)):
            for j in range(numW[i]):
                nan = False
                if math.isnan(elem_water[i][j].tii_water) and math.isnan(tii_water_prediter[i][j]):
                    nan = True
                if math.fabs(elem_water[i][j].tii_water - tii_water_prediter[i][j]) < eps or nan:
                    every += 1
            usl_tii_water = False if every == sum(numW) else True
        every = 0
        for i in range(len(elem_air)):
            for j in range(numA[i]):
                nan = False
                if math.isnan(elem_air[i][j].tii_air) and math.isnan(tii_air_prediter[i][j]):
                    nan = True
                if math.fabs(elem_air[i][j].tii_air - tii_air_prediter[i][j]) < eps or nan:
                    every += 1
            usl_tii_air = False if every == sum(numA) else True
        every = 0
        for i in range(len(elem_gaz)):
            for j in range(numG[i]):
                nan = False
                if math.isnan(elem_gaz[i][j].vii) and math.isnan(vii_prediter[i][j]):
                    nan = True
                if math.fabs(elem_gaz[i][j].vii - vii_prediter[i][j]) < eps or nan:
                    every += 1
            usl_vii = False if every == sum(numG) else True
        n += 1
    boiler.poisk_korney()
    boiler.n_iter = n


def iter_par(elem_trakt):
    ind = elem_par.index(elem_trakt)
    new_t_razds = [e for e in t_razds if e.stream_number_alter == ind + 1]
    for item in new_t_razds:
        item.main_trakt = False
    new_t_sms = [e for e in t_sms if e.stream_number_alter == ind + 1]
    for item in new_t_sms:
        item.main_trakt = False
    new_t_cvds = [e for e in cvds if e.stream_number_alter == ind + 1]
    for item in new_t_cvds:
        item.main_trakt = False
    new_t_vprysks = [e for e in vprysks if e.stream_number_alter == ind + 1]
    for item in new_t_vprysks:
        item.main_trakt = False
    for i in range(len(elem_trakt)):
        varia = elem_trakt[i].varia
        for j in range(len(varia)):
            match varia[j]:
                case 'hi':
                    elem_trakt[i].ti = elem_trakt[i - 1].tii if i != 0 else elem_trakt[i].ti
                    elem_trakt[i].hi = elem_trakt[i - 1].hii if i != 0 else elem_trakt[i].hi
                case 'hii':
                    elem_trakt[i].tii = elem_trakt[i + 1].ti if i != len(elem_trakt) - 1 else elem_trakt[i].tii
                    elem_trakt[i].hii = elem_trakt[i + 1].hi if i != len(elem_trakt) - 1 else elem_trakt[i].hii
                case _:
                    pass
        if i != 0:
            elem_trakt[i].Pi = elem_trakt[i - 1].Pii
            elem_trakt[i].Di = elem_trakt[i - 1].Dii
        elem_trakt[i].poisk_korney()
    for item in new_t_razds:
        item.main_trakt = True
    for item in new_t_sms:
        item.main_trakt = True
    for item in new_t_cvds:
        item.main_trakt = True
    for item in new_t_vprysks:
        item.main_trakt = True


def iter_water(elem_trakt):
    ind = elem_water.index(elem_trakt)
    new_t_razds = [e for e in t_razds if e.stream_number_alter == ind + 1]
    for item in new_t_razds:
        item.main_trakt = False
    new_t_sms = [e for e in t_sms if e.stream_number_alter == ind + 1]
    for item in new_t_sms:
        item.main_trakt = False
    for i in range(len(elem_trakt)):
        varia = elem_trakt[i].varia
        for j in range(len(varia)):
            match varia[j]:
                case 'hi_water':
                    elem_trakt[i].ti_water = elem_trakt[i - 1].tii_water if i != 0 else elem_trakt[i].ti_water
                    elem_trakt[i].hi_water = elem_trakt[i - 1].hii_water if i != 0 else elem_trakt[i].hi_water
                case 'hii_water':
                    elem_trakt[i].tii_water = elem_trakt[i + 1].ti_water if i != len(elem_trakt) - 1 \
                        else elem_trakt[i].tii_water
                    elem_trakt[i].hii_water = elem_trakt[i + 1].hi_water if i != len(elem_trakt) - 1 \
                        else elem_trakt[i].hii_water
                case _:
                    pass
        if i != 0:
            elem_trakt[i].Pi_water = elem_trakt[i - 1].Pii_water
            elem_trakt[i].Gi = elem_trakt[i - 1].Gii
        elem_trakt[i].poisk_korney()
    for item in new_t_razds:
        item.main_trakt = True
    for item in new_t_sms:
        item.main_trakt = True


def iter_air(elem_trakt):
    ind = elem_air.index(elem_trakt)
    new_t_razds = [e for e in t_razds if e.stream_number_alter == ind + 1]
    for item in new_t_razds:
        item.main_trakt = False
    new_t_sms = [e for e in t_sms if e.stream_number_alter == ind + 1]
    for item in new_t_sms:
        item.main_trakt = False
    for i in range(len(elem_trakt)):
        varia = elem_trakt[i].varia
        for j in range(len(varia)):
            match varia[j]:
                case 'hi_air':
                    elem_trakt[i].ti_air = elem_trakt[i - 1].tii_air if i != 0 else elem_trakt[i].ti_air
                    elem_trakt[i].Hi_air = elem_trakt[i - 1].Hii_air if i != 0 else elem_trakt[i].Hi_air
                case 'hii_air':
                    elem_trakt[i].tii_air = elem_trakt[i + 1].ti_air if i != len(elem_trakt) - 1 \
                        else elem_trakt[i].tii_air
                    elem_trakt[i].Hii_air = elem_trakt[i + 1].Hi_air if i != len(elem_trakt) - 1 \
                        else elem_trakt[i].Hii_air
                case _:
                    pass
        if i != len(elem_trakt) - 1:
            pass
        if i != 0:
            elem_trakt[i].bettagvi = elem_trakt[i - 1].bettagvii
            elem_trakt[i].Bi_air = elem_trakt[i - 1].Bii_air
        elem_trakt[i].poisk_korney()
    for item in new_t_razds:
        item.main_trakt = True
    for item in new_t_sms:
        item.main_trakt = True


def iter_gaz(elem_trakt):
    ind = elem_gaz.index(elem_trakt)
    new_t_razds = [e for e in t_razds if e.stream_number_alter == ind + 1]
    for item in new_t_razds:
        item.main_trakt = False
    new_t_sms = [e for e in t_sms if e.stream_number_alter == ind + 1]
    for item in new_t_sms:
        item.main_trakt = False
    items_topka = [e for e in single_zone_topkas if e.stream_number_alter == ind + 1]
    for item in items_topka:
        item.main_trakt = False
    for i in range(len(elem_trakt)):
        varia = elem_trakt[i].varia
        for j in range(len(varia)):
            match varia[j]:
                case 'Hi':
                    elem_trakt[i].vi = elem_trakt[i - 1].vii if i != 0 else elem_trakt[i].vi
                    elem_trakt[i].Hi = elem_trakt[i - 1].Hii if i != 0 else elem_trakt[i].Hi
                case 'Hii':
                    elem_trakt[i].vii = elem_trakt[i + 1].vi if i != len(elem_trakt) - 1 \
                        else elem_trakt[i].vii
                    elem_trakt[i].Hii = elem_trakt[i + 1].Hi if i != len(elem_trakt) - 1 \
                        else elem_trakt[i].Hii
                case _:
                    pass
        if i != 0:
            elem_trakt[i].Bi = elem_trakt[i - 1].Bii
            elem_trakt[i].Qlvh = elem_trakt[i - 1].Qlvyh
            elem_trakt[i].alfai = elem_trakt[i - 1].alfaii
        elem_trakt[i].poisk_korney()
    for item in new_t_razds:
        item.main_trakt = True
    for item in new_t_sms:
        item.main_trakt = True
    for item in items_topka:
        item.main_trakt = True









