from musiclang.core.library import *
from musiclang import *
import pickle
import partitura as pt
from partitura.io.importmidi import load_score_midi
from musiclang.parser.analytical import parse_to_musiclang, analysis_to_musiclang_score
import os
#

# Write a small partition
from musiclang.core.library import *


filename_beeth = 'locals/data_composers/beeth/elise.mid'
filename_mozart = 'locals/mozart.mid'
filename_haydn = 'locals/data_composers/haydn/hay_40_1.mid'
filename_chopin = 'locals/data_composers/chopin/chpn_op35_1.mid'
filename_bach = 'locals/data_composers/bach/bach_846.mid'

dir_beeth = 'locals/When-in-Rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op027_No2(Moonlight)/1'
filename_moonlight = 'locals/data_composers/beeth/mond_1.mid'
dir_mozart = 'locals/When-in-Rome/Corpus/Piano_Sonatas/Mozart,_Wolfgang_Amadeus/K311/1/'
filename_mozart = os.path.join(dir_mozart, 'score.mid')


if True:
    score1, config1 = parse_to_musiclang(filename_moonlight)
    score2, config2 = parse_to_musiclang(filename_bach)

    score1.to_pickle('locals/score1.pickle')
    score2.to_pickle('locals/score2.pickle')


    import pickle
    with open('locals/score1_config.pickle', 'wb') as f:
        pickle.dump(config1, f)
    with open('locals/score2_config.pickle', 'wb') as f:
        pickle.dump(config2, f)

    score3, config3 = parse_to_musiclang(filename_chopin)
    score3.to_pickle('locals/score3.pickle')
    with open('locals/score3_config.pickle', 'wb') as f:
        pickle.dump(config3, f)


score1 = Score.from_pickle('locals/score1.pickle')
score2 = Score.from_pickle('locals/score2.pickle')
score3 = Score.read_pickle('locals/score3.pickle')
config1 = pickle.load(open('locals/score1_config.pickle', 'rb'))
config2 = pickle.load(open('locals/score2_config.pickle', 'rb'))
config3 = pickle.load(open('locals/score3_config.pickle', 'rb'))
# Keep only piano__3 for score 1 and piano__4 for score2
chords1 = config1['annotation']
chords2 = config2['annotation']
chords3 = config2['annotation']


analysis = "m1 c: i \n m2 V64 \n m3 i \n "
#score3 = analysis_to_musiclang_score(analysis)
#score1 = score1[['piano__3']]
#score2 = score2[['piano__4']]

def merge_moonlight_bach(moonlight, bach, chopin):
    from fractions import Fraction as frac
    df_moon = moonlight.to_sequence()
    # Keep only 3-notes
    # Keep only bass and soprano
    df_moon = df_moon[(df_moon['end'] - df_moon['start']) != frac(1, 3)]
    #df_moon.loc[df_moon['pitch'] > 0, 'instrument'] = df_moon.loc[df_moon['pitch'] > 0, 'instrument'].str.replace('piano', 'oboe')
    df_moon.loc[df_moon['pitch'] <= 0, 'instrument'] = df_moon.loc[df_moon['pitch'] <= 0, 'instrument'].str.replace('piano', 'cello')
    df_moon = df_moon[~df_moon['instrument'].str.contains('piano')]
    df_moon['instrument'] = df_moon['instrument'].str.replace('cello__0', 'cello__12')
    df_moon['instrument'] = df_moon['instrument'].str.replace('cello__1', 'cello__13')
    moonlight = Score.from_sequence(df_moon).pp
    #bach = bach.reduce(n_voices=1, start_low=False, instruments=['piano__0'])
    score = bach.pp.project_on_score(moonlight.copy(), keep_score=True)

    # Find melody of chopin
    chopin_melody = chopin.get_score_between(24, 40)
    df_chopin = chopin_melody.to_sequence()
    df_chopin['is_silence'] = df_chopin['note'].apply(lambda x: not x.is_note)
    df_chopin.loc[(df_chopin['pitch']) < 10, 'is_silence'] = True
    chopin = Score.from_sequence(df_chopin)
    C = chopin.get_score_between(4, 8).mf
    chopin = sum([chopin.mf] * 16, None)
    chopin = chopin.reduce(n_voices=1, start_low=False, instruments=['oboe__24']).o(0)
    score = chopin.project_on_score(score, keep_score=True)
    return score

#reduced_score = score1.optimize_voices()
reduced_score1 = score1.reduce(n_voices=1, start_low=False, instruments=['harp__0']).pp
reduced_score1_bass = score1.reduce(n_voices=1, start_low=True, instruments=['cello__0']).o(-1).pp
reduced_score2 = score2.reduce(n_voices=1, start_low=False, instruments=['oboe__0']).mf

score = merge_moonlight_bach(score1, score2, score3)
#score = score1.project_on_score(score3, keep_score=False)
score[0:16].to_midi('locals/test.mid', tempo=70)

from pdb import set_trace; set_trace()