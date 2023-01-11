from musiclang.core.library import *
from fractions import Fraction as frac

# GLOBAL SCORE VARIABLES

TEMPO = 120
FILENAME = "locals/test.mid"  # REPLACE WITH YOUR DESTINATION

###

piano__0_0 = s0.o(-1).p + r.hd
piano__1_0 = s4.o(-1).p + r.hd
piano__3_0 = s0.mf + r.hd
piano__4_0 = s2.o(1).p + r + s0.o(1).pp + s1.o(1).pp
piano__5_0 = s4.o(1).p + r + s2.o(1).p + s3.o(1).p
piano__7_0 = s0.o(2).mf + r + s3.s.o(2).mf + s2.s.o(2).p + s1.s.o(2).p + \
    s2.s.o(2).p + s4.s.o(2).mf + s3.s.o(2).p + s2.s.o(2).p + s3.s.o(2).p
chord_0 = (I % II.M)(piano__0=piano__0_0, piano__1=piano__1_0, piano__3=piano__3_0,
                     piano__4=piano__4_0, piano__5=piano__5_0, piano__7=piano__7_0)

piano__4_1 = s2.o(1).pp + r.hd
piano__5_1 = s4.o(1).p + r.hd
piano__7_1 = s4.o(2).mf + r + s4.t.o(2).p + r.sd + s5.t.o(2).p + \
    r.sd + s6.t.o(2).p + r.sd + s0.t.o(3).p + r.sd
chord_1 = (I % II.M)(piano__4=piano__4_1,
                     piano__5=piano__5_1, piano__7=piano__7_1)

piano__3_2 = s2.e.pp + r.e + s0.e.pp + r.e + \
    s1.e.pp + r.e + s4.t.pp + r.augment(frac(7, 8))
piano__4_2 = r.e + s0.e.o(1).pp + r.e + s0.e.o(1).pp + \
    r.e + s0.e.o(1).pp + r.e + s6.t.pp + r.sd
piano__7_2 = s4.o(2).p + s2.o(2).p + s4.s.o(2).p + s3.s.o(2).p + \
    s2.s.o(2).p + s3.s.o(2).p + s4.t.o(2).p + r.sd + s3.t.o(2).p + r.sd
chord_2 = (I % II.M)(piano__3=piano__3_2,
                     piano__4=piano__4_2, piano__7=piano__7_2)

piano__3_3 = s4.o(-1).p + r.hd
piano__4_3 = s4.p + r + s4.pp + s5.pp
piano__5_3 = r.h + s6.p + s0.o(1).p
piano__7_3 = h10.e.o(1).p + s6.e.o(1).p + r + s0.s.o(2).mf + s6.s.o(1).p + s5.s.o(
    1).p + s6.s.o(1).p + s1.s.o(2).mf + s0.s.o(2).p + s6.s.o(1).p + s0.s.o(2).p
chord_3 = (IV[7] % II.M)(piano__3=piano__3_3, piano__4=piano__4_3,
                         piano__5=piano__5_3, piano__7=piano__7_3)

piano__8_4 = s4.o(2).mf + r + s4.t.o(2).p + r.sd + s5.t.o(2).p + \
    r.sd + s6.t.o(2).p + r.sd + s0.t.o(3).p + r.sd
piano__5_4 = s2.o(1).pp + r.hd
piano__7_4 = s4.o(1).p + r.hd
chord_4 = (I % II.M)(piano__8=piano__8_4,
                     piano__5=piano__5_4, piano__7=piano__7_4)

piano__8_5 = s4.o(2).p + r + s4.s.o(2).p + r.ed + \
    s4.s.o(2).p + s3.s.o(2).p + r.e
piano__3_5 = s2.e.pp + r.e + s0.e.pp + r.e + s1.e.pp + r.e + s4.e.pp + r.e
piano__4_5 = r.e + s0.e.o(1).pp + r.e + s0.e.o(1).pp + \
    r.e + s0.e.o(1).pp + r.e + s6.e.pp
piano__7_5 = r + s2.o(2).p + r.s + s3.s.o(2).p + s2.s.o(2).p + \
    s3.s.o(2).p + r.e + s2.s.o(2).p + s1.s.o(2).p
chord_5 = (I % II.M)(piano__8=piano__8_5, piano__3=piano__3_5,
                     piano__4=piano__4_5, piano__7=piano__7_5)

piano__4_6 = s0.s.o(1).pp + r.ed + s0.s.o(1).pp + r.ed + s0.s.o(1).pp + \
    r.augment(frac(5, 8)) + s0.s.o(1).pp + r.ed + s1.t.o(1).pp
piano__5_6 = r.e + s2.s.o(1).pp + r.s + s4.s.o(1).p + r.s + s2.s.o(1).pp + \
    r.augment(frac(5, 8)) + s2.s.o(1).pp + r.ed + s2.s.o(1).pp + r.sd
piano__7_6 = s0.s.o(2).p + r.augment(frac(7, 4)) + s2.t.o(2).p + s3.t.o(2).p + s2.t.o(2).p + s3.s.o(2).p + \
    s2.t.o(2).p + s3.t.o(2).p + s2.s.o(2).p + s3.t.o(2).p + \
    s2.t.o(2).p + s1.s.o(2).p + s0.s.o(2).p + s6.t.o(1).p
chord_6 = (I % II.M)(piano__4=piano__4_6,
                     piano__5=piano__5_6, piano__7=piano__7_6)

piano__3_7 = r.augment(frac(31, 8)) + s0.t.pp
piano__4_7 = l.t + r.ed + s4.s.pp + r.ed + s4.sd.p + \
    r.augment(frac(5, 8)) + s4.s.pp + s3.s.pp + s2.s.pp + s1.sd.pp
piano__5_7 = r.sd + s6.s.pp + r.s + \
    s0.s.o(1).p + r.s + s6.s.pp + r.e + s5.s.pp + s6.s.pp + s5.sd.pp + r
piano__7_7 = l.t + r.augment(frac(7, 4)) + \
    s4.s.o(1).p + r.augment(frac(7, 4)) + s4.t.o(1).p
chord_7 = (V[7] % II.M)(piano__3=piano__3_7, piano__4=piano__4_7,
                        piano__5=piano__5_7, piano__7=piano__7_7)

piano__3_8 = l.t + r.augment(frac(7, 8)) + s0.s.pp + \
    r.augment(frac(13, 8)) + s6.s.o(-1).pp + r.ed + s5.t.o(-1).pp
piano__4_8 = l.t + r.sd + s2.s.pp + r.ed + s2.s.pp + r.s + \
    s0.s.pp + r.s + s2.s.pp + r.augment(frac(5, 8)) + s2.s.pp + r.sd
piano__5_8 = r + s0.s.o(1).p + r.augment(frac(11, 4))
piano__7_8 = l.t + r.augment(frac(15, 8)) + \
    s6.t.o(1).p + r.qd + s4.s.o(1).p + s3.t.o(1).p
piano__8_8 = r.augment(frac(17, 8)) + s0.t.o(2).p + s6.s.o(1).p + s0.t.o(2).p + s6.t.o(
    1).p + s0.t.o(2).p + s6.s.o(1).p + s0.t.o(2).p + s6.t.o(1).p + s5.sd.o(1).p + r.s
chord_8 = (V[7] % II.M)(piano__3=piano__3_8, piano__4=piano__4_8,
                        piano__5=piano__5_8, piano__7=piano__7_8, piano__8=piano__8_8)

piano__1_9 = r.augment(frac(17, 8)) + s0.sd.pp + r.qd
piano__3_9 = l.t + r.ed + s2.s.pp + r.ed + s2.sd.p + \
    r.t + s1.s.pp + s2.s.pp + s3.sd.pp + r.ed
piano__4_9 = l.t + r.s + \
    s0.s.o(1).pp + r.ed + s0.s.o(1).pp + r.qd + \
    s4.s.pp + s5.s.p + s6.s.p + s0.t.o(1).p
piano__5_9 = r.augment(frac(7, 8)) + s4.s.o(1).p + r.augment(frac(23, 8))
piano__7_9 = l.t + r.augment(frac(7, 4)) + \
    s2.s.o(2).p + r.augment(frac(7, 4)) + s2.t.o(2).p
chord_9 = (I % II.M)(piano__1=piano__1_9, piano__3=piano__3_9,
                     piano__4=piano__4_9, piano__5=piano__5_9, piano__7=piano__7_9)

piano__8_10 = r.augment(frac(5, 8)) + s2.s.o(2).p + s3.s.o(2).p + s4.s.o(2).p + s5.s.o(
    2).p + s6.s.o(2).p + s0.s.o(3).p + s6.s.o(2).p + s5.s.o(2).p + s4.sd.o(2).p + r
piano__3_10 = l.t + r.augment(frac(9, 4)) + s2.s.pp + \
    r.s + s2.s.pp + r.s + s2.s.pp + r.s + s3.t.pp
piano__4_10 = l.augment(frac(7, 8)) + r.qd + s4.s.pp + \
    r.s + s4.s.pp + r.s + s4.s.pp + r.s + s5.t.p
piano__7_10 = l.t + s0.s.o(2).p + s1.sd.o(2).p + r.augment(frac(17, 8)) + \
    s3.s.o(2).p + s2.s.o(2).p + s1.s.o(2).p + s0.s.o(2).p + s1.t.o(2).p
chord_10 = (I % II.M)(piano__8=piano__8_10, piano__3=piano__3_10,
                      piano__4=piano__4_10, piano__7=piano__7_10)

piano__3_11 = l.augment(frac(7, 8)) + r.qd + s2.s.pp + \
    r.s + s2.s.pp + r.augment(frac(7, 8))
piano__4_11 = l.augment(frac(7, 8)) + r.qd + s4.s.pp + \
    r.s + s4.s.pp + r.s + h4.s.pp + r.s + s3.t.p
piano__5_11 = r.augment(frac(27, 8)) + s4.s.pp + s4.sd.o(1).p
piano__7_11 = l.t + s1.s.o(2).p + s0.s.o(2).p + h11.s.o(1).p + s0.s.o(2).p + s1.s.o(2).p + s2.sd.o(2).p + r.augment(
    frac(5, 8)) + s2.s.o(2).p + s1.s.o(2).p + s0.s.o(2).p + s6.s.o(1).p + s5.sd.o(1).p + r.t + s5.t.o(1).p
piano__8_11 = r.augment(frac(13, 8)) + s3.s.o(2).p + \
    s4.s.o(2).p + s3.sd.o(2).p + r.qd
chord_11 = (II % II.M)(piano__3=piano__3_11, piano__4=piano__4_11,
                       piano__5=piano__5_11, piano__7=piano__7_11, piano__8=piano__8_11)

piano__1_12 = r.augment(frac(11, 8)) + s3.s.o(-1).pp + r.s + \
    s2.e.o(-1).p + s0.e.o(-1).p + s3.s.o(-1).p + r.augment(frac(7, 8))
piano__3_12 = l.sd + s6.e.o(-1).pp + s5.s.o(-1).pp + \
    r.augment(frac(9, 4)) + s5.s.o(-1).p + r.sd
piano__4_12 = l.sd + r.augment(frac(7, 2)) + s0.t.p
piano__5_12 = r.augment(frac(5, 8)) + s0.sd.o(1).pp + r.hd
piano__7_12 = l.t + s3.s.o(1).p + s2.sd.o(1).p + r.t + s3.s.o(1).p + \
    r.qd + s4.sd.o(1).p + r.sd + s4.s.o(1).p + s3.s.o(1).p + s2.t.o(1).p
piano__8_12 = r.augment(frac(15, 8)) + s6.s.o(1).p + s0.s.o(2).p + \
    s6.sd.o(1).p + r.t + s6.s.o(1).p + s5.sd.o(1).p + r.e
chord_12 = (V[7] % II.M)(piano__1=piano__1_12, piano__3=piano__3_12, piano__4=piano__4_12,
                         piano__5=piano__5_12, piano__7=piano__7_12, piano__8=piano__8_12)

piano__1_13 = r.augment(frac(11, 8)) + s3.s.o(-1).p + r.s + \
    s2.e.o(-1).p + s0.e.o(-1).p + s3.s.o(-1).p + r.ed + s0.t.o(-1).p
piano__3_13 = l.sd + s6.e.o(-1).p + s5.s.o(-1).p + \
    r.augment(frac(9, 4)) + s5.s.o(-1).p + r.s + s4.t.o(-1).p
piano__4_13 = l.sd + r.augment(frac(7, 2)) + s0.t.p
piano__5_13 = r.augment(frac(5, 8)) + s0.sd.o(1).p + r.hd
piano__7_13 = l.t + s3.s.o(1).p + s2.sd.o(1).p + r.t + s3.s.o(1).p + \
    r.qd + s4.sd.o(1).p + r.sd + s4.s.o(1).p + s3.s.o(1).p + s2.t.o(1).mf
piano__8_13 = r.augment(frac(15, 8)) + s6.s.o(1).mf + s0.s.o(2).p + \
    s6.sd.o(1).p + r.t + s6.s.o(1).mf + s5.sd.o(1).p + r.e
chord_13 = (V[7] % II.M)(piano__1=piano__1_13, piano__3=piano__3_13, piano__4=piano__4_13,
                         piano__5=piano__5_13, piano__7=piano__7_13, piano__8=piano__8_13)

piano__1_14 = l.sd + r.e + \
    s0.e.o(-1).p + r.e + s4.e.o(-2).p + r.e + \
    s0.e.o(-1).p + r.augment(frac(5, 8))
piano__3_14 = l.sd + r.e + \
    s2.e.o(-1).p + r.e + s1.e.o(-1).p + r.e + \
    s2.e.o(-1).p + r.augment(frac(5, 8))
piano__4_14 = l.sd + r.e + \
    s4.e.o(-1).p + r.e + s4.e.o(-1).mf + r.e + \
    s4.e.o(-1).mf + r.augment(frac(5, 8))
piano__5_14 = r.augment(frac(5, 8)) + s4.s.mf + r.augment(frac(25, 8))
piano__7_14 = l.t + s1.s.o(1).mf + s6.s.mf + r + s0.s.o(1).mf + s6.s.mf + \
    s1.s.o(1).mf + s6.s.mf + s4.s.mf + r.ed + s0.s.o(1).mf + s6.t.mf
piano__8_14 = r.augment(frac(7, 8)) + s2.s.o(1).mf + s4.s.o(1).mf + s2.s.o(1).mf + \
    r.augment(frac(5, 4)) + s2.s.o(1).mf + s4.s.o(1).mf + \
    s2.s.o(1).mf + r.s + s1.t.o(1).f
chord_14 = (IV % VI.M)(piano__1=piano__1_14, piano__3=piano__3_14, piano__4=piano__4_14,
                       piano__5=piano__5_14, piano__7=piano__7_14, piano__8=piano__8_14)

piano__1_15 = l.sd + s0.s.o(-1).p + r.s + s0.s.o(-1).p + r.s + s0.s.o(-1).p + \
    r.s + s0.augment(frac(7, 8)).o(-1).p + r.augment(frac(5, 4))
piano__2_15 = r.sd + s4.s.o(-1).p + r.s + s2.s.o(-1).p + r.s + s2.s.o(-1).p + \
    r.s + s2.augment(frac(7, 8)).o(-1).p + r.augment(frac(5, 4))
piano__3_15 = l.sd + s2.s.o(-1).p + r.s + s4.s.o(-1).p + r.s + s4.s.o(-1).p + \
    r.s + s4.augment(frac(7, 8)).o(-1).p + r.augment(frac(5, 4))
piano__4_15 = l.sd + s0.s.p + r.s + s0.s.p + r.s + s0.s.p + r.s + \
    s0.augment(frac(7, 8)).p + r.augment(frac(9, 8)) + s0.t.pp
piano__7_15 = l.t + r.s + s2.s.o(1).p + r.s + s2.s.o(1).p + r.s + s2.s.o(1).p + r.s + s2.augment(
    frac(7, 8)).o(1).p + s3.t.o(1).p + s2.s.o(1).p + s1.s.o(1).pp + s2.s.o(1).pp + s3.s.o(1).pp + r.t
piano__8_15 = l.t + r.s + s4.s.o(1).p + r.s + s4.s.o(1).p + r.s + s4.s.o(
    1).p + r.s + s4.augment(frac(7, 8)).o(1).p + r.augment(frac(9, 8)) + h6.t.o(1).p
piano__10_15 = r.sd + s0.s.o(2).mf + r.s + s0.s.o(2).mf + r.s + s0.s.o(
    2).mf + r.s + s0.augment(frac(7, 8)).o(2).mf + r.augment(frac(5, 4))
chord_15 = (I % VI.M)(piano__1=piano__1_15, piano__2=piano__2_15, piano__3=piano__3_15,
                      piano__4=piano__4_15, piano__7=piano__7_15, piano__8=piano__8_15, piano__10=piano__10_15)

piano__4_16 = l.sd + r.e + s1.e.pp + s3.e.pp + \
    s2.e.pp + r.e + s0.e.pp + s2.e.pp + s1.t.pp
piano__5_16 = r.sd + s2.e.pp + r.qd + s4.e.pp + r.augment(frac(9, 8))
piano__7_16 = l.t + r.augment(frac(15, 4)) + s2.t.o(1).p
piano__8_16 = l.sd + s4.e.o(1).p + r.e + s4.e.o(1).pp + \
    r + s5.e.o(1).p + s4.e.o(1).p + r.t
piano__10_16 = r.augment(frac(15, 8)) + s0.e.o(2).p + \
    s6.e.o(1).p + r.augment(frac(9, 8))
chord_16 = (I % VI.M)(piano__4=piano__4_16, piano__5=piano__5_16,
                      piano__7=piano__7_16, piano__8=piano__8_16, piano__10=piano__10_16)

piano__3_17 = l.sd + r.augment(frac(5, 2)) + \
    s0.e.o(-1).pp + r.augment(frac(5, 8))
piano__4_17 = l.sd + r.e + s6.e.o(-1).pp + s4.e.o(-1).pp + \
    s2.e.o(-1).pp + s4.e.o(-1).pp + r.e + s6.e.o(-1).pp + s5.t.o(-1).pp
piano__5_17 = r.sd + s1.e.pp + r.hd + s2.t.p
piano__7_17 = l.sd + s6.e.p + r.qd + s6.e.p + s5.e.p + s4.e.p + r.t
piano__8_17 = l.sd + r + s6.e.pp + s0.e.o(1).p + r.augment(frac(13, 8))
chord_17 = (V[7] % VI.M)(piano__3=piano__3_17, piano__4=piano__4_17,
                         piano__5=piano__5_17, piano__7=piano__7_17, piano__8=piano__8_17)

piano__3_18 = l.sd + r.augment(frac(5, 2)) + \
    s5.e.o(-1).pp + r.e + s4.t.o(-1).pp
piano__4_18 = l.sd + r.e + s6.e.o(-1).pp + r.e + s0.e.pp + r + s0.e.pp + r.t
piano__5_18 = l.sd + s4.e.pp + r.e + s4.e.pp + \
    r.e + s4.e.pp + r.augment(frac(9, 8))
piano__7_18 = l.sd + s0.e.o(1).p + r.e + s1.e.o(1).p + \
    h3.e.o(1).p + s2.e.o(1).p + r + s2.t.o(1).p
piano__8_18 = l.sd + r.augment(frac(23, 8)) + s4.t.o(1).p + s3.e.o(1).p + r.t
chord_18 = (I[7] % VI.M)(piano__3=piano__3_18, piano__4=piano__4_18,
                         piano__5=piano__5_18, piano__7=piano__7_18, piano__8=piano__8_18)

piano__8_19 = l.sd + r + s3.s.o(1).p + s2.s.o(1).p + \
    r + s3.s.o(1).p + r.s + h6.s.o(1).p + r.s + h6.t.o(1).p
piano__3_19 = l.sd + r.qd + s4.o(-1).pp + r.augment(frac(9, 8))
piano__4_19 = l.sd + s0.e.pp + s2.e.pp + s0.e.pp + s6.o(-1).pp + r + s0.t.pp
piano__7_19 = l.augment(frac(11, 8)) + r.e + s1.e.o(1).p + \
    s2.s.o(1).p + r.augment(frac(11, 8))
chord_19 = (I[7] % VI.M)(piano__8=piano__8_19, piano__3=piano__3_19,
                         piano__4=piano__4_19, piano__7=piano__7_19)

piano__4_20 = l.sd + s2.e.pp + s1.e.pp + r.e + \
    s2.e.pp + r.e + s0.e.pp + s2.s.pp + r.s + s1.t.pp
piano__5_20 = l.sd + r + s3.e.pp + r.e + s4.s.pp + r.augment(frac(11, 8))
piano__7_20 = l.augment(frac(11, 8)) + r.augment(frac(5, 2)) + s2.t.o(1).p
piano__8_20 = l.sd + s4.e.o(1).p + r.augment(frac(5, 8)) + s4.t.o(
    1).pp + h6.t.o(1).pp + s4.t.o(1).pp + r.qd + s4.s.o(1).p + r.sd
