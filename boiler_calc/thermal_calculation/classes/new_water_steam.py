import math, numpy as np


def eheatV(p, h):
    if p >= 221.2:
        if 1700 < h < 2300:
            vv = vkr(p, h)
            return vv

        if h >= 2300.0:
            vv = vd(p, h)
            return vv
        else:
            t11 = 5.0
            t12 = 330.0
    else:
        t = eheatTs(p)
        hh1 = eheatH1(t)
        hh11 = eheatH11(t)

        if h > hh11:
            if 150 < p < 2750:
                vv = vkr(p, h)
                return vv

            if h >= 1700.0:
                vv = vd(p, h)
                return vv
            else:
                t11 = 5.0
                t12 = 330.0
        else:
            if h > hh1:
                vv1 = eheatV1(t)
                vv11 = eheatV11(t)
                x = (h - hh1) / (hh11 - hh1)
                vv = vv1 + x * (vv11 - vv1)
                return vv
            else:
                t11 = 5.0
                t12 = t

    eps = 5.0E-05 * t11
    t = hfunc(h, p, t11, t12, hw, eps)
    vv = vw(p, t)
    return vv


def eheatT(p, h):
    if p >= 221.2:
        if 1700 < h < 2700:
            txx = tkr(p, h)
            return txx

        if h >= 2700:
            txx = td(p, h)
            return txx
    else:
        t = eheatTs(p)
        hh1 = eheatH1(t)
        hh11 = eheatH11(t)

        if h > hh11:
            if h < 2700.0:
                txx = tkr(p, h)
                return txx
            if h >= 1500.0:
                txx = td(p, h)
                return txx
        else:
            if h > hh1:
                txx = t
                return txx

    t11 = 5.0
    t12 = 350.0
    eps = t11 * 5.0E-05
    t = hfunc(h, p, t11, t12, hw, eps)
    txx = t
    return txx


def eheatS(p, h):
    t = eheatTs(p)
    hh1 = eheatH1(t)
    hh11 = eheatH11(t)

    if p >= 221.2:
        if h < 3200:
            sx = skr(p, h)
            return sx
        if h >= 3200:
            sx = sd(p, h)
            return sx
    else:
        if h > hh11:
            if p > 125 and h < 2900:
                sx = skr(p, h)
                return sx
            if h >= 2500.0:
                sx = sd(p, h)
                return sx
        else:
            if h < hh1:
                ss1 = eheatS1(t)
                ss11 = eheatS11(t)
                x = (h - hh1) / (hh11 - hh1)
                sx = ss1 + x * (ss11 - ss1)
                return sx

    ss1 = eheatS1(t)
    ss11 = eheatS11(t)
    x = (h - hh1) / (hh11 - hh1)
    sx = ss1 + x * (ss11 - ss1)
    return sx


def eheatHPS(p, sq):
    if p >= 221.2:
        hn = 2400.0
        eps = hn * 1.0E-05
        hh1 = hfunc(sq, p, hn, 3900, eheatS, eps)
        hpsx = hh1
        return hpsx
    else:
        t = eheatTs(p)
        ss1 = eheatS1(t)
        ss11 = eheatS11(t)

        if sq >= ss11:
            hn = eheatH11(t)
            eps = hn * 1.0E-08
            hh1 = hfunc(sq, p, hn, 3900, eheatS, eps)
            hpsx = hh1
            return hpsx
        elif sq >= ss1:
            hh1 = eheatH1(t)
            hh11 = eheatH11(t)
            x = (sq - ss1) / (ss11 - ss1)
            hpsx = hh1 + x * (hh11 - hh1)
            return hpsx

        ds = ss1 - sq
        tx = t / (1 + 0.72 * ds)
        hpsx = hw(p, tx)
        return hpsx


def eheatHPT(p, t):
    if p >= 221.2:
        if t > 374:
            hn = 2400.0
            eps = hn * 1.0E-05
            h = hfunc(t, p, hn, 3900, eheatT, eps)
            return h
        else:
            h = hw(p, t)
            return h
    else:
        tt = eheatTs(p)
        if t >= tt:
            hn = eheatH11(tt)
            eps = hn * 1.0E-07
            h = hfunc(t, p, hn, 3900, td, eps)
            if p > 100 and (h < 2700 or math.isnan(h)):
                h = hfunc(t, p, hn, 3900, tkr, eps)
                return h
            return h
        else:
            h = hw(p, t)
            return h


