from music21 import corpus


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

import os

output_dir = 'locals/chords_data'
to_replace = '/Users/floriangardin/code/music/musiclang2/venv/lib/python3.10/site-packages/music21/corpus/'
os.makedirs(output_dir, exist_ok=True)


CREATE_ANNOTATED = False
CREATE_CHORDS = True
CREATE_FULL_MUSIC = False

if CREATE_ANNOTATED:
    from musiclang.analyze import get_chords_from_analysis
    paths = [str(path) for path in corpus.getPaths('rntxt')]
    for path in paths:

        raw_file = '_'.join(path.replace(to_replace, '').replace('.musicxml', '').replace('.rntxt', '').split('/'))
        if os.path.exists(os.path.join(output_dir, f"{raw_file}_0.txt")):
            print('Already done : ', raw_file)
            continue

        score = get_chords_from_analysis(path)
        scores = get_score_in_every_tonality_quick(score)

        for idx, score in enumerate(scores):
            file = f"{raw_file}_{idx}.txt"
            with open(os.path.join(output_dir, file), 'w') as f:
                f.write(str(score))

        # Transpose 12 time
        # Save

# Create all from existing mxl files
if CREATE_CHORDS:
    from musiclang.analyze import get_chords_from_mxl
    paths = [str(path) for path in corpus.getPaths('mxl')]
    for path in paths:
        try:
            print(len(os.listdir(output_dir)))
            raw_file = '_'.join(path.replace(to_replace, '').replace('.musicxml', '').replace('.mxl', '').split('/'))
            print(raw_file)
            if os.path.exists(os.path.join(output_dir, f"{raw_file}_0.txt")):
                print('Already done : ', raw_file)
                continue
            score = get_chords_from_mxl(path)
            scores = get_score_in_every_tonality_quick(score)

            for idx, score in enumerate(scores):
                file = f"{raw_file}_{idx}.txt"
                with open(os.path.join(output_dir, file), 'w') as f:
                    f.write(str(score))
        except:
            print('Error with', path.replace(to_replace, ''))
        # Transpose 12 time
        # Save

if CREATE_FULL_MUSIC:
    from musiclang import Score
    output_dir = 'locals/full_data'
    to_replace = '/Users/floriangardin/code/music/musiclang2/venv/lib/python3.10/site-packages/music21/corpus/'
    os.makedirs(output_dir, exist_ok=True)
    paths = [str(path) for path in corpus.getPaths('mxl')]
    import music21
    for path in paths:
        print(path)
        try:
            raw_file = '_'.join(path.replace(to_replace, '').replace('.musicxml', '').replace('.mxl', '').split('/'))
            if os.path.exists(os.path.join(output_dir, f"{raw_file}_0.txt")):
                print('Already done : ', raw_file)
                continue
            score = Score.from_xml(path)
            score = score.decompose_duration()
            scores = get_score_in_every_tonality_quick(score)
            for idx, score in enumerate(scores):
                file = f"{raw_file}_{idx}.txt"
                with open(os.path.join(output_dir, file), 'w') as f:
                    f.write(str(score))
        except music21.repeat.ExpanderException:
            print('Repeat exception')
        except music21.romanText.translate.RomanTextTranslateException:
            print('Roman text translate exception')
