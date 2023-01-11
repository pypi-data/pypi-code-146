from musiclang.core.library import *
from fractions import Fraction as frac

# GLOBAL SCORE VARIABLES

TEMPO = 120
FILENAME = ""  # REPLACE WITH YOUR DESTINATION

###

piano__0_0 = s0.w.o(-2).pp
piano__1_0 = s0.w.o(-1).pp
piano__2_0 = s4.e3.o(-1).pp + s0.e3.pp + s2.e3.pp + s4.e3.o(-1).pp + s0.e3.pp + \
    s2.e3.pp + s4.e3.o(-1).pp + s0.e3.pp + s2.e3.pp + \
    s4.e3.o(-1).pp + s0.e3.pp + s2.e3.pp
chord_0 = (I % II.b.m)(piano__0=piano__0_0,
                       piano__1=piano__1_0, piano__2=piano__2_0)

piano__0_1 = s4.w.o(-3).pp
piano__1_1 = s4.w.o(-2).pp
piano__2_1 = s2.e3.o(-1).pp + s5.e3.o(-1).pp + s0.e3.pp + s2.e3.o(-1).pp + s5.e3.o(-1).pp + \
    s0.e3.pp + s2.e3.o(-1).pp + s5.e3.o(-1).pp + s0.e3.pp + \
    s2.e3.o(-1).pp + s5.e3.o(-1).pp + s0.e3.pp
chord_1 = (I['64'] % III.M)(piano__0=piano__0_1,
                            piano__1=piano__1_1, piano__2=piano__2_1)

piano__0_2 = s0.h.o(-3).p
piano__1_2 = s0.h.o(-2).p
piano__2_2 = s0.e3.o(-1).p + s2.e3.o(-1).pp + s4.e3.o(-1).pp + \
    s0.e3.o(-1).pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp
chord_2 = (VI % II.b.m)(piano__0=piano__0_2,
                        piano__1=piano__1_2, piano__2=piano__2_2)

piano__0_3 = s2.h.o(-3).pp
piano__1_3 = s2.h.o(-2).pp
piano__2_3 = s4.e3.o(-1).p + s0.e3.pp + s2.e3.pp + \
    s4.e3.o(-1).pp + s0.e3.pp + s2.e3.pp
chord_3 = (I['6'] % II.M)(piano__0=piano__0_3,
                          piano__1=piano__1_3, piano__2=piano__2_3)

piano__0_4 = s0.h.o(-3).p + s0.o(-3).pp
piano__1_4 = s0.h.o(-2).p + s0.o(-2).pp
piano__2_4 = s0.e3.o(-1).pp + s2.e3.o(-1).pp + s6.e3.o(-1).pp + s0.e3.o(-1).pp + \
    s3.e3.o(-1).pp + s5.e3.o(-1).pp + s0.e3.o(-1).pp + \
    s3.e3.o(-1).pp + s4.e3.o(-1).pp
chord_4 = (V % II.b.m)(piano__0=piano__0_4,
                       piano__1=piano__1_4, piano__2=piano__2_4)

piano__2_5 = s6.e3.o(-2).pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp
chord_5 = (V['7'] % II.b.m)(piano__2=piano__2_5)

piano__0_6 = s0.w.o(-2).pp
piano__1_6 = s4.hd.o(-2).pp + s4.ed.p + s4.s.p
piano__2_6 = s0.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp + s4.e3.o(-1).pp + s0.e3.pp + \
    s2.e3.pp + s4.e3.o(-1).pp + s0.e3.pp + s2.e3.pp + \
    s4.e3.o(-1).pp + s0.e3.pp + s2.e3.pp
chord_6 = (I % II.b.m)(piano__0=piano__0_6,
                       piano__1=piano__1_6, piano__2=piano__2_6)

piano__0_7 = s2.w.o(-3).pp
piano__1_7 = s0.hd.o(-2).pp + s0.ed.p + s0.s.p
piano__2_7 = s2.e3.o(-2).pp + s4.e3.o(-1).pp + s6.e3.o(-1).pp + s0.e3.o(-1).pp + s4.e3.o(-1).pp + s6.e3.o(-1).pp + \
    s0.e3.o(-1).pp + s4.e3.o(-1).pp + s6.e3.o(-1).pp + \
    s0.e3.o(-1).pp + s4.e3.o(-1).pp + s6.e3.o(-1).pp
chord_7 = (V['7'] % II.b.m)(piano__0=piano__0_7,
                            piano__1=piano__1_7, piano__2=piano__2_7)

piano__0_8 = s0.h.o(-2).pp
piano__1_8 = s4.h.p
piano__2_8 = s0.e3.o(-1).pp + s0.e3.pp + s2.e3.pp + \
    s4.e3.o(-1).pp + s0.e3.pp + s2.e3.pp
chord_8 = (I % II.b.m)(piano__0=piano__0_8,
                       piano__1=piano__1_8, piano__2=piano__2_8)

piano__0_9 = s0.h.o(-3).pp
piano__1_9 = s0.h.o(-2).pp
piano__2_9 = s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp + \
    s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp
chord_9 = (II % III.M)(piano__0=piano__0_9,
                       piano__1=piano__1_9, piano__2=piano__2_9)

piano__0_10 = s4.h.o(-3).p
piano__1_10 = s2.h.p
piano__2_10 = s4.e3.o(-2).p + s4.e3.o(-1).pp + s0.e3.pp + \
    s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp
chord_10 = (I['64'] % III.M)(piano__0=piano__0_10,
                             piano__1=piano__1_10, piano__2=piano__2_10)

piano__0_11 = s0.h.o(-3).p
piano__1_11 = s4.o(-1).p + s0.p
piano__2_11 = s0.e3.o(-2).p + s0.e3.o(-1).pp + s2.e3.o(-1).pp + \
    s6.e3.o(-2).pp + s0.e3.o(-1).pp + s2.e3.o(-1).pp
chord_11 = (V['7'] % III.M)(piano__0=piano__0_11,
                            piano__1=piano__1_11, piano__2=piano__2_11)

piano__1_12 = s0.w.o(-2).pp
piano__2_12 = s0.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp + \
    s0.e3.pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp + \
    s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp
chord_12 = (I % III.M)(piano__1=piano__1_12, piano__2=piano__2_12)

piano__1_13 = s0.hd.o(-2).pp + s2.ed.p + s2.s.p
piano__2_13 = s0.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp + \
    s0.e3.pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp + \
    s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp
chord_13 = (I % III.m)(piano__1=piano__1_13, piano__2=piano__2_13)

