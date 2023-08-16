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


def output_data(elem, shape):
    ti = round(elem.ti, 3)
    hi = round(elem.hi, 3)
    tii = round(elem.tii, 3)
    hii = round(elem.hii, 3)
    vi = round(elem.vi, 3)
    vii = round(elem.vii, 3)
    Hi = round(elem.Hi, 3)
    Hii = round(elem.Hii, 3)
    F = round(elem.F, 3)
    k = round(elem.k, 3)
    deltat = round(elem.deltat, 3)
    wg = round(elem.wg, 3)
    Pi = round(elem.Pi, 3)
    Pii = round(elem.Pii, 3)
    Vg = round(elem.Vg, 3)
    Qb = round(elem.Qb / elem.Bii, 3)
    Br = round(elem.Bii, 3)
    D = round(elem.Dii, 3)

    section = shape.AddSection(243)
    shape.AddNamedRow(section, "ti", 0)
    shape.Cells("Prop.ti.Label").Formula = "\"Температура пара на входе в ПП t' °C\""
    shape.Cells("Prop.ti").ResultIU = ti
    shape.AddNamedRow(section, "tii", 0)
    shape.Cells("Prop.tii.Label").Formula = "\"Температура пара на выходе из ПП t'' °C\""
    shape.Cells("Prop.tii").ResultIU = tii
    shape.AddNamedRow(section, "hi", 0)
    shape.Cells("Prop.hi.Label").Formula = "\"Энтальпия пара на входе в ПП h' кДж/кг\""
    shape.Cells("Prop.hi").ResultIU = hi
    shape.AddNamedRow(section, "hii", 0)
    shape.Cells("Prop.hii.Label").Formula = "\"Энтальпия пара на выходе из ПП h'' °C\""
    shape.Cells("Prop.hii").ResultIU = hii
    shape.AddNamedRow(section, "vi", 0)
    shape.Cells("Prop.vi.Label").Formula = "\"Температура газа на входе в ПП v' °C\""
    shape.Cells("Prop.vi").ResultIU = vi
    shape.AddNamedRow(section, "vii", 0)
    shape.Cells("Prop.vii.Label").Formula = "\"Температура газа на входе в ПП v'' °C\""
    shape.Cells("Prop.vii").ResultIU = vii
    shape.AddNamedRow(section, "Higaz", 0)
    shape.Cells("Prop.Higaz.Label").Formula = "\"Энтальпия газа на входе в ПП H' кДж/кг\""
    shape.Cells("Prop.Higaz").ResultIU = Hi
    shape.AddNamedRow(section, "Hiigaz", 0)
    shape.Cells("Prop.Hiigaz.Label").Formula = "\"Энтальпия газа на выходе из ПП H'' кДж/кг\""
    shape.Cells("Prop.Hiigaz").ResultIU = Hii
    shape.AddNamedRow(section, "F", 0)
    shape.Cells("Prop.F.Label").Formula = "\"Площадь ПП F, м²\""
    shape.Cells("Prop.F").ResultIU = F
    shape.AddNamedRow(section, "k", 0)
    shape.Cells("Prop.k.Label").Formula = "\"Коэффициент теплопередачи K, Вт/м²*K\""
    shape.Cells("Prop.k").ResultIU = k
    shape.AddNamedRow(section, "deltat", 0)
    shape.Cells("Prop.deltat.Label").Formula = "\"Температурный напор Δt, K\""
    shape.Cells("Prop.deltat").ResultIU = deltat
    shape.AddNamedRow(section, "wg", 0)
    shape.Cells("Prop.wg.Label").Formula = "\"Скорость газов wg, м/с\""
    shape.Cells("Prop.wg").ResultIU = wg
    shape.AddNamedRow(section, "Vg", 0)
    shape.Cells("Prop.Vg.Label").Formula = "\"Объем газов Vg, м/с\""
    shape.Cells("Prop.Vg").ResultIU = Vg
    shape.AddNamedRow(section, "Pi", 0)
    shape.Cells("Prop.Pi.Label").Formula = "\"Давление на входе в ПП Pi, бар\""
    shape.Cells("Prop.Pi").ResultIU = Pi
    shape.AddNamedRow(section, "Pii", 0)
    shape.Cells("Prop.Pii.Label").Formula = "\"Давление на выходе из ПП Pii, бар\""
    shape.Cells("Prop.Pii").ResultIU = Pii
    shape.AddNamedRow(section, "Qb", 0)
    shape.Cells("Prop.Qb.Label").Formula = "\"Qb балансовое тепло, кДж/кг\""
    shape.Cells("Prop.Qb").ResultIU = Qb
    shape.AddNamedRow(section, "Br", 0)
    shape.Cells("Prop.Br.Label").Formula = "\"Br расход топлива, кг/с\""
    shape.Cells("Prop.Br").ResultIU = Br
    shape.AddNamedRow(section, "D", 0)
    shape.Cells("Prop.D.Label").Formula = "\"D расход пара, кг/с\""
    shape.Cells("Prop.D").ResultIU = D
    shape.AddNamedRow(section, "Qluch", 0)
    shape.Cells("Prop.Qluch.Label").Formula = "\"Лучистое тепло, кДж/кг\""
    shape.Cells("Prop.Qluch").ResultIU = elem.Qlvh - elem.Qlvyh


