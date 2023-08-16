import numpy as np
import math
from .exceptions import *


def argum_nan(argum):
    for i in argum:
        if math.isnan(argum[i]):
            if i == 'Hi':
                argum['Hi'] = 700
            elif i == 'hi':
                argum['hi'] = 400
            elif i == 'hi_water':
                argum['hi_water'] = 400
            elif i == 'hi_air':
                argum['hi_air'] = 400
            elif i == 'Hii':
                argum['Hii'] = 700
            elif i == 'hii':
                argum['hii'] = 400
            elif i == 'hii_water':
                argum['hii_water'] = 400
            elif i == 'hii_air':
                argum['hii_air'] = 400
            elif i == 'F':
                argum['F'] = 3000
            else:
                continue


def argum_pre(unknown, argum):
    for i in unknown:
        if i == 'Hi':
            argum['Hi'] = max(argum["Hii"], argum['hii']) + 4
        elif i == 'hi':
            argum['hi'] = min(argum['Hii'], argum['hii']) - 2
        elif i == 'hi_water':
            argum['hi_water'] = min(argum['Hii'], argum['hii_water']) - 2
        elif i == 'hi_air':
            argum['hi_air'] = min(argum['Hii'], argum['hii_air']) - 2
        elif i == 'Hii':
            argum['Hii'] = argum['Hi'] - 2
        elif i == 'hii':
            argum['hii'] = argum['hi'] + 1
        elif i == 'hii_water':
            argum["hii_water"] = argum["hi_water"] + 1
        elif i == 'hii_air':
            argum['hii_air'] = argum['hi_air'] + 1
        elif i == 'F':
            argum['F'] = 3000
        else:
            continue


def restrictions(unknown_local, tipdvizh, access, vi, ti, vii, tii):
    if tipdvizh == 'Прямоток':
        if vi < ti:
            vi = ti + 1 if 'Hi' in unknown_local else vi
            ti = vi - 1 if 'hi' in unknown_local else ti
            access = True
        if vii < tii:
            vii = tii + 1 if 'Hii' in unknown_local else vii
            tii = vii - 1 if 'hii' in unknown_local else tii
            access = True
    elif tipdvizh == 'Противоток':
        if vi < tii:
            vi = tii + 1 if 'Hi' in unknown_local else vi
            tii = vi - 1 if 'hii' in unknown_local else tii
            access = True
        if vii < ti:
            vii = ti + 1 if 'Hii' in unknown_local else vii
            ti = vii - 1 if 'hi' in unknown_local else ti
            access = True
    else:
        pass
    return vi, ti, vii, tii, access


eps = 0.000001


def __df_one(Y_plus, Y_minus):
    der = (Y_plus - Y_minus) / (2 * eps)
    return der


def __vector_f(type_elem, argum):
    prov_argum = type_elem(argum)
    keys = prov_argum.keys()
    i = 0
    func = np.zeros(len(prov_argum))
    for key in keys:
        func[i] = argum[key] - prov_argum[key]
        i += 1
    return func


@handle_zero_division
def __matrix_df(type_elem, argum, unknowns):
    df = np.zeros((len(unknowns), len(unknowns)))
    for i in range(len(unknowns)):
        argum[unknowns[i]] += eps
        Y_plus = __vector_f(type_elem, argum)
        argum[unknowns[i]] -= 2 * eps
        Y_minus = __vector_f(type_elem, argum)
        argum[unknowns[i]] += eps
        der = __df_one(Y_plus, Y_minus)
        for j in range(len(unknowns)):
            df[j, i] = der[j]
    return df


@handle_zero_division
def newton_method(type_elem, argum, unknowns):
    X = np.zeros(len(unknowns))
    iter = 0
    Dx = math.inf #float('inf')

    while Dx > eps:
        iter += 1
        Y = __vector_f(type_elem, argum)

        for i in range(len(unknowns)):
            X[i] = argum[unknowns[i]]

        W = __matrix_df(type_elem, argum, unknowns)
        xlast = X.copy()
        X -= np.linalg.inv(W).dot(Y)

        for i in range(len(unknowns)):
            argum[unknowns[i]] = X[i]

        dx = X - xlast
        Dx = sum(abs(x) for x in dx)
        if (iter > 1000):
            return