def eheatHPX(p, x):
    t = eheatTs(p)
    hh1 = eheatH1(t)
    hh11 = eheatH11(t)

    hx = x * (hh11 - hh1) + hh1

    return hx


def hfunc(yz, p, a, b, fct, eps):
    def evaluate_function(p, x):
        return yz - fct(p, x)

    c = 0
    fa = evaluate_function(p, a)
    fb = evaluate_function(p, b)

    i = 0

    if math.isnan(abs(fb)):
        c = np.nan

    while abs(fb) >= eps:
        x = b - a
        y = fb - fa

        if abs(x) < 1.0E-06:
            x = x / abs(x) * 1.0E-04
        if abs(y) < 1.0E-06:
            y = y / abs(y) * 1.0E-04

        c = b - fb * x / y
        fc = evaluate_function(p, c)

        fa = fb
        fb = fc
        a = b
        b = c
        i += 1

        if i > 1000:
            # clrscr()
            # print("\n Fatal error hfunc() !")
            c = 0.1
            break
            # exit(1)

    return c


def eheatTs(p):
    pp = p / 0.980665
    a = math.log(pp)

    tt = (((((((((((-4.292460291E-08 * a - 4.26956851E-07) * a +
                   1.534373134E-06) * a + 2.207171179E-05) * a -
                   1.741775190E-05) * a - 3.739348425E-04) * a +
                   1.328377290E-03) * a + 2.129682011E-02) * a +
                   2.107780463E-01) * a + 2.375357647) * a +
                   2.785424215E+01) * a + 9.909271199E+01)

    tx = tt
    return tx


def eheatPs(t):
    tt = t * 0.01

    a = (((((((((1.553179872E-04 * tt - 2.693452728E-03) * tt +
                2.015339284E-02) * tt - 8.659024966E-02) * tt +
                2.477563380E-01) * tt - 5.608659370E-01) * tt +
                1.256759065) * tt - 3.033726807) * tt +
                7.270489907) * tt - 5.078709984)
    psx = 0.980665 * math.exp(a)

    return psx


def eheatV1(t):
    a = t * 0.01

    vv = (((((((((5.9683570E-07 * a - 8.26704100E-06) * a +
                 4.8021276E-05) * a - 1.50442234E-04) * a +
                 2.7254276E-04) * a - 2.79795890E-04) * a +
                 1.4001053E-04) * a + 2.06393470E-05) * a +
                 1.3905330E-07) * a + 1.00017890E-03)

    v1x = vv
    return v1x


def eheatV11(t):
    a = t * 0.01
    pp = eheatPs(t)

    vv = ((((((((2.0409848E-06 * a - 2.8638253E-05) * a +
                1.4519652E-04) * a - 3.4194103E-04) * a +
                3.3979946E-04) * a - 3.1684010E-04) * a -
                3.1913345E-05) * a + 4.5945234E-03) * a +
                1.2600000E-02)

    vv = vv * 100 / pp
    v11x = vv
    return v11x


def eheatH1(t):
    a = t * 0.01

    hh = (((((((((1.1936422E-04 * a - 1.6994910E-03) * a +
               1.0322371E-02) * a - 3.4536790E-02) * a +
               6.9214690E-02) * a - 8.3823420E-02) * a +
               6.2229560E-02) * a - 2.5507948E-02) * a +
               4.2290733E-01) * a - 4.1600000E-05) * 1.0E+03
    h1 = hh
    return h1


def eheatH11(t):
    a = t * 0.01

    hh = (((((((-3.4714286E-04 * a + 2.7325329E-03) * a -
             8.0477568E-03) * a + 9.3849700E-03) * a -
             1.2737746E-02) * a + 1.9591100E-04) * a +
             1.8430540E-01) * a + 2.50096) * 1.0E+03
    h11 = hh
    return h11