def poisk_stat(shape):
    vii = "Hii" if shape.CellExistsU(
        "Prop.svob_vii", 0) == -1 and shape.CellsU("Prop.svob_vii").ResultStr(231) == 'GUARD(1)' else None
    tii = "hii" if shape.CellExistsU(
        "Prop.svob_tii", 0) == -1 and shape.CellsU("Prop.svob_tii").ResultStr(231) == 'GUARD(1)' else None
    tii_water = "hii_water" if shape.CellExistsU(
        "Prop.svob_tii_water", 0) == -1 and shape.CellsU("Prop.svob_tii_water").ResultStr(231) == 'GUARD(1)' else None
    tii_air = "hii_air" if shape.CellExistsU(
        "Prop.svob_tii_air", 0) == -1 and shape.CellsU("Prop.svob_tii_air").ResultStr(231) == 'GUARD(1)' else None
    F = "F" if shape.CellExistsU(
        "Prop.svob_F", 0) == -1 and shape.CellsU("Prop.svob_F").ResultStr(231) == 'GUARD(1)' else None
    stat = [vii, tii, tii_water, tii_air, F]
    stat = list(item for item in stat if item is not None)
    return stat


def poisk_neizv(shape):
    vi = shape.CellsU("Prop.svob_vi").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_vi", 0) == -1 else None
    ti = shape.CellsU("Prop.svob_ti").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_ti", 0) == -1 else None
    ti_water = shape.CellsU("Prop.svob_ti_water").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_ti_water",
                                                                                        0) == -1 else None
    ti_air = shape.CellsU("Prop.svob_ti_air").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_ti_air",
                                                                                        0) == -1 else None
    F = shape.CellsU("Prop.svob_F").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_F", 0) == -1 else None
    vii = shape.CellsU("Prop.svob_vii").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_vii", 0) == -1 else None
    tii = shape.CellsU("Prop.svob_tii").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_tii", 0) == -1 else None
    tii_water = shape.CellsU("Prop.svob_tii_water").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_tii_water",
                                                                                        0) == -1 else None
    tii_air = shape.CellsU("Prop.svob_tii_air").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_tii_air",
                                                                                        0) == -1 else None
    vi_alter = shape.CellsU("Prop.svob_vi_alter").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_vi_alter",
                                                                                      0) == -1 else None
    ti_alter = shape.CellsU("Prop.svob_ti_alter").ResultInt(32, 0) if shape.CellExistsU("Prop.svob_ti_alter",
                                                                                        0) == -1 else None
    ti_water_alter = shape.CellsU("Prop.svob_ti_water_alter").ResultInt(32, 0) if shape.CellExistsU(
                                                                    "Prop.svob_ti_water_alter", 0) == -1 else None
    ti_air_alter = shape.CellsU("Prop.svob_ti_air_alter").ResultInt(32, 0) if shape.CellExistsU(
        "Prop.svob_ti_air_alter", 0) == -1 else None
    collection = {
        'Hi' : vi,
        "hi_water": ti_water,
        "hi_air": ti_air,
        "hi": ti,
        "Hi_alter": vi_alter,
        "hi_water_alter": ti_water_alter,
        "hi_air_alter": ti_air_alter,
        "hi_alter": ti_alter,
        "F": F,
        "Hii": vii,
        "hii_water": tii_water,
        "hii_air": tii_air,
        "hii": tii
    }
    collection = {key : value for key, value in collection.items() if value != -1}
    znach = [key for key, value in collection.items() if value == 0]
    return znach


