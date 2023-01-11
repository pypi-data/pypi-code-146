from multiprocessing.spawn import freeze_support

from musiclang.predict.score_predictor.score_predictor import ScoreTransformerPredictor
from musiclang.predict.score_predictor.score_tokenizer import PARSER
from musiclang import Score
from musiclang.core.library import *

"""
In this example we will train a simple language model to extends the chord progression of our choice
"""
# Test

TRAIN = True
RESTART_TRAIN = True


if TRAIN:
    # Open all sheets
    import os
    import random
    scores = []
    files = os.listdir('locals/dataset_score')
    print('PROCESSING FILES')
    for f in files:
        with open(os.path.join('locals/dataset_score', f), 'r') as fd:
            scores.append(fd.read())
    print('FINISHED PROCESSING FILE')
    # Shuffle scores
    random.shuffle(scores)

    train_scores = scores
    eval_scores = scores
    if RESTART_TRAIN:
        model = ScoreTransformerPredictor.load_model('locals/score_model.ml')
    else:
        model = ScoreTransformerPredictor()
    print('START TRAINING')
    model.train(train_scores, eval_scores, epochs=5)
    model.save_model('locals/score_model.ml')
else:
    model = ScoreTransformerPredictor.load_model('locals/score_model.ml')

predicted_score = model.predict('(VI % I.M)(piano__0=s0.e + s2.e + s4.e)+', temperature=0.1, output='score', include_start=True, n_tokens=200)

print(predicted_score)
#predicted_score.to_voicings().p.to_midi('locals/test.mid', tempo=240)
predicted_score.to_midi('locals/test.mid', tempo=120)