piano__10_20 = r.augment(frac(11, 8)) + s5.t.o(1).pp + r.sd + s0.s.o(2).p + \
    r.s + s6.s.o(1).p + r.s + s5.s.o(1).p + r.augment(frac(7, 8))
chord_20 = (I % VI.M)(piano__4=piano__4_20, piano__5=piano__5_20,
                      piano__7=piano__7_20, piano__8=piano__8_20, piano__10=piano__10_20)

piano__3_21 = l.sd + r.qd + \
    s2.e.o(-1).pp + r.e + s0.e.o(-1).pp + r.augment(frac(5, 8))
piano__4_21 = l.sd + r + \
    s4.e.o(-1).pp + r.e + s4.s.o(-1).pp + r.ed + \
    s2.s.o(-1).pp + r.s + s3.t.o(-1).pp
piano__5_21 = l.sd + s1.e.pp + s6.e.o(-1).pp + r.augment(frac(21, 8))
piano__7_21 = l.sd + s6.e.p + r.augment(frac(5, 8)) + s6.t.pp + s5.t.pp + \
    s6.t.pp + r.e + s6.s.p + r.s + s5.s.p + r.s + s4.s.p + r.s + s5.t.p
piano__8_21 = l.sd + r + s0.t.o(1).pp + r.sd + \
    s0.s.o(1).p + r.augment(frac(15, 8))
chord_21 = (V[7] % VI.M)(piano__3=piano__3_21, piano__4=piano__4_21,
                         piano__5=piano__5_21, piano__7=piano__7_21, piano__8=piano__8_21)

piano__2_22 = r.augment(frac(7, 8)) + s3.o(-1).pp + r.augment(frac(17, 8))
piano__3_22 = l.sd + r.qd + s4.h.o(-1).pp + r.t
piano__4_22 = l.augment(frac(7, 8)) + r.h + s1.pp + r.t
piano__5_22 = l.sd + r.e + s3.pp + s2.pp + r.ed + s5.t.pp + r.s
piano__7_22 = l.augment(frac(5, 8)) + r.s + s5.ed.p + s1.s.o(1).p + s0.o(1).p + \
    s6.t.p + s0.t.o(1).pp + s6.t.p + s0.t.o(1).pp + \
    s6.s.p + r.t + s6.t.pp + r.t
piano__8_22 = l.sd + r.s + s4.s.o(1).p + r.augment(frac(25, 8))
chord_22 = (I % VI.M)(piano__2=piano__2_22, piano__3=piano__3_22, piano__4=piano__4_22,
                      piano__5=piano__5_22, piano__7=piano__7_22, piano__8=piano__8_22)

piano__4_23 = l.n + s0.pp + r.hd
piano__5_23 = l.sd + r.augment(frac(25, 8)) + s4.s.p + r.s
piano__7_23 = l.n + s0.s.o(1).p + r.augment(frac(5, 4)) + s0.s.o(1).p + \
    r.s + s1.s.o(1).p + r.s + s0.s.o(1).p + r.s + s6.s.p + r.ed
piano__8_23 = l.s + s4.s.o(1).p + h6.s.o(1).p + s4.s.o(1).p + r.s + s4.s.o(1).p + h6.s.o(1).p + s4.s.o(1).p + s3.s.o(
    1).p + s4.s.o(1).p + s3.s.o(1).p + s4.s.o(1).p + s3.s.o(1).mf + s4.s.o(1).p + s3.s.o(1).p + s4.s.o(1).p
piano__10_23 = r + s5.s.o(1).p + r.augment(frac(11, 4))
chord_23 = (I % VI.M)(piano__4=piano__4_23, piano__5=piano__5_23,
                      piano__7=piano__7_23, piano__8=piano__8_23, piano__10=piano__10_23)

piano__3_24 = l.sd + r.augment(frac(25, 8)) + s4.s.o(-1).p + r.s
piano__4_24 = l.augment(frac(7, 8)) + r.augment(frac(5, 8)) + \
    s0.s.p + r.s + s1.s.p + r.s + s0.s.p + r.s + s6.s.o(-1).p + r.ed
piano__7_24 = l.n + s0.o(1).p + r.hd
piano__8_24 = l.n + s2.s.o(1).p + s4.s.o(1).p + h6.s.o(1).p + s4.s.o(1).p + r.s + s4.s.o(1).p + h6.s.o(1).p + s4.s.o(
    1).p + s3.s.o(1).p + s4.s.o(1).p + s3.s.o(1).p + s4.s.o(1).p + s3.s.o(1).mf + s4.s.o(1).p + s3.s.o(1).p + s4.s.o(1).p
piano__10_24 = r + s5.s.o(1).p + r.augment(frac(11, 4))
chord_24 = (I % VI.M)(piano__3=piano__3_24, piano__4=piano__4_24,
                      piano__7=piano__7_24, piano__8=piano__8_24, piano__10=piano__10_24)

piano__4_25 = l.n + s0.s.p + r.augment(frac(15, 4))
piano__5_25 = l.s + s4.s.pp + h6.s.pp + s4.s.pp + s5.s.pp + s4.s.pp + h6.s.pp + \
    s4.s.pp + s3.s.p + s4.s.pp + s3.s.p + \
    s4.s.pp + s3.s.p + s4.s.pp + s3.s.p + s4.s.pp
piano__7_25 = l.n + s0.o(1).p + r.hd
piano__8_25 = l.sd + r.augment(frac(25, 8)) + s4.s.o(1).p + r.s
piano__10_25 = r.qd + s0.s.o(2).p + r.s + s1.s.o(2).mf + \
    r.s + s0.s.o(2).p + r.s + s6.s.o(1).mf + r.ed
chord_25 = (I % VI.M)(piano__4=piano__4_25, piano__5=piano__5_25,
                      piano__7=piano__7_25, piano__8=piano__8_25, piano__10=piano__10_25)

piano__0_26 = r.augment(frac(7, 2)) + s4.s.o(-2).p + r.s
piano__1_26 = l.sd + r.augment(frac(9, 8)) + s0.s.o(-1).p + r.s + \
    s1.s.o(-1).mf + r.s + s0.s.o(-1).p + r.s + s6.s.o(-2).p + r.ed
piano__10_26 = s0.o(2).p + r.hd
piano__5_26 = l.n + s2.s.pp + s4.s.pp + h6.s.pp + s4.s.pp + s5.s.pp + s4.s.pp + h6.s.pp + \
    s4.s.pp + s3.s.p + s4.s.pp + s3.s.p + \
    s4.s.pp + s3.s.p + s4.s.pp + s3.s.p + s4.s.pp
chord_26 = (I % VI.M)(piano__0=piano__0_26, piano__1=piano__1_26,
                      piano__10=piano__10_26, piano__5=piano__5_26)

piano__1_27 = l.n + s0.o(-1).p + r.hd
piano__4_27 = l.augment(frac(7, 8)) + r.augment(frac(9, 8)) + \
    s1.s.pp + r.s + s1.s.pp + r.s + s0.s.pp + r.s + s0.s.pp + r.s
piano__5_27 = l.n + s2.p + s2.s.pp + r.s + s2.s.pp + r.augment(frac(9, 4))
piano__7_27 = l.augment(frac(5, 8)) + r.augment(frac(5, 8)) + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp
piano__8_27 = l.sd + r.augment(frac(5, 8)) + s4.o(1).p + s3.o(1).p + s2.o(1).p
chord_27 = (I % VI.M)(piano__1=piano__1_27, piano__4=piano__4_27,
                      piano__5=piano__5_27, piano__7=piano__7_27, piano__8=piano__8_27)

piano__8_28 = l.n + s2.ed.o(1).p + s2.t.o(1).p + \
    s1.t.o(1).p + r.augment(frac(23, 8)) + s1.t.o(1).p
piano__10_28 = r.ed + s3.n.o(1).p + r.t + s2.s.o(1).p + r.s + s3.s.o(
    1).p + r.s + s5.e.o(1).p + s4.e.o(1).p + s3.e.o(1).p + s2.e.o(1).p + r.t
piano__5_28 = l.n + s0.s.pp + \
    r.augment(frac(5, 8)) + s0.s.pp + r.ed + s0.s.pp + \
    r.ed + s0.s.pp + r.ed + s6.t.o(-1).pp
piano__7_28 = l.s + s4.s.pp + s3.s.pp + s4.t.pp + r.s + s4.s.pp + s3.s.pp + \
    s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp + \
    r.s + s4.s.pp + s3.s.pp + s4.s.pp + r.t
chord_28 = (IV % VI.M)(piano__8=piano__8_28, piano__10=piano__10_28,
                       piano__5=piano__5_28, piano__7=piano__7_28)

piano__2_29 = r.augment(frac(31, 8)) + s3.t.o(-1).p
piano__4_29 = l.augment(frac(7, 8)) + r + s1.s.p + \
    r.s + s1.s.pp + r.s + s0.s.p + r.s + s0.s.pp + r.sd
piano__5_29 = l.t + r.ed + s2.s.p + r.s + s2.s.pp + r.augment(frac(19, 8))
piano__7_29 = l.t + s0.s.o(1).pp + s6.s.pp + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + s1.t.o(1).mf
piano__8_29 = l.sd + r.e + s4.o(1).p + s3.o(1).p + s2.o(1).p + r.t
chord_29 = (I % VI.M)(piano__2=piano__2_29, piano__4=piano__4_29,
                      piano__5=piano__5_29, piano__7=piano__7_29, piano__8=piano__8_29)

piano__2_30 = l.t + r.ed + s2.s.o(-1).p + r.augment(frac(23, 8))
piano__3_30 = l.sd + s4.s.o(-1).pp + r.ed + s4.s.o(-1).pp + r.s + \
    s3.s.o(-1).pp + r.ed + s3.s.o(-1).p + r.augment(frac(7, 8))
piano__4_30 = l.t + s0.s.pp + r.s + s0.s.pp + r.s + s0.s.pp + r.s + \
    s0.s.pp + r.e + s6.s.o(-1).p + r.ed + s5.s.o(-1).pp + r.s + s6.t.o(-1).p
piano__5_30 = l.t + r.h + s1.s.p + r.s + \
    s1.s.p + r.s + s2.s.pp + r.s + s2.s.pp + r.t
piano__7_30 = l.augment(frac(5, 8)) + r + s0.s.o(1).p + s6.mf + s0.t.o(1).p + \
    r.t + s0.t.o(1).p + s1.t.o(1).p + s0.s.o(1).p + \
    s6.t.p + s0.t.o(1).p + s6.t.mf
piano__8_30 = l.sd + r.s + s4.s.o(1).p + s3.s.o(1).p + s2.s.o(1).p + s1.s.o(
    1).p + r.augment(frac(11, 8)) + s1.t.o(1).p + r.augment(frac(7, 8))
chord_30 = (II[7] % VI.M)(piano__2=piano__2_30, piano__3=piano__3_30,
                          piano__4=piano__4_30, piano__5=piano__5_30, piano__7=piano__7_30, piano__8=piano__8_30)

piano__4_31 = l.t + r.augment(frac(7, 4)) + s1.s.pp + \
    r.s + s1.s.pp + r.s + s0.s.pp + r.s + s0.s.pp + r.sd
piano__5_31 = l.t + s4.s.p + s2.s.pp + s4.s.pp + s2.s.pp + \
    r.s + s2.s.pp + r.augment(frac(9, 4)) + s3.t.pp
piano__7_31 = l.sd + r.ed + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.t
piano__8_31 = l.sd + r.e + s4.o(1).p + s3.o(1).p + s2.o(1).p + r.t
piano__10_31 = r.augment(frac(31, 8)) + s5.t.o(1).p
chord_31 = (I % VI.M)(piano__4=piano__4_31, piano__5=piano__5_31,
                      piano__7=piano__7_31, piano__8=piano__8_31, piano__10=piano__10_31)

piano__8_32 = l.sd + r.e + s1.t.o(1).p + r.hd
piano__10_32 = l.augment(frac(5, 8)) + s3.t.o(1).p + s2.t.o(1).p + r.t + s2.s.o(
    1).p + r.s + s3.s.o(1).p + r.s + s5.e.o(1).p + s4.e.o(1).p + s3.e.o(1).p + s2.e.o(1).p
piano__5_32 = l.t + r.augment(frac(7, 8)) + \
    s0.s.pp + r.ed + s0.s.pp + r.ed + s0.s.pp + r.ed
piano__7_32 = l.t + s4.s.pp + s3.s.pp + s4.s.pp + r.sd + s4.s.pp + s3.s.pp + \
    s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp
chord_32 = (IV % VI.M)(piano__8=piano__8_32, piano__10=piano__10_32,
                       piano__5=piano__5_32, piano__7=piano__7_32)

piano__8_33 = l.n + s4.e.o(1).p + r.e + s4.o(1).p + s3.o(1).p + s2.o(1).p
piano__4_33 = l.t + r.augment(frac(15, 8)) + s1.s.p + \
    r.s + s1.s.pp + r.s + s0.s.p + r.s + s0.s.pp + r.s
piano__5_33 = l.n + s2.s.pp + r.ed + s2.s.p + \
    r.s + s2.s.pp + r.augment(frac(9, 4))
piano__7_33 = l.s + s0.s.o(1).pp + s6.s.pp + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp
chord_33 = (I % VI.M)(piano__8=piano__8_33, piano__4=piano__4_33,
                      piano__5=piano__5_33, piano__7=piano__7_33)

piano__2_34 = l.n + s2.s.o(-1).p + r.ed + s2.s.o(-1).p + r.augment(frac(11, 4))
piano__3_34 = l.sd + r.t + \
    s4.s.o(-1).pp + r.ed + s4.s.o(-1).pp + r.s + \
    s3.s.o(-1).pp + r.ed + s3.s.o(-1).p + r.ed
piano__4_34 = l.t + r.t + s0.s.pp + r.s + s0.s.pp + r.s + s0.s.pp + \
    r.s + s0.s.pp + r.e + s6.s.o(-1).p + r.ed + s5.s.o(-1).pp + r.s
piano__5_34 = l.t + r.augment(frac(17, 8)) + s1.s.p + \
    r.s + s1.s.p + r.s + s2.s.pp + r.s + s2.s.pp
piano__7_34 = l.n + s0.ed.o(1).mf + r + s0.s.o(1).p + s6.mf + s0.t.o(
    1).p + r.t + s0.t.o(1).p + s1.t.o(1).p + s0.t.o(1).p + s6.t.p + s0.t.o(1).p + r.t
piano__8_34 = l.sd + r.sd + s4.s.o(1).p + s3.s.o(1).p + s2.s.o(
    1).p + s1.s.o(1).p + r.augment(frac(11, 8)) + s1.t.o(1).p + r.ed
chord_34 = (II[7] % VI.M)(piano__2=piano__2_34, piano__3=piano__3_34,
                          piano__4=piano__4_34, piano__5=piano__5_34, piano__7=piano__7_34, piano__8=piano__8_34)

piano__3_35 = l.sd + r.augment(frac(9, 8)) + s4.s.o(-1).p + \
    r.augment(frac(7, 4)) + s4.s.o(-1).p + r.s
piano__4_35 = l.n + s0.p + r.e + \
    s6.s.o(-1).p + r.s + s0.p + r.e + s6.s.o(-1).p + r.s
piano__5_35 = l.n + s2.p + r.e + s1.s.p + r.s + s2.p + r.e + s1.s.p + r.s
piano__7_35 = l.n + s0.s.o(1).mf + s4.s.p + s0.s.o(1).mf + r + \
    s1.s.o(1).p + s0.s.o(1).mf + s4.s.p + s0.s.o(1).mf + r + s1.s.o(1).p
piano__8_35 = l.sd + r.sd + s2.s.o(1).p + s4.s.o(1).mf + s2.s.o(1).p + s3.s.o(
    1).mf + r + s2.s.o(1).p + s4.s.o(1).mf + s2.s.o(1).p + s3.s.o(1).mf + r.s
chord_35 = (I % VI.M)(piano__3=piano__3_35, piano__4=piano__4_35,
                      piano__5=piano__5_35, piano__7=piano__7_35, piano__8=piano__8_35)

piano__0_36 = r + h11.e.o(-3).p + r.e + s0.e.o(-2).p + r.qd
piano__3_36 = l.sd + r.augment(frac(5, 8)) + \
    h11.e.o(-2).mf + r.e + s0.e.o(-1).mf + r.qd
piano__4_36 = l.n + s2.e.o(-1).p + r.augment(frac(7, 2))
piano__5_36 = l.n + s4.e.o(-1).mf + r.augment(frac(7, 2))
piano__7_36 = l.n + s2.e.mf + r.qd + s2.e.mf + r.qd
piano__8_36 = l.sd + r.augment(frac(5, 8)) + s3.e.mf + r.e + s4.e.mf + r.qd
piano__9_36 = r + s1.e.o(1).mf + r.augment(frac(5, 2))
piano__10_36 = l.augment(frac(5, 8)) + r.sd + \
    s5.e.mf + r.e + s2.e.o(1).mf + r.qd
chord_36 = (VI % VI.M)(piano__0=piano__0_36, piano__3=piano__3_36, piano__4=piano__4_36, piano__5=piano__5_36,
                       piano__7=piano__7_36, piano__8=piano__8_36, piano__9=piano__9_36, piano__10=piano__10_36)

piano__2_37 = l.n + s6.h.o(-2).pp + r.h
piano__3_37 = l.sd + r.augment(frac(13, 8)) + s0.h.o(-1).pp
piano__4_37 = l.t + r.augment(frac(27, 8)) + s4.s.o(-1).pp + r.s
piano__5_37 = l.t + r.sd + s0.s.pp + r.s + s0.e.pp + \
    s6.s.o(-1).pp + r.s + s6.e.o(-1).pp + \
    s5.s.o(-1).pp + r.s + s5.e.o(-1).pp + r.e
piano__7_37 = l.n + s1.e.pp + r.qd + s4.e.p + \
    s3.s.p + r.s + s3.e.p + s2.s.p + r.s
piano__8_37 = l.n + s6.e.p + s5.s.p + r.s + \
    s5.e.p + s4.s.p + r.augment(frac(9, 4))
chord_37 = (V[7] % VI.M)(piano__2=piano__2_37, piano__3=piano__3_37, piano__4=piano__4_37,
                         piano__5=piano__5_37, piano__7=piano__7_37, piano__8=piano__8_37)

piano__1_38 = l.sd + r.augment(frac(13, 8)) + s3.o(-2).pp + r
piano__3_38 = l.sd + r.augment(frac(5, 8)) + s0.o(-1).pp + r.h
piano__4_38 = l.n + s3.o(-1).pp + r.hd
piano__5_38 = l.n + s4.h.o(-1).pp + s5.o(-1).pp + r
piano__6_38 = s2.h.p + r.h
piano__7_38 = l.n + s6.h.o(-1).p + s3.p + r
chord_38 = (V[7] % VI.M)(piano__1=piano__1_38, piano__3=piano__3_38, piano__4=piano__4_38,
                         piano__5=piano__5_38, piano__6=piano__6_38, piano__7=piano__7_38)

piano__0_39 = s0.o(-1).p + r.hd
piano__1_39 = l.n + s4.o(-1).p + r.hd
piano__2_39 = l.n + s0.mf + r.hd
piano__5_39 = l.t + r.augment(frac(15, 8)) + s0.o(1).pp + r
piano__6_39 = s2.o(1).p + r + s2.o(1).p + s1.o(1).pp
piano__7_39 = l.n + s4.o(1).p + r.h + s3.o(1).p
piano__8_39 = l.n + s0.o(2).mf + r.qd + s1.s.o(2).p + \
    r.e + s3.s.o(2).p + r.s + s3.s.o(2).p
piano__9_39 = r.h + s3.s.o(2).mf + s2.s.o(2).p + \
    r.s + s2.s.o(2).p + r.e + s2.s.o(2).p + r.s
piano__10_39 = l.augment(frac(5, 8)) + \
    r.augment(frac(19, 8)) + s4.s.o(2).mf + r.ed
chord_39 = (I % II.M)(piano__0=piano__0_39, piano__1=piano__1_39, piano__2=piano__2_39, piano__5=piano__5_39,
                      piano__6=piano__6_39, piano__7=piano__7_39, piano__8=piano__8_39, piano__9=piano__9_39, piano__10=piano__10_39)

piano__10_40 = l.n + s4.o(2).mf + r + s4.t.o(2).p + r.sd + \
    s5.t.o(2).p + r.sd + s6.t.o(2).p + r.sd + s0.t.o(3).p + r.sd
piano__6_40 = s2.o(1).pp + r.hd
piano__7_40 = l.n + s4.o(1).p + r.hd
chord_40 = (I % II.M)(piano__10=piano__10_40,
                      piano__6=piano__6_40, piano__7=piano__7_40)

piano__2_41 = l.t + r.augment(frac(7, 8)) + s0.e.pp + r.augment(frac(5, 2))
piano__3_41 = l.n + s2.e.pp + r.qd + s1.e.pp + r.qd
piano__4_41 = l.t + r.augment(frac(23, 8)) + s4.t.pp + r.augment(frac(7, 8))
piano__5_41 = l.t + r.sd + \
    s0.e.o(1).pp + r.e + s0.e.o(1).pp + r.e + \
    s0.e.o(1).pp + r.e + s6.t.pp + r.sd