def RaspoznKPP(shape, boiler, elemPar, elemGaz, kpps, all_elems):
    type = shape.CellsU("Prop.type").ResultStr(231)
    gaz_stream_number = shape.CellsU("Prop.gaz_stream_number").ResultInt(32, 0)
    gaz_number = shape.CellsU("Prop.gaz_number").ResultInt(32, 0)
    name = shape.Name
    tipdvizh = shape.CellsU("Prop.tipdvizh").ResultStr(231)
    vii = shape.CellsU("Prop.znach_vii").ResultIU
    F = shape.CellsU("Prop.znach_F").ResultIU
    delta_P = shape.CellsU("Prop.delta_P").ResultIU
    fg = shape.CellsU("Prop.fg").ResultIU
    fi_pp = shape.CellsU("Prop.fi_ugl").ResultIU
    ksi = shape.CellsU("Prop.ksi").ResultIU
    n = shape.CellsU("Prop.param_n").ResultIU
    s1 = shape.CellsU("Prop.s1").ResultIU
    dn = shape.CellsU("Prop.dn").ResultIU
    A = shape.CellsU("Prop.param_A").ResultIU
    m = shape.CellsU("Prop.param_m").ResultIU
    delta_alfa = shape.CellsU("Prop.delta_alfa").ResultIU
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    tii = shape.CellsU("Prop.znach_tii").ResultIU
    steam_stream_number = shape.CellsU("Prop.steam_stream_number").ResultInt(32, 0)
    steam_number = shape.CellsU("Prop.steam_number").ResultInt(32, 0)
    obj = KPP(boiler, name, unknown, stat, tipdvizh, vii, tii, F, delta_P, fg, fi_pp,
        delta_alfa, ksi, n, s1, dn, A, m, gaz_number, steam_number)
    elemPar[steam_stream_number - 1].append(obj)
    kpps.append(obj)
    elemGaz[gaz_stream_number - 1].append(obj)
    all_elems.append(obj)


def RaspoznVEK(shape, boiler, elemWater, elemGaz, veks, all_elems):
    type = shape.CellsU("Prop.type").ResultStr(231)
    gaz_stream_number = shape.CellsU("Prop.gaz_stream_number").ResultInt(32, 0)
    gaz_number = shape.CellsU("Prop.gaz_number").ResultInt(32, 0)
    name = shape.Name
    tipdvizh = shape.CellsU("Prop.tipdvizh").ResultStr(231)
    vii = shape.CellsU("Prop.znach_vii").ResultIU
    F = shape.CellsU("Prop.znach_F").ResultIU
    delta_P = shape.CellsU("Prop.delta_P").ResultIU
    fg = shape.CellsU("Prop.fg").ResultIU
    fi_pp = shape.CellsU("Prop.fi_ugl").ResultIU
    ksi = shape.CellsU("Prop.ksi").ResultIU
    n = shape.CellsU("Prop.param_n").ResultIU
    s1 = shape.CellsU("Prop.s1").ResultIU
    dn = shape.CellsU("Prop.dn").ResultIU
    A = shape.CellsU("Prop.param_A").ResultIU
    m = shape.CellsU("Prop.param_m").ResultIU
    delta_alfa = shape.CellsU("Prop.delta_alfa").ResultIU
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    tii_water = shape.CellsU("Prop.znach_tii_water").ResultIU
    water_stream_number = shape.CellsU("Prop.water_stream_number").ResultInt(32, 0)
    water_number = shape.CellsU("Prop.water_number").ResultInt(32, 0)
    obj = VEK(boiler, name, unknown, stat, tipdvizh, vii, tii_water, F, delta_P, fg, fi_pp,
        delta_alfa, ksi, n, s1, dn, A, m, gaz_number, water_number)
    elemWater[water_stream_number - 1].append(obj)
    veks.append(obj)
    elemGaz[gaz_stream_number - 1].append(obj)
    all_elems.append(obj)