piano__0_14 = s4.w.o(-3).pp
piano__1_14 = s0.hd.p + s0.ed.p + s0.s.p
piano__2_14 = s4.e3.o(-2).pp + s2.e3.o(-1).pp + s6.e3.o(-1).pp + s0.e3.o(-1).pp + s2.e3.o(-1).pp + s6.e3.o(-1).pp + \
    s0.e3.o(-1).pp + s2.e3.o(-1).pp + s6.e3.o(-1).pp + \
    s0.e3.o(-1).pp + s2.e3.o(-1).pp + s6.e3.o(-1).pp
chord_14 = (V['43'] % I.M)(piano__0=piano__0_14,
                           piano__1=piano__1_14, piano__2=piano__2_14)

piano__0_15 = s0.o(-3).pp
piano__1_15 = s4.o(-1).p
piano__2_15 = s0.e3.o(-2).pp + s0.e3.o(-1).pp + s2.e3.o(-1).pp
chord_15 = (VI % III.m)(piano__0=piano__0_15,
                        piano__1=piano__1_15, piano__2=piano__2_15)

piano__0_16 = s4.o(-3).p
piano__2_16 = s4.e3.o(-2).p + s4.e3.o(-1).pp + s0.e3.pp
chord_16 = (I['64'] % III.m)(piano__0=piano__0_16, piano__2=piano__2_16)

piano__0_17 = s0.o(-4).p
piano__1_17 = s0.o(-3).p
piano__2_17 = s6.e3.o(-3).pp + s2.e3.o(-2).p + s4.e3.o(-2).p
chord_17 = (VII['2'] % VII.m)(piano__0=piano__0_17,
                              piano__1=piano__1_17, piano__2=piano__2_17)

piano__1_18 = s0.o(-1).p
piano__2_18 = s0.e3.o(-2).p + s4.e3.o(-2).pp + s6.e3.o(-2).pp
chord_18 = (V['7'] % VII.m)(piano__1=piano__1_18, piano__2=piano__2_18)

piano__0_19 = s0.h.o(-3).p
piano__1_19 = s0.h.o(-2).p
piano__2_19 = s4.e3.o(-2).pp + s0.e3.o(-1).pp + s2.e3.o(-1).pp + \
    s4.e3.o(-2).pp + s0.e3.o(-1).pp + s2.e3.o(-1).pp
chord_19 = (I % VII.m)(piano__0=piano__0_19,
                       piano__1=piano__1_19, piano__2=piano__2_19)

piano__1_20 = s5.o(-4).p + s0.o(-3).pp
piano__2_20 = s0.e3.o(-2).pp + s2.e3.o(-2).pp + s3.e3.o(-2).pp + \
    s5.e3.o(-3).pp + s2.e3.o(-2).pp + s3.e3.o(-2).pp
chord_20 = (VI['6'] % VII.m)(piano__1=piano__1_20, piano__2=piano__2_20)

piano__0_21 = l.h + s4.h.o(-4).pp
piano__1_21 = s4.h.o(-3).p + s4.h.o(-3).pp
piano__2_21 = s4.e3.o(-2).p + s0.e3.o(-1).pp + s2.e3.o(-1).pp + s4.e3.o(-2).pp + s0.e3.o(-1).pp + s2.e3.o(-1).pp + \
    s4.e3.o(-2).pp + s6.e3.o(-2).pp + s1.e3.o(-1).pp + \
    s4.e3.o(-2).pp + s6.e3.o(-2).pp + s1.e3.o(-1).pp
chord_21 = (I % VII.m)(piano__0=piano__0_21,
                       piano__1=piano__1_21, piano__2=piano__2_21)

piano__0_22 = s0.w.o(-3).pp
piano__1_22 = s0.hd.o(-2).pp + s0.p
piano__2_22 = s0.e3.o(-1).pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.o(-1).pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp + \
    s0.e3.o(-1).p + h4.e3.o(-1).pp + s4.e3.o(-1).pp + \
    s0.e3.o(-1).p + h4.e3.o(-1).pp + s4.e3.o(-1).pp
chord_22 = (I % VII.m)(piano__0=piano__0_22,
                       piano__1=piano__1_22, piano__2=piano__2_22)

piano__1_23 = s0.mf + s2.o(-3).p + s4.o(-3).p + s2.o(-3).p
piano__2_23 = s6.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).p + s2.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).p + \
    s4.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).p + \
    s2.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).pp
chord_23 = (VI['6'] % III.m)(piano__1=piano__1_23, piano__2=piano__2_23)

piano__0_24 = s0.w.o(-3).p
piano__1_24 = s0.hd.p + s0.p
piano__2_24 = s0.e3.o(-2).p + s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.o(-1).pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp + \
    s0.e3.o(-1).p + s2.e3.o(-1).pp + s4.e3.o(-1).pp + \
    s0.e3.o(-1).p + s2.e3.o(-1).pp + s4.e3.o(-1).pp
chord_24 = (V % III.m)(piano__0=piano__0_24,
                       piano__1=piano__1_24, piano__2=piano__2_24)

piano__1_25 = s0.mf + s2.o(-3).p + s4.o(-3).p + s2.o(-3).p
piano__2_25 = s6.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).p + s2.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).p + \
    s4.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).p + \
    s2.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).pp
chord_25 = (VI['6'] % III.m)(piano__1=piano__1_25, piano__2=piano__2_25)

piano__0_26 = s0.h.o(-3).pp
piano__1_26 = s0.h.p
piano__2_26 = s0.e3.o(-2).pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp + \
    s0.e3.o(-1).pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp
chord_26 = (V % III.m)(piano__0=piano__0_26,
                       piano__1=piano__1_26, piano__2=piano__2_26)

piano__0_27 = s2.h.o(-4).pp
piano__1_27 = s2.h.o(-3).pp
piano__2_27 = s4.e3.o(-2).pp + s6.e3.o(-2).pp + s0.e3.o(-1).pp + \
    s4.e3.o(-2).pp + s6.e3.o(-2).pp + s0.e3.o(-1).pp
chord_27 = (VII['65'] % IV.s.m)(piano__0=piano__0_27,
                                piano__1=piano__1_27, piano__2=piano__2_27)

piano__0_28 = s0.h.o(-4).pp
piano__1_28 = s0.h.o(-3).pp
piano__2_28 = s4.e3.o(-2).pp + s5.e3.o(-2).pp + s2.e3.o(-1).pp + \
    s4.e3.o(-2).pp + s5.e3.o(-2).pp + s2.e3.o(-1).pp