piano__9_41 = r + s2.o(2).p + r.s + s3.s.o(2).p + \
    s2.s.o(2).p + s3.s.o(2).p + r.e + s3.t.o(2).p + r.sd
piano__10_41 = l.n + s4.o(2).p + r + s4.s.o(2).p + \
    r.ed + s4.t.o(2).p + r.augment(frac(7, 8))
chord_41 = (I % II.M)(piano__2=piano__2_41, piano__3=piano__3_41, piano__4=piano__4_41,
                      piano__5=piano__5_41, piano__9=piano__9_41, piano__10=piano__10_41)

piano__2_42 = l.n + s0.p + r.hd
piano__5_42 = l.n + s0.o(1).p + r + s0.o(1).pp + s1.o(1).pp
piano__7_42 = l.sd + r.augment(frac(21, 8)) + s3.o(1).p
piano__8_42 = l.sd + r.augment(frac(13, 8)) + s2.o(1).p + r
piano__9_42 = h3.e.o(2).p + s2.e.o(2).p + r + s3.s.o(2).mf + s2.s.o(2).p + s1.s.o(
    2).p + s2.s.o(2).p + s4.s.o(2).mf + s3.s.o(2).p + s2.s.o(2).p + s3.s.o(2).p
chord_42 = (I % II.M)(piano__2=piano__2_42, piano__5=piano__5_42,
                      piano__7=piano__7_42, piano__8=piano__8_42, piano__9=piano__9_42)

piano__9_43 = s4.o(2).mf + r + s4.t.o(2).p + r.augment(frac(15, 8))
piano__10_43 = l.augment(frac(5, 8)) + r.augment(frac(15, 8)) + \
    s5.t.o(2).p + r.sd + s6.t.o(2).p + r.sd + s0.t.o(3).p + r.sd
piano__6_43 = s2.o(1).pp + r.hd
piano__7_43 = l.n + s4.o(1).p + r.hd
chord_43 = (I % II.M)(piano__9=piano__9_43, piano__10=piano__10_43,
                      piano__6=piano__6_43, piano__7=piano__7_43)

piano__2_44 = l.t + r.augment(frac(7, 8)) + s0.e.pp + r.augment(frac(5, 2))
piano__3_44 = l.n + s2.e.pp + r.qd + s1.e.pp + r.qd
piano__4_44 = l.t + r.augment(frac(23, 8)) + s4.e.pp + r.e
piano__5_44 = l.t + r.sd + \
    s0.e.o(1).pp + r.e + s0.e.o(1).pp + r.e + s0.e.o(1).pp + r.e + s6.e.pp
piano__8_44 = l.sd + r.augment(frac(27, 8)) + s1.s.o(2).p
piano__9_44 = r + s2.o(2).p + r.s + s3.s.o(2).p + s2.s.o(2).p + \
    s3.s.o(2).p + s4.s.o(2).p + s3.s.o(2).p + s2.s.o(2).p + r.s
piano__10_44 = l.n + s4.o(2).p + r + s4.s.o(2).p + r.augment(frac(7, 4))
chord_44 = (I % II.M)(piano__2=piano__2_44, piano__3=piano__3_44, piano__4=piano__4_44,
                      piano__5=piano__5_44, piano__8=piano__8_44, piano__9=piano__9_44, piano__10=piano__10_44)

piano__5_45 = l.n + s0.s.o(1).pp + r.ed + s0.s.o(1).pp + \
    r.ed + s0.s.o(1).pp + r.ed + s0.s.o(1).pp + r.ed
piano__6_45 = r.e + s2.s.o(1).pp + r.ed + s2.s.o(1).pp + \
    r.ed + s2.s.o(1).pp + r.ed + s2.s.o(1).pp + r.s
piano__7_45 = l.sd + r.augment(frac(5, 8)) + \
    s4.s.o(1).p + r.augment(frac(11, 4))
piano__8_45 = l.n + s0.s.o(2).p + r.h + s2.s.o(2).p + \
    r + s1.s.o(2).p + s0.s.o(2).p
piano__9_45 = r.h + s2.t.o(2).p + s3.t.o(2).p + r.s + s3.t.o(2).p + s2.t.o(
    2).p + s3.t.o(2).p + s2.s.o(2).p + s3.t.o(2).p + s2.s.o(2).p + r.e
chord_45 = (I % II.M)(piano__5=piano__5_45, piano__6=piano__6_45,
                      piano__7=piano__7_45, piano__8=piano__8_45, piano__9=piano__9_45)

piano__4_46 = l.t + r.augment(frac(29, 8)) + s1.s.pp
piano__5_46 = l.t + r.augment(frac(25, 8)) + s3.s.pp + s2.s.pp + r.s
piano__6_46 = s4.s.pp + r.ed + s4.s.pp + r.ed + \
    s4.s.p + s5.s.pp + r.s + s5.s.pp + s4.s.pp + r.ed
piano__7_46 = l.sd + r.t + s6.s.pp + r.s + \
    s0.s.o(1).p + r.s + s6.s.pp + r.ed + s6.s.pp + r.augment(frac(5, 4))
piano__8_46 = l.n + s2.s.o(1).p + r.augment(frac(7, 4)) + \
    s4.s.o(1).p + r.augment(frac(7, 4))
chord_46 = (V[7] % II.M)(piano__4=piano__4_46, piano__5=piano__5_46,
                         piano__6=piano__6_46, piano__7=piano__7_46, piano__8=piano__8_46)

piano__3_47 = l.sd + r.augment(frac(21, 8)) + s6.s.o(-1).pp + r.ed
piano__4_47 = l.n + s0.s.pp + r.ed + s0.s.pp + \
    r.ed + s0.s.pp + r.augment(frac(7, 4))
piano__5_47 = l.t + r.sd + s2.s.pp + r.ed + \
    s2.s.pp + r.ed + s2.s.pp + r.ed + s2.s.pp + r.s
piano__7_47 = l.sd + r.augment(frac(5, 8)) + \
    s0.s.o(1).p + r.augment(frac(11, 4))
piano__8_47 = l.n + s4.s.o(1).p + r.augment(frac(7, 2)) + s4.s.o(1).p
piano__9_47 = r.h + s6.t.o(1).p + s0.t.o(2).p + s6.s.o(1).p + s0.t.o(2).p + s6.t.o(
    1).p + s0.t.o(2).p + s6.s.o(1).p + s0.t.o(2).p + s6.s.o(1).p + s5.s.o(1).p + r.s
chord_47 = (V[7] % II.M)(piano__3=piano__3_47, piano__4=piano__4_47, piano__5=piano__5_47,
                         piano__7=piano__7_47, piano__8=piano__8_47, piano__9=piano__9_47)

piano__2_48 = l.t + r.augment(frac(17, 8)) + s0.s.pp + r.qd
piano__3_48 = l.n + s2.s.pp + r.ed + s2.s.pp + r.ed + \
    s2.s.p + r.s + s1.s.pp + s2.s.pp + s3.s.pp + r.ed
piano__4_48 = l.t + r.augment(frac(25, 8)) + s4.s.pp + s5.s.p + r.s
piano__5_48 = l.t + r.sd + s0.s.o(1).pp + r.ed + s0.s.o(1).pp + r.h + s6.s.p
piano__7_48 = l.sd + r.augment(frac(5, 8)) + \
    s4.s.o(1).p + r.augment(frac(11, 4))
piano__8_48 = l.n + s0.s.o(2).p + r.augment(frac(15, 4))
piano__9_48 = r.h + s2.s.o(2).p + r.augment(frac(7, 4))
chord_48 = (I % II.M)(piano__2=piano__2_48, piano__3=piano__3_48, piano__4=piano__4_48,
                      piano__5=piano__5_48, piano__7=piano__7_48, piano__8=piano__8_48, piano__9=piano__9_48)

piano__3_49 = l.sd + r.augment(frac(17, 8)) + \
    s2.s.pp + r.s + s2.s.pp + r.s + s2.s.pp + r.s
piano__4_49 = l.t + r.augment(frac(19, 8)) + \
    s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp + r.s
piano__5_49 = l.n + s0.o(1).p + r.hd
piano__8_49 = l.s + s0.s.o(2).p + s1.s.o(2).p + \
    r.augment(frac(11, 4)) + s1.s.o(2).p + s0.s.o(2).p
piano__9_49 = s2.s.o(2).p + r.e + s2.s.o(2).p + s3.s.o(2).p + \
    r.qd + s4.s.o(2).p + s3.s.o(2).p + s2.s.o(2).p + r.e
piano__10_49 = l.augment(frac(5, 8)) + r.augment(frac(5, 8)) + s4.s.o(2).p + s5.s.o(
    2).p + s6.s.o(2).p + s0.s.o(3).p + s6.s.o(2).p + s5.s.o(2).p + r.augment(frac(5, 4))
chord_49 = (I % II.M)(piano__3=piano__3_49, piano__4=piano__4_49, piano__5=piano__5_49,
                      piano__8=piano__8_49, piano__9=piano__9_49, piano__10=piano__10_49)

piano__3_50 = l.n + s2.pp + r.qd + s2.s.pp + r.s + s2.s.pp + r.ed
piano__4_50 = l.n + s4.p + r.qd + s4.s.pp + r.s + s4.s.pp + r.s + h4.s.pp + r.s
piano__5_50 = l.t + r.augment(frac(27, 8)) + s4.s.pp + r.s
piano__7_50 = l.sd + r.augment(frac(27, 8)) + s4.s.o(1).p
piano__8_50 = l.n + s0.s.o(2).p + r.s + s0.s.o(2).p + h11.s.o(1).p + s0.s.o(
    2).p + r.augment(frac(7, 4)) + s0.s.o(2).p + s6.s.o(1).p + s5.s.o(1).p + r.s
piano__9_50 = r.s + s1.s.o(2).p + r.ed + s1.s.o(2).p + s2.s.o(2).p + \
    s3.s.o(2).p + r.s + s3.s.o(2).p + s2.s.o(2).p + s1.s.o(2).p + r
piano__10_50 = l.augment(frac(5, 8)) + r.augment(frac(11, 8)
                                                 ) + s4.s.o(2).p + r.augment(frac(7, 4))
chord_50 = (II % II.M)(piano__3=piano__3_50, piano__4=piano__4_50, piano__5=piano__5_50,
                       piano__7=piano__7_50, piano__8=piano__8_50, piano__9=piano__9_50, piano__10=piano__10_50)

piano__1_51 = l.sd + r.augment(frac(17, 8)) + s4.e.o(-1).p + r
piano__2_51 = l.t + r.augment(frac(11, 8)) + \
    s0.s.pp + r.s + s6.e.o(-1).p + r.e + s0.s.p + r.ed
piano__3_51 = l.sd + r.t + s3.e.pp + s2.s.pp + \
    r.augment(frac(9, 4)) + s2.s.p + r.s
piano__4_51 = l.n + s4.e.p + r.augment(frac(7, 2))
piano__7_51 = l.sd + r.sd + s4.s.o(1).pp + r.hd
piano__8_51 = l.n + s6.s.o(1).p + s0.s.o(2).p + s6.s.o(1).p + r.s + \
    s0.s.o(2).p + r.qd + s1.s.o(2).p + r.e + s1.s.o(2).p + s0.s.o(2).p
piano__9_51 = r.h + s3.s.o(2).p + s4.s.o(2).p + \
    s3.s.o(2).p + r.s + s3.s.o(2).p + s2.s.o(2).p + r.e
chord_51 = (I[7] % II.M)(piano__1=piano__1_51, piano__2=piano__2_51, piano__3=piano__3_51,
                         piano__4=piano__4_51, piano__7=piano__7_51, piano__8=piano__8_51, piano__9=piano__9_51)

piano__1_52 = l.sd + r.augment(frac(17, 8)) + s4.e.o(-1).p + r
piano__2_52 = l.t + r.augment(frac(11, 8)) + \
    s0.s.p + r.s + s6.e.o(-1).p + r.e + s0.s.p + r.ed
piano__3_52 = l.sd + r.t + s3.e.p + s2.s.p + \
    r.augment(frac(9, 4)) + s2.s.p + r.s
piano__4_52 = l.n + s4.e.p + r.augment(frac(7, 2))
piano__7_52 = l.sd + r.sd + s4.s.o(1).p + r.hd
piano__8_52 = l.n + s6.s.o(1).p + s0.s.o(2).p + s6.s.o(1).p + r.s + \
    s0.s.o(2).p + r.qd + s1.s.o(2).p + r.e + s1.s.o(2).p + s0.s.o(2).p
piano__9_52 = r.h + s3.s.o(2).mf + s4.s.o(2).p + \
    s3.s.o(2).p + r.s + s3.s.o(2).mf + s2.s.o(2).p + r.e
chord_52 = (I[7] % II.M)(piano__1=piano__1_52, piano__2=piano__2_52, piano__3=piano__3_52,
                         piano__4=piano__4_52, piano__7=piano__7_52, piano__8=piano__8_52, piano__9=piano__9_52)

piano__1_53 = l.n + s4.e.o(-2).p + r.qd + s4.e.o(-2).p + r.qd
piano__2_53 = l.t + r.augment(frac(7, 8)) + s0.e.o(-1).p + r.e + \
    s1.e.o(-1).p + r.e + s0.sd.o(-1).p + r.augment(frac(5, 8))
piano__3_53 = l.n + s1.e.o(-1).p + r.e + s2.e.o(-1).p + \
    r.qd + s2.sd.o(-1).p + r.augment(frac(5, 8))
piano__4_53 = l.n + s4.e.o(-1).p + r.e + s4.e.o(-1).p + r.e + \
    s4.e.o(-1).mf + r.e + s4.sd.o(-1).mf + r.augment(frac(5, 8))
piano__7_53 = l.sd + r.sd + s4.s.mf + r.augment(frac(7, 4)) + s4.s.mf + r
piano__8_53 = l.n + s6.s.mf + s1.s.o(1).mf + s6.s.mf + r + s0.s.o(
    1).mf + s6.s.mf + s1.s.o(1).mf + s6.s.mf + r + s0.s.o(1).mf
piano__9_53 = r + s2.s.o(1).mf + s4.s.o(1).mf + s2.s.o(1).mf + r.augment(
    frac(5, 4)) + s2.t.o(1).mf + r.t + s4.s.o(1).mf + s2.s.o(1).mf + r.s
chord_53 = (IV[7] % VI.M)(piano__1=piano__1_53, piano__2=piano__2_53, piano__3=piano__3_53,
                          piano__4=piano__4_53, piano__7=piano__7_53, piano__8=piano__8_53, piano__9=piano__9_53)

piano__1_54 = l.sd + r.t + s0.t.o(-1).p + r.sd + s0.t.o(-1).p + r.sd + \
    s0.t.o(-1).p + r.sd + s0.augment(frac(7, 8)
                                     ).o(-1).p + r.augment(frac(9, 8))
piano__2_54 = l.t + r.sd + s2.t.o(-1).p + r.sd + s2.t.o(-1).p + r.sd + \
    s2.t.o(-1).p + r.sd + s2.augment(frac(7, 8)
                                     ).o(-1).p + r.augment(frac(9, 8))
piano__3_54 = l.sd + r.t + s4.t.o(-1).p + r.sd + s4.t.o(-1).p + r.sd + \
    s4.t.o(-1).p + r.sd + s4.augment(frac(7, 8)
                                     ).o(-1).p + r.augment(frac(9, 8))
piano__4_54 = l.t + r.sd + s0.t.p + r.sd + s0.t.p + r.sd + \
    s0.t.p + r.sd + s0.augment(frac(7, 8)).p + r.augment(frac(9, 8))
piano__7_54 = l.sd + r.augment(frac(23, 8)) + s1.s.o(1).pp + r.e
piano__8_54 = l.n + s2.t.o(1).mf + r.sd + s2.t.o(1).p + r.sd + s2.t.o(1).p + r.sd + s2.t.o(1).p + \
    r.sd + s2.augment(frac(7, 8)).o(1).p + s3.t.o(1).p + \
    s2.s.o(1).p + r.s + s2.s.o(1).pp + s3.s.o(1).pp
piano__9_54 = s4.t.o(1).f + r.sd + s4.t.o(1).p + r.sd + s4.t.o(1).p + r.sd + \
    s4.t.o(1).p + r.sd + s4.augment(frac(7, 8)).o(1).p + r.augment(frac(9, 8))
piano__10_54 = l.e + s0.t.o(2).mf + r.sd + s0.t.o(2).mf + r.sd + s0.t.o(
    2).mf + r.sd + s0.augment(frac(7, 8)).o(2).mf + r.augment(frac(9, 8))
chord_54 = (I % VI.M)(piano__1=piano__1_54, piano__2=piano__2_54, piano__3=piano__3_54, piano__4=piano__4_54,
                      piano__7=piano__7_54, piano__8=piano__8_54, piano__9=piano__9_54, piano__10=piano__10_54)

piano__4_55 = l.n + s0.e.pp + r.e + s1.e.pp + r.qd + s0.e.pp + r.e
piano__5_55 = l.t + r.sd + s2.e.pp + r.e + s3.e.pp + s2.e.pp + r + s2.e.pp
piano__6_55 = r.augment(frac(5, 2)) + s4.e.pp + r
piano__9_55 = h6.e.o(1).p + s4.e.o(1).p + r.e + \
    s4.e.o(1).pp + r + s5.e.o(1).p + s4.e.o(1).p
piano__10_55 = l.augment(frac(5, 8)) + \
    r.augment(frac(11, 8)) + s0.e.o(2).p + s6.e.o(1).p + r
chord_55 = (I % VI.M)(piano__4=piano__4_55, piano__5=piano__5_55,
                      piano__6=piano__6_55, piano__9=piano__9_55, piano__10=piano__10_55)

piano__3_56 = l.sd + r.augment(frac(21, 8)) + s0.e.o(-1).pp + r.e
piano__4_56 = l.t + r.augment(frac(11, 8)) + \
    s4.e.o(-1).pp + s2.e.o(-1).pp + s4.e.o(-1).pp + r
piano__5_56 = l.n + s4.e.o(-1).pp + r.e + s6.e.o(-1).pp + r.h + s6.e.o(-1).pp
piano__6_56 = r.e + s1.e.pp + r.hd
piano__7_56 = l.sd + r.augment(frac(25, 8)) + s4.e.p
piano__8_56 = l.n + s5.e.p + s6.e.p + r.e + \
    s6.e.pp + r.e + s6.e.p + s5.e.p + r.e
piano__9_56 = r.h + s0.e.o(1).p + r.qd
chord_56 = (V[7] % VI.M)(piano__3=piano__3_56, piano__4=piano__4_56, piano__5=piano__5_56,
                         piano__6=piano__6_56, piano__7=piano__7_56, piano__8=piano__8_56, piano__9=piano__9_56)

piano__3_57 = l.sd + r.augment(frac(21, 8)) + s5.e.o(-1).pp + r.e
piano__4_57 = l.t + r.augment(frac(7, 8)) + \
    s6.e.o(-1).pp + r.e + s0.e.pp + r + s0.e.pp
piano__5_57 = l.n + s2.e.pp + r.augment(frac(7, 2))
piano__6_57 = r.e + s4.e.pp + r.e + s4.e.pp + r.e + s4.e.pp + r
piano__7_57 = l.n + s6.e.p + s0.e.o(1).p + r.e + s1.e.o(1).p + r.h
piano__8_57 = l.sd + r.augment(frac(13, 8)) + \
    h3.e.o(1).p + s2.e.o(1).p + r.e + s3.e.o(1).p
piano__9_57 = r.augment(frac(27, 8)) + s4.t.o(1).p + r.e
chord_57 = (I[7] % VI.M)(piano__3=piano__3_57, piano__4=piano__4_57, piano__5=piano__5_57,
                         piano__6=piano__6_57, piano__7=piano__7_57, piano__8=piano__8_57, piano__9=piano__9_57)

piano__3_58 = l.n + s4.e.o(-1).pp + r.qd + s4.o(-1).pp + r
piano__4_58 = l.t + r.sd + s0.e.pp + r.e + s0.e.pp + s6.o(-1).pp + r
piano__5_58 = l.t + r.augment(frac(7, 8)) + s2.e.pp + r.augment(frac(5, 2))
piano__7_58 = l.sd + r.augment(frac(13, 8)) + s1.e.o(1).p + r.qd
piano__8_58 = l.n + s2.qd.o(1).p + s3.s.o(1).p + s2.s.o(1).p + \
    r.e + s2.s.o(1).p + r.s + s3.s.o(1).p + r.ed
piano__9_58 = r.augment(frac(7, 2)) + h6.s.o(1).p + r.s
chord_58 = (I[7] % VI.M)(piano__3=piano__3_58, piano__4=piano__4_58, piano__5=piano__5_58,
                         piano__7=piano__7_58, piano__8=piano__8_58, piano__9=piano__9_58)