def RaspoznShirmPov(shape, boiler, elemPar, elemGaz, ShirmPovs, all_elems):
    steam_stream_number = shape.CellsU("Prop.steam_stream_number").ResultInt(32, 0)
    gaz_stream_number = shape.CellsU("Prop.gaz_stream_number").ResultInt(32, 0)
    steam_number = shape.CellsU("Prop.steam_number").ResultInt(32, 0)
    gaz_number = shape.CellsU("Prop.gaz_number").ResultInt(32, 0)
    type = shape.CellsU("Prop.type").ResultStr(231)
    name = shape.Name
    text = shape.Text
    tipdvizh = shape.CellsU("Prop.tipdvizh").ResultStr(231)
    vii = shape.CellsU("Prop.znach_vii").ResultIU
    tii = shape.CellsU("Prop.znach_tii").ResultIU
    F = shape.CellsU("Prop.znach_F").ResultIU
    delta_P = shape.CellsU("Prop.delta_P").ResultIU
    fg = shape.CellsU("Prop.fg").ResultIU
    fi_pp = shape.CellsU("Prop.fi_ugl").ResultIU
    delta_alfa = shape.CellsU("Prop.delta_alfa").ResultIU
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    obj = Shirm_pov(boiler, type, name, text, unknown, stat, tipdvizh, vii, tii, F, delta_P, fg, fi_pp,
              delta_alfa, steam_number, gaz_number)
    elemPar[steam_stream_number - 1].append(obj)
    ShirmPovs.append(obj)
    elemGaz[gaz_stream_number - 1].append(obj)
    all_elems.append(obj)


def RaspoznRPP(shape, boiler, elemPar, rpps, all_elems):
    steam_stream_number = shape.CellsU("Prop.steam_stream_number").ResultInt(32, 0)
    type = shape.CellsU("Prop.class").ResultStr(231)
    name = shape.Name
    tip_rpp = shape.CellsU("Prop.tip_rpp").ResultStr(231)
    Tpk = 0
    ql = 0
    tii = shape.CellsU("Prop.znach_tii").ResultIU
    F = shape.CellsU("Prop.znach_F").ResultIU
    delta_P = shape.CellsU("Prop.delta_P").ResultIU
    nu_v = shape.CellsU("Prop.nu_v").ResultIU
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    steam_number = shape.CellsU("Prop.steam_number").ResultInt(32, 0)
    obj = RPP(boiler, type, name, unknown, stat, tip_rpp, Tpk, ql, tii, F, delta_P, nu_v, steam_number)
    elemPar[steam_stream_number - 1].append(obj)
    rpps.append(obj)
    all_elems.append(obj)


def RaspoznVZP(shape, boiler, elemAir, elemGaz, vzps, all_elems):
    air_stream_number = shape.CellsU("Prop.air_stream_number").ResultInt(32, 0)
    gaz_stream_number = shape.CellsU("Prop.gaz_stream_number").ResultInt(32, 0)
    type = shape.CellsU("Prop.type").ResultStr(231)
    name = shape.Name
    tipdvizh = shape.CellsU("Prop.tipdvizh").ResultStr(231)
    vii = shape.CellsU("Prop.znach_vii").ResultIU
    tii = shape.CellsU("Prop.znach_tii_air").ResultIU
    F = shape.CellsU("Prop.znach_F").ResultIU
    fg = shape.CellsU("Prop.fg").ResultIU
    fi_pp = shape.CellsU("Prop.fi_ugl").ResultIU
    ksi0 = shape.CellsU("Prop.ksi0").ResultIU
    delta_ksi = shape.CellsU("Prop.delta_ksi").ResultIU
    wg = shape.CellsU("Prop.wg").ResultIU
    wp = shape.CellsU("Prop.wp").ResultIU
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    delta_alfa = shape.CellsU("Prop.delta_alfa").ResultIU
    air_number = shape.CellsU("Prop.air_number").ResultInt(32, 0)
    gaz_number = shape.CellsU("Prop.gaz_number").ResultInt(32, 0)
    obj = VZP(boiler, type, name, unknown, stat, tipdvizh, vii, tii, F, fg, fi_pp, delta_alfa,
        ksi0, delta_ksi, wg, wp, air_number, gaz_number)
    elemAir[air_stream_number - 1].append(obj)
    vzps.append(obj)
    elemGaz[gaz_stream_number - 1].append(obj)
    all_elems.append(obj)


