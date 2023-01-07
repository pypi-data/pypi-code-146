"""Define the seven SI base units.

Source : http://physics.nist.gov/cuu/Units/units.html)
"""

from robotpy_toolkit_7407.unum import Unum
unit = Unum.unit

m = M = unit("m", 0, "meter")
Ym = YM = unit("Ym", 10**24 * m, "yottameter")
Zm = ZM = unit("Zm", 10**21 * m, "zettameter")
Em = EM = unit("Em", 10**18 * m, "exameter")
Pm = PM = unit("Pm", 10**15 * m, "petameter")
Tm = TM = unit("Tm", 10**12 * m, "terameter")
Gm = GM = unit("Gm", 10**9 * m, "gigameter")
Mm = MM = unit("Mm", 10**6 * m, "megameter")
km = KM = unit("km", 10**3 * m, "kilometer")
hm = HM = unit("hm", 10**2 * m, "hectometer")
dam = DAM = unit("dam", 10**1 * m, "decameter")
ym = YM = unit("ym", 10**-24 * m, "yoctometer")
zm = ZM = unit("zm", 10**-21 * m, "zeptometer")
am = AM = unit("am", 10**-18 * m, "attometer")
fm = FM = unit("fm", 10**-15 * m, "femtometer")
pm = PM = unit("pm", 10**-12 * m, "picometer")
nm = NM = unit("nm", 10**-9 * m, "nanometer")
um = UM = unit("um", 10**-6 * m, "micrometer")
mm = MM = unit("mm", 10**-3 * m, "millimeter")
cm = CM = unit("cm", 10**-2 * m, "centimeter")
dm = DM = unit("dm", 10**-1 * m, "decimeter")

# Uppercase S is Siements; seconds can only use lowercase s
s = unit("s", 0, "second")
Ys = unit("Ys", 10**24 * s, "yottasecond")
Zs = unit("Zs", 10**21 * s, "zettasecond")
Es = unit("Es", 10**18 * s, "exasecond")
Ps = unit("Ps", 10**15 * s, "petasecond")
Ts = unit("Ts", 10**12 * s, "terasecond")
Gs = unit("Gs", 10**9 * s, "gigasecond")
Ms = unit("Ms", 10**6 * s, "megasecond")
ks = unit("ks", 10**3 * s, "kilosecond")
hs = unit("hs", 10**2 * s, "hectosecond")
das = unit("das", 10**1 * s, "decasecond")
ys = unit("ys", 10**-24 * s, "yoctosecond")
zs = unit("zs", 10**-21 * s, "zeptosecond")
#as = unit("as", 10**-18 * s, "attosecond") # as is a reserved word
fs = unit("fs", 10**-15 * s, "femtosecond")
ps = unit("ps", 10**-12 * s, "picosecond")
ns = unit("ns", 10**-9 * s, "nanosecond")
us = unit("us", 10**-6 * s, "microsecond")
ms = unit("ms", 10**-3 * s, "millisecond")
cs = unit("cs", 10**-2 * s, "centisecond")
ds = unit("ds", 10**-1 * s, "decisecond")


A = A = unit("A", 0, "ampere")
YA = YA = unit("YA", 10**24 * A, "yottaampere")
ZA = ZA = unit("ZA", 10**21 * A, "zettaampere")
EA = EA = unit("EA", 10**18 * A, "exaampere")
PA = PA = unit("PA", 10**15 * A, "petaampere")
TA = TA = unit("TA", 10**12 * A, "teraampere")
GA = GA = unit("GA", 10**9 * A, "gigaampere")
MA = MA = unit("MA", 10**6 * A, "megaampere")
kA = KA = unit("kA", 10**3 * A, "kiloampere")
hA = HA = unit("hA", 10**2 * A, "hectoampere")
daA = DAA = unit("daA", 10**1 * A, "decaampere")
yA = YA = unit("yA", 10**-24 * A, "yoctoampere")
zA = ZA = unit("zA", 10**-21 * A, "zeptoampere")
aA = AA = unit("aA", 10**-18 * A, "attoampere")
fA = FA = unit("fA", 10**-15 * A, "femtoampere")
pA = PA = unit("pA", 10**-12 * A, "picoampere")
nA = NA = unit("nA", 10**-9 * A, "nanoampere")
uA = UA = unit("uA", 10**-6 * A, "microampere")
mA = MA = unit("mA", 10**-3 * A, "milliampere")
cA = CA = unit("cA", 10**-2 * A, "centiampere")
dA = DA = unit("dA", 10**-1 * A, "deciampere")


K = K = unit("K", 0, "kelvin")
YK = YK = unit("YK", 10**24 * K, "yottakelvin")
ZK = ZK = unit("ZK", 10**21 * K, "zettakelvin")
EK = EK = unit("EK", 10**18 * K, "exakelvin")
PK = PK = unit("PK", 10**15 * K, "petakelvin")
TK = TK = unit("TK", 10**12 * K, "terakelvin")
GK = GK = unit("GK", 10**9 * K, "gigakelvin")
MK = MK = unit("MK", 10**6 * K, "megakelvin")
kK = KK = unit("kK", 10**3 * K, "kilokelvin")
hK = HK = unit("hK", 10**2 * K, "hectokelvin")
daK = DAK = unit("daK", 10**1 * K, "decakelvin")
yK = YK = unit("yK", 10**-24 * K, "yoctokelvin")
zK = ZK = unit("zK", 10**-21 * K, "zeptokelvin")
aK = AK = unit("aK", 10**-18 * K, "attokelvin")
fK = FK = unit("fK", 10**-15 * K, "femtokelvin")
pK = PK = unit("pK", 10**-12 * K, "picokelvin")
nK = NK = unit("nK", 10**-9 * K, "nanokelvin")
uK = UK = unit("uK", 10**-6 * K, "microkelvin")
mK = MK = unit("mK", 10**-3 * K, "millikelvin")
cK = CK = unit("cK", 10**-2 * K, "centikelvin")
dK = DK = unit("dK", 10**-1 * K, "decikelvin")