piano__4_59 = l.n + s0.e.pp + r.e + s1.e.pp + r.qd + s0.e.pp + r.e
piano__5_59 = l.t + r.sd + s2.e.pp + r.e + s3.e.pp + s2.e.pp + r + s2.s.pp + r.s
piano__6_59 = r.augment(frac(5, 2)) + s4.s.pp + r.augment(frac(5, 4))
piano__8_59 = l.n + h6.e.o(1).p + r.augment(frac(7, 2))
piano__9_59 = r.e + s4.e.o(1).p + r.e + s5.t.o(1).pp + s4.t.o(1).pp + \
    h6.t.o(1).pp + s4.t.o(1).pp + r + s5.s.o(1).p + r.s + s4.s.o(1).p + r.s
piano__10_59 = l.augment(frac(5, 8)) + r.augment(frac(11, 8)) + \
    s0.s.o(2).p + r.s + s6.s.o(1).p + r.augment(frac(5, 4))
chord_59 = (I % VI.M)(piano__4=piano__4_59, piano__5=piano__5_59, piano__6=piano__6_59,
                      piano__8=piano__8_59, piano__9=piano__9_59, piano__10=piano__10_59)

piano__3_60 = l.sd + r.augment(frac(21, 8)) + s0.e.o(-1).pp + r.e
piano__4_60 = l.t + r.augment(frac(11, 8)) + s4.e.o(-1).pp + \
    s2.e.o(-1).pp + s4.s.o(-1).pp + r.ed + s2.s.o(-1).pp + r.s
piano__5_60 = l.n + s4.e.o(-1).pp + r.e + s6.e.o(-1).pp + r.augment(frac(5, 2))
piano__6_60 = r.e + s1.e.pp + r.hd
piano__7_60 = l.sd + r.augment(frac(25, 8)) + s4.s.p + r.s
piano__8_60 = l.n + s5.e.p + s6.e.p + \
    r.augment(frac(5, 8)) + s6.t.pp + s5.t.pp + \
    s6.t.pp + r.e + s6.s.p + r.s + s5.s.p + r.ed
piano__9_60 = r.qd + s0.t.o(1).pp + r.sd + s0.s.o(1).p + r.augment(frac(7, 4))
chord_60 = (V[7] % VI.M)(piano__3=piano__3_60, piano__4=piano__4_60, piano__5=piano__5_60,
                         piano__6=piano__6_60, piano__7=piano__7_60, piano__8=piano__8_60, piano__9=piano__9_60)

piano__2_61 = l.t + r.augment(frac(7, 8)) + s3.o(-1).pp + r.h
piano__3_61 = l.sd + r.augment(frac(13, 8)) + \
    s4.augment(frac(15, 8)).o(-1).pp + r.t
piano__4_61 = l.n + s0.pp + r.h + s1.augment(frac(7, 8)).pp + r.t
piano__5_61 = l.t + r.augment(frac(7, 8)) + s3.pp + s2.pp + r
piano__6_61 = r + s5.ed.p + r.augment(frac(15, 8)) + s5.t.pp + r.s
piano__7_61 = l.sd + r.augment(frac(11, 8)) + s1.s.o(1).p + s0.o(
    1).p + s6.t.p + s0.t.o(1).pp + s6.t.p + s0.t.o(1).pp + s6.t.p + r.t + s6.t.pp + r.t
piano__8_61 = l.n + s2.ed.o(1).p + r.augment(frac(13, 4))
piano__9_61 = r.ed + s4.s.o(1).p + r.hd
chord_61 = (I % VI.M)(piano__2=piano__2_61, piano__3=piano__3_61, piano__4=piano__4_61, piano__5=piano__5_61,
                      piano__6=piano__6_61, piano__7=piano__7_61, piano__8=piano__8_61, piano__9=piano__9_61)

piano__4_62 = l.n + s0.pp + r.hd
piano__6_62 = r.augment(frac(7, 2)) + s4.s.p + r.s
piano__7_62 = l.n + s0.s.o(1).p + r.augment(frac(5, 4)) + s0.s.o(1).p + \
    r.s + s1.s.o(1).p + r.s + s0.s.o(1).p + r.s + s6.s.p + r.ed
piano__8_62 = l.sd + r.augment(frac(13, 8)) + s3.s.o(1).p + \
    r.s + s3.s.o(1).p + r.s + s3.s.o(1).mf + r.s + s3.s.o(1).p + r.s
piano__9_62 = r.s + s4.s.o(1).p + h6.s.o(1).p + s4.s.o(1).p + s5.s.o(1).p + s4.s.o(1).p + h6.s.o(
    1).p + s4.s.o(1).p + r.s + s4.s.o(1).p + r.s + s4.s.o(1).p + r.s + s4.s.o(1).p + r.s + s4.s.o(1).p
chord_62 = (I % VI.M)(piano__4=piano__4_62, piano__6=piano__6_62,
                      piano__7=piano__7_62, piano__8=piano__8_62, piano__9=piano__9_62)

piano__3_63 = l.sd + r.augment(frac(25, 8)) + s4.s.o(-1).p + r.s
piano__4_63 = l.t + r.augment(frac(11, 8)) + \
    s0.s.p + r.ed + s0.s.p + r.s + s6.s.o(-1).p + r.ed
piano__5_63 = l.t + r.augment(frac(15, 8)) + s1.s.p + r.augment(frac(7, 4))
piano__7_63 = l.n + s0.o(1).p + r.hd
piano__8_63 = l.n + s2.s.o(1).p + r.augment(frac(7, 4)) + s3.s.o(1).p + \
    r.s + s3.s.o(1).p + r.s + s3.s.o(1).mf + r.s + s3.s.o(1).p + r.s
piano__9_63 = r.s + s4.s.o(1).p + h6.s.o(1).p + s4.s.o(1).p + s5.s.o(1).p + s4.s.o(1).p + h6.s.o(
    1).p + s4.s.o(1).p + r.s + s4.s.o(1).p + r.s + s4.s.o(1).p + r.s + s4.s.o(1).p + r.s + s4.s.o(1).p
chord_63 = (I % VI.M)(piano__3=piano__3_63, piano__4=piano__4_63, piano__5=piano__5_63,
                      piano__7=piano__7_63, piano__8=piano__8_63, piano__9=piano__9_63)

piano__4_64 = l.n + s0.s.p + r.augment(frac(15, 4))
piano__5_64 = l.t + r.sd + h6.s.pp + \
    r.augment(frac(5, 4)) + s3.s.p + r.s + s3.s.p + \
    r.s + s3.s.p + r.s + s3.s.p + r.s
piano__6_64 = r.s + s4.s.pp + r.s + s4.s.pp + s5.s.pp + s4.s.pp + h6.s.pp + \
    s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp
piano__7_64 = l.n + s0.o(1).p + r.hd
piano__9_64 = r.augment(frac(7, 2)) + s4.s.o(1).p + r.s
piano__10_64 = l.augment(frac(5, 8)) + r.augment(frac(7, 8)) + s0.s.o(
    2).p + r.s + s1.s.o(2).mf + r.s + s0.s.o(2).p + r.s + s6.s.o(1).mf + r.ed
chord_64 = (I % VI.M)(piano__4=piano__4_64, piano__5=piano__5_64, piano__6=piano__6_64,
                      piano__7=piano__7_64, piano__9=piano__9_64, piano__10=piano__10_64)

piano__0_65 = r.augment(frac(7, 2)) + s4.s.o(-2).p + r.s
piano__1_65 = l.sd + r.augment(frac(9, 8)) + s0.s.o(-1).p + r.s + \
    s1.s.o(-1).mf + r.s + s0.s.o(-1).p + r.s + s6.s.o(-2).p + r.ed
piano__5_65 = l.n + s2.s.pp + \
    r.augment(frac(7, 4)) + s3.s.p + r.s + s3.s.p + \
    r.s + s3.s.p + r.s + s3.s.p + r.s
piano__6_65 = r.s + s4.s.pp + h6.s.pp + s4.s.pp + s5.s.pp + s4.s.pp + h6.s.pp + \
    s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp
piano__10_65 = l.n + s0.o(2).p + r.hd
chord_65 = (I % VI.M)(piano__0=piano__0_65, piano__1=piano__1_65,
                      piano__5=piano__5_65, piano__6=piano__6_65, piano__10=piano__10_65)

piano__1_66 = l.n + s0.o(-1).p + r.hd
piano__4_66 = l.t + r.augment(frac(15, 8)) + s1.s.pp + \
    r.s + s1.s.pp + r.s + s0.s.pp + r.s + s0.s.pp + r.s
piano__5_66 = l.n + s2.p + s2.s.pp + r.s + s2.s.pp + r.augment(frac(9, 4))
piano__7_66 = l.sd + r.augment(frac(7, 8)) + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp
piano__8_66 = l.sd + r.augment(frac(13, 8)) + s3.o(1).p + s2.o(1).p
piano__9_66 = r + s4.o(1).p + r.h
chord_66 = (I % VI.M)(piano__1=piano__1_66, piano__4=piano__4_66, piano__5=piano__5_66,
                      piano__7=piano__7_66, piano__8=piano__8_66, piano__9=piano__9_66)

piano__9_67 = s2.ed.o(1).p + s2.t.o(1).p + s1.t.o(1).p + \
    s2.s.o(1).p + r.augment(frac(9, 4)) + s2.e.o(1).p
piano__10_67 = l.augment(frac(5, 8)) + r.t + s3.n.o(1).p + r.ed + \
    s3.s.o(1).p + r.s + s5.e.o(1).p + s4.e.o(1).p + s3.e.o(1).p + r.e
piano__5_67 = l.n + s0.s.pp + r.ed + s0.s.pp + \
    r.ed + s0.s.pp + r.ed + s0.s.pp + r.ed
piano__7_67 = l.s + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + \
    s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp
chord_67 = (IV % VI.M)(piano__9=piano__9_67, piano__10=piano__10_67,
                       piano__5=piano__5_67, piano__7=piano__7_67)

piano__4_68 = l.t + r.augment(frac(15, 8)) + s1.s.p + \
    r.s + s1.s.pp + r.s + s0.s.p + r.s + s0.s.pp + r.s
piano__5_68 = l.n + s2.s.pp + r.ed + s2.s.p + \
    r.s + s2.s.pp + r.augment(frac(9, 4))
piano__7_68 = l.s + s0.s.o(1).pp + s6.s.pp + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp
piano__8_68 = l.sd + r.augment(frac(13, 8)) + s3.o(1).p + s2.o(1).p
piano__9_68 = s4.e.o(1).p + r.e + s4.o(1).p + r.h
chord_68 = (I % VI.M)(piano__4=piano__4_68, piano__5=piano__5_68,
                      piano__7=piano__7_68, piano__8=piano__8_68, piano__9=piano__9_68)

piano__2_69 = l.n + s2.s.o(-1).p + r.ed + s2.t.o(-1).p + r.augment(frac(23, 8))
piano__3_69 = l.sd + r.t + \
    s4.s.o(-1).pp + r.ed + s4.s.o(-1).pp + r.s + \
    s3.s.o(-1).pp + r.ed + s3.s.o(-1).p + r.ed
piano__4_69 = l.t + r.t + s0.s.pp + r.s + s0.s.pp + r.s + s0.s.pp + \
    r.s + s0.s.pp + r.e + s6.s.o(-1).p + r.ed + s5.s.o(-1).pp + r.s
piano__5_69 = l.t + r.augment(frac(17, 8)) + s1.s.p + \
    r.s + s1.s.p + r.s + s2.s.pp + r.s + s2.s.pp
piano__7_69 = l.n + s0.ed.o(1).mf + r + s0.s.o(1).p + s6.mf + s0.t.o(
    1).p + r.t + s0.t.o(1).p + r.t + s0.t.o(1).p + s6.t.p + s0.t.o(1).p + r.t
piano__8_69 = l.sd + r.augment(frac(7, 8)) + s2.s.o(1).p + s1.s.o(
    1).p + r.augment(frac(11, 8)) + s1.t.o(1).p + r.t + s1.t.o(1).p + r.e
piano__9_69 = r.ed + s4.s.o(1).p + s3.t.o(1).p + r.augment(frac(23, 8))
chord_69 = (II[7] % VI.M)(piano__2=piano__2_69, piano__3=piano__3_69, piano__4=piano__4_69,
                          piano__5=piano__5_69, piano__7=piano__7_69, piano__8=piano__8_69, piano__9=piano__9_69)

piano__4_70 = l.n + s0.s.p + \
    r.augment(frac(7, 4)) + s1.s.pp + r.s + s1.s.pp + \
    r.s + s0.s.pp + r.s + s0.s.pp + r.s
piano__5_70 = l.t + r.sd + s2.s.pp + r.s + \
    s2.s.pp + r.s + s2.s.pp + r.augment(frac(9, 4))
piano__6_70 = r.s + s4.s.p + r.s + s4.s.pp + r.hd
piano__7_70 = l.n + s0.e.o(1).mf + r.ed + s0.s.o(1).pp + r.s + s0.s.o(1).pp + \
    r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + \
    s0.s.o(1).pp + r.s + s0.s.o(1).pp
piano__8_70 = l.sd + r.augment(frac(13, 8)) + s3.o(1).p + s2.o(1).p
piano__9_70 = r + s4.o(1).p + r.h
chord_70 = (I % VI.M)(piano__4=piano__4_70, piano__5=piano__5_70, piano__6=piano__6_70,
                      piano__7=piano__7_70, piano__8=piano__8_70, piano__9=piano__9_70)

piano__9_71 = s2.ed.o(1).p + s2.t.o(1).p + s1.t.o(1).p + \
    s2.s.o(1).p + r.augment(frac(9, 4)) + s2.e.o(1).p
piano__10_71 = l.augment(frac(5, 8)) + r.t + s3.n.o(1).p + r.ed + \
    s3.s.o(1).p + r.s + s5.e.o(1).p + s4.e.o(1).p + s3.e.o(1).p + r.e
piano__5_71 = l.n + s0.s.pp + r.ed + s0.s.pp + \
    r.ed + s0.s.pp + r.ed + s0.s.pp + r.ed
piano__7_71 = l.s + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + \
    s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp
chord_71 = (IV % VI.M)(piano__9=piano__9_71, piano__10=piano__10_71,
                       piano__5=piano__5_71, piano__7=piano__7_71)

piano__4_72 = l.t + r.augment(frac(15, 8)) + s1.s.p + \
    r.s + s1.s.pp + r.s + s0.s.p + r.s + s0.s.pp + r.s
piano__5_72 = l.n + s2.s.pp + r.ed + s2.s.p + \
    r.s + s2.s.pp + r.augment(frac(9, 4))
piano__7_72 = l.s + s0.s.o(1).pp + s6.s.pp + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp
piano__8_72 = l.sd + r.augment(frac(13, 8)) + s3.o(1).p + s2.o(1).p
piano__9_72 = s4.e.o(1).p + r.e + s4.o(1).p + r.h
chord_72 = (I % VI.M)(piano__4=piano__4_72, piano__5=piano__5_72,
                      piano__7=piano__7_72, piano__8=piano__8_72, piano__9=piano__9_72)

piano__2_73 = l.n + s2.s.o(-1).p + r.ed + s2.t.o(-1).p + r.augment(frac(23, 8))
piano__3_73 = l.sd + r.t + \
    s4.s.o(-1).pp + r.ed + s4.s.o(-1).pp + r.s + \
    s3.s.o(-1).pp + r.ed + s3.s.o(-1).p + r.ed
piano__4_73 = l.t + r.t + s0.s.pp + r.s + s0.s.pp + r.s + s0.s.pp + \
    r.s + s0.s.pp + r.e + s6.s.o(-1).p + r.ed + s5.s.o(-1).pp + r.s
piano__5_73 = l.t + r.augment(frac(17, 8)) + s1.s.p + \
    r.s + s1.s.p + r.s + s2.s.pp + r.s + s2.s.pp
piano__7_73 = l.n + s0.ed.o(1).mf + r + s0.s.o(1).p + s6.mf + s0.t.o(
    1).p + r.t + s0.t.o(1).p + r.t + s0.t.o(1).p + s6.t.p + s0.t.o(1).p + r.t
piano__8_73 = l.sd + r.augment(frac(7, 8)) + s2.s.o(1).p + s1.s.o(
    1).p + r.augment(frac(11, 8)) + s1.t.o(1).p + r.t + s1.t.o(1).p + r.e
piano__9_73 = r.ed + s4.s.o(1).p + s3.t.o(1).p + r.augment(frac(23, 8))
chord_73 = (II[7] % VI.M)(piano__2=piano__2_73, piano__3=piano__3_73, piano__4=piano__4_73,
                          piano__5=piano__5_73, piano__7=piano__7_73, piano__8=piano__8_73, piano__9=piano__9_73)

piano__3_74 = l.sd + r.augment(frac(9, 8)) + s4.s.o(-1).p + \
    r.augment(frac(7, 4)) + s4.s.o(-1).p + r.s
piano__4_74 = l.n + s0.p + r.e + \
    s6.s.o(-1).p + r.s + s0.p + r.e + s6.s.o(-1).p + r.s
piano__5_74 = l.n + s2.p + r.e + s1.s.p + r.s + s2.p + r.e + s1.s.p + r.s
piano__6_74 = r.s + s4.s.p + r.augment(frac(7, 4)) + s4.s.p + r.qd
piano__7_74 = l.n + s0.s.o(1).mf + r.s + s0.s.o(1).mf + r + \
    s1.s.o(1).p + s0.s.o(1).mf + r.s + s0.s.o(1).mf + r + s1.s.o(1).p
piano__8_74 = l.sd + r.sd + s2.s.o(1).p + r.s + s2.s.o(1).p + s3.s.o(
    1).mf + r + s2.s.o(1).p + r.s + s2.s.o(1).p + s3.s.o(1).mf + r.s
piano__9_74 = r + s4.s.o(1).mf + r.augment(frac(7, 4)) + s4.s.o(1).mf + r.ed
chord_74 = (I % VI.M)(piano__3=piano__3_74, piano__4=piano__4_74, piano__5=piano__5_74,
                      piano__6=piano__6_74, piano__7=piano__7_74, piano__8=piano__8_74, piano__9=piano__9_74)

piano__0_75 = r + h11.e.o(-3).p + r.e + s0.e.o(-2).p + r.qd
piano__3_75 = l.sd + r.augment(frac(5, 8)) + \
    h11.e.o(-2).mf + r.e + s0.e.o(-1).mf + r.qd
piano__4_75 = l.n + s2.e.o(-1).p + r.augment(frac(7, 2))
piano__5_75 = l.n + s4.e.o(-1).mf + r.augment(frac(7, 2))
piano__7_75 = l.n + s2.e.mf + r.e + s3.e.mf + r.e + s2.e.mf + r.qd
piano__8_75 = l.sd + r.augment(frac(5, 8)) + s5.e.mf + r.e + s4.e.mf + r.qd
piano__10_75 = l.augment(frac(5, 8)) + r.sd + \
    s1.e.o(1).mf + r.e + s2.e.o(1).mf + r.qd
chord_75 = (VI % VI.M)(piano__0=piano__0_75, piano__3=piano__3_75, piano__4=piano__4_75,
                       piano__5=piano__5_75, piano__7=piano__7_75, piano__8=piano__8_75, piano__10=piano__10_75)

piano__2_76 = l.n + s6.h.o(-2).pp + r.h
piano__3_76 = l.sd + r.augment(frac(13, 8)) + s0.h.o(-1).pp
piano__4_76 = l.t + r.augment(frac(27, 8)) + s4.s.o(-1).pp + r.s
piano__5_76 = l.t + r.augment(frac(11, 8)) + s6.s.o(-1).pp + \
    r.s + s6.e.o(-1).pp + s5.s.o(-1).pp + r.s + s5.e.o(-1).pp + r.e
piano__6_76 = s1.e.pp + s0.s.pp + r.s + s0.e.pp + r.augment(frac(5, 2))
piano__7_76 = l.sd + r.augment(frac(9, 8)) + s4.s.p + \
    r.s + s4.e.p + s3.s.p + r.s + s3.e.p + s2.s.p + r.s
piano__8_76 = l.n + s6.e.p + s5.s.p + r.s + s5.e.p + r.augment(frac(5, 2))
chord_76 = (V[7] % VI.M)(piano__2=piano__2_76, piano__3=piano__3_76, piano__4=piano__4_76,
                         piano__5=piano__5_76, piano__6=piano__6_76, piano__7=piano__7_76, piano__8=piano__8_76)

piano__1_77 = l.sd + r.augment(frac(13, 8)) + s3.o(-2).pp + r
piano__3_77 = l.sd + r.augment(frac(5, 8)) + s0.o(-1).pp + r.h
piano__4_77 = l.n + s3.o(-1).pp + r.hd
piano__5_77 = l.n + s4.h.o(-1).pp + s5.o(-1).pp + r
piano__6_77 = s6.h.o(-1).p + r.h
piano__7_77 = l.n + s2.h.p + s3.p + r
chord_77 = (V[7] % VI.M)(piano__1=piano__1_77, piano__3=piano__3_77, piano__4=piano__4_77,
                         piano__5=piano__5_77, piano__6=piano__6_77, piano__7=piano__7_77)