def RaspoznClosingPoint(shape, boiler, elemAir, elemGaz, elemWater, elemPar, closing_points, all_elems):
    bettagv = 0
    type = shape.CellsU("Prop.type").ResultStr(231)
    name = shape.Name
    text = shape.Text
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    if "Газ" in type:
        vii = shape.CellsU("Prop.znach_vii").ResultIU if shape.CellExists("Prop.znach_vii", 0) == -1 else 0
        B = shape.CellsU("Prop.Bii").ResultIU if shape.CellExists("Prop.Bii", 0) == -1 else 0
        B_set = shape.CellsU("Prop.Bii_set").ResultStr(231) if shape.CellExists("Prop.Bii_set", 0) == -1 else ""
        gaz_stream_number = shape.CellsU("Prop.gaz_stream_number").ResultInt(32, 0)
        gaz_number = shape.CellsU("Prop.gaz_number").ResultInt(32, 0)
        obj = Closing_point(boiler, type, name, text, vii, unknown, stat, gaz_number, bettagv, 0, B, B_set)
        elemGaz[gaz_stream_number - 1].append(obj)
    elif 'Возд' in type:
        bettagv = shape.CellsU("Prop.betta_gv").ResultIU if shape.CellExists("Prop.betta_gv", 0) == -1 else 0
        tii = shape.CellsU("Prop.znach_tii_air").ResultIU if shape.CellExists("Prop.znach_tii_air", 0) == -1 else 0
        air_stream_number = shape.CellsU("Prop.air_stream_number").ResultInt(32, 0)
        air_number = shape.CellsU("Prop.air_number").ResultInt(32, 0)
        obj = Closing_point(boiler, type, name, text, tii, unknown, stat, air_number, bettagv, 0, 0, "")
        elemAir[air_stream_number - 1].append(obj)
    elif 'Вод' in type:
        tii = shape.CellsU("Prop.znach_tii_water").ResultIU if shape.CellExists("Prop.znach_tii_water", 0) == -1 else 0
        if type == 'НачалоВодТ':
            P = shape.CellsU("Prop.Pii").ResultIU
            G = shape.CellsU("Prop.Gii").ResultIU
        else:
            P = 0
            G = 0
        water_stream_number = shape.CellsU("Prop.water_stream_number").ResultInt(32, 0)
        water_number = shape.CellsU("Prop.water_number").ResultInt(32, 0)
        obj = Closing_point(boiler, type, name, text, tii, unknown, stat, water_number, bettagv, P, G, "")
        elemWater[water_stream_number - 1].append(obj)
    elif 'Пар' in type:
        tii = shape.CellsU("Prop.znach_tii").ResultIU if shape.CellExists("Prop.znach_tii", 0) == -1 else 0
        D = shape.CellsU("Prop.Gii").ResultIU if shape.CellExists("Prop.Gii", 0) == -1 else 0
        P = shape.CellsU("Prop.Pii").ResultIU if shape.CellExists("Prop.Pii", 0) == -1 else 0
        steam_stream_number = shape.CellsU("Prop.steam_stream_number").ResultInt(32, 0)
        steam_number = shape.CellsU("Prop.steam_number").ResultInt(32, 0)
        obj = Closing_point(boiler, type, name, text, tii, unknown, stat, steam_number, bettagv, P, D, "")
        elemPar[steam_stream_number - 1].append(obj)
    else:
        obj = None
    closing_points.append(obj)
    all_elems.append(obj)


def RaspoznVprysk(shape, boiler, elemPar, vprysks, all_elems):
    steam_stream_number = shape.CellsU("Prop.steam_stream_number").ResultInt(32, 0)
    stream_number_alter = shape.CellsU("Prop.stream_number_alter").ResultInt(32, 0)
    type = shape.CellsU("Prop.class").ResultStr(231)
    name = shape.Name
    Gvpr = 5
    tii = shape.CellsU("Prop.znach_tii").ResultIU
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    steam_number = shape.CellsU("Prop.steam_number").ResultInt(32, 0)
    steam_number_alter = shape.CellsU("Prop.steam_number_alter").ResultInt(32, 0)
    obj = Vprysk(boiler, type, name, unknown, stat, tii, Gvpr, steam_number, steam_number_alter,
           steam_stream_number, stream_number_alter)
    vprysks.append(obj)
    elemPar[steam_stream_number - 1].append(obj)
    elemPar[stream_number_alter - 1].append(obj)
    all_elems.append(obj)