def eheatS1(t):
    a = t * 0.01

    ss = ((((((((1.6720190E-04 * a - 2.4670640E-03) * a +
              1.5734212E-02) * a - 5.6232060E-02) * a +
              1.2375197E-01) * a - 1.7724907E-01) * a +
              2.0307179E-01) * a - 3.4417244E-01) * a +
              1.5446705) * a - 1.10E-04
    s1x = ss
    return s1x


def eheatS11(t):
    a = t * 0.01

    ss = ((((((((-1.4000000E-04 * a + 2.8728000E-03) * a -
              2.4050010E-02) * a + 1.0649010E-01) * a -
              2.7846878E-01) * a + 4.8081603E-01) * a -
              7.3158620E-01) * a + 1.3274657) * a -
              2.6836757) * a + 9.1563856
    s11x = ss
    return s11x


def vd(p, h):
    a = p * 0.01
    b = h * 0.001

    vq = (((1.9500000E-05 * a - 6.19938600E-04) * a +
           3.6843960E-03) * a - 3.99990000E-04)
    v2 = (((-5.7200000E-05 * a + 2.00064330E-03) * a -
           1.0384305E-02) * a + 2.67914050E-02) * (b - 2.0)
    v3 = (((2.6000000E-05 * a - 1.46772810E-03) * a +
           7.6498837E-03) * a - 1.70785740E-03) * (b - 2.0) * (b - 2.0)
    v4 = ((3.129600E-04 * a - 1.70630E-03) * a - 7.4127E-06) * (b - 2.0) * (b - 2.0) * (b - 2.0)
    b = 1.4 / (b - 1.68)
    b = b * b
    b = b * b
    v0 = 1.0E-05 * (8.4 - 7.1 * a + 1.420 * a * a -
                   8.4 / (1.0 + 4.6 * a + 120.0 * a * a * a)) * b * (b - 1.0)
    vv = v0 + vq + v2 + v3 + v4
    vx = vv / a
    return vx


def td(p, h):
    a = p * 0.01
    b = h * 0.001 - 3.375

    t1 = ((((5.840000E-04 * a - 5.952300E-03) * a +
           2.672350E-02) * a - 1.050978E-01) * a +
           6.328634E-01) * a + 4.45436
    t2 = (((((4.138000E-03 * a - 3.326290E-02) * a +
           6.423340E-02) * a + 1.614632E-01) * a -
           1.0776543) * a + 4.780516) * b
    t3 = (((((-7.794000E-03 * a + 4.877040E-02) * a +
           3.426200E-03) * a - 6.221451E-01) * a +
           1.5939256) * a - 3.611830E-01) * b * b
    t4 = (((((-5.635100E-02 * a + 5.555955E-01) * a -
           2.0225651) * a + 3.4448816) * a -
           2.7602368) * a - 2.066310E-01) * b * b * b
    t5 = (((((-2.3995E-02 * a + 3.440185E-01) * a -
           1.652921) * a + 3.35518) * a -
           3.289364) * a + 1.977026) * b * b * b * b
    t6 = (((1.647E-01 * a - 1.186) * a +
           2.439) * a - 1.051) * b * b * b * b * b
    t0 = ((((-192.1987 * b + 26.0892) * b - 0.3625) * b +
           0.0018) * b + 0.5214) * (1.0 / (100.0 +
           a * (730.0 + a * (-1400.0 + a * 14500.0))))
    tdx = 100.0 * (t0 + t1 + t2 + t3 + t4 + t5 + t6)
    return tdx


