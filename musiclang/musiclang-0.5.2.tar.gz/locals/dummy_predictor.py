from musiclang.predict.dummy.dummy_predictor import DummyPredictor

model = DummyPredictor()


predicted_score = model.predict('(VI % I.M)(piano__0=', temperature=0.1, output='score', include_start=True, n_tokens=500)

print(predicted_score)
#predicted_score.to_voicings().p.to_midi('locals/test.mid', tempo=240)
predicted_score.to_midi('locals/test.mid', tempo=120)