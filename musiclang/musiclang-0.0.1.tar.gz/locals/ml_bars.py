from musiclang.core.library import *
from musiclang import *
import pickle
import partitura as pt
from partitura.io.importmidi import load_score_midi
from musiclang.parser import MidiToMusicLang


#

# Write a small partition
from musiclang.core.library import *


filename_beeth = 'locals/data_composers/beeth/elise.mid'
filename_mozart = 'locals/mozart.mid'
filename_haydn = 'locals/data_composers/haydn/hay_40_1.mid'
filename_chopin = 'locals/data_composers/chopin/chpn_op35_1.mid'
print('mozart')
score1, tempo = MidiToMusicLang(filename_mozart).get_score()

print('beeth')
score1, tempo = MidiToMusicLang(filename_beeth).get_score()
print('haydn')
score1, tempo = MidiToMusicLang(filename_haydn).get_score()
print('chopin')
score1, tempo = MidiToMusicLang(filename_chopin).get_score()