mol = MOL = unit("mol", 0, "mole")
Ymol = YMOL = unit("Ymol", 10**24 * mol, "yottamole")
Zmol = ZMOL = unit("Zmol", 10**21 * mol, "zettamole")
Emol = EMOL = unit("Emol", 10**18 * mol, "examole")
Pmol = PMOL = unit("Pmol", 10**15 * mol, "petamole")
Tmol = TMOL = unit("Tmol", 10**12 * mol, "teramole")
Gmol = GMOL = unit("Gmol", 10**9 * mol, "gigamole")
Mmol = MMOL = unit("Mmol", 10**6 * mol, "megamole")
kmol = KMOL = unit("kmol", 10**3 * mol, "kilomole")
hmol = HMOL = unit("hmol", 10**2 * mol, "hectomole")
damol = DAMOL = unit("damol", 10**1 * mol, "decamole")
ymol = YMOL = unit("ymol", 10**-24 * mol, "yoctomole")
zmol = ZMOL = unit("zmol", 10**-21 * mol, "zeptomole")
amol = AMOL = unit("amol", 10**-18 * mol, "attomole")
fmol = FMOL = unit("fmol", 10**-15 * mol, "femtomole")
pmol = PMOL = unit("pmol", 10**-12 * mol, "picomole")
nmol = NMOL = unit("nmol", 10**-9 * mol, "nanomole")
umol = UMOL = unit("umol", 10**-6 * mol, "micromole")
mmol = MMOL = unit("mmol", 10**-3 * mol, "millimole")
cmol = CMOL = unit("cmol", 10**-2 * mol, "centimole")
dmol = DMOL = unit("dmol", 10**-1 * mol, "decimole")


cd = CD = unit("cd", 0, "candela")
Ycd = YCD = unit("Ycd", 10**24 * cd, "yottacandela")
Zcd = ZCD = unit("Zcd", 10**21 * cd, "zettacandela")
Ecd = ECD = unit("Ecd", 10**18 * cd, "exacandela")
Pcd = PCD = unit("Pcd", 10**15 * cd, "petacandela")
Tcd = TCD = unit("Tcd", 10**12 * cd, "teracandela")
Gcd = GCD = unit("Gcd", 10**9 * cd, "gigacandela")
Mcd = MCD = unit("Mcd", 10**6 * cd, "megacandela")
kcd = KCD = unit("kcd", 10**3 * cd, "kilocandela")
hcd = HCD = unit("hcd", 10**2 * cd, "hectocandela")
dacd = DACD = unit("dacd", 10**1 * cd, "decacandela")
ycd = YCD = unit("ycd", 10**-24 * cd, "yoctocandela")
zcd = ZCD = unit("zcd", 10**-21 * cd, "zeptocandela")
acd = ACD = unit("acd", 10**-18 * cd, "attocandela")
fcd = FCD = unit("fcd", 10**-15 * cd, "femtocandela")
pcd = PCD = unit("pcd", 10**-12 * cd, "picocandela")
ncd = NCD = unit("ncd", 10**-9 * cd, "nanocandela")
ucd = UCD = unit("ucd", 10**-6 * cd, "microcandela")
mcd = MCD = unit("mcd", 10**-3 * cd, "millicandela")
ccd = CCD = unit("ccd", 10**-2 * cd, "centicandela")
dcd = DCD = unit("dcd", 10**-1 * cd, "decicandela")


kg = KG = unit("kg", 0, "kilogram")
Yg = YG = unit("Yg", 10**21 * kg, "yottagram")
Zg = ZG = unit("Zg", 10**18 * kg, "zettagram")
Eg = EG = unit("Eg", 10**15 * kg, "exagram")
Pg = PG = unit("Pg", 10**12 * kg, "petagram")
Tg = TG = unit("Tg", 10**9 * kg, "teragram")
Gg = GG = unit("Gg", 10**6 * kg, "gigagram")
Mg = MG = unit("Mg", 10**3 * kg, "megagram")
hg = HG = unit("hg", 10**-1 * kg, "hectogram")
dag = DAG = unit("dag", 10**-2 * kg, "decagram")
yg = YG = unit("yg", 10**-27 * kg, "yoctogram")
zg = ZG = unit("zg", 10**-24 * kg, "zeptogram")
ag = AG = unit("ag", 10**-21 * kg, "attogram")
fg = FG = unit("fg", 10**-18 * kg, "femtogram")
pg = PG = unit("pg", 10**-15 * kg, "picogram")
ng = NG = unit("ng", 10**-12 * kg, "nanogram")
ug = UG = unit("ug", 10**-9 * kg, "microgram")
mg = MG = unit("mg", 10**-6 * kg, "milligram")
cg = CG = unit("cg", 10**-5 * kg, "centigram")
dg = DG = unit("dg", 10**-4 * kg, "decigram")
g = unit("g", 10**-3 * kg, "gram")


# cleaning
del Unum
del unit