chord_28 = (VII % IV.s.m)(piano__0=piano__0_28,
                          piano__1=piano__1_28, piano__2=piano__2_28)

piano__0_29 = s0.h.o(-3).p
piano__1_29 = s0.h.o(-2).p
piano__2_29 = s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp + \
    s2.e3.o(-1).pp + s4.e3.o(-1).pp + s0.e3.pp
chord_29 = (I % IV.s.m)(piano__0=piano__0_29,
                        piano__1=piano__1_29, piano__2=piano__2_29)

piano__0_30 = s2.h.o(-3).p
piano__1_30 = s0.h.p
piano__2_30 = s2.e3.o(-2).p + s2.e3.o(-1).pp + s4.e3.o(-1).pp + \
    s0.e3.o(-1).p + s2.e3.o(-1).pp + s4.e3.o(-1).pp
chord_30 = (I['6'] % V.M)(piano__0=piano__0_30,
                          piano__1=piano__1_30, piano__2=piano__2_30)

piano__0_31 = s0.h.o(-3).p
piano__1_31 = s4.h.o(-1).p
piano__2_31 = s0.e3.o(-2).p + s6.e3.o(-2).pp + s2.e3.o(-1).pp + \
    s4.e3.o(-2).pp + s6.e3.o(-2).pp + s2.e3.o(-1).pp
chord_31 = (VII['7'] % II.b.m)(piano__0=piano__0_31,
                               piano__1=piano__1_31, piano__2=piano__2_31)

piano__1_32 = s4.h.o(-3).pp + s4.o(-3).pp + s4.o(-1).p
piano__2_32 = s4.e3.o(-2).pp + s0.e3.o(-1).pp + s2.e3.o(-1).pp + s4.e3.o(-2).pp + s0.e3.o(-1).pp + s2.e3.o(-1).pp + \
    s4.e3.o(-2).pp + s0.e3.o(-1).pp + s1.e3.o(-1).pp + \
    s4.e3.o(-2).pp + s6.e3.o(-2).pp + s1.e3.o(-1).pp
chord_32 = (I['64'] % IV.s.m)(piano__1=piano__1_32, piano__2=piano__2_32)

piano__0_33 = s0.w.o(-3).pp
piano__1_33 = s4.hd.o(-3).pp + s4.ed.p + s4.s.p
piano__2_33 = s0.e3.o(-2).pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp + s2.e3.o(-1).pp + s4.e3.o(-1).pp + \
    s0.e3.pp + s4.e3.o(-1).pp + s0.e3.pp + s2.e3.pp + \
    s4.e3.o(-1).p + s0.e3.pp + s2.e3.pp
chord_33 = (I % IV.s.m)(piano__0=piano__0_33,
                        piano__1=piano__1_33, piano__2=piano__2_33)

piano__0_34 = s2.w.o(-2).pp
piano__1_34 = s2.hd.o(-3).pp + s0.ed.p + s0.s.p
piano__2_34 = s0.e3.o(-2).pp + s4.e3.o(-1).pp + s6.e3.o(-1).pp + s0.e3.o(-1).p + s4.e3.o(-1).pp + s6.e3.o(-1).pp + \
    s0.e3.o(-1).p + s4.e3.o(-1).pp + s6.e3.o(-1).pp + \
    s0.e3.o(-1).p + s4.e3.o(-1).pp + s6.e3.o(-1).pp
chord_34 = (V['7'] % IV.s.m)(piano__0=piano__0_34,
                             piano__1=piano__1_34, piano__2=piano__2_34)

piano__1_35 = s0.h.o(-2).pp
piano__2_35 = s0.e3.o(-1).pp + s0.e3.pp + s2.e3.pp + \
    s4.e3.o(-1).p + s0.e3.p + s2.e3.p
chord_35 = (I % IV.s.m)(piano__1=piano__1_35, piano__2=piano__2_35)

piano__1_36 = s2.o(-3).p
piano__2_36 = s2.e3.o(-2).p + s4.e3.o(-1).p + s6.e3.o(-1).p
chord_36 = (VII['7'] % II.b.m)(piano__1=piano__1_36, piano__2=piano__2_36)

piano__1_37 = s4.o(-3).p
piano__2_37 = s4.e3.o(-2).p + s0.e3.p + s2.e3.p
chord_37 = (IV['64'] % II.b.m)(piano__1=piano__1_37, piano__2=piano__2_37)

piano__0_38 = s2.hd.o(-2).p + s2.o(-3).p
piano__1_38 = s2.hd.o(-3).p + s0.o(-2).p
piano__2_38 = s0.e3.o(-2).p + s6.e3.o(-1).p + s0.e3.p + s4.e3.o(-1).p + s6.e3.o(-1).p + \
    s0.e3.p + s4.e3.o(-1).p + s6.e3.o(-1).p + s0.e3.p + \
    s2.e3.o(-2).p + s6.e3.o(-1).p + s0.e3.p
chord_38 = (V['7'] % II.b.m)(piano__0=piano__0_38,
                             piano__1=piano__1_38, piano__2=piano__2_38)

piano__0_39 = s0.h.o(-2).p
piano__1_39 = s4.h.o(-2).p
piano__2_39 = s0.e3.o(-1).p + s4.e3.p + s0.e3.o(1).p + \
    s2.e3.p + s4.e3.p + s0.e3.o(1).p
chord_39 = (I % II.b.m)(piano__0=piano__0_39,
                        piano__1=piano__1_39, piano__2=piano__2_39)

piano__0_40 = s4.o(-4).p
piano__1_40 = s2.mf
piano__2_40 = s4.e3.o(-3).p + s4.e3.o(-1).p + s6.e3.o(-1).p
chord_40 = (VII['43'] % II.b.m)(piano__0=piano__0_40,
                                piano__1=piano__1_40, piano__2=piano__2_40)

piano__0_41 = s0.o(-4).p
piano__1_41 = s4.o(-1).p
piano__2_41 = s0.e3.o(-3).p + s6.e3.o(-2).pp + s2.e3.o(-1).pp
chord_41 = (VII['7'] % VI.b.m)(piano__0=piano__0_41,
                               piano__1=piano__1_41, piano__2=piano__2_41)

piano__0_42 = s0.augment(frac(4, 3)).o(-3).p + s2.e3.o(-1).p + s4.e3.o(-1).p
piano__2_42 = s0.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).p + s0.mf
chord_42 = (V % II.b.m)(piano__0=piano__0_42, piano__2=piano__2_42)