def RaspoznDrum(shape, boiler, elemPar, elemWater, drums, all_elems):
    water_stream_number = shape.CellsU("Prop.water_stream_number").ResultInt(32, 0)
    steam_stream_number = shape.CellsU("Prop.steam_stream_number").ResultInt(32, 0)
    water_number = shape.CellsU("Prop.water_number").ResultInt(32, 0)
    steam_number = shape.CellsU("Prop.steam_number").ResultInt(32, 0)
    Gpr = 0
    name = shape.Name
    obj = Drum(boiler, steam_number, water_number, Gpr, name)
    drums.append(obj)
    elemWater[water_stream_number - 1].append(obj)
    elemPar[steam_stream_number - 1].append(obj)
    all_elems.append(obj)


def RaspoznTopka(shape, boiler, elemAir, elemGaz, SingleZoneTopkas, all_elems):
    name = shape.Name
    stream_number_alter = shape.CellsU("Prop.stream_number_alter").ResultInt(32, 0)
    air_stream_number = shape.CellsU("Prop.air_stream_number").ResultInt(32, 0)
    gaz_stream_number = shape.CellsU("Prop.gaz_stream_number").ResultInt(32, 0)
    Ffst = shape.Cells("Prop.F_front").ResultIU
    Fzst = shape.Cells("Prop.F_back").ResultIU
    Fbok = shape.Cells("Prop.F_side").ResultIU
    Fvok = shape.Cells("Prop.F_vyh").ResultIU
    bt = shape.Cells("Prop.bt").ResultIU
    ht = shape.Cells("Prop.Ht").ResultIU
    hg = shape.Cells("Prop.Hg").ResultIU
    Vt = shape.Cells("Prop.Vt").ResultIU
    ksi = shape.Cells("Prop.ksi").ResultIU
    x = shape.Cells("Prop.x").ResultIU
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    delta_alfa = shape.Cells("Prop.delta_alfa").ResultIU
    alfat = shape.Cells("Prop.alfat").ResultIU
    air_number = shape.Cells("Prop.air_number").ResultInt(32, 0)
    gaz_number = shape.Cells("Prop.gaz_number").ResultInt(32, 0)
    gaz_number_alter = shape.Cells("Prop.gaz_number_alter").ResultInt(32, 0)
    obj = SingleZoneTopka(boiler, name, unknown, stat, Ffst, Fzst, Fbok, Fvok, bt, ht, hg, Vt, ksi, x, delta_alfa, alfat,
                    gaz_number, air_number, gaz_number_alter, stream_number_alter)
    SingleZoneTopkas.append(obj)
    elemAir[air_stream_number - 1].append(obj)
    elemGaz[gaz_stream_number - 1].append(obj)
    elemGaz[stream_number_alter - 1].append(obj)
    all_elems.append(obj)


def RaspoznPovCam(shape, boiler, elemGaz, pov_cams, all_elems):
    name = shape.Name
    gaz_stream_number = shape.Cells("Prop.gaz_stream_number").ResultInt(32, 0)
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    Vpk = shape.Cells("Prop.Vpk").ResultIU
    gaz_number = shape.Cells("Prop.gaz_number").ResultInt(32, 0)
    obj = Pov_cam(boiler, name, gaz_number, unknown, stat, Vpk)
    pov_cams.append(obj)
    elemGaz[gaz_stream_number - 1].append(obj)
    all_elems.append(obj)


def RaspoznUmenshTemp(shape, boiler, elemGaz, UmenshTemps, all_elems):
    name = shape.Name
    gaz_stream_number = shape.Cells("Prop.gaz_stream_number").ResultInt(32, 0)
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    delta_v = shape.Cells("Prop.delta_v").ResultIU
    gaz_number = shape.Cells("Prop.gaz_number").ResultInt(32, 0)
    obj = UmenshTemp(boiler, name, gaz_number, unknown, stat, delta_v)
    UmenshTemps.append(obj)
    elemGaz[gaz_stream_number - 1].append(obj)
    all_elems.append(obj)


