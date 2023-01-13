from gwdg_idm_api.util import username_prediction

predictions = [
    ("Markus", "Stabrin", "markus.stabrin"),  # Normal
    ("Markus", "Stabrinabcde", "m.stabrinabcde"),  # gt 18
    ("Markus", "Stabrinabcdefghijklmnop", "m.stabrinabcdefghi"),  # gt 18 after gt 18
    ("Markus", "Stabrinå", "markus.stabrina"),  # å to a
    ("Markus", "Stabrinß", "markus.stabrinss"),  # ß to ss
    ("Markus", "Stabrin\u0256", "markus.stabrind"),  # lowercase d bar to d
    ("Markus", "Stabrin s", "markus.stabrins"),  # space to no space
]

error = False
for given_name, surname, expected in predictions:
    prediction = username_prediction(given_name, surname)
    if prediction != expected:
        print(f"  Failed: {prediction=} != {expected=}")
        error = True
    else:
        print(f"Success: {given_name=} {surname=} {prediction=}")

if error:
    raise Exception("Errors occured")