piano__0_43 = l.e3 + s0.e3.o(-1).p + s2.e3.o(-1).p
piano__2_43 = s6.o(-1).mf
chord_43 = (VII['2'] % II.b.m)(piano__0=piano__0_43, piano__2=piano__2_43)

piano__0_44 = l.e3 + s0.e3.o(-1).p + s2.e3.o(-1).p
piano__2_44 = s4.o(-1).mf
chord_44 = (VII['43'] % II.b.m)(piano__0=piano__0_44, piano__2=piano__2_44)

piano__0_45 = s0.e3.o(-3).p + s2.e3.o(-1).p + r.e3 + s0.o(-1).mf
piano__2_45 = s0.q3.o(-2).p + s4.e3.o(-1).p + r.e3 + \
    s2.e3.o(-1).p + s4.e3.o(-1).p
chord_45 = (V % II.b.m)(piano__0=piano__0_45, piano__2=piano__2_45)

piano__0_46 = s6.o(-2).mf
piano__2_46 = r.e3 + s0.e3.o(-1).p + s2.e3.o(-1).p
chord_46 = (VII['2'] % II.b.m)(piano__0=piano__0_46, piano__2=piano__2_46)

piano__0_47 = s4.o(-2).p
piano__2_47 = r.e3 + s0.e3.o(-1).p + s2.e3.o(-1).p
chord_47 = (VII['43'] % II.b.m)(piano__0=piano__0_47, piano__2=piano__2_47)

piano__0_48 = s4.augment(frac(4, 3)).o(-3).p + s2.e3.p + \
    s4.e3.p + r.e3 + s2.e3.mf + s4.e3.mf + r.e3 + s2.e3.p + s4.e3.p
piano__2_48 = s4.e3.o(-2).p + s2.e3.p + s4.e3.p + \
    s0.o(1).mf + s2.o(1).mf + s0.o(1).mf
chord_48 = (I['64'] % II.b.m)(piano__0=piano__0_48, piano__2=piano__2_48)

piano__0_49 = s4.e3.o(-3).p + s2.e3.o(-1).p + \
    s4.e3.o(-1).p + s0.mf + s2.mf + s0.mf
piano__2_49 = s4.augment(frac(4, 3)).o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).p + \
    r.e3 + s2.e3.o(-1).p + s4.e3.o(-1).p + r.e3 + s2.e3.o(-1).p + s4.e3.o(-1).p
chord_49 = (I['64'] % II.b.m)(piano__0=piano__0_49, piano__2=piano__2_49)

piano__0_50 = s0.e3.o(-3).p + s1.e3.o(-1).p + s6.e3.o(-2).p + \
    s2.e3.o(-1).p + s1.e3.o(-1).p + r.augment(frac(7, 3))
piano__2_50 = s0.augment(frac(5, 3)).o(-2).p + s4.e3.o(-1).p + s2.e3.o(-1).p + \
    s6.e3.o(-1).p + s4.e3.o(-1).p + s1.e3.p + s6.e3.o(-1).p + s2.e3.p
chord_50 = (V['7'] % II.b.m)(piano__0=piano__0_50, piano__2=piano__2_50)

piano__0_51 = s4.e3.o(-3).p + s0.e3.p + s4.e3.o(-1).p + \
    r.e3 + s0.e3.p + r.augment(frac(7, 3))
piano__2_51 = s4.o(-2).p + s2.e3.p + r.e3 + s4.e3.p + s2.e3.p + \
    s0.e3.o(1).p + s4.e3.p + s2.e3.o(1).p + s0.e3.o(1).p + s4.e3.p
chord_51 = (I['64'] % II.b.m)(piano__0=piano__0_51, piano__2=piano__2_51)

piano__0_52 = s4.w.o(-3).p
piano__2_52 = s4.e3.o(-2).p + h6.e3.p + s2.e3.p + h9.e3.p + h6.e3.p + s0.e3.o(1).mf + \
    h9.e3.mf + s2.e3.o(1).mf + s0.e3.o(1).mf + \
    h6.e3.o(1).mf + s2.e3.o(1).mf + h9.e3.o(1).mf
chord_52 = (I['64'] % II.b.m)(piano__0=piano__0_52, piano__2=piano__2_52)

piano__0_53 = s0.w.o(-3).p
piano__2_53 = s0.e3.o(-2).p + s2.e3.mf + s1.e3.mf + s4.e3.mf + s2.e3.mf + s6.e3.f + \
    s4.e3.mf + s1.e3.o(1).f + s6.e3.f + s2.e3.o(1).f + \
    s1.e3.o(1).f + s4.e3.o(1).f
chord_53 = (V % II.b.m)(piano__0=piano__0_53, piano__2=piano__2_53)

piano__0_54 = l.augment(frac(11, 3)) + s4.e3.o(-1).f
piano__2_54 = s2.e3.o(1).f + s6.e3.f + s1.e3.o(1).f + s4.e3.f + s6.e3.f + \
    s2.e3.f + s4.e3.f + s1.e3.f + s2.e3.f + s6.e3.o(-1).f + s1.e3.f + r.e3
chord_54 = (V['7'] % II.b.m)(piano__0=piano__0_54, piano__2=piano__2_54)

piano__0_55 = s4.e3.o(-1).f + s0.e3.o(-1).f + s2.e3.o(-1).f + s6.e3.o(-2).f + \
    s0.e3.o(-1).mf + s4.e3.o(-2).f + \
    s6.e3.o(-2).mf + s2.q3.o(-2).f + s1.o(-2).f
piano__2_55 = r.augment(frac(8, 3)) + s4.e3.o(-2).mf + \
    r.e3 + s4.e3.o(-2).mf + s6.e3.o(-2).mf
chord_55 = (VII['43'] % II.b.m)(piano__0=piano__0_55, piano__2=piano__2_55)

piano__0_56 = s0.h.o(-3).p + s4.o(-2).mf
piano__2_56 = s0.e3.o(-2).p + s6.e3.o(-2).mf + s0.e3.o(-1).mf + s1.e3.o(-1).mf + \
    s0.e3.o(-1).mf + s6.e3.o(-2).mf + r.e3 + s6.e3.o(-2).mf + s1.e3.o(-1).mf
chord_56 = (V['7'] % II.b.m)(piano__0=piano__0_56, piano__2=piano__2_56)

piano__0_57 = s4.o(-2).mf
piano__2_57 = r.e3 + s0.e3.o(-1).mf + s2.e3.o(-1).mf
chord_57 = (IV['64'] % II.b.m)(piano__0=piano__0_57, piano__2=piano__2_57)