def RaspoznTRazd(shape, boiler, elemAir, elemGaz, elemWater, elemPar, t_razds, all_elems):
    type = shape.Cells("Prop.type").ResultStr(231)
    name = shape.Name
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    rD_main = shape.Cells("Prop.D_main").ResultIU
    rD_alter = shape.Cells("Prop.D_alter").ResultIU
    stream_number_alter = shape.Cells("Prop.stream_number_alter").ResultInt(32, 0)
    if type == 'steam':
        steam_number = shape.Cells("Prop.steam_number").ResultInt(32, 0)
        steam_stream_number = shape.Cells("Prop.steam_stream_number").ResultInt(32, 0)
        obj = T_razd(boiler, type, name, unknown, stat, steam_number, rD_main, rD_alter, steam_stream_number,
               stream_number_alter)
        t_razds.append(obj)
        elemPar[steam_stream_number - 1].append(obj)
        elemPar[stream_number_alter - 1].append(obj)
    elif type == 'water':
        water_number = shape.Cells("Prop.water_number").ResultInt(32, 0)
        water_stream_number = shape.Cells("Prop.water_stream_number").ResultInt(32, 0)
        obj = T_razd(boiler, type, name, unknown, stat, water_number, rD_main, rD_alter, water_stream_number,
               stream_number_alter)
        t_razds.append(obj)
        elemWater[water_stream_number - 1].append(obj)
        elemWater[stream_number_alter - 1].append(obj)
    elif type == 'air':
        air_number = shape.Cells("Prop.air_number").ResultInt(32, 0)
        air_stream_number = shape.Cells("Prop.air_stream_number").ResultInt(32, 0)
        obj = T_razd(boiler, type, name, unknown, stat, air_number, rD_main, rD_alter, air_stream_number,
                     stream_number_alter)
        t_razds.append(obj)
        elemAir[air_stream_number - 1].append(obj)
        elemAir[stream_number_alter - 1].append(obj)
    elif type == 'gaz':
        gaz_number = shape.Cells("Prop.gaz_number").ResultInt(32, 0)
        gaz_stream_number = shape.Cells("Prop.gaz_stream_number").ResultInt(32, 0)
        obj = T_razd(boiler, type, name, unknown, stat, gaz_number, rD_main, rD_alter, gaz_stream_number,
                     stream_number_alter)
        t_razds.append(obj)
        elemGaz[gaz_stream_number - 1].append(obj)
        elemGaz[stream_number_alter - 1].append(obj)
    else:
        obj = None
    all_elems.append(obj)