def sd(p, h):
    a = p * 0.01
    b = h * 0.01 - 20.0
    c = (2.9 - 0.1 * b) * (2.9 - 0.1 * b) - 2.6
    d = math.log10(b)

    sq = (((-7.502900E-05 * a + 9.8525900E-04) * a -
           7.897500E-03) * a + 5.8636936E-02) * a + 1.824347E-03
    s2 = ((((-1.631495E-04 * a + 1.6666720E-03) * a -
           9.989430E-03) * a + 4.7405603E-02) * a -
           6.029610E-04) * c
    s3 = ((((-2.446494E-04 + 2.5383324E-02) * a -
           1.033025E-02) * a + 2.2024349E-02) * a +
           3.492510E-04) * c * c
    s4 = ((((-2.031894E-04 * a + 2.0922070E-03) * a -
           7.243208E-03) * a + 9.4231710E-03) * a +
           3.154860E-04) * c * c * c
    s5 = ((((-1.155620E-05 * a + 7.7918100E-05) * a -
           3.643037E-04) * a + 1.1724252E-03) * a -
           1.449407E-04) * c * c * c * c
    b = math.fabs(1.7 - 0.1 * b)
    b = b * b
    b = b * b
    b = b * b
    s0 = (((0.43144 * d - 1.44026) * d + 1.98819) * d + 2.92696) * d + 6.29835 - 1.062689 * math.log10(a * 1.0E+04) + (0.13 * a - 0.12 * a * a) / (1.07 + 7.2 * a * a + 4.0 * a * a * a) * b
    sdx = s0 + sq + s2 + s3 + s4 + s5
    return sdx


def vw(p, t):
    a = t * 0.01
    b = p * 0.01

    v0 = ((((-5.0004200E-07 * a + 7.8565550E-06) * a -
          2.6236907E-05) * a + 6.5359352E-05) * a -
          3.4631890E-06) * a + 9.9942695E-04
    vq = ((((2.1289600E-07 * a - 1.8355930E-06) * a +
          4.8681740E-06) * a - 6.6884440E-06) * a +
          3.5044300E-06) * a - 4.6091520E-06
    a4 = a * a * a * a
    a16 = a4 * a4 * a4 * a4
    v2 = 4.55E-12 * a16 + 8.0E-07 * a4 + 7.0E-07 * a + 3.0E-06
    vx = v0 + vq * b + v2 * (1.0 / (b + 2.0) - 0.227 + 0.018 * b)
    return vx


def hw(p, t):
    a = t * 0.01
    b = p * 0.01

    h0 = ((((4.5199700E-04 * a - 1.8508140E-03) * a +
          6.3656960E-03) * a - 6.5218115E-03) * a +
          4.1982594E-01) * a + 6.4E-04
    hq = ((((-2.2009100E-05 * a + 1.2093020E-04) * a -
          8.0696010E-04) * a + 1.6722356E-03) * a -
          3.0725260E-03) * a + 9.6859913E-03
    a6 = a * a * a * a * a * a
    a16 = a6 * a6 * a * a * a * a
    h2 = 1.682E-09 * a16 + 5.44E-05 * a6 + 3.2E-03 * a - 2.88E-03
    hwx = (h0 + hq * b + h2 * (1.0 / (b + 2.0) - 0.24927 + 0.021 * b)) * 1.0E+03
    return hwx


def tkr(p, h):
    a = p * 0.01
    b = h * 0.001 - 2

    t1 = (((1.889530E-02 * a - 2.103973E-01) * a +
           8.140622E-01) * a - 1.0673765) * a + 3.9617281
    t2 = ((((-4.573110E-02 * a + 5.157483E-01) * a -
           2.22961190) * a + 4.9117969) * a -
           4.2831428) * b
    t3 = ((((-2.933476E-01 * a + 3.3288459) * a -
           1.3799105E+1) * a + 2.4806751E+01) * a -
           1.7360934E+1) * b * b
    t4 = ((((4.6792610E-01 * a - 5.1865516) * a +
           2.1088377E+01) * a - 3.7861085E+01) * a +
           2.7102834E+01) * b * b * b
    t5 = ((((8.639461E-01 * a - 9.7562310) * a +
           4.0227972E+01) * a - 7.1613017E+01) * a +
           4.7253670E+01) * b * b * b * b
    t6 = ((((-1.259397 * a + 1.4047099E+01) * a -
           5.7194453E+01) * a + 1.0075819E+02) * a -
           6.5775645E+01) * b * b * b * b * b
    tkr = 100.0 * (t1 + t2 + t3 + t4 + t5 + t6)
    return tkr