piano__0_58 = s0.h.o(-3).p
piano__2_58 = s0.e3.o(-2).p + s6.e3.o(-2).mf + s0.e3.o(-1).mf + \
    s1.e3.o(-1).mf + s0.e3.o(-1).mf + s6.e3.o(-2).mf
chord_58 = (V['7'] % II.b.m)(piano__0=piano__0_58, piano__2=piano__2_58)

piano__0_59 = s0.o(-1).mf
piano__2_59 = r.e3 + s2.e3.o(-1).mf + s4.e3.o(-1).mf
chord_59 = (I['6'] % II.M)(piano__0=piano__0_59, piano__2=piano__2_59)

piano__0_60 = s4.o(-2).mf
piano__2_60 = r.e3 + s0.e3.o(-1).mf + s2.e3.o(-1).mf
chord_60 = (IV['64'] % II.b.m)(piano__0=piano__0_60, piano__2=piano__2_60)

piano__0_61 = s0.h.o(-3).p + s1.o(-3).p + \
    s3.e3.o(-2).mf + s5.e3.o(-2).mf + r.e3
piano__2_61 = s0.e3.o(-2).p + s6.e3.o(-2).mf + s0.e3.o(-1).mf + s1.e3.o(-1).mf + s0.e3.o(-1).mf + \
    s6.e3.o(-2).mf + s1.e3.o(-2).p + s5.e3.o(-2).mf + \
    s3.e3.o(-1).mf + r.q3 + s3.e3.o(-1).mf
chord_61 = (V['7'] % II.b.m)(piano__0=piano__0_61, piano__2=piano__2_61)

piano__0_62 = s0.o(-3).pp
piano__2_62 = s0.e3.o(-2).pp + s2.e3.o(-1).mf + s4.e3.o(-1).mf
chord_62 = (IV % II.b.m)(piano__0=piano__0_62, piano__2=piano__2_62)

piano__0_63 = s0.e3.o(-1).mf + r.q3
piano__2_63 = r.e3 + s4.e3.o(-1).p + s6.e3.o(-1).p
chord_63 = (II['65'] % II.b.m)(piano__0=piano__0_63, piano__2=piano__2_63)

piano__0_64 = s0.o(-3).p
piano__2_64 = s0.e3.o(-2).p + s0.e3.o(-1).p + s2.e3.o(-1).p
chord_64 = (V % II.b.m)(piano__0=piano__0_64, piano__2=piano__2_64)

piano__0_65 = s4.e3.o(-2).p + s6.e3.o(-2).p + r.e3
piano__2_65 = r.q3 + s2.e3.o(-1).pp
chord_65 = (V['64'] % II.b.m)(piano__0=piano__0_65, piano__2=piano__2_65)

piano__0_66 = s0.hd.o(-1).p
piano__1_66 = s0.hd.o(-2).p
piano__2_66 = s4.e3.o(-2).p + s4.e3.o(-1).pp + s0.e3.pp + s4.e3.o(-1).p + \
    s0.e3.pp + s2.e3.pp + s4.e3.o(-1).p + s0.e3.pp + s2.e3.pp
chord_66 = (I % II.b.m)(piano__0=piano__0_66,
                        piano__1=piano__1_66, piano__2=piano__2_66)

piano__0_67 = s4.e3.o(-1).p + r.q3
piano__1_67 = s4.ed.p + s4.s.p
piano__2_67 = r.e3 + s0.e3.pp + s2.e3.pp
chord_67 = (I % II.b.m)(piano__0=piano__0_67,
                        piano__1=piano__1_67, piano__2=piano__2_67)

piano__0_68 = s2.o(-2).p + s0.e3.o(-1).pp + r.q3 + \
    s0.e3.o(-1).p + r.q3 + s0.e3.o(-1).p + r.q3
piano__1_68 = s2.hd.o(-3).p + s0.ed.p + s0.s.p
piano__2_68 = s0.e3.o(-2).p + s4.e3.o(-1).pp + s6.e3.o(-1).pp + r.e3 + s4.e3.o(-1).pp + \
    s6.e3.o(-1).pp + r.e3 + s4.e3.o(-1).pp + s6.e3.o(-1).pp + \
    r.e3 + s4.e3.o(-1).pp + s6.e3.o(-1).pp
chord_68 = (V['7'] % II.b.m)(piano__0=piano__0_68,
                             piano__1=piano__1_68, piano__2=piano__2_68)

piano__0_69 = s4.e3.o(-1).p + r.q3 + s4.e3.o(-1).p + r.q3
piano__1_69 = s0.h.o(-2).p
piano__2_69 = s0.e3.o(-1).p + s0.e3.pp + s2.e3.pp + r.e3 + s0.e3.pp + s2.e3.pp
chord_69 = (I % II.b.m)(piano__0=piano__0_69,
                        piano__1=piano__1_69, piano__2=piano__2_69)

piano__0_70 = s0.o(-3).p + s2.e3.o(-1).p + r.q3
piano__1_70 = s0.h.o(-2).p
piano__2_70 = r.e3 + s4.e3.o(-1).pp + s0.e3.pp + \
    r.e3 + s4.e3.o(-1).pp + s0.e3.pp
chord_70 = (IV % II.b.m)(piano__0=piano__0_70,
                         piano__1=piano__1_70, piano__2=piano__2_70)

piano__0_71 = s4.e3.o(-3).p + s4.e3.o(-1).pp + r.e3 + \
    s2.e3.o(-1).pp + s4.e3.o(-1).pp + r.e3
piano__1_71 = s2.h.p
piano__2_71 = s4.q3.o(-2).p + s0.e3.pp + r.q3 + s0.e3.pp
chord_71 = (I['64'] % III.M)(piano__0=piano__0_71,
                             piano__1=piano__1_71, piano__2=piano__2_71)

piano__0_72 = s0.e3.o(-3).p + s0.e3.o(-1).pp + r.e3 + \
    s6.e3.o(-2).pp + s0.e3.o(-1).pp + r.e3
piano__1_72 = s4.o(-1).p + s0.p
piano__2_72 = s0.q3.o(-2).p + s2.e3.o(-1).pp + r.q3 + s2.e3.o(-1).pp
chord_72 = (V['7'] % III.M)(piano__0=piano__0_72,
                            piano__1=piano__1_72, piano__2=piano__2_72)

piano__0_73 = s0.e3.o(-2).p + s4.e3.o(-1).pp + r.e3 + s4.e3.o(-1).pp + \
    r.q3 + s4.e3.o(-1).pp + r.q3 + s4.e3.o(-1).pp + r.q3
