from multiprocessing.spawn import freeze_support
from musiclang.predict.score_predictor.score_predictor import ScoreTransformerPredictor
from musiclang import Score


def get_score_in_every_tonality(score):
    df_score = score.to_sequence()
    result = []
    for i in range(12):
        df = df_score.copy()
        df['tonality_degree'] = (df['tonality_degree'] + i) % 12
        new_score = Score.from_sequence(df)
        result.append(new_score)
    return result

def get_score_in_every_tonality_quick(score):
    scores = []
    for i in range(12):
        new_score = None
        for chord in score:
            new_chord = chord.copy()
            new_chord.tonality.degree = (new_chord.tonality.degree + i) % 12
            new_score += new_chord
        scores.append(new_score)

    return scores


def loop_function(f):
    from musiclang.predict.score_predictor.score_predictor import ScoreTransformerPredictor
    from musiclang.predict.score_predictor.score_tokenizer import PARSER
    import os
    transformer = ScoreTransformerPredictor()
    text = ''
    try:
        print(f)
        score = Score.from_midi(f)
        text = transformer.score_to_text(score)
        assert PARSER.parse(text)
        scores = get_score_in_every_tonality(score)
        for idx, s in enumerate(scores):
            text = transformer.score_to_text(s)
            assert PARSER.parse(text)
            filename = f.split('/')[-2] + '_' + f.split('/')[-1].replace('.mid', '') + '_{}.txt'.format(idx)
            with open(os.path.join('locals/dataset_score', filename), 'w') as fd:
                fd.write(text.replace('+', '+\n'))  # For readability
            s.to_pickle(os.path.join('locals/dataset_pickle', filename.replace('.txt', '.pickle')))
    except Exception as e:
        print(text)
        print(e)
        print('Error with', f)




def main():
    # Create score dataset of all composers as str
    import os
    import multiprocessing as mlp

    import shutil
    os.makedirs('locals/dataset_score', exist_ok=True)
    os.makedirs('locals/dataset_pickle', exist_ok=True)
    with mlp.Pool(10, maxtasksperchild=1) as pool:
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk('locals/data_composers') for f in filenames if
                  os.path.splitext(f)[-1] == '.mid']
        transformer = ScoreTransformerPredictor()
        already_done = ['_'.join(s.split('_')[1:-1]) + '.mid' for s in os.listdir('locals/dataset_score')]
        print(already_done)
        files_to_do = []
        for f in files:
            if f.split('/')[-1] in already_done:
                print(f, " already done")
                continue
            else:
                files_to_do.append(f)

        pool.map(loop_function, files)


if __name__ == '__main__':
    freeze_support()
    main()