def vkr(p, h):
    a = p * 0.01
    b = h * 0.001 - 2

    vq = (9.740E-05 * a + 7.3294E-04) * a + 3.66681E-03
    v2 = ((4.6223E-04 * a - 4.00691E-03) * a + 1.673873E-02) * b
    v3 = ((-1.3672E-04 * a - 1.31204E-03) * a + 1.584386E-02) * b * b
    v4 = ((-7.4695E-04 * a + 7.55585E-03) * a - 1.491102E-02) * b * b * b
    v5 = ((6.2142E-04 * a - 5.9612E-04) * a - 1.000221E-02) * b * b * b * b
    v6 = ((-2.7310E-04 * a - 2.73716E-03) * a + 1.381305E-02) * b * b * b * b * b
    vkr = 100.0 * (vq + v2 + v3 + v4 + v5 + v6)

    vkr = vkr / p
    return vkr


def skr(p, h):
    a = p * 0.01 - 2.5
    b = h * 0.001 - 2

    sq = ((((1.7700E-03 * a - 6.660E-04) * a -
           5.1800E-03) * a + 8.033E-03) * a -
           3.8343E-03) * a + 4.265774
    s2 = (((((-4.1830E-03 * a + 4.418E-03) * a -
           3.2610E-03) * a + 2.1437E-02) * a -
           6.0136E-02) * a + 1.526792) * b
    s3 = (((((-1.2770E-02 * a + 1.1204E-02) * a +
           1.3291E-02) * a - 9.0800E-04) * a -
           6.0450E-02) * a - 4.1270E-02) * b * b
    s4 = (((((1.3570E-02 * a - 1.4960E-02) * a -
           9.4080E-03) * a - 6.5280E-03) * a +
           1.6150E-02) * a + 6.5699E-02) * b * b * b
    s5 = (((((9.3000E-04 * a + 1.6390E-03) * a -
           5.2150E-03) * a + 1.0506E-02) * a +
           1.2379E-02) * a - 7.4354E-02) * b * b * b * b
    skr = sq + s2 + s3 + s4 + s5
    return skr


def eheatXPH(p, h):
    t = eheatTs(p)
    hh1 = eheatH1(t)
    hh11 = eheatH11(t)
    xh = (h - hh1) / (hh11 - hh1)

    if xh >= 1.0:
        xh = 1.0
    elif xh <= 0.0:
        xh = 0.0

    return xh


def eheatXPS(p, s):
    t = eheatTs(p)
    ss1 = eheatS1(t)
    ss11 = eheatS11(t)
    xs = (s - ss1) / (ss11 - ss1)

    if xs >= 1.0:
        xs = 1.0
    elif xs <= 0.0:
        xs = 0.0

    return xs


def eheatXPV(p, v):
    t = eheatTs(p)
    vv1 = eheatV1(t)
    vv11 = eheatV11(t)
    xv = (v - vv1) / (vv11 - vv1)

    if xv >= 1.0:
        xv = 1.0
    elif xv <= 0.0:
        xv = 0.0

    return xv


def eheatH0(pa, eha, pb):
    tna = eheatTs(pa)
    EHAB = eheatH1(tna)
    EHAP = eheatH11(tna)
    SAB = eheatS1(tna)
    SAP = eheatS11(tna)

    tnb = eheatTs(pb)
    EHBB = eheatH1(tnb)
    EHBP = eheatH11(tnb)
    SBB = eheatS1(tnb)
    SBP = eheatS11(tnb)

    if eha > EHAP:
        SA = eheatS(pa, eha)
        if SA > SBP:
            EHB = eheatHPS(pb, SA)
            HA = eha - EHB
            return HA
        else:
            XB = (SA - SBB) / (SBP - SBB)
            EHB = EHBP * XB + (1 - XB) * EHBB
            HA = eha - EHB
            return HA
    else:
        XA = (eha - EHAB) / (EHAP - EHAB)
        SA = SAP * XA + SAB * (1 - XA)
        XB = (SA - SBB) / (SBP - SBB)
        EHB = EHBP * XB + (1 - XB) * EHBB
        HA = eha - EHB
        return HA