piano__8_78 = l.sd + r.augment(frac(25, 8)) + s5.s.o(1).p + r.s
piano__9_78 = r.qd + s0.s.o(2).p + r.s + s0.e.o(2).p + \
    s6.s.o(1).p + r.s + s6.e.o(1).p + r.e
piano__10_78 = l.n + s2.e.o(2).p + s1.s.o(2).p + \
    r.s + s1.e.o(2).p + r.augment(frac(5, 2))
chord_78 = (II[7] % III.mm)(piano__8=piano__8_78,
                            piano__9=piano__9_78, piano__10=piano__10_78)

piano__1_79 = l.n + s2.w.o(-1).p
piano__4_79 = l.n + s2.w.p
piano__6_79 = r.augment(frac(5, 2)) + s0.s.o(1).p + \
    r.s + s0.e.o(1).p + s6.s.p + r.s
piano__7_79 = l.sd + r.t + \
    s2.s.o(1).p + r.s + s2.e.o(1).mf + s1.s.o(1).p + r.s + s1.e.o(1).p + r.qd
piano__8_79 = l.n + h5.e.o(1).mf + r.augment(frac(7, 2))
piano__9_79 = s4.w.o(1).mf
chord_79 = (III % III.mm)(piano__1=piano__1_79, piano__4=piano__4_79,
                          piano__6=piano__6_79, piano__7=piano__7_79, piano__8=piano__8_79, piano__9=piano__9_79)

piano__6_80 = r.hd + s4.e.pp + r.e
piano__7_80 = l.sd + r.augment(frac(5, 8)) + \
    s0.e.o(1).pp + r.qd + s2.e.o(1).p + r.e
piano__8_80 = l.n + s4.e.o(1).p + r.e + s2.e.o(1).p + r.augment(frac(5, 2))
piano__9_80 = r.e + s5.s.o(1).p + r.augment(frac(5, 4)) + \
    h10.e.o(1).p + s6.s.o(1).p + r.augment(frac(5, 4))
piano__10_80 = l.augment(frac(5, 8)) + r.augment(frac(7, 8)
                                                 ) + s0.e.o(2).p + r.qd + s1.e.o(2).p
chord_80 = (III % III.mm)(piano__6=piano__6_80, piano__7=piano__7_80,
                          piano__8=piano__8_80, piano__9=piano__9_80, piano__10=piano__10_80)

piano__0_81 = r.qd + s3.s.o(-2).p + r.ed + s2.s.o(-2).p + \
    r.s + s2.e.o(-2).p + s1.s.o(-2).p + r.s
piano__1_81 = l.n + s5.e.o(-2).mf + s4.s.o(-2).mf + \
    r.s + s4.e.o(-2).mf + r.e + s3.e.o(-2).mf + r.qd
piano__10_81 = l.n + s2.h.o(1).p + s3.o(1).p + r
piano__9_81 = s0.h.o(1).p + s1.o(1).p + r
chord_81 = (VII % III.mm)(piano__0=piano__0_81, piano__1=piano__1_81,
                          piano__10=piano__10_81, piano__9=piano__9_81)

piano__8_82 = l.sd + r.augment(frac(17, 8)) + \
    s6.s.p + r.s + s6.e.p + s5.s.p + r.s
piano__9_82 = r + s1.e.o(1).p + s0.s.o(1).p + r.s + s0.e.o(1).p + r.qd
piano__10_82 = l.n + s2.e.o(1).p + s1.s.o(1).p + r.augment(frac(13, 4))
chord_82 = (IV[7] % VII.m)(piano__8=piano__8_82,
                           piano__9=piano__9_82, piano__10=piano__10_82)

piano__1_83 = l.n + s2.w.o(-2).p
piano__4_83 = l.n + s2.w.o(-1).p
piano__6_83 = r.h + h1.e.mf + s0.s.p + r.s + s0.e.mf + s6.s.o(-1).p + r.s
piano__7_83 = l.n + h4.e.mf + s2.s.p + r.s + \
    s2.e.mf + h1.s.p + r.augment(frac(9, 4))
piano__8_83 = l.n + s4.w.mf
chord_83 = (VI % VI.M)(piano__1=piano__1_83, piano__4=piano__4_83,
                       piano__6=piano__6_83, piano__7=piano__7_83, piano__8=piano__8_83)

piano__5_84 = l.t + r.augment(frac(23, 8)) + s4.e.o(-1).pp + r.e
piano__6_84 = r + s0.e.pp + r.augment(frac(5, 2))
piano__7_84 = l.sd + r.augment(frac(5, 8)) + s2.e.p + r.qd + s2.e.p + r.e
piano__8_84 = l.n + s4.e.p + s5.s.p + r.augment(frac(13, 4))
piano__9_84 = r.h + h9.e.p + s6.s.p + r.augment(frac(5, 4))
piano__10_84 = l.augment(frac(5, 8)) + r.augment(frac(7, 8)
                                                 ) + s0.e.o(1).p + r.qd + h1.e.o(1).p
chord_84 = (VI % VI.M)(piano__5=piano__5_84, piano__6=piano__6_84, piano__7=piano__7_84,
                       piano__8=piano__8_84, piano__9=piano__9_84, piano__10=piano__10_84)

piano__0_85 = r.e + h1.s.o(-2).mf + r.s + h1.e.o(-2).mf + s0.s.o(-2).p + \
    r.s + s0.e.o(-2).mf + s6.s.o(-3).p + r.s + \
    s6.e.o(-3).p + s5.s.o(-3).p + r.s
piano__1_85 = l.n + s2.e.o(-2).mf + r.augment(frac(7, 2))
piano__8_85 = l.n + s4.h.p + s5.p + r
piano__9_85 = s6.h.p + r.h
piano__10_85 = l.augment(frac(5, 8)) + r.augment(frac(11, 8)) + s0.o(1).p + r
chord_85 = (VI[7] % VI.M)(piano__0=piano__0_85, piano__1=piano__1_85,
                          piano__8=piano__8_85, piano__9=piano__9_85, piano__10=piano__10_85)

piano__9_86 = r.qd + s2.s.o(2).p + r.s + s2.s.o(2).p + r.s + \
    s2.s.o(2).p + r.s + s2.s.o(2).p + r.s + s2.s.o(2).p + r.s
piano__10_86 = l.n + s2.s.o(2).p + s0.s.o(3).p + s2.s.o(2).p + s0.s.o(3).p + s2.s.o(2).p + s0.s.o(
    3).p + r.s + s0.s.o(3).p + r.s + s0.s.o(3).p + r.s + s0.s.o(3).p + r.s + s0.s.o(3).p + r.s + s0.s.o(3).p
piano__4_86 = l.t + r.augment(frac(11, 8)) + s5.s.p + \
    r.s + s5.e.p + s4.s.p + r.s + s4.e.p + h6.s.p + r.s
piano__5_86 = l.n + s0.e.o(1).p + s6.s.p + r.s + s6.e.p + r.augment(frac(5, 2))
chord_86 = (I % II.M)(piano__9=piano__9_86, piano__10=piano__10_86,
                      piano__4=piano__4_86, piano__5=piano__5_86)

piano__1_87 = l.n + s6.h.o(-3).p + s0.h.o(-2).p
piano__10_87 = l.s + h4.s.o(1).p + r.s + h4.s.o(1).p + r.s + h4.s.o(1).p + r.s + h4.s.o(
    1).p + r.s + s2.s.o(1).p + r.s + s2.s.o(1).p + r.s + s2.s.o(1).p + r.s + s2.s.o(1).p
piano__4_87 = l.n + s6.h.o(-2).mf + s0.h.o(-1).mf
piano__9_87 = s4.s.mf + r.s + s4.s.mf + r.s + s4.s.mf + r.s + s4.s.mf + \
    r.s + s4.s.mf + r.s + s4.s.mf + r.s + s4.s.p + r.s + s4.s.p + r.s
chord_87 = (VII[7] % VII.M)(piano__1=piano__1_87,
                            piano__10=piano__10_87, piano__4=piano__4_87, piano__9=piano__9_87)

piano__3_88 = l.sd + r.augment(frac(17, 8)) + s6.s.o(-2).p + \
    r.s + s6.e.o(-2).p + h10.s.o(-2).p + r.s
piano__4_88 = l.t + r.sd + \
    h2.s.o(-1).p + r.s + h2.e.o(-1).p + \
    s0.s.o(-1).p + r.s + s0.e.o(-1).p + r.qd
piano__5_88 = l.n + s2.e.o(-1).p + r.augment(frac(7, 2))
piano__8_88 = l.n + s4.s.p + r.s + s4.s.p + r.s + s4.s.p + r.s + s4.s.p + \
    r.s + s4.s.p + r.s + s4.s.p + r.s + s4.s.p + r.s + s4.s.p + r.s
piano__10_88 = l.s + s3.s.o(1).p + r.s + s3.s.o(1).p + r.s + s3.s.o(1).p + r.s + s3.s.o(
    1).p + r.s + s2.s.o(1).p + r.s + s2.s.o(1).p + r.s + s2.s.o(1).p + r.s + s2.s.o(1).p
chord_88 = (VI[7] % VII.m)(piano__3=piano__3_88, piano__4=piano__4_88,
                           piano__5=piano__5_88, piano__8=piano__8_88, piano__10=piano__10_88)

piano__0_89 = s6.h.o(-2).p + s0.h.o(-1).p
piano__8_89 = l.n + s4.s.o(1).mf + r.s + s4.s.o(1).mf + r.s + s4.s.o(1).mf + r.s + s4.s.o(
    1).mf + r.s + h6.s.o(1).mf + r.s + h6.s.o(1).mf + r.s + h6.s.o(1).p + r.s + h6.s.o(1).p + r.s
piano__10_89 = l.s + s3.s.o(2).p + r.s + s3.s.o(2).p + r.s + s3.s.o(2).p + r.s + s3.s.o(
    2).p + r.s + h3.s.o(2).p + r.s + h3.s.o(2).p + r.s + h3.s.o(2).p + r.s + h3.s.o(2).p
piano__3_89 = l.n + s6.h.o(-1).mf + s0.h.mf
chord_89 = (I[7] % IV.s.M)(piano__0=piano__0_89, piano__8=piano__8_89,
                           piano__10=piano__10_89, piano__3=piano__3_89)

piano__3_90 = l.n + s0.s.o(-1).p + r.ed + s0.s.o(-1).p + \
    r.ed + s0.s.o(-1).p + r.ed + s0.s.o(-1).p + r.ed
piano__4_90 = l.t + r.sd + \
    s2.s.o(-1).p + r.augment(frac(7, 4)) + s2.s.o(-1).p + r.augment(frac(5, 4))
piano__5_90 = l.t + r.t + s4.s.o(-1).pp + r.s + s4.s.o(-1).pp + r.s + s4.s.o(-1).pp + s2.s.o(-1).p + \
    s4.s.o(-1).pp + r.s + s4.s.o(-1).pp + r.s + s4.s.o(-1).pp + \
    r.s + s4.s.o(-1).pp + s2.s.o(-1).p + s4.s.o(-1).pp
piano__8_90 = l.n + s2.p + r.hd
piano__9_90 = r.qd + s6.sd.p + r.t + h10.pp + r
piano__10_90 = l.n + h2.e.o(1).p + s0.sd.o(1).p + r.t + s0.e.o(1).p + \
    r.e + s4.e.o(1).p + s3.sd.o(1).p + r.t + s3.e.o(1).p + s2.sd.o(1).p + r.t
chord_90 = (VI % VII.m)(piano__3=piano__3_90, piano__4=piano__4_90, piano__5=piano__5_90,
                        piano__8=piano__8_90, piano__9=piano__9_90, piano__10=piano__10_90)

piano__3_91 = l.n + s4.s.o(-1).p + r.ed + s4.s.o(-1).p + r.ed + \
    h6.s.o(-1).p + r.ed + h6.s.o(-1).p + r.s + h9.s.o(-1).p + r.s
piano__4_91 = l.t + r.sd + \
    s6.s.o(-1).p + r.ed + s6.s.o(-1).p + r.ed + \
    h9.s.o(-1).p + r.augment(frac(5, 4))
piano__5_91 = l.t + r.t + s1.s.pp + r.s + s1.s.pp + r.s + s1.s.pp + r.s + \
    s1.s.pp + r.s + s2.s.pp + r.s + s2.s.pp + r.s + s2.s.pp + r.s + s2.s.pp
piano__8_91 = l.sd + r.augment(frac(13, 8)) + s2.e.o(1).mf + \
    s1.sd.o(1).p + r.t + s1.e.o(1).mf + s0.sd.o(1).p + r.t
piano__9_91 = s5.e.o(1).p + s4.sd.o(1).p + r.t + \
    s4.e.o(1).p + s3.sd.o(1).p + r.augment(frac(17, 8))
piano__10_91 = l.n + s6.h.o(1).p + s0.h.o(2).mf
chord_91 = (I % VII.m)(piano__3=piano__3_91, piano__4=piano__4_91, piano__5=piano__5_91,
                       piano__8=piano__8_91, piano__9=piano__9_91, piano__10=piano__10_91)

piano__1_92 = l.sd + r.augment(frac(13, 8)) + s4.h.o(-2).pp
piano__3_92 = l.n + s4.h.o(-1).pp + r.h
piano__5_92 = l.t + r.augment(frac(19, 8)) + \
    s2.s.pp + r.s + s2.e.pp + s1.s.pp + r.s
piano__6_92 = s5.e.pp + s4.s.pp + r.s + s4.e.pp + s3.s.pp + r.s + s3.e.pp + r.qd
piano__7_92 = l.sd + r.augment(frac(21, 8)) + s0.e.o(1).p + s6.s.p + r.s
piano__8_92 = l.sd + r.t + s2.s.o(1).p + r.s + s2.e.o(1).p + s1.s.o(
    1).p + r.s + s1.e.o(1).p + s0.s.o(1).p + r.augment(frac(5, 4))
piano__9_92 = s3.e.o(1).p + r.augment(frac(7, 2))
chord_92 = (I % VII.m)(piano__1=piano__1_92, piano__3=piano__3_92, piano__5=piano__5_92,
                       piano__6=piano__6_92, piano__7=piano__7_92, piano__8=piano__8_92, piano__9=piano__9_92)

piano__0_93 = r + s3.o(-2).pp + s6.o(-3).pp + r
piano__1_93 = l.n + s6.o(-2).pp + r.hd
piano__5_93 = l.n + s0.h.pp + s1.pp + r
piano__6_93 = s2.h.p + r.h
piano__7_93 = l.n + s5.h.p + s6.p + r
chord_93 = (II[7] % VII.m)(piano__0=piano__0_93, piano__1=piano__1_93,
                           piano__5=piano__5_93, piano__6=piano__6_93, piano__7=piano__7_93)

piano__1_94 = l.n + s0.h.o(-1).p + s6.o(-2).p + r
piano__4_94 = l.n + s0.h.mf + s6.o(-1).p + r
piano__5_94 = l.n + s2.h.p + s2.p + r
piano__6_94 = s4.h.p + s4.p + r
piano__7_94 = l.n + s0.h.o(1).mf + h1.o(1).mf + r
chord_94 = (IV[7] % IV.s.m)(piano__1=piano__1_94, piano__4=piano__4_94,
                            piano__5=piano__5_94, piano__6=piano__6_94, piano__7=piano__7_94)

piano__1_95 = l.n + s0.h.o(-1).pp + s6.o(-2).pp + r
piano__3_95 = l.n + s0.h.pp + s6.o(-1).pp + r
piano__7_95 = l.n + s2.h.o(1).pp + r.h
piano__8_95 = l.n + s4.qd.o(1).p + h8.e.o(1).pp + s3.o(1).pp + r
piano__9_95 = r.h + s5.o(1).p + r
chord_95 = (I[7] % V.M)(piano__1=piano__1_95, piano__3=piano__3_95,
                        piano__7=piano__7_95, piano__8=piano__8_95, piano__9=piano__9_95)

piano__3_96 = l.sd + r.augment(frac(21, 8)) + s0.s.p + r.s + s0.s.pp + r.s
piano__4_96 = l.t + r.augment(frac(7, 8)) + s2.s.p + r.s + \
    s2.s.pp + r.s + s1.s.p + r.s + s1.s.pp + r.augment(frac(5, 4))
piano__6_96 = r.augment(frac(5, 4)) + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + \
    s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp
piano__7_96 = l.sd + r.augment(frac(21, 8)) + s2.o(1).p
piano__8_96 = l.sd + r.augment(frac(5, 8)) + s4.o(1).p + s3.o(1).p + r
chord_96 = (I % V.M)(piano__3=piano__3_96, piano__4=piano__4_96,
                     piano__6=piano__6_96, piano__7=piano__7_96, piano__8=piano__8_96)

piano__5_97 = l.n + s0.s.p + r.ed + s0.s.p + \
    r.ed + s0.s.pp + r.ed + s0.s.pp + r.ed
piano__6_97 = r.s + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + \
    s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp
piano__8_97 = l.sd + r.e + s1.t.o(1).p + r.hd
piano__9_97 = s2.ed.o(1).p + s2.t.o(1).p + r.t + s2.s.o(1).p + r.s + \
    s3.s.o(1).p + r.ed + s4.s.o(1).p + r.s + s3.e.o(1).p + s2.s.o(1).p + r.s
piano__10_97 = l.augment(frac(5, 8)) + r.t + s3.n.o(1).p + \
    r.augment(frac(5, 4)) + s5.e.o(1).p + r.qd
chord_97 = (IV % V.M)(piano__5=piano__5_97, piano__6=piano__6_97,
                      piano__8=piano__8_97, piano__9=piano__9_97, piano__10=piano__10_97)

piano__3_98 = l.sd + r.augment(frac(21, 8)) + s0.s.pp + r.s + s0.s.pp + r.s
piano__4_98 = l.n + s2.s.p + r.ed + s2.s.pp + r.s + s2.s.pp + \
    r.s + s1.s.pp + r.s + s1.s.pp + r.augment(frac(5, 4))
piano__6_98 = r.s + s0.s.o(1).p + s6.s.pp + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp
piano__7_98 = l.sd + r.augment(frac(13, 8)) + s3.o(1).p + s2.o(1).p
piano__8_98 = l.n + s4.e.o(1).p + r.e + s4.o(1).p + r.h
chord_98 = (I % V.M)(piano__3=piano__3_98, piano__4=piano__4_98,
                     piano__6=piano__6_98, piano__7=piano__7_98, piano__8=piano__8_98)

piano__1_99 = l.n + s2.s.o(-1).pp + r.augment(frac(15, 4))
piano__2_99 = l.t + r.sd + s4.s.o(-1).pp + r.s + s2.t.o(-1).pp + r.sd + \
    s4.s.o(-1).pp + r.s + s3.s.o(-1).pp + r.ed + s3.s.o(-1).pp + r.ed
piano__3_99 = l.sd + r.augment(frac(17, 8)) + \
    s6.s.o(-1).pp + r.ed + s5.s.o(-1).pp + r.s
piano__4_99 = l.t + r.t + s0.s.pp + r.s + s0.s.pp + r.s + \
    s0.s.pp + r.s + s0.s.pp + r.s + s1.s.pp + r.s + s1.s.pp + r
piano__5_99 = l.t + r.augment(frac(25, 8)) + s2.s.pp + r.s + s2.s.pp
piano__6_99 = s0.ed.o(1).p + r + s0.s.o(1).p + s6.p + s0.t.o(1).p + \
    r.t + s0.t.o(1).p + r.t + s0.t.o(1).p + s6.t.pp + s0.t.o(1).pp + r.t
piano__7_99 = l.sd + r.augment(frac(7, 8)) + s2.s.o(1).p + s1.s.o(
    1).p + r.augment(frac(11, 8)) + s1.t.o(1).pp + r.t + s1.t.o(1).p + r.e
piano__8_99 = l.sd + r.augment(frac(5, 8)) + \
    s3.t.o(1).p + r.augment(frac(23, 8))
piano__9_99 = r.ed + s4.s.o(1).p + r.hd
chord_99 = (II[7] % V.M)(piano__1=piano__1_99, piano__2=piano__2_99, piano__3=piano__3_99, piano__4=piano__4_99,
                         piano__5=piano__5_99, piano__6=piano__6_99, piano__7=piano__7_99, piano__8=piano__8_99, piano__9=piano__9_99)

piano__3_100 = l.n + s0.s.pp + \
    r.augment(frac(11, 4)) + s0.s.p + r.s + s0.s.pp + r.s
piano__4_100 = l.t + r.augment(frac(15, 8)) + \
    s1.s.p + r.s + s1.s.pp + r.augment(frac(5, 4))
piano__5_100 = l.t + r.t + s4.s.pp + s2.s.pp + s4.s.pp + \
    s2.s.p + r.s + s2.s.pp + r.augment(frac(9, 4))
piano__6_100 = s0.e.o(1).p + r.ed + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + \
    s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp
piano__7_100 = l.sd + r.augment(frac(13, 8)) + s3.o(1).p + s2.o(1).p
piano__8_100 = l.sd + r.augment(frac(5, 8)) + s4.o(1).p + r.h
chord_100 = (I % V.M)(piano__3=piano__3_100, piano__4=piano__4_100, piano__5=piano__5_100,
                      piano__6=piano__6_100, piano__7=piano__7_100, piano__8=piano__8_100)

piano__5_101 = l.n + s0.s.p + r.ed + s0.s.p + \
    r.ed + s0.s.pp + r.ed + s0.s.pp + r.ed
piano__6_101 = r.s + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + \
    s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp
piano__8_101 = l.n + s2.ed.o(1).p + s2.t.o(1).p + \
    s1.t.o(1).p + s2.s.o(1).p + r.augment(frac(11, 4))
piano__9_101 = r.ed + s3.n.o(1).p + r.ed + s3.s.o(1).p + \
    r.ed + s4.s.o(1).p + r.s + s3.e.o(1).p + s2.s.o(1).p + r.s
piano__10_101 = l.augment(frac(5, 8)) + \
    r.augment(frac(11, 8)) + s5.e.o(1).p + r.qd
chord_101 = (IV % V.M)(piano__5=piano__5_101, piano__6=piano__6_101,
                       piano__8=piano__8_101, piano__9=piano__9_101, piano__10=piano__10_101)

piano__3_102 = l.sd + r.augment(frac(21, 8)) + s0.s.pp + r.s + s0.s.pp + r.s
piano__4_102 = l.t + r.augment(frac(15, 8)) + \
    s1.s.pp + r.s + s1.s.pp + r.augment(frac(5, 4))
piano__5_102 = l.n + s2.s.p + r.ed + s2.s.pp + \
    r.s + s2.s.pp + r.augment(frac(9, 4))
piano__6_102 = r.s + s0.s.o(1).p + s6.s.pp + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp
piano__7_102 = l.sd + r.augment(frac(13, 8)) + s3.o(1).p + s2.o(1).p
piano__8_102 = l.n + s4.e.o(1).p + r.e + s4.o(1).p + r.h
chord_102 = (I % V.M)(piano__3=piano__3_102, piano__4=piano__4_102, piano__5=piano__5_102,
                      piano__6=piano__6_102, piano__7=piano__7_102, piano__8=piano__8_102)

piano__1_103 = l.n + s2.s.o(-1).pp + r.augment(frac(15, 4))
piano__2_103 = l.t + r.sd + s4.s.o(-1).pp + r.s + s2.t.o(-1).pp + r.sd + \
    s4.s.o(-1).pp + r.s + s3.s.o(-1).pp + r.ed + s3.s.o(-1).pp + r.ed
piano__3_103 = l.sd + r.augment(frac(17, 8)) + \
    s6.s.o(-1).pp + r.ed + s5.s.o(-1).pp + r.s
piano__4_103 = l.t + r.t + s0.s.pp + r.s + \
    s0.s.pp + r.s + s0.s.pp + r.s + s0.s.pp + r.h
piano__5_103 = l.t + r.augment(frac(17, 8)) + s1.s.pp + \
    r.s + s1.s.pp + r.s + s2.s.pp + r.s + s2.s.pp
piano__6_103 = s0.ed.o(1).p + r + s0.s.o(1).p + s6.p + s0.t.o(1).p + \
    r.t + s0.t.o(1).p + r.t + s0.t.o(1).p + s6.t.pp + s0.t.o(1).pp + r.t
piano__7_103 = l.sd + r.augment(frac(7, 8)) + s2.s.o(1).p + s1.s.o(
    1).p + r.augment(frac(11, 8)) + s1.t.o(1).pp + r.t + s1.t.o(1).p + r.e
piano__8_103 = l.sd + r.sd + s4.s.o(1).p + s3.t.o(1).p + r.augment(frac(23, 8))
chord_103 = (II[7] % V.M)(piano__1=piano__1_103, piano__2=piano__2_103, piano__3=piano__3_103, piano__4=piano__4_103,
                          piano__5=piano__5_103, piano__6=piano__6_103, piano__7=piano__7_103, piano__8=piano__8_103)

piano__3_104 = l.n + s0.p + r.e + \
    s6.s.o(-1).pp + r.s + s0.p + r.e + s6.s.o(-1).pp + r.s
piano__5_104 = l.n + s2.p + r.e + s4.s.p + r.s + s4.p + r.e + s4.s.p + r.s
piano__6_104 = s0.s.o(1).p + s1.s.o(1).p + s0.s.o(1).p + s6.s.p + s0.s.o(1).p + r.s + s1.s.o(
    1).p + r.e + s1.s.o(1).p + s0.s.o(1).p + s6.s.p + s0.s.o(1).p + r.s + s1.s.o(1).p + r.s
piano__7_104 = l.sd + r.augment(frac(7, 8)) + s2.s.o(1).p + r.s + \
    s3.s.o(1).p + s2.s.o(1).p + r + s2.s.o(1).p + r.s + s3.s.o(1).p
chord_104 = (I % V.M)(piano__3=piano__3_104, piano__5=piano__5_104,
                      piano__6=piano__6_104, piano__7=piano__7_104)

piano__2_105 = l.t + r.augment(frac(27, 8)) + s5.s.o(-1).pp + r.s
piano__3_105 = l.n + s0.p + r.e + \
    s6.s.o(-1).pp + r.s + s0.s.p + r.s + s6.s.o(-1).pp + \
    r.s + s0.s.pp + r.s + s0.s.p + r.s
piano__5_105 = l.n + s4.p + r.e + s4.s.p + r.s + \
    s4.s.p + r.s + s4.s.p + r.s + s4.s.p + r.ed
piano__6_105 = r.s + s1.s.o(1).p + s0.s.o(1).p + s6.s.p + \
    s0.s.o(1).p + r.s + s1.s.o(1).p + r + s1.s.o(1).p + r
piano__7_105 = l.n + s2.s.o(1).p + r + s2.s.o(1).p + r.s + s3.s.o(
    1).p + s2.s.o(1).p + r.s + s3.s.o(1).p + r.s + s2.s.o(1).p + r.ed
piano__8_105 = l.sd + r.augment(frac(15, 8)) + s4.s.o(1).p + \
    r.ed + s4.s.o(1).p + h6.s.o(1).p + s5.s.o(1).p
chord_105 = (I % V.M)(piano__2=piano__2_105, piano__3=piano__3_105, piano__5=piano__5_105,
                      piano__6=piano__6_105, piano__7=piano__7_105, piano__8=piano__8_105)

piano__2_106 = l.t + r.augment(frac(11, 8)) + \
    s6.s.o(-1).p + r.s + s0.p + r.e + s6.s.o(-1).p + r.s
piano__3_106 = l.n + s2.p + r.hd
piano__4_106 = l.n + s4.p + r.e + s4.s.p + r.s + s4.p + r.e + s4.s.p + r.s
piano__8_106 = l.n + s0.s.o(2).p + s1.s.o(2).p + s0.s.o(2).p + s6.s.o(1).p + s0.s.o(2).p + r.s + s1.s.o(
    2).p + r.e + s1.s.o(2).p + s0.s.o(2).p + s6.s.o(1).p + s0.s.o(2).p + r.s + s1.s.o(2).p + r.s
piano__9_106 = r.augment(frac(5, 4)) + s2.s.o(2).p + r.s + \
    s3.s.o(2).p + s2.s.o(2).p + r + s2.s.o(2).p + r.s + s3.s.o(2).p
chord_106 = (I % II.M)(piano__2=piano__2_106, piano__3=piano__3_106,
                       piano__4=piano__4_106, piano__8=piano__8_106, piano__9=piano__9_106)

piano__2_107 = l.n + s6.o(-1).p + r.e + h11.s.o(-1).p + \
    r.s + s0.p + r.e + h11.s.o(-1).p + r.s
piano__4_107 = l.n + s3.p + r.e + s4.s.p + r.s + s4.p + r.e + s4.s.p + r.s
piano__8_107 = l.s + s0.s.o(2).p + s6.s.o(1).p + s5.s.o(1).p + s6.s.o(
    1).p + s0.s.o(2).p + r + s0.s.o(2).mf + h11.s.o(1).p + s0.s.o(2).mf + r.ed
piano__9_107 = s1.s.o(2).p + r.augment(frac(5, 4)) + s1.s.o(2).mf + r.s + \
    s2.s.o(2).mf + s1.s.o(2).p + r.ed + s1.s.o(2).p + s2.s.o(2).mf + r.s
piano__10_107 = l.augment(frac(5, 8)) + r.augment(frac(9, 8)) + \
    s3.s.o(2).p + r.augment(frac(7, 4)) + s3.s.o(2).p
chord_107 = (II[7] % II.M)(piano__2=piano__2_107, piano__4=piano__4_107,
                           piano__8=piano__8_107, piano__9=piano__9_107, piano__10=piano__10_107)

piano__2_108 = l.n + s0.p + r.e + s0.s.p + r.augment(frac(7, 4)) + s0.s.p + r.s
piano__3_108 = l.sd + r.augment(frac(13, 8)) + s1.p + r
piano__4_108 = l.n + s4.p + r.hd
piano__5_108 = l.t + r.augment(frac(11, 8)) + \
    s5.s.p + r.s + s6.mf + r.e + s5.s.p + r.s
piano__8_108 = l.sd + r.t + \
    s0.s.o(2).mf + h11.s.o(1).mf + s0.s.o(2).mf + r.qd + s0.s.o(2).p + r
piano__9_108 = r.s + s1.s.o(2).mf + r.ed + s1.s.o(2).mf + s2.s.o(2).mf + \
    r.e + s2.s.o(2).p + s1.s.o(2).mf + r.s + s1.s.o(2).mf + s2.s.o(2).mf + r.e
piano__10_108 = l.n + s2.s.o(2).mf + r.qd + s4.s.o(2).p + \
    s3.s.o(2).mf + r.augment(frac(5, 4)) + s3.s.o(2).mf + s4.s.o(2).p
chord_108 = (II[7] % II.M)(piano__2=piano__2_108, piano__3=piano__3_108, piano__4=piano__4_108,
                           piano__5=piano__5_108, piano__8=piano__8_108, piano__9=piano__9_108, piano__10=piano__10_108)

piano__3_109 = l.n + s6.o(-1).p + r.hd
piano__5_109 = l.n + s4.mf + r.augment(frac(5, 2)) + h8.s.p + r.s
piano__6_109 = r.qd + s6.s.p + r.s + \
    s0.s.o(1).mf + r.s + s6.s.p + r.s + s0.s.o(1).mf + r.ed
piano__8_109 = l.sd + r.sd + s5.s.o(1).mf + r.hd
piano__9_109 = r.s + s0.s.o(2).mf + s6.s.o(1).mf + r.s + \
    s6.s.o(1).mf + s0.s.o(2).mf + r.h + s6.s.o(1).mf + r.s
piano__10_109 = l.n + s1.s.o(2).mf + r.augment(frac(5, 4)) + s1.s.o(2).mf + h5.s.o(2).p + s2.s.o(
    2).mf + s4.s.o(2).p + s1.s.o(2).mf + s4.s.o(2).p + s2.s.o(2).mf + s4.s.o(2).p + r.s + s2.s.o(2).p
chord_109 = (IV[7] % II.M)(piano__3=piano__3_109, piano__5=piano__5_109, piano__6=piano__6_109,
                           piano__8=piano__8_109, piano__9=piano__9_109, piano__10=piano__10_109)

piano__4_110 = l.t + r.augment(frac(27, 8)) + h4.s.p + r.s
piano__5_110 = l.n + s6.s.mf + r.s + h9.s.p + r.s + s6.s.mf + r.s + \
    s4.s.p + r.s + s5.s.mf + r.s + s4.s.p + r.s + s5.s.mf + r.ed
piano__7_110 = l.sd + r.augment(frac(25, 8)) + s4.s.o(1).mf + r.s
piano__8_110 = l.sd + r.augment(frac(9, 8)) + s6.s.o(1).mf + \
    r.ed + s6.s.o(1).mf + r.augment(frac(5, 4))
piano__9_110 = s1.s.o(2).mf + r.s + s0.s.o(2).mf + r.s + s1.s.o(2).mf + r.e + s2.s.o(2).p + \
    s0.s.o(2).mf + s2.s.o(2).p + r.s + s2.s.o(2).p + \
    s0.s.o(2).mf + s2.s.o(2).p + r.s + s0.s.o(2).p
piano__10_110 = l.s + s3.s.o(2).p + r.s + s3.s.o(2).p + \
    r.s + s3.s.o(2).p + r.augment(frac(5, 2))
chord_110 = (III[7] % II.M)(piano__4=piano__4_110, piano__5=piano__5_110, piano__7=piano__7_110,
                            piano__8=piano__8_110, piano__9=piano__9_110, piano__10=piano__10_110)

piano__3_111 = l.sd + r.augment(frac(13, 8)) + s0.p + r
piano__4_111 = l.n + s2.s.mf + r.s + h3.s.p + \
    r.s + s2.s.mf + r.s + s1.s.p + r.s + s2.mf + r
piano__5_111 = l.t + r.augment(frac(11, 8)) + h5.s.p + r.augment(frac(9, 4))
piano__7_111 = l.sd + r.t + s3.s.o(1).mf + r.augment(frac(13, 4))
piano__8_111 = l.n + s4.s.o(1).mf + s6.s.o(1).p + r.s + s6.s.o(1).p + s4.s.o(1).mf + s6.s.o(1).p + h8.s.o(
    1).mf + s6.s.o(1).p + s5.s.o(1).mf + h8.s.o(1).mf + s5.s.o(1).mf + s6.s.o(1).p + r.s + s6.s.o(1).p + r.e
piano__9_111 = r.hd + s0.s.o(2).mf + r.s + s0.s.o(2).mf + s1.s.o(2).p
chord_111 = (IV[7] % II.M)(piano__3=piano__3_111, piano__4=piano__4_111, piano__5=piano__5_111,
                           piano__7=piano__7_111, piano__8=piano__8_111, piano__9=piano__9_111)

piano__3_112 = l.n + s4.s.o(-1).p + r.s + s4.s.o(-1).pp + r.s + s4.s.o(-1).pp + r.s + s4.s.o(-1).pp + \
    r.s + s4.s.o(-1).p + r.s + s4.s.o(-1).pp + r.s + \
    h7.s.o(-1).pp + r.s + h7.s.o(-1).pp + r.s
piano__5_112 = l.n + s2.s.p + r.s + s2.s.pp + r.s + s2.s.pp + r.s + s2.s.pp + \
    r.s + s2.s.p + r.s + s2.s.pp + r.s + s2.s.pp + r.s + s2.s.pp + r.s
piano__7_112 = l.sd + r.augment(frac(23, 8)) + \
    s1.s.o(1).mf + s0.s.o(1).mf + s6.s.mf
piano__8_112 = l.sd + r.augment(frac(13, 8)) + \
    s2.s.o(1).mf + r.ed + s2.s.o(1).mf + r.ed
piano__9_112 = r.augment(frac(5, 4)) + s5.s.o(1).mf + s4.s.o(1).mf + \
    s3.s.o(1).mf + r.s + s3.s.o(1).mf + s4.s.o(1).mf + s3.s.o(1).mf + r
piano__10_112 = l.n + s6.s.o(1).p + s0.s.o(2).p + s1.s.o(2).mf + \
    s0.s.o(2).mf + s6.s.o(1).mf + r.augment(frac(11, 4))
chord_112 = (VII % II.M)(piano__3=piano__3_112, piano__5=piano__5_112, piano__7=piano__7_112,
                         piano__8=piano__8_112, piano__9=piano__9_112, piano__10=piano__10_112)

piano__1_113 = l.sd + r.augment(frac(17, 8)) + s4.e.o(-1).p + r
piano__2_113 = l.t + r.augment(frac(11, 8)) + \
    s0.s.p + r.s + s6.e.o(-1).p + r.e + s0.s.p + r.ed
piano__3_113 = l.sd + r.t + s3.e.p + s2.s.p + \
    r.augment(frac(9, 4)) + s2.s.p + r.s
piano__4_113 = l.n + s4.e.p + r.augment(frac(7, 2))
piano__6_113 = r.ed + s4.s.o(1).p + r.hd
piano__7_113 = l.n + s6.s.o(1).mf + s0.s.o(2).mf + s6.s.o(1).p + \
    r.s + s0.s.o(2).mf + r.augment(frac(5, 2)) + s0.s.o(2).p
piano__8_113 = l.sd + r.augment(frac(19, 8)) + \
    s1.s.o(2).p + r.s + s2.s.o(2).p + s1.s.o(2).p + r.s
piano__9_113 = r.h + s3.s.o(2).mf + s4.s.o(2).p + \
    s3.s.o(2).p + r.s + s3.s.o(2).mf + r.ed
chord_113 = (I[7] % II.M)(piano__1=piano__1_113, piano__2=piano__2_113, piano__3=piano__3_113, piano__4=piano__4_113,
                          piano__6=piano__6_113, piano__7=piano__7_113, piano__8=piano__8_113, piano__9=piano__9_113)

piano__1_114 = l.sd + r.augment(frac(17, 8)) + s4.e.o(-1).p + r
piano__2_114 = l.t + r.augment(frac(11, 8)) + \
    s0.s.p + r.s + s6.e.o(-1).p + r.e + s0.s.p + r.ed
piano__3_114 = l.sd + r.t + s3.e.p + s2.s.p + \
    r.augment(frac(9, 4)) + s2.s.p + r.s
piano__4_114 = l.n + s4.e.p + r.augment(frac(7, 2))
piano__6_114 = r.ed + s4.s.o(1).p + r.hd
piano__7_114 = l.n + s6.s.o(1).mf + s0.s.o(2).p + s6.s.o(1).p + \
    r.s + s0.s.o(2).mf + r.augment(frac(5, 2)) + s0.s.o(2).mf
piano__8_114 = l.sd + r.augment(frac(19, 8)) + \
    s1.s.o(2).p + r.e + s1.s.o(2).p + r.s
piano__9_114 = r.h + s3.s.o(2).mf + s4.s.o(2).p + \
    s3.s.o(2).p + r.s + s3.s.o(2).mf + s2.s.o(2).p + r.e
chord_114 = (I[7] % II.M)(piano__1=piano__1_114, piano__2=piano__2_114, piano__3=piano__3_114, piano__4=piano__4_114,
                          piano__6=piano__6_114, piano__7=piano__7_114, piano__8=piano__8_114, piano__9=piano__9_114)

piano__1_115 = l.n + s4.e.o(-2).p + r.qd + s4.e.o(-2).p + r.qd
piano__2_115 = l.t + r.augment(frac(7, 8)) + s0.e.o(-1).p + \
    r.e + s1.e.o(-1).p + r.e + s0.e.o(-1).p + r.e
piano__3_115 = l.n + s1.e.o(-1).p + r.e + \
    s2.e.o(-1).p + r.qd + s2.e.o(-1).p + r.e
piano__4_115 = l.n + s4.e.o(-1).p + r.e + s4.e.o(-1).p + \
    r.e + s4.e.o(-1).mf + r.e + s4.e.o(-1).mf + r.e
piano__6_115 = r.ed + s4.s.mf + r.augment(frac(7, 4)) + s4.s.p + r
piano__7_115 = l.n + s6.s.mf + r.s + s6.s.mf + r + \
    s0.s.o(1).mf + s6.s.mf + r.s + s6.s.p + r + s0.s.o(1).mf
piano__8_115 = l.s + s1.s.o(1).mf + r.e + s2.s.o(1).mf + r.s + \
    s2.s.o(1).mf + r.e + s1.s.o(1).p + r.e + s2.s.o(1).mf + r.ed
piano__9_115 = r.augment(frac(5, 4)) + s4.s.o(1).mf + \
    r.augment(frac(7, 4)) + s4.s.o(1).mf + s2.s.o(1).mf + r.s
chord_115 = (IV[7] % VI.M)(piano__1=piano__1_115, piano__2=piano__2_115, piano__3=piano__3_115, piano__4=piano__4_115,
                           piano__6=piano__6_115, piano__7=piano__7_115, piano__8=piano__8_115, piano__9=piano__9_115)

piano__1_116 = l.sd + r.t + s0.t.o(-1).p + r.sd + s0.t.o(-1).p + r.sd + \
    s0.t.o(-1).p + r.sd + s0.augment(frac(7, 8)
                                     ).o(-1).p + r.augment(frac(9, 8))
piano__2_116 = l.t + r.sd + s2.t.o(-1).p + r.sd + s2.t.o(-1).p + r.sd + \
    s2.t.o(-1).p + r.sd + s2.augment(frac(7, 8)
                                     ).o(-1).p + r.augment(frac(9, 8))
piano__3_116 = l.sd + r.t + s4.t.o(-1).p + r.sd + s4.t.o(-1).p + r.sd + \
    s4.t.o(-1).p + r.sd + s4.augment(frac(7, 8)
                                     ).o(-1).p + r.augment(frac(9, 8))
piano__4_116 = l.t + r.sd + s0.t.p + r.sd + s0.t.p + r.sd + \
    s0.t.p + r.sd + s0.augment(frac(7, 8)).p + r.augment(frac(9, 8))
