import json

MIN_PERCENTAGE = 95

with open('coverage.json') as file:
    coverage_json = json.load(file)
    
assert coverage_json['totals']['percent_covered'] > MIN_PERCENTAGE