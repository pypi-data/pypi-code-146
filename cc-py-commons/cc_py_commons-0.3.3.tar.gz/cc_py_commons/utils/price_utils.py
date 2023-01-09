import math


def convert_to_cents(price_in_dollars):
  return (price_in_dollars * 100) if price_in_dollars is not None else None

def convert_to_cents_and_round(price_in_dollars):
  price_in_cents = convert_to_cents(price_in_dollars)
  return round(price_in_cents) if price_in_cents is not None else None

def convert_to_dollars(price_in_cents):
  return (price_in_cents / 100) if price_in_cents is not None else None

def convert_to_dollars_and_round(price_in_cents):
  price_in_dollars = convert_to_dollars(price_in_cents)
  return round(price_in_dollars) if price_in_dollars is not None else None

def extract_amount_in_cents(value):
  parsed_value = value

  if type(value) is str:
    if len(value) > 0:
      clean_value = value.replace(',', '').replace('$', '')
      if '.' in clean_value:
        clean_value = clean_value.split('.')[0]
      parsed_value = float(clean_value)
  else:
    parsed_value = float(value)

  if parsed_value and not math.isnan(parsed_value):
    return int(parsed_value * 100) #convert to cents
  else:
    return None
