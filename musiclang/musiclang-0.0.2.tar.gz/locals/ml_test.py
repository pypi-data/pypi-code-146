from musiclang.predict.chord_predictor.chord_predictor import ChordTransformerPredictor
from musiclang import Score
from musiclang.core.library import *

"""
In this example we will train a simple language model to extends the chord progression of our choice
"""

def get_score_in_every_tonality(score):
    df_score = score.to_sequence()
    result = []
    for i in range(12):
        df = df_score.copy()
        df['tonality_degree'] = (df['tonality_degree'] + i) % 12
        new_score = Score.from_sequence(df)
        result.append(new_score)
    return result

score = Score.from_pickle('locals/beethoven.pickle')
# Transpose to every tonality


PREPARE_DATASET = False
IMPROVE_DATASET = False
TRAIN = True
RESTART_TRAIN = False

if PREPARE_DATASET:
    # Create score dataset of all composers as str
    import os
    import shutil
    os.makedirs('locals/dataset', exist_ok=True)
    os.makedirs('locals/dataset_pickle', exist_ok=True)
    import os

    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk('locals/data_composers') for f in filenames if
              os.path.splitext(f)[-1] == '.mid']
    transformer = ChordTransformerPredictor()
    for f in files:
        print(f)
        try:
            score = Score.from_midi(f)
            scores = get_score_in_every_tonality(score)
            for idx, s in enumerate(scores):
                text = transformer.score_to_text(s)
                filename = f.split('/')[-2] + '_' + f.split('/')[-1].replace('.mid', '') + '_{}.txt'.format(idx)
                with open(os.path.join('locals/dataset', filename), 'w') as fd:
                    fd.write(text.replace('+', '+\n'))  # For readability
                s.to_pickle(os.path.join('locals/dataset_pickle', filename.replace('.txt', '.pickle')))
        except Exception as e:
            print(e)
            print('Error with', f)

if IMPROVE_DATASET:
    import os
    dest = 'locals/dataset_clean'
    os.makedirs('locals/dataset_clean', exist_ok=True)
    files = os.listdir('locals/dataset')
    for f in files:
        new_score = []
        with open(os.path.join('locals/dataset', f), 'r') as fd:
            temp_score = fd.read().split('\n')

        previous_chord = None
        for chord in temp_score:
            if chord == previous_chord:
                continue
            else:
                previous_chord = chord
                new_score.append(chord)


        with open(os.path.join('locals/dataset_clean', f), 'w') as fd:
            fd.write('\n'.join(new_score))

if TRAIN:
    # Open all sheets
    import os
    import random
    scores = []
    files = os.listdir('locals/dataset_clean')
    for f in files:
        with open(os.path.join('locals/dataset_clean', f), 'r') as fd:
            scores.append(fd.read().replace('\n', ''))

    # Shuffle scores
    random.shuffle(scores)

    train_scores = scores
    eval_scores = scores
    if RESTART_TRAIN:
        model = ChordTransformerPredictor.load_model('locals/model.ml')
    else:
        model = ChordTransformerPredictor()
    model.train(train_scores, eval_scores, epochs=3)
    model.save_model('locals/model.ml')
else:
    model = ChordTransformerPredictor.load_model('locals/model.ml')

predicted_score = model.predict('(VI % I.M) + (II % ', output='score', include_start=True, n_tokens=50)

print(predicted_score)
#predicted_score.to_voicings().p.to_midi('locals/test.mid', tempo=240)
predicted_score.to_voicings().to_midi('locals/test.mid', tempo=120)
