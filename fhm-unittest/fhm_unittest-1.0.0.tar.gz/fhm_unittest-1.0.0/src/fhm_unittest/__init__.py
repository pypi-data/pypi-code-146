def output_test(returned_output, expected_output):
  from fuzzywuzzy import fuzz
  score = fuzz.WRatio(returned_output, expected_output)
  if score == 100:
    print("Accepted")
  elif score >= 90:
    print(f'Accepted [{score}%]')
  elif score >= 50:
    print(f'Not Accepted [{score}%]')
  else:
    print(f"Wrong Answer [{score}%]")