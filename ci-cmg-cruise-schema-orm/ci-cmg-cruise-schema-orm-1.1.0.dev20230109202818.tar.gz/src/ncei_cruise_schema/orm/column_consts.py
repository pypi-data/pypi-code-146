WKT_PLACEHOLDER = "SDO_UTIL.FROM_WKTGEOMETRY(?)"
DATE_PLACEHOLDER = "TO_DATE(?,'YYYY-MM-DD\"T\"HH24:MI:SS')"

def wkt_select_name(name):
  return "TO_CLOB(SDO_UTIL.TO_WKTGEOMETRY({name}))".format(name=name)

def date_select_name(name):
  return "TO_CHAR({name},'YYYY-MM-DD\"T\"HH24:MI:SS')".format(name=name)

def xml_to_clob_select_name(name):
  return "{name}.getClobVal()".format(name=name)