piano__1_73 = s0.q3.p + r.augment(frac(7, 3)) + s4.ed.mf + s4.s.p
piano__2_73 = s0.q3.o(-1).p + s0.e3.pp + r.e3 + s0.e3.pp + s2.e3.pp + \
    r.e3 + s0.e3.pp + s2.e3.pp + r.e3 + s0.e3.pp + s2.e3.pp
chord_73 = (I % III.M)(piano__0=piano__0_73,
                       piano__1=piano__1_73, piano__2=piano__2_73)

piano__0_74 = s2.o(-3).pp + s0.e3.o(-1).pp + r.q3 + \
    s0.e3.o(-1).pp + r.q3 + s0.e3.o(-1).pp + r.q3
piano__1_74 = s0.hd.mf + s0.ed.mf + s0.s.p
piano__2_74 = s2.e3.o(-2).pp + s4.e3.o(-1).pp + s6.e3.o(-1).pp + r.e3 + s4.e3.o(-1).pp + \
    s6.e3.o(-1).pp + r.e3 + s4.e3.o(-1).pp + s6.e3.o(-1).pp + \
    r.e3 + s4.e3.o(-1).pp + s6.e3.o(-1).pp
chord_74 = (V['65'] % III.M)(piano__0=piano__0_74,
                             piano__1=piano__1_74, piano__2=piano__2_74)

piano__0_75 = s4.e3.o(-1).pp + r.q3 + s4.e3.o(-1).pp + r.q3
piano__1_75 = s0.h.o(-2).pp
piano__2_75 = s0.e3.o(-1).pp + s0.e3.pp + s2.e3.pp + r.e3 + s0.e3.pp + s2.e3.pp
chord_75 = (I % III.M)(piano__0=piano__0_75,
                       piano__1=piano__1_75, piano__2=piano__2_75)

piano__0_76 = s2.e3.o(-1).pp + r.q3
piano__1_76 = s4.o(-3).pp
piano__2_76 = s4.e3.o(-2).pp + s6.e3.o(-1).p + s0.e3.p
chord_76 = (V % II.b.m)(piano__0=piano__0_76,
                        piano__1=piano__1_76, piano__2=piano__2_76)

piano__0_77 = s0.e3.p + r.q3
piano__1_77 = s0.o(-2).pp
piano__2_77 = s0.e3.o(-1).pp + s2.e3.p + s4.e3.p
chord_77 = (I % II.b.m)(piano__0=piano__0_77,
                        piano__1=piano__1_77, piano__2=piano__2_77)

piano__0_78 = s2.o(-2).p + s4.e3.o(-1).p + r.q3
piano__1_78 = s2.h.o(-3).p
piano__2_78 = s0.e3.o(-2).p + s6.e3.o(-1).p + s0.e3.p + \
    r.e3 + s6.e3.o(-1).p + s0.e3.p
chord_78 = (V['65'] % II.b.m)(piano__0=piano__0_78,
                              piano__1=piano__1_78, piano__2=piano__2_78)

piano__0_79 = s0.h.o(-2).pp
piano__1_79 = s4.h.o(-2).pp
piano__2_79 = s0.e3.o(-1).pp + s4.e3.pp + s0.e3.o(1).pp + \
    s2.e3.pp + s4.e3.pp + s0.e3.o(1).pp
chord_79 = (I % II.b.m)(piano__0=piano__0_79,
                        piano__1=piano__1_79, piano__2=piano__2_79)

piano__0_80 = s2.o(-3).p + s0.e3.pp + r.q3
piano__1_80 = s2.h.o(-2).p
piano__2_80 = r.e3 + s2.e3.pp + s4.e3.pp + r.e3 + s2.e3.pp + s4.e3.pp
chord_80 = (I['6'] % II.M)(piano__0=piano__0_80,
                           piano__1=piano__1_80, piano__2=piano__2_80)

piano__0_81 = s0.e3.o(-3).p + s6.e3.o(-1).pp + r.e3 + s2.e3.o(-1).pp + r.q3
piano__1_81 = s0.h.o(-2).p
piano__2_81 = r.q3 + s0.e3.pp + r.e3 + s6.e3.o(-1).pp + s0.e3.pp
chord_81 = (V % II.b.m)(piano__0=piano__0_81,
                        piano__1=piano__1_81, piano__2=piano__2_81)

piano__0_82 = s0.e3.o(-2).pp + s2.e3.pp + r.e3 + s0.e3.pp + \
    s2.e3.pp + r.e3 + s0.e3.pp + r.q3 + s0.e3.pp + h4.e3.pp + r.e3
piano__1_82 = s0.hd.o(1).p + s0.o(1).p
piano__2_82 = s0.q3.o(-1).pp + s4.e3.pp + r.q3 + s4.e3.pp + \
    r.e3 + h4.e3.pp + s4.e3.pp + r.q3 + s4.e3.pp
chord_82 = (I % II.b.m)(piano__0=piano__0_82,
                        piano__1=piano__1_82, piano__2=piano__2_82)

piano__0_83 = s6.e3.o(-2).pp + r.q3 + s6.e3.o(-2).p + \
    r.q3 + s4.o(-2).p + s6.e3.o(-2).mf + r.q3
piano__1_83 = s0.mf + s2.o(-3).p + r + s2.o(-3).p
piano__2_83 = r.e3 + s2.e3.o(-1).p + s4.e3.o(-1).pp + s2.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).p + \
    s4.e3.o(-3).p + s2.e3.o(-1).p + s4.e3.o(-1).p + \
    s2.e3.o(-2).p + s2.e3.o(-1).p + s4.e3.o(-1).p
chord_83 = (VI['6'] % IV.s.m)(piano__0=piano__0_83,
                              piano__1=piano__1_83, piano__2=piano__2_83)

piano__0_84 = s0.o(-3).p + s0.e3.o(-1).pp + r.q3 + \
    s0.e3.o(-1).pp + r.q3 + s0.e3.o(-1).pp + r.q3
piano__1_84 = s0.hd.p + s0.p
piano__2_84 = s0.e3.o(-2).p + s2.e3.o(-1).pp + s4.e3.o(-1).pp + r.e3 + s2.e3.o(-1).pp + \
    s4.e3.o(-1).pp + r.e3 + s2.e3.o(-1).pp + s4.e3.o(-1).pp + \
    r.e3 + s2.e3.o(-1).pp + s4.e3.o(-1).pp
chord_84 = (V % IV.s.m)(piano__0=piano__0_84,
                        piano__1=piano__1_84, piano__2=piano__2_84)