piano__7_116 = l.n + s2.t.o(1).mf + r.sd + s2.t.o(1).p + r.sd + s2.t.o(1).p + \
    r.sd + s2.t.o(1).p + r.sd + s2.augment(frac(7, 8)
                                           ).o(1).p + r.augment(frac(9, 8))
piano__8_116 = l.n + s4.t.o(1).f + r.sd + s4.t.o(1).p + r.sd + s4.t.o(1).p + r.sd + s4.t.o(
    1).p + r.sd + s4.augment(frac(7, 8)).o(1).p + r.t + s5.s.o(1).p + s4.s.o(1).pp + s5.s.o(1).pp + r.s
piano__9_116 = r.e + s0.t.o(2).mf + r.sd + s0.t.o(2).mf + r.sd + s0.t.o(
    2).mf + r.sd + s0.augment(frac(7, 8)).o(2).mf + h10.t.o(1).p + r.ed + h10.s.o(1).pp
chord_116 = (I % VI.M)(piano__1=piano__1_116, piano__2=piano__2_116, piano__3=piano__3_116,
                       piano__4=piano__4_116, piano__7=piano__7_116, piano__8=piano__8_116, piano__9=piano__9_116)

piano__9_117 = h6.e.o(2).p + s4.e.o(2).p + r.e + \
    s4.e.o(2).pp + r.qd + s4.e.o(2).p
piano__10_117 = l.augment(frac(5, 8)) + r.augment(frac(11, 8)) + \
    s0.e.o(3).p + s6.e.o(2).p + s5.e.o(2).p + r.e
piano__5_117 = l.n + s0.e.o(1).pp + r.e + s1.e.o(1).pp + \
    r.e + s2.e.o(1).pp + r.e + s0.e.o(1).pp + s2.e.o(1).pp
piano__6_117 = r.e + s2.e.o(1).pp + r.e + s3.e.o(1).pp + r.e + s4.e.o(1).pp + r
chord_117 = (I % II.M)(piano__9=piano__9_117, piano__10=piano__10_117,
                       piano__5=piano__5_117, piano__6=piano__6_117)

piano__4_118 = l.t + r.augment(frac(23, 8)) + s0.e.pp + r.e
piano__5_118 = l.n + s4.e.pp + r + s4.e.pp + s2.e.pp + s4.e.pp + r
piano__6_118 = r + s6.e.pp + r.h + s6.e.pp
piano__7_118 = l.sd + r.t + s1.e.o(1).pp + r.hd
piano__8_118 = l.n + s5.e.o(1).p + r.augment(frac(5, 2)
                                             ) + s5.e.o(1).p + s4.e.o(1).p
piano__9_118 = r.e + s6.e.o(1).p + r.e + s6.e.o(1).pp + \
    s0.e.o(2).p + s6.e.o(1).p + r
chord_118 = (V[7] % II.M)(piano__4=piano__4_118, piano__5=piano__5_118, piano__6=piano__6_118,
                          piano__7=piano__7_118, piano__8=piano__8_118, piano__9=piano__9_118)

piano__4_119 = l.t + r.augment(frac(23, 8)) + s5.e.pp + r.e
piano__5_119 = l.t + r.augment(frac(7, 8)) + \
    s6.e.pp + r.e + s0.e.o(1).pp + r + s0.e.o(1).pp
piano__6_119 = s2.e.o(1).pp + s4.e.o(1).pp + r.e + \
    s4.e.o(1).pp + r.e + s4.e.o(1).pp + r
piano__7_119 = l.n + s6.e.o(1).p + s0.e.o(2).p + r.hd
piano__8_119 = l.sd + r.augment(frac(9, 8)) + \
    s1.e.o(2).p + h3.e.o(2).p + s2.e.o(2).p + r
piano__9_119 = r.augment(frac(27, 8)) + s4.t.o(2).p + s3.e.o(2).p
chord_119 = (I[7] % II.M)(piano__4=piano__4_119, piano__5=piano__5_119, piano__6=piano__6_119,
                          piano__7=piano__7_119, piano__8=piano__8_119, piano__9=piano__9_119)

piano__4_120 = l.n + s4.e.pp + r.qd + s4.pp + r
piano__5_120 = l.t + r.sd + s0.e.o(1).pp + r.e + s0.e.o(1).pp + s6.pp + r
piano__6_120 = r + s2.e.o(1).pp + r.augment(frac(5, 2))
piano__8_120 = l.n + s2.qd.o(2).p + r.s + s2.s.o(2).p + \
    s1.e.o(2).p + s2.s.o(2).p + r.s + s3.s.o(2).p + r.ed
piano__9_120 = r.qd + s3.s.o(2).p + r.augment(frac(7, 4)) + h6.s.o(2).p + r.s
chord_120 = (I[7] % II.M)(piano__4=piano__4_120, piano__5=piano__5_120,
                          piano__6=piano__6_120, piano__8=piano__8_120, piano__9=piano__9_120)

piano__9_121 = h6.e.o(2).p + s4.e.o(2).p + r.e + \
    s4.e.o(2).pp + r + s5.s.o(2).p + r.s + s4.s.o(2).p + r.s
piano__10_121 = l.augment(frac(5, 8)) + r.augment(frac(11, 8)) + \
    s0.s.o(3).p + r.s + h10.s.o(2).p + r.augment(frac(5, 4))
piano__5_121 = l.n + s0.e.o(1).pp + r.e + s1.e.o(1).pp + \
    r.e + s2.e.o(1).pp + r.e + s0.e.o(1).pp + r.e
piano__6_121 = r.e + s2.e.o(1).pp + r.e + s3.e.o(1).pp + \
    r.e + s4.s.o(1).pp + r.ed + s2.s.o(1).pp + r.s
chord_121 = (I % II.m)(piano__9=piano__9_121, piano__10=piano__10_121,
                       piano__5=piano__5_121, piano__6=piano__6_121)

piano__4_122 = l.t + r.augment(frac(23, 8)) + s0.e.pp + r.e
piano__5_122 = l.t + r.augment(frac(11, 8)) + \
    s4.e.pp + s2.e.pp + s4.s.pp + r.ed + s2.s.pp + r.s
piano__6_122 = s4.e.pp + r.e + s6.e.pp + r.augment(frac(5, 2))
piano__7_122 = l.sd + r.t + h1.e.o(1).pp + r.hd
piano__8_122 = l.n + s5.e.o(1).p + s6.e.o(1).p + r.augment(frac(5, 8)) + s6.t.o(1).pp + s5.t.o(
    1).pp + s6.t.o(1).pp + r.e + s6.s.o(1).p + r.s + h8.s.o(1).p + r.s + s4.s.o(1).p + r.s
piano__9_122 = r.qd + s0.t.o(2).pp + r.sd + s0.s.o(2).p + r.augment(frac(7, 4))
chord_122 = (V[7] % II.M)(piano__4=piano__4_122, piano__5=piano__5_122, piano__6=piano__6_122,
                          piano__7=piano__7_122, piano__8=piano__8_122, piano__9=piano__9_122)

piano__4_123 = l.t + r.augment(frac(7, 8)) + h10.e.pp + r.e + s5.e.pp + r.qd
piano__5_123 = l.n + s0.e.o(1).pp + \
    r.augment(frac(5, 2)) + s1.e.o(1).pp + s0.e.o(1).pp
piano__6_123 = r.e + s4.e.o(1).pp + r.e + s4.e.o(1).pp + r.e + s2.e.o(1).pp + r
piano__7_123 = l.sd + r.augment(frac(13, 8)) + s6.e.o(1).p + s0.e.o(2).p + r
piano__8_123 = l.n + s3.e.o(2).p + s2.e.o(2).p + r.e + s1.e.o(2).pp + r.h
piano__9_123 = r.augment(frac(7, 2)) + h6.e.o(2).p
chord_123 = (I % II.m)(piano__4=piano__4_123, piano__5=piano__5_123, piano__6=piano__6_123,
                       piano__7=piano__7_123, piano__8=piano__8_123, piano__9=piano__9_123)

piano__0_124 = r.hd + s5.s.o(-2).p + r.s + s4.s.o(-2).p + r.s
piano__1_124 = l.sd + r.augment(frac(17, 8)) + \
    h10.s.o(-2).p + r.augment(frac(5, 4))
piano__3_124 = l.sd + r.augment(frac(17, 8)) + h10.s.o(-1).p + \
    r.s + s5.s.o(-1).p + r.s + s4.s.o(-1).mf + r.s
piano__4_124 = l.n + s0.e.pp + r.qd + s0.e.pp + r.qd
piano__5_124 = l.t + r.sd + s3.e.pp + r.e + s3.e.pp + s2.e.pp + r.qd
piano__6_124 = r + h8.e.pp + r.augment(frac(5, 2))
piano__9_124 = s6.h.o(1).p + s0.e.o(2).p + r.qd
chord_124 = (I[7] % VI.M)(piano__0=piano__0_124, piano__1=piano__1_124, piano__3=piano__3_124,
                          piano__4=piano__4_124, piano__5=piano__5_124, piano__6=piano__6_124, piano__9=piano__9_124)

piano__0_125 = s0.o(-1).p + r.hd
piano__2_125 = l.n + s0.mf + r.hd
piano__6_125 = r.augment(frac(7, 2)) + s4.s.o(1).p + r.s
piano__7_125 = l.sd + r.augment(frac(9, 8)) + s0.s.o(2).p + \
    r.ed + s0.s.o(2).p + r.s + s6.s.o(1).p + r.ed
piano__8_125 = l.n + s2.s.o(2).p + r.augment(frac(7, 4)) + \
    s1.s.o(2).p + r.s + s3.s.o(2).p + r.augment(frac(5, 4))
piano__9_125 = r.s + s4.s.o(2).p + h6.s.o(2).p + s4.s.o(2).p + r.s + s4.s.o(2).p + h6.s.o(2).p + s4.s.o(
    2).p + s3.s.o(2).mf + s4.s.o(2).p + r.s + s4.s.o(2).p + s3.s.o(2).mf + s4.s.o(2).p + s3.s.o(2).p + s4.s.o(2).p
piano__10_125 = l.augment(frac(5, 8)) + r.sd + \
    s5.s.o(2).p + r.augment(frac(11, 4))
chord_125 = (I % II.M)(piano__0=piano__0_125, piano__2=piano__2_125, piano__6=piano__6_125,
                       piano__7=piano__7_125, piano__8=piano__8_125, piano__9=piano__9_125, piano__10=piano__10_125)

piano__4_126 = l.t + r.augment(frac(27, 8)) + s4.s.p + r.s
piano__5_126 = l.t + r.augment(frac(11, 8)) + s0.s.o(1).p + \
    r.s + s1.s.o(1).p + r.s + s0.s.o(1).p + r.s + s6.s.p + r.ed
piano__7_126 = l.n + s0.o(2).p + r.hd
piano__8_126 = l.n + s2.s.o(2).p + r.augment(frac(15, 4))
piano__9_126 = r.s + s4.s.o(2).p + h6.s.o(2).p + s4.s.o(2).p + r.s + s4.s.o(2).p + h6.s.o(2).p + s4.s.o(2).p + s3.s.o(
    2).p + s4.s.o(2).p + s3.s.o(2).p + s4.s.o(2).p + s3.s.o(2).mf + s4.s.o(2).p + s3.s.o(2).p + s4.s.o(2).p
piano__10_126 = l.augment(frac(5, 8)) + r.sd + \
    s5.s.o(2).p + r.augment(frac(11, 4))
chord_126 = (I % II.M)(piano__4=piano__4_126, piano__5=piano__5_126, piano__7=piano__7_126,
                       piano__8=piano__8_126, piano__9=piano__9_126, piano__10=piano__10_126)

piano__5_127 = l.n + s0.s.o(1).p + r.augment(frac(15, 4))
piano__6_127 = r.s + s4.s.o(1).pp + h6.s.o(1).p + s4.s.o(1).pp + r.s + s4.s.o(1).pp + h6.s.o(1).p + s4.s.o(1).pp + s3.s.o(
    1).p + s4.s.o(1).pp + s3.s.o(1).p + s4.s.o(1).pp + s3.s.o(1).p + s4.s.o(1).pp + s3.s.o(1).p + s4.s.o(1).pp
piano__7_127 = l.sd + r.augment(frac(5, 8)) + \
    s5.s.o(1).p + r.augment(frac(11, 4))
piano__8_127 = l.n + s2.o(2).p + r.hd
piano__9_127 = r.augment(frac(7, 2)) + s4.s.o(2).p + r.s
piano__10_127 = l.augment(frac(5, 8)) + r.augment(frac(7, 8)) + s0.s.o(
    3).p + r.s + s1.s.o(3).mf + r.s + s0.s.o(3).p + r.s + s6.s.o(2).mf + r.ed
chord_127 = (I % II.M)(piano__5=piano__5_127, piano__6=piano__6_127, piano__7=piano__7_127,
                       piano__8=piano__8_127, piano__9=piano__9_127, piano__10=piano__10_127)

piano__1_128 = l.sd + r.augment(frac(25, 8)) + s4.s.o(-1).p + r.s
piano__2_128 = l.t + r.augment(frac(11, 8)) + \
    s0.s.p + r.ed + s0.s.p + r.s + s6.s.o(-1).p + r.ed
piano__3_128 = l.sd + r.augment(frac(13, 8)) + s1.s.mf + r.augment(frac(7, 4))
piano__6_128 = s2.s.o(1).pp + s4.s.o(1).pp + h6.s.o(1).p + s4.s.o(1).pp + r.s + s4.s.o(1).pp + h6.s.o(1).p + s4.s.o(
    1).pp + s3.s.o(1).p + s4.s.o(1).p + s3.s.o(1).p + s4.s.o(1).pp + s3.s.o(1).p + s4.s.o(1).p + s3.s.o(1).p + s4.s.o(1).pp
piano__7_128 = l.sd + r.augment(frac(5, 8)) + \
    s5.s.o(1).pp + r.augment(frac(11, 4))
piano__10_128 = l.n + s0.o(3).p + r.hd
chord_128 = (I % II.M)(piano__1=piano__1_128, piano__2=piano__2_128, piano__3=piano__3_128,
                       piano__6=piano__6_128, piano__7=piano__7_128, piano__10=piano__10_128)

piano__2_129 = l.n + s0.p + r.hd
piano__5_129 = l.t + r.augment(frac(15, 8)) + s1.s.o(1).pp + r.s + \
    s1.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s
piano__6_129 = s2.o(1).p + s2.s.o(1).pp + r.s + \
    s2.s.o(1).pp + r.augment(frac(9, 4))
piano__7_129 = l.sd + r.augment(frac(7, 8)) + s0.s.o(2).pp + r.s + s0.s.o(
    2).pp + r.s + s0.s.o(2).pp + r.s + s0.s.o(2).pp + r.s + s0.s.o(2).pp + r.s + s0.s.o(2).pp
piano__8_129 = l.sd + r.augment(frac(13, 8)) + s3.o(2).p + s2.o(2).p
piano__9_129 = r + s4.o(2).p + r.h
chord_129 = (I % II.M)(piano__2=piano__2_129, piano__5=piano__5_129, piano__6=piano__6_129,
                       piano__7=piano__7_129, piano__8=piano__8_129, piano__9=piano__9_129)

piano__9_130 = s2.ed.o(2).p + s2.t.o(2).p + s1.t.o(2).p + \
    s2.t.o(2).p + r.augment(frac(19, 8)) + s2.s.o(2).p + r.s
piano__10_130 = l.augment(frac(5, 8)) + r.t + s3.n.o(2).p + r.ed + \
    s3.s.o(2).p + r.s + s5.e.o(2).p + s4.s.o(2).p + r.s + s3.e.o(2).p + r.e
piano__6_130 = s0.s.o(1).pp + r.ed + s0.t.o(1).pp + \
    r.augment(frac(7, 8)) + s0.s.o(1).pp + r.ed + s0.s.o(1).pp + r.ed
piano__7_130 = l.s + s4.s.o(1).pp + s3.s.o(1).pp + s4.s.o(1).pp + r.s + s4.s.o(1).pp + s3.s.o(1).pp + s4.s.o(
    1).pp + r.s + s4.s.o(1).pp + s3.s.o(1).pp + s4.s.o(1).pp + r.s + s4.s.o(1).pp + s3.s.o(1).pp + s4.s.o(1).pp
chord_130 = (IV % II.M)(piano__9=piano__9_130, piano__10=piano__10_130,
                        piano__6=piano__6_130, piano__7=piano__7_130)

piano__5_131 = l.t + r.augment(frac(15, 8)) + s1.s.o(1).p + r.s + \
    s1.s.o(1).pp + r.s + s0.s.o(1).p + r.s + s0.s.o(1).pp + r.s
piano__6_131 = s2.s.o(1).pp + r.ed + s2.s.o(1).p + r.s + \
    s2.s.o(1).pp + r.augment(frac(9, 4))
piano__7_131 = l.s + s0.s.o(2).pp + s6.s.o(1).pp + s0.s.o(2).pp + r.s + s0.s.o(2).pp + r.s + s0.s.o(
    2).pp + r.s + s0.s.o(2).pp + r.s + s0.s.o(2).pp + r.s + s0.s.o(2).pp + r.s + s0.s.o(2).pp
piano__8_131 = l.sd + r.augment(frac(13, 8)) + s3.o(2).p + s2.o(2).p
piano__9_131 = s4.e.o(2).p + r.e + s4.o(2).p + r.h
chord_131 = (I % II.M)(piano__5=piano__5_131, piano__6=piano__6_131,
                       piano__7=piano__7_131, piano__8=piano__8_131, piano__9=piano__9_131)

piano__3_132 = l.n + s2.s.p + r.ed + s2.s.p + r.augment(frac(11, 4))
piano__4_132 = l.t + r.sd + s4.s.pp + r.ed + s4.s.pp + \
    r.s + s3.t.pp + r.augment(frac(7, 8)) + s3.s.p + r.ed
piano__5_132 = l.t + r.t + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.e + s6.s.p + r.ed + s5.s.pp + r.s
piano__6_132 = r.augment(frac(9, 4)) + s1.s.o(1).p + r.s + \
    s1.s.o(1).p + r.s + s2.s.o(1).pp + r.s + s2.s.o(1).pp
piano__7_132 = l.n + s0.ed.o(2).mf + r + s0.s.o(2).p + s6.augment(frac(7, 8)).o(1).mf + \
    r.t + s0.t.o(2).p + r.t + s0.t.o(2).p + r.t + \
    s0.t.o(2).p + s6.t.o(1).p + s0.t.o(2).p + r.t
piano__8_132 = l.sd + r.augment(frac(7, 8)) + s2.s.o(2).p + s1.s.o(
    2).p + r.augment(frac(11, 8)) + s1.t.o(2).p + r.t + s1.t.o(2).p + r.e
piano__9_132 = r.ed + s4.s.o(2).p + s3.s.o(2).p + r.augment(frac(11, 4))
chord_132 = (II[7] % II.M)(piano__3=piano__3_132, piano__4=piano__4_132, piano__5=piano__5_132,
                           piano__6=piano__6_132, piano__7=piano__7_132, piano__8=piano__8_132, piano__9=piano__9_132)

piano__2_133 = l.t + r.augment(frac(19, 8)) + \
    s1.s.pp + r.s + s0.s.pp + r.s + s0.s.pp + r.s
piano__3_133 = l.sd + r.augment(frac(5, 8)) + s2.s.pp + \
    r.s + s2.s.pp + r.s + s1.s.pp + r.augment(frac(7, 4))
piano__5_133 = l.n + s0.s.o(1).p + r.s + s0.s.o(1).pp + r.e + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp
piano__6_133 = r.s + s2.s.o(1).p + r.s + s2.s.o(1).pp + \
    s4.o(1).p + s3.o(1).p + s2.o(1).p
piano__7_133 = l.n + s0.e.o(2).mf + r.augment(frac(7, 2))
chord_133 = (I % II.M)(piano__2=piano__2_133, piano__3=piano__3_133,
                       piano__5=piano__5_133, piano__6=piano__6_133, piano__7=piano__7_133)

piano__3_134 = l.n + s0.s.pp + r.ed + s0.t.pp + \
    r.augment(frac(7, 8)) + s0.s.pp + r.ed + s0.s.pp + r.ed
piano__5_134 = l.t + r.t + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + \
    s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp + r.s + s4.s.pp + s3.s.pp + s4.s.pp
piano__6_134 = s2.ed.o(1).p + s2.t.o(1).p + s1.t.o(1).p + \
    s2.t.o(1).p + r.augment(frac(23, 8))
piano__7_134 = l.sd + r.sd + s3.n.o(1).p + r.ed + s3.s.o(
    1).p + r.s + s5.e.o(1).p + s4.e.o(1).p + s3.e.o(1).p + s2.e.o(1).p
chord_134 = (IV % II.M)(piano__3=piano__3_134, piano__5=piano__5_134,
                        piano__6=piano__6_134, piano__7=piano__7_134)

piano__0_135 = r + s2.s.o(-1).p + r.ed + s1.s.o(-1).p + r.s + \
    s1.s.o(-1).p + r.s + s0.s.o(-1).p + r.s + s0.s.o(-1).p + r.s