def RaspoznTSm(shape, boiler, elemAir, elemGaz, elemWater, elemPar, t_sms, all_elems):
    type = shape.Cells("Prop.type").ResultStr(231)
    name = shape.Name
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    izv = shape.Cells("Prop.znach_izvii").ResultIU
    stream_number_alter = shape.Cells("Prop.stream_number_alter").ResultInt(32, 0)
    if type == 'steam':
        steam_number = shape.Cells("Prop.steam_number").ResultInt(32, 0)
        steam_number_alter = shape.Cells("Prop.steam_number_alter").ResultInt(32, 0)
        steam_stream_number = shape.Cells("Prop.steam_stream_number").ResultInt(32, 0)
        obj = T_sm(boiler, type, name, unknown, stat, izv, steam_number, steam_number_alter, steam_stream_number,
             stream_number_alter)
        t_sms.append(obj)
        elemPar[steam_stream_number - 1].append(obj)
        elemPar[stream_number_alter - 1].append(obj)
    elif type == 'water':
        water_number = shape.Cells("Prop.water_number").ResultInt(32, 0)
        water_number_alter = shape.Cells("Prop.water_number_alter").ResultInt(32, 0)
        water_stream_number = shape.Cells("Prop.water_stream_number").ResultInt(32, 0)
        obj = T_sm(boiler, type, name, unknown, stat, izv, water_number, water_number_alter, water_stream_number,
             stream_number_alter)
        t_sms.append(obj)
        elemWater[water_stream_number - 1].append(obj)
        elemWater[stream_number_alter - 1].append(obj)
    elif type == 'air':
        air_number = shape.Cells("Prop.air_number").ResultInt(32, 0)
        air_number_alter = shape.Cells("Prop.air_number_alter").ResultInt(32, 0)
        air_stream_number = shape.Cells("Prop.air_stream_number").ResultInt(32, 0)
        obj = T_sm(boiler, type, name, unknown, stat, izv, air_number, air_number_alter, air_stream_number,
             stream_number_alter)
        t_sms.append(obj)
        elemAir[air_stream_number - 1].append(obj)
        elemAir[stream_number_alter - 1].append(obj)
    elif type == 'gaz':
        gaz_number = shape.Cells("Prop.gaz_number").ResultInt(32, 0)
        gaz_number_alter = shape.Cells("Prop.gaz_number_alter").ResultInt(32, 0)
        gaz_stream_number = shape.Cells("Prop.gaz_stream_number").ResultInt(32, 0)
        obj = T_sm(boiler, type, name, unknown, stat, izv, gaz_number, gaz_number_alter, gaz_stream_number,
             stream_number_alter)
        t_sms.append(obj)
        elemGaz[gaz_stream_number - 1].append(obj)
        elemGaz[stream_number_alter - 1].append(obj)
    else:
        obj = None
    all_elems.append(obj)


def RaspoznSteamCondencer(shape, boiler, elemPar, elemWater, SteamCondensers, all_elems):
    steam_stream_number = shape.Cells("Prop.steam_stream_number").ResultInt(32, 0)
    water_stream_number = shape.Cells("Prop.water_stream_number").ResultInt(32, 0)
    type = shape.Cells("Prop.class").ResultStr(231)
    name = shape.Name
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    steam_number = shape.Cells("Prop.steam_number").ResultInt(32, 0)
    water_number = shape.Cells("Prop.water_number").ResultInt(32, 0)
    tii = 0
    tii_water = 0
    obj = SteamCondenser(boiler, type, name, unknown, stat, tii, tii_water, steam_number, water_number)
    SteamCondensers.append(obj)
    elemPar[steam_stream_number - 1].append(obj)
    elemWater[water_stream_number - 1].append(obj)
    all_elems.append(obj)


def RaspoznCVD(shape, boiler, elemPar, CVDs, all_elems):
    name = shape.Name
    type = shape.Cells("Prop.type").ResultStr(231)
    rD_main = shape.Cells("Prop.D_main").ResultIU
    rD_alter = shape.Cells("Prop.D_alter").ResultIU
    Pii_alter = shape.Cells("Prop.Pii_alter").ResultIU
    tii_alter = shape.Cells("Prop.tii_alter").ResultIU
    kpd_noi = shape.Cells("Prop.kpd_noi").ResultIU
    stream_number_alter = shape.Cells("Prop.stream_number_alter").ResultInt(32, 0)
    steam_number = shape.Cells("Prop.steam_number").ResultInt(32, 0)
    steam_stream_number = shape.Cells("Prop.steam_stream_number").ResultInt(32, 0)
    obj = CVD(boiler, name, rD_main, rD_alter, Pii_alter, kpd_noi, tii_alter, steam_number, steam_stream_number,
        stream_number_alter)
    CVDs.append(obj)
    elemPar[steam_stream_number - 1].append(obj)
    elemPar[stream_number_alter - 1].append(obj)
    all_elems.append(obj)


def RaspoznCalorifer(shape, boiler, elemAir, Calorifiers, all_elems):
    air_stream_number = shape.Cells("Prop.air_stream_number").ResultInt(32, 0)
    type = shape.Cells("Prop.type").ResultStr(231)
    name = shape.Name
    tii = shape.Cells("Prop.znach_tii_air").ResultIU
    unknown = poisk_neizv(shape)
    stat = poisk_stat(shape)
    air_number = shape.Cells("Prop.air_number").ResultInt(32, 0)
    obj = Calorifer(boiler, type, name, unknown, stat, tii, air_number)
    elemAir[air_stream_number - 1].append(obj)
    Calorifiers.append(obj)
    all_elems.append(obj)