piano__0_85 = s4.e3.o(-1).pp + r.q3 + s4.e3.o(-1).p + r.q3
piano__1_85 = s5.mf + s0.o(-2).p
piano__2_85 = r.e3 + s0.e3.p + s2.e3.p + s0.e3.o(-1).p + s0.e3.p + s2.e3.p
chord_85 = (I % IV.s.m)(piano__0=piano__0_85,
                        piano__1=piano__1_85, piano__2=piano__2_85)

piano__0_86 = s4.e3.o(-1).p + r.q3 + s4.e3.o(-1).mf + r.q3
piano__1_86 = s2.o(-2).p + s0.o(-2).p
piano__2_86 = s2.e3.o(-1).p + s0.e3.p + s2.e3.p + \
    s0.e3.o(-1).p + s0.e3.p + s2.e3.pp
chord_86 = (I % IV.s.m)(piano__0=piano__0_86,
                        piano__1=piano__1_86, piano__2=piano__2_86)

piano__0_87 = s0.o(-3).pp + s0.e3.o(-1).pp + r.q3
piano__1_87 = s0.h.mf
piano__2_87 = s0.e3.o(-2).pp + s2.e3.o(-1).pp + \
    s4.e3.o(-1).pp + r.e3 + s2.e3.o(-1).pp + s4.e3.o(-1).pp
chord_87 = (V % IV.s.m)(piano__0=piano__0_87,
                        piano__1=piano__1_87, piano__2=piano__2_87)

piano__0_88 = s0.o(-3).p + s4.e3.o(-1).pp + r.q3
piano__1_88 = s0.h.o(-2).p
piano__2_88 = r.e3 + s0.e3.pp + s2.e3.pp + r.e3 + s0.e3.pp + s2.e3.pp
chord_88 = (I % IV.s.m)(piano__0=piano__0_88,
                        piano__1=piano__1_88, piano__2=piano__2_88)

piano__0_89 = s2.o(-3).p + s0.e3.o(-1).pp + r.q3 + s0.e3.o(-1).pp + r.q3
piano__1_89 = s0.hd.p
piano__2_89 = s2.e3.o(-2).p + s4.e3.o(-1).pp + s6.e3.o(-1).pp + r.e3 + \
    s4.e3.o(-1).pp + s6.e3.o(-1).pp + r.e3 + s4.e3.o(-1).pp + s6.e3.o(-1).pp
chord_89 = (V['65'] % III.M)(piano__0=piano__0_89,
                             piano__1=piano__1_89, piano__2=piano__2_89)

piano__0_90 = s0.e3.o(-2).p + s0.e3.pp + r.e3
piano__1_90 = s4.p
piano__2_90 = s0.q3.o(-1).p + s2.e3.pp
chord_90 = (I % III.M)(piano__0=piano__0_90,
                       piano__1=piano__1_90, piano__2=piano__2_90)

piano__0_91 = s4.o(-3).p
piano__1_91 = s2.p
piano__2_91 = s4.e3.o(-2).p + s6.e3.o(-1).pp + s1.e3.pp
chord_91 = (IV['43'] % II.b.m)(piano__0=piano__0_91,
                               piano__1=piano__1_91, piano__2=piano__2_91)

piano__0_92 = s2.e3.o(-3).pp + s2.e3.o(-1).pp + r.e3
piano__1_92 = s6.o(-1).p
piano__2_92 = s2.q3.o(-2).pp + s4.e3.o(-1).pp
chord_92 = (VII['65'] % II.b.m)(piano__0=piano__0_92,
                                piano__1=piano__1_92, piano__2=piano__2_92)

piano__0_93 = s2.e3.o(-3).p + s4.e3.o(-1).pp + r.e3
piano__1_93 = s0.p
piano__2_93 = s2.q3.o(-2).p + s6.e3.o(-1).pp
chord_93 = (V['65'] % II.b.m)(piano__0=piano__0_93,
                              piano__1=piano__1_93, piano__2=piano__2_93)

piano__0_94 = s0.e3.o(-2).pp + s0.e3.pp + r.e3
piano__1_94 = s4.p
piano__2_94 = s0.q3.o(-1).pp + s2.e3.pp
chord_94 = (I % II.b.m)(piano__0=piano__0_94,
                        piano__1=piano__1_94, piano__2=piano__2_94)

piano__0_95 = s6.e3.o(-4).p + s1.e3.o(-1).p + r.e3 + \
    s4.e3.o(-2).p + s1.e3.o(-1).p + r.e3
piano__1_95 = s6.h.o(-3).p
piano__2_95 = r.q3 + s2.e3.o(-1).p + r.q3 + s2.e3.o(-1).p
chord_95 = (VII['2'] % II.b.m)(piano__0=piano__0_95,
                               piano__1=piano__1_95, piano__2=piano__2_95)

piano__0_96 = s0.o(-3).p
piano__1_96 = s0.o(-2).p
piano__2_96 = r.e3 + s3.e3.o(-1).p + s4.e3.o(-1).p
chord_96 = (V % II.b.m)(piano__0=piano__0_96,
                        piano__1=piano__1_96, piano__2=piano__2_96)

piano__0_97 = s6.e3.o(-4).p + s3.e3.o(-1).p + r.e3
piano__1_97 = s6.o(-3).p
piano__2_97 = r.q3 + s4.e3.o(-1).p
chord_97 = (V['2'] % II.b.m)(piano__0=piano__0_97,
                             piano__1=piano__1_97, piano__2=piano__2_97)

piano__0_98 = s4.o(-3).p + s4.e3.o(-1).pp + r.q3
piano__1_98 = s4.h.o(-2).p
piano__2_98 = r.e3 + s0.e3.pp + s2.e3.pp + r.e3 + s0.e3.pp + s2.e3.pp
chord_98 = (I['64'] % II.b.m)(piano__0=piano__0_98,
                              piano__1=piano__1_98, piano__2=piano__2_98)

piano__0_99 = s0.e3.o(-3).p + s2.e3.o(-1).pp + r.e3
piano__1_99 = s0.o(-2).p
piano__2_99 = r.q3 + s4.e3.o(-1).pp
chord_99 = (V % II.b.m)(piano__0=piano__0_99,
                        piano__1=piano__1_99, piano__2=piano__2_99)

piano__0_100 = s6.e3.o(-2).pp + r.q3
piano__2_100 = r.e3 + s2.e3.o(-1).pp + s4.e3.o(-1).pp
chord_100 = (V['7'] % II.b.m)(piano__0=piano__0_100, piano__2=piano__2_100)