piano__1_135 = l.sd + r.augment(frac(9, 8)) + \
    s2.s.o(-1).pp + r.augment(frac(9, 4))
piano__2_135 = l.t + r.augment(frac(9, 8)) + s0.s.pp + r.s + \
    s0.s.pp + r.s + s0.s.p + r.s + s0.s.p + r.s + s0.s.p + r.s + s0.s.p
piano__3_135 = l.n + s2.s.pp + r.augment(frac(15, 4))
piano__5_135 = l.t + r.t + s0.s.o(1).pp + s6.s.pp + s0.s.o(1).pp + r.hd
piano__6_135 = s4.e.o(1).p + r.e + s4.o(1).p + s3.o(1).p + s2.o(1).p
piano__8_135 = l.sd + r.augment(frac(13, 8)) + s3.o(2).mf + s2.o(2).mf
piano__9_135 = r + s4.o(2).mf + r.h
chord_135 = (I % II.M)(piano__0=piano__0_135, piano__1=piano__1_135, piano__2=piano__2_135, piano__3=piano__3_135,
                       piano__5=piano__5_135, piano__6=piano__6_135, piano__8=piano__8_135, piano__9=piano__9_135)

piano__1_136 = l.n + s2.s.o(-1).p + r.s + s4.s.o(-1).p + r.s + s2.s.o(-1).p + r.s + \
    s4.s.o(-1).p + r.s + s3.t.o(-1).p + \
    r.augment(frac(7, 8)) + s3.s.o(-1).p + r.ed
piano__2_136 = l.t + r.t + s0.s.p + r.s + s0.s.p + r.s + s0.s.p + \
    r.s + s0.s.p + r.e + s6.s.o(-1).p + r.ed + s5.s.o(-1).p + r.s
piano__3_136 = l.sd + r.augment(frac(15, 8)) + \
    s1.s.p + r.s + s1.s.p + r.s + s2.s.p + r.s + s2.s.p
piano__5_136 = l.n + s0.ed.o(1).p + r.augment(frac(13, 4))
piano__7_136 = l.sd + r.augment(frac(11, 8)) + s0.s.o(2).mf + \
    s6.augment(frac(7, 8)).o(1).mf + r.ed + s6.t.o(1).p + r.s
piano__8_136 = l.n + s0.ed.o(2).mf + r.e + s2.s.o(2).mf + s1.s.o(2).mf + r.augment(frac(5, 4)) + s0.t.o(
    2).p + s1.t.o(2).p + s0.t.o(2).mf + s1.t.o(2).p + s0.t.o(2).mf + r.t + s0.t.o(2).p + r.t
piano__9_136 = r.ed + s4.s.o(2).p + s3.s.o(2).mf + r.augment(frac(11, 4))
chord_136 = (II[7] % II.M)(piano__1=piano__1_136, piano__2=piano__2_136, piano__3=piano__3_136,
                           piano__5=piano__5_136, piano__7=piano__7_136, piano__8=piano__8_136, piano__9=piano__9_136)

piano__0_137 = s0.o(-1).p + r.hd
piano__1_137 = l.n + s4.o(-1).p + r.hd
piano__2_137 = l.n + s0.mf + r.hd
piano__5_137 = l.t + r.augment(frac(15, 8)) + s0.o(1).pp + s1.o(1).pp
piano__6_137 = s2.o(1).mf + r + s2.o(1).p + s3.o(1).p
piano__7_137 = l.n + s4.o(1).mf + r.hd
piano__8_137 = l.n + s0.o(2).mf + r + s3.s.o(2).mf + s2.s.o(2).p + \
    s1.s.o(2).p + s2.s.o(2).p + r.e + s2.s.o(2).p + s3.s.o(2).p
piano__9_137 = r.hd + s4.s.o(2).mf + s3.s.o(2).p + r.e
chord_137 = (I % II.M)(piano__0=piano__0_137, piano__1=piano__1_137, piano__2=piano__2_137, piano__5=piano__5_137,
                       piano__6=piano__6_137, piano__7=piano__7_137, piano__8=piano__8_137, piano__9=piano__9_137)

piano__9_138 = s4.o(2).mf + r + s4.t.o(2).p + r.sd + \
    s5.t.o(2).p + r.augment(frac(11, 8))
piano__10_138 = l.augment(frac(5, 8)) + r.augment(frac(19, 8)) + \
    s6.t.o(2).p + r.sd + s0.t.o(3).p + r.sd
piano__6_138 = s2.o(1).pp + r.hd
piano__7_138 = l.n + s4.o(1).p + r.hd
chord_138 = (I % II.M)(piano__9=piano__9_138, piano__10=piano__10_138,
                       piano__6=piano__6_138, piano__7=piano__7_138)

piano__2_139 = l.t + r.augment(frac(7, 8)) + s0.e.pp + r.e + s1.e.pp + r.qd
piano__3_139 = l.n + s2.e.pp + r.augment(frac(7, 2))
piano__4_139 = l.t + r.augment(frac(23, 8)) + s4.t.pp + r.augment(frac(7, 8))
piano__5_139 = l.t + r.sd + \
    s0.e.o(1).pp + r.e + s0.e.o(1).pp + r.e + \
    s0.e.o(1).pp + r.e + s6.t.pp + r.sd
piano__8_139 = l.sd + r.augment(frac(5, 8)) + s2.o(2).p + r.s + s3.s.o(
    2).p + s2.s.o(2).p + s3.s.o(2).p + r.e + s3.t.o(2).p + r.sd
piano__9_139 = s4.o(2).p + r + s4.s.o(2).p + r.ed + \
    s4.t.o(2).p + r.augment(frac(7, 8))
chord_139 = (I % II.M)(piano__2=piano__2_139, piano__3=piano__3_139, piano__4=piano__4_139,
                       piano__5=piano__5_139, piano__8=piano__8_139, piano__9=piano__9_139)

piano__2_140 = l.n + s0.p + r.hd
piano__5_140 = l.n + s0.o(1).p + r + s0.s.o(1).pp + r.s + \
    s0.s.o(1).pp + r.s + s1.s.o(1).pp + r.s + s1.s.o(1).pp + r.s
piano__6_140 = r.h + s2.s.o(1).p + r.s + s2.s.o(1).pp + \
    r.s + s3.s.o(1).p + r.s + s3.s.o(1).pp + r.s
piano__7_140 = l.sd + r.augment(frac(17, 8)) + \
    s1.s.o(2).p + r.augment(frac(5, 4))
piano__8_140 = l.n + h3.e.o(2).p + s2.e.o(2).p + r + s3.s.o(2).mf + s2.s.o(
    2).p + r.s + s2.s.o(2).p + r.s + s3.s.o(2).p + s2.s.o(2).p + s3.s.o(2).p
piano__9_140 = r.hd + s4.s.o(2).mf + r.ed
chord_140 = (I % II.M)(piano__2=piano__2_140, piano__5=piano__5_140, piano__6=piano__6_140,
                       piano__7=piano__7_140, piano__8=piano__8_140, piano__9=piano__9_140)

piano__9_141 = s4.o(2).mf + r + s4.t.o(2).p + r.sd + \
    s5.t.o(2).p + r.augment(frac(11, 8))
piano__10_141 = l.augment(frac(5, 8)) + r.augment(frac(19, 8)) + \
    s6.t.o(2).p + r.sd + s0.t.o(3).p + r.sd
piano__6_141 = s2.o(1).pp + r.hd
piano__7_141 = l.n + s4.o(1).p + r.hd
chord_141 = (I % II.M)(piano__9=piano__9_141, piano__10=piano__10_141,
                       piano__6=piano__6_141, piano__7=piano__7_141)

piano__2_142 = l.t + r.augment(frac(7, 8)) + s0.e.pp + r.e + s1.e.pp + r.qd
piano__3_142 = l.n + s2.e.pp + r.augment(frac(7, 2))
piano__4_142 = l.t + r.augment(frac(23, 8)) + s4.e.pp + r.e
piano__5_142 = l.t + r.sd + \
    s0.e.o(1).pp + r.e + s0.e.o(1).pp + r.e + s0.e.o(1).pp + r.e + s6.e.pp
piano__8_142 = l.sd + r.augment(frac(5, 8)) + s2.o(2).p + r.s + s3.s.o(
    2).p + s2.s.o(2).p + s3.s.o(2).p + r.s + s3.s.o(2).p + s2.s.o(2).p + s1.s.o(2).p
piano__9_142 = s4.o(2).p + r + s4.s.o(2).p + r.ed + s4.s.o(2).p + r.ed
chord_142 = (I % II.M)(piano__2=piano__2_142, piano__3=piano__3_142, piano__4=piano__4_142,
                       piano__5=piano__5_142, piano__8=piano__8_142, piano__9=piano__9_142)

piano__3_143 = l.n + s6.s.o(-1).p + r.ed + \
    s6.s.o(-1).p + r.ed + s0.s.p + r.ed + s0.s.p + r.ed
piano__4_143 = l.t + r.sd + s1.s.pp + r.ed + \
    s1.s.pp + r.ed + s2.s.pp + r.ed + s2.s.pp + r.s
piano__5_143 = l.t + r.t + s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp + r.s + \
    s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp + r.s + s4.s.pp
piano__7_143 = l.n + s4.s.o(1).p + r.augment(frac(15, 4))
piano__8_143 = l.s + s5.s.o(1).p + s6.s.o(1).p + \
    s0.s.o(2).p + r.augment(frac(11, 4)) + s0.s.o(2).p
piano__9_143 = r + s1.s.o(2).p + s2.s.o(2).p + r.qd + s2.s.o(2).p + r.ed
piano__10_143 = l.augment(frac(5, 8)) + r.augment(frac(7, 8)) + \
    s3.s.o(2).p + s4.t.o(2).p + r.t + s4.o(2).p + r
chord_143 = (IV % II.M)(piano__3=piano__3_143, piano__4=piano__4_143, piano__5=piano__5_143,
                        piano__7=piano__7_143, piano__8=piano__8_143, piano__9=piano__9_143, piano__10=piano__10_143)

piano__4_144 = l.n + s2.s.p + r.ed + s2.s.p + \
    r.ed + s2.s.p + r.ed + s2.s.p + r.ed
piano__5_144 = l.t + r.sd + s5.s.pp + r.ed + \
    s5.s.pp + r.ed + s6.s.pp + r.ed + s6.s.pp + r.s
piano__6_144 = r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(1).pp + r.s + s0.s.o(
    1).pp + r.s + s1.s.o(1).pp + r.s + s1.s.o(1).pp + r.s + s1.s.o(1).pp + r.s + s1.s.o(1).pp
piano__7_144 = l.sd + r.augment(frac(27, 8)) + s4.s.o(1).p
piano__8_144 = l.n + s0.o(2).p + r.ed + s5.s.o(1).p + \
    s6.o(1).p + s1.e.o(2).p + r.e
piano__9_144 = r + s2.e.o(2).p + r.augment(frac(5, 2))
chord_144 = (III[7] % II.M)(piano__4=piano__4_144, piano__5=piano__5_144,
                            piano__6=piano__6_144, piano__7=piano__7_144, piano__8=piano__8_144, piano__9=piano__9_144)

piano__3_145 = l.n + s6.s.o(-1).p + r.ed + \
    s6.s.o(-1).p + r.ed + s0.s.p + r.ed + s0.s.p + r.ed
piano__4_145 = l.t + r.sd + s1.s.p + r.ed + \
    s1.s.p + r.ed + s2.s.p + r.ed + s2.s.pp + r.s
piano__5_145 = l.t + r.t + s4.s.pp + r.s + s4.s.p + r.s + s4.s.p + r.s + \
    s4.s.p + r.s + s4.s.p + r.s + s4.s.p + r.s + s4.s.pp + r.s + s4.s.pp
piano__7_145 = l.n + s4.s.o(1).p + r.augment(frac(15, 4))
piano__8_145 = l.s + s5.s.o(1).p + s6.s.o(1).p + r.augment(frac(13, 4))
piano__9_145 = r.ed + s0.s.o(2).p + s1.s.o(2).p + s2.s.o(2).p + \
    r.augment(frac(7, 4)) + s2.s.o(2).p + s1.s.o(2).p + s0.s.o(2).p
piano__10_145 = l.augment(frac(5, 8)) + r.augment(frac(7, 8)) + s3.s.o(2).p + s4.s.o(
    2).p + s5.s.o(2).mf + s4.s.o(2).p + s3.s.o(2).p + s4.s.o(2).p + s3.s.o(2).mf + r.ed
chord_145 = (IV % II.M)(piano__3=piano__3_145, piano__4=piano__4_145, piano__5=piano__5_145,
                        piano__7=piano__7_145, piano__8=piano__8_145, piano__9=piano__9_145, piano__10=piano__10_145)

piano__4_146 = l.n + s4.s.p + r.ed + s4.s.p + \
    r.ed + s4.s.p + r.ed + s4.s.p + r.ed
piano__5_146 = l.t + r.sd + \
    s0.s.o(1).pp + r.ed + s0.s.o(1).pp + r.ed + \
    s1.s.o(1).pp + r.ed + s1.s.o(1).pp + r.s
piano__6_146 = r.s + s2.s.o(1).pp + r.s + s2.s.o(1).pp + r.s + s2.s.o(1).pp + r.s + s2.s.o(
    1).pp + r.s + s3.s.o(1).pp + r.s + s3.s.o(1).pp + r.s + s3.s.o(1).pp + r.s + s3.s.o(1).pp
piano__7_146 = l.sd + r.augment(frac(11, 8)) + \
    s0.s.o(2).p + r.qd + s0.s.o(2).p + s6.s.o(1).p
piano__8_146 = l.n + s2.s.o(2).mf + s3.s.o(2).p + r.e + s3.s.o(2).p + s2.s.o(2).p + s1.s.o(
    2).p + r.s + h1.s.o(2).p + s1.s.o(2).p + s2.s.o(2).p + s3.s.o(2).p + s2.s.o(2).p + s1.s.o(2).p + r.e
piano__9_146 = r.e + h6.s.o(2).p + s4.s.o(2).p + r.hd
chord_146 = (I % II.M)(piano__4=piano__4_146, piano__5=piano__5_146, piano__6=piano__6_146,
                       piano__7=piano__7_146, piano__8=piano__8_146, piano__9=piano__9_146)

piano__4_147 = l.t + r.augment(frac(11, 8)) + \
    s4.s.p + r.augment(frac(7, 4)) + s4.s.p + r.s
piano__5_147 = l.n + s0.o(1).p + r.e + s1.s.o(1).p + \
    r.s + s0.o(1).p + r.e + s1.s.o(1).p + r.s
piano__6_147 = s2.o(1).p + r + s2.o(1).p + r
piano__7_147 = l.n + s0.s.o(2).mf + s4.s.o(1).p + s0.s.o(2).mf + r.augment(
    frac(5, 4)) + s0.s.o(2).mf + s4.s.o(1).p + s0.s.o(2).mf + r.augment(frac(5, 4))
piano__8_147 = l.sd + r.sd + s2.s.o(2).p + r.s + s2.s.o(2).p + s3.s.o(
    2).mf + s1.s.o(2).p + r.ed + s2.s.o(2).p + r.s + s2.s.o(2).p + r.s + s1.s.o(2).p
piano__9_147 = r + s4.s.o(2).mf + r.augment(frac(7, 4)) + \
    s4.s.o(2).mf + r.s + s3.s.o(2).mf + r.s
chord_147 = (I % II.M)(piano__4=piano__4_147, piano__5=piano__5_147, piano__6=piano__6_147,
                       piano__7=piano__7_147, piano__8=piano__8_147, piano__9=piano__9_147)

piano__1_148 = l.sd + r.augment(frac(5, 8)) + \
    h11.e.o(-2).p + r.e + s0.e.o(-1).p + r.qd
piano__4_148 = l.t + r.augment(frac(7, 8)) + \
    h11.e.o(-1).mf + r.e + s0.e.mf + r.qd
piano__5_148 = l.n + s2.e.p + r.augment(frac(7, 2))
piano__6_148 = s4.e.mf + r.augment(frac(7, 2))
piano__7_148 = l.n + s2.e.o(1).mf + r.qd + s2.e.o(1).mf + r.qd
piano__8_148 = l.sd + r.augment(frac(5, 8)) + \
    s3.e.o(1).mf + r.e + s4.e.o(1).mf + r.qd
piano__9_148 = r + s5.e.o(1).mf + r.augment(frac(5, 2))
piano__10_148 = l.augment(frac(5, 8)) + r.sd + \
    s1.e.o(2).mf + r.e + s2.e.o(2).mf + r.qd
chord_148 = (VI % II.M)(piano__1=piano__1_148, piano__4=piano__4_148, piano__5=piano__5_148, piano__6=piano__6_148,
                        piano__7=piano__7_148, piano__8=piano__8_148, piano__9=piano__9_148, piano__10=piano__10_148)

piano__1_149 = l.n + s6.h.o(-2).pp + s0.h.o(-1).pp
piano__3_149 = l.n + s6.h.o(-1).pp + r.h
piano__4_149 = l.t + r.augment(frac(15, 8)) + s0.h.pp
piano__5_149 = l.t + r.augment(frac(27, 8)) + s4.s.pp + r.s
piano__6_149 = r.e + s0.s.o(1).pp + r.ed + s6.s.pp + \
    r.s + s6.e.pp + s5.s.pp + r.s + s5.e.pp + r.e
piano__7_149 = l.n + s1.e.o(1).pp + r.e + s0.e.o(1).pp + \
    r + s3.s.o(1).p + r.s + s3.e.o(1).p + s2.s.o(1).p + r.s
piano__8_149 = l.n + s6.e.o(1).p + s5.s.o(1).p + r.s + \
    s5.e.o(1).p + s4.s.o(1).p + r.s + s4.e.o(1).p + r.qd
chord_149 = (V[7] % II.M)(piano__1=piano__1_149, piano__3=piano__3_149, piano__4=piano__4_149,
                          piano__5=piano__5_149, piano__6=piano__6_149, piano__7=piano__7_149, piano__8=piano__8_149)

piano__0_150 = r.h + s3.o(-2).pp + r
piano__1_150 = l.sd + r.augment(frac(5, 8)) + s0.o(-1).pp + r.h
piano__2_150 = l.n + s3.o(-1).pp + r.hd
piano__5_150 = l.n + s4.h.pp + r.h
piano__6_150 = s6.h.p + s5.pp + r
piano__7_150 = l.n + s2.h.o(1).p + s3.o(1).p + r
chord_150 = (V[7] % II.M)(piano__0=piano__0_150, piano__1=piano__1_150, piano__2=piano__2_150,
                          piano__5=piano__5_150, piano__6=piano__6_150, piano__7=piano__7_150)


score = chord_0 + chord_1 + chord_2 + chord_3 + chord_4 + chord_5 + chord_6 + chord_7 + chord_8 + chord_9 + chord_10 + chord_11 + chord_12 + chord_13 + chord_14 + chord_15 + chord_16 + chord_17 + chord_18 + chord_19 + chord_20 + chord_21 + chord_22 + chord_23 + chord_24 + chord_25 + chord_26 + chord_27 + chord_28 + chord_29 + chord_30 + chord_31 + chord_32 + chord_33 + chord_34 + chord_35 + chord_36 + chord_37 + chord_38 + chord_39 + chord_40 + chord_41 + chord_42 + chord_43 + chord_44 + chord_45 + chord_46 + chord_47 + chord_48 + chord_49 + chord_50 + chord_51 + chord_52 + chord_53 + chord_54 + chord_55 + chord_56 + chord_57 + chord_58 + chord_59 + chord_60 + chord_61 + chord_62 + chord_63 + chord_64 + chord_65 + chord_66 + chord_67 + chord_68 + chord_69 + chord_70 + chord_71 + chord_72 + chord_73 + chord_74 + chord_75 + chord_76 + chord_77 + \
    chord_78 + chord_79 + chord_80 + chord_81 + chord_82 + chord_83 + chord_84 + chord_85 + chord_86 + chord_87 + chord_88 + chord_89 + chord_90 + chord_91 + chord_92 + chord_93 + chord_94 + chord_95 + chord_96 + chord_97 + chord_98 + chord_99 + chord_100 + chord_101 + chord_102 + chord_103 + chord_104 + chord_105 + chord_106 + chord_107 + chord_108 + chord_109 + chord_110 + chord_111 + chord_112 + chord_113 + chord_114 + \
    chord_115 + chord_116 + chord_117 + chord_118 + chord_119 + chord_120 + chord_121 + chord_122 + chord_123 + chord_124 + chord_125 + chord_126 + chord_127 + chord_128 + chord_129 + chord_130 + chord_131 + chord_132 + \
    chord_133 + chord_134 + chord_135 + chord_136 + chord_137 + chord_138 + chord_139 + chord_140 + chord_141 + \
    chord_142 + chord_143 + chord_144 + chord_145 + \
    chord_146 + chord_147 + chord_148 + chord_149 + chord_150

score.to_midi(FILENAME, tempo=TEMPO)