piano__0_101 = s0.e3.o(-2).pp + s4.e3.o(-1).pp + r.e3 + s4.e3.o(-1).pp + r.q3
piano__1_101 = s4.h.o(-2).p
piano__2_101 = r.q3 + s0.e3.pp + r.e3 + s0.e3.pp + s2.e3.pp
chord_101 = (I % II.b.m)(piano__0=piano__0_101,
                         piano__1=piano__1_101, piano__2=piano__2_101)

piano__0_102 = s4.e3.o(-1).pp + r.q3 + s4.e3.o(-1).pp + \
    r.augment(frac(5, 12)) + s4.s.o(-2).p
piano__2_102 = r.e3 + s0.e3.pp + s2.e3.pp + r.e3 + s0.e3.pp + s2.e3.pp
chord_102 = (I['64'] % II.b.m)(piano__0=piano__0_102, piano__2=piano__2_102)

piano__0_103 = s2.o(-3).pp + s0.e3.o(-1).pp + r.q3 + s0.e3.o(-1).pp + \
    r.q3 + s0.e3.o(-1).pp + r.augment(frac(5, 12)) + s0.s.o(-2).p
piano__2_103 = r.e3 + s4.e3.o(-1).pp + s6.e3.o(-1).pp + r.e3 + s4.e3.o(-1).pp + s6.e3.o(-1).pp + \
    r.e3 + s4.e3.o(-1).pp + s6.e3.o(-1).pp + r.e3 + \
    s4.e3.o(-1).pp + s6.e3.o(-1).pp
chord_103 = (V['7'] % II.b.m)(piano__0=piano__0_103, piano__2=piano__2_103)

piano__0_104 = s0.hd.o(-2).pp
piano__2_104 = r.e3 + s2.e3.pp + s0.e3.pp + s4.e3.p + s2.e3.p + \
    s0.e3.o(1).p + s4.e3.p + s2.e3.o(1).p + s0.e3.o(1).p
chord_104 = (I % II.b.m)(piano__0=piano__0_104, piano__2=piano__2_104)

piano__0_105 = s4.ed.o(-2).p + s4.s.o(-2).p
piano__2_105 = s4.e3.o(1).mf + s2.e3.o(1).mf + s0.e3.o(1).mf
chord_105 = (I['64'] % II.b.m)(piano__0=piano__0_105, piano__2=piano__2_105)

piano__0_106 = s0.h.o(-3).pp + s4.e3.o(-1).mf + r.e3 + \
    s1.e3.o(-1).p + s2.ed.o(-1).p + s0.s.o(-2).p
piano__2_106 = s2.e3.mf + s4.e3.mf + s1.e3.mf + s2.e3.mf + \
    s6.e3.o(-1).mf + s1.e3.mf + r.e3 + s6.e3.o(-1).p + \
    r.q3 + s0.e3.o(-1).p + s6.e3.o(-2).p
chord_106 = (V['7'] % II.b.m)(piano__0=piano__0_106, piano__2=piano__2_106)

piano__0_107 = s0.hd.o(-2).pp
piano__2_107 = s0.e3.p + s2.e3.pp + s0.e3.p + s4.e3.p + s2.e3.p + \
    s0.e3.o(1).p + s4.e3.mf + s2.e3.o(1).mf + s0.e3.o(1).mf
chord_107 = (I % II.b.m)(piano__0=piano__0_107, piano__2=piano__2_107)

piano__0_108 = s4.ed.o(-2).p + s4.s.o(-2).p
piano__2_108 = s4.e3.o(1).mf + s2.e3.o(1).mf + s0.e3.o(1).mf
chord_108 = (I['64'] % II.b.m)(piano__0=piano__0_108, piano__2=piano__2_108)

piano__0_109 = s0.h.o(-3).pp + s4.e3.o(-1).p + s6.e3.o(-1).p + \
    s1.e3.o(-1).p + s2.ed.o(-1).p + s0.s.o(-2).p
piano__2_109 = s2.e3.mf + s4.e3.mf + s1.e3.mf + s2.e3.mf + \
    s6.e3.o(-1).p + s1.e3.p + r.augment(frac(4, 3)) + \
    s0.e3.o(-1).pp + s6.e3.o(-2).pp
chord_109 = (V % II.b.m)(piano__0=piano__0_109, piano__2=piano__2_109)

piano__0_110 = s0.e3.o(-2).pp + s4.e3.o(-1).p + s0.e3.p + r.q3 + s4.e3.o(-1).p + \
    s0.e3.o(-1).p + s2.e3.o(-1).p + r.q3 + s4.e3.o(-1).p + s2.e3.o(-1).p
piano__2_110 = s0.e3.p + r.q3 + s2.e3.p + \
    s0.e3.p + r + s4.e3.o(-1).p + s0.e3.p + r.q3
chord_110 = (I % II.b.m)(piano__0=piano__0_110, piano__2=piano__2_110)


score = chord_0 + chord_1 + chord_2 + chord_3 + chord_4 + chord_5 + chord_6 + chord_7 + chord_8 + chord_9 + chord_10 + chord_11 + chord_12 + chord_13 + chord_14 + chord_15 + chord_16 + chord_17 + chord_18 + chord_19 + chord_20 + chord_21 + chord_22 + chord_23 + chord_24 + chord_25 + chord_26 + chord_27 + chord_28 + chord_29 + chord_30 + chord_31 + chord_32 + chord_33 + chord_34 + chord_35 + chord_36 + chord_37 + chord_38 + chord_39 + chord_40 + chord_41 + chord_42 + chord_43 + chord_44 + chord_45 + chord_46 + chord_47 + chord_48 + chord_49 + chord_50 + chord_51 + chord_52 + chord_53 + chord_54 + chord_55 + \
    chord_56 + chord_57 + chord_58 + chord_59 + chord_60 + chord_61 + chord_62 + chord_63 + chord_64 + chord_65 + chord_66 + chord_67 + chord_68 + chord_69 + chord_70 + chord_71 + chord_72 + chord_73 + chord_74 + chord_75 + chord_76 + chord_77 + chord_78 + chord_79 + chord_80 + chord_81 + chord_82 + chord_83 + \
    chord_84 + chord_85 + chord_86 + chord_87 + chord_88 + chord_89 + chord_90 + chord_91 + chord_92 + chord_93 + chord_94 + chord_95 + chord_96 + chord_97 + \
    chord_98 + chord_99 + chord_100 + chord_101 + chord_102 + chord_103 + \
    chord_104 + chord_105 + chord_106 + chord_107 + chord_108 + chord_109 + chord_110

score.to_midi(FILENAME, tempo=TEMPO)
