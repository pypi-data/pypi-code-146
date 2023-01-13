from itertools import zip_longest
from typing import List, Dict, Sequence

from solid2.core.object_base import OpenSCADObject

g_bom_headers: List[str] = []

def set_bom_headers(*args):
    global g_bom_headers
    g_bom_headers += args

class bill_of_material(OpenSCADObject):
    def __init__(self, elements):
        #set the OpenSCADIdentifier to a non identifer to raise a compile error
        #if rendered
        super().__init__('bill of matrrial not render-able', {})
        self.elements = elements

    def _render(self):
        s = ""
        for child in self.children:
            s += child._render()
        return s

def bom_part(description='', per_unit_price=None, currency='US$', *args, **kwargs):
    def wrap(f):
        name = description if description else f.__name__

        elements = {'name': name, 'Count':0, 'currency':currency, 'Unit Price':per_unit_price}
        # This update also adds empty key value pairs to prevent key exceptions.
        elements.update(dict(zip_longest(g_bom_headers, args, fillvalue='')))
        elements.update(kwargs)

        def wrapped_f(*wargs, **wkwargs):
            scad_obj = f(*wargs, **wkwargs)
            return bill_of_material(elements)(scad_obj)

        return wrapped_f

    return wrap

def bill_of_materials(root_obj:OpenSCADObject, csv:bool=False) -> str:
    traits_dicts = _traits_bom_dicts(root_obj)
    # Build a single dictionary from the ones stored on each child object
    # (This is an adaptation of an earlier version, and probably not the most
    # direct way to accomplish this)
    all_bom_traits = {}
    for traits_dict in traits_dicts:
        name = traits_dict['name']
        if name in all_bom_traits:
            all_bom_traits[name]['Count'] += 1
        else:
            all_bom_traits[name] = traits_dict
            all_bom_traits[name]['Count'] = 1
    bom = _make_bom(all_bom_traits, csv)
    return bom

#=====================
# = helper functions =
#=====================

def is_bill_of_material(x):
    return isinstance(x, bill_of_material)

def _traits_bom_dicts(root_obj:OpenSCADObject) -> List[Dict[str, float]]:
    all_child_traits = [_traits_bom_dicts(c) for c in root_obj.children]
    child_traits = [item for subl in all_child_traits for item in subl if item]

    if is_bill_of_material(root_obj):
        bom_trait = root_obj.elements
        child_traits.append(bom_trait)

    return child_traits

def _make_bom(bom_parts_dict: Dict[str, float], csv:bool=False, ) -> str:
    field_names = ["Description", "Count", "Unit Price", "Total Price"]
    field_names += g_bom_headers
    
    rows = []
    
    all_costs: Dict[str, float] = {}
    for desc, elements in bom_parts_dict.items():
        row = []
        count = elements['Count']
        currency = elements['currency']
        price = elements['Unit Price']

        if count > 0:
            if price:
                total = price * count
                if currency not in all_costs:
                    all_costs[currency] = 0 
                
                all_costs[currency] += total
                unit_price = _currency_str(price, currency)
                total_price = _currency_str(total, currency)
            else:
                unit_price = total_price = ""
            row = [desc, count, unit_price, total_price]

        for key in g_bom_headers:
            value = elements[key]
            row.append(value)
        rows.append(row)

    # Add total costs if we have values to add
    if len(all_costs) > 0:
        empty_row = [""] * len(field_names)
        rows.append(empty_row)
        for currency, cost in all_costs.items():
            row = empty_row[:]
            row[0] = "Total Cost, {currency:>4}".format(**vars())
            row[3] = "{currency:>4} {cost:.2f}".format(**vars())
            
            rows.append(row)

    res = _table_string(field_names, rows, csv)

    return res

def _currency_str(value:float, currency: str="$") -> str:
    return "{currency:>4} {value:.2f}".format(**vars())
    
def _table_string(field_names: Sequence[str], rows:Sequence[Sequence[float]], csv:bool=False) -> str:
    # Output a justified table string using the prettytable module.
    # Fall back to Excel-ready tab-separated values if prettytable's not found 
    # or CSV is requested
    if not csv:
        try:
            import prettytable
            table = prettytable.PrettyTable(field_names=field_names)
            for row in rows:
                table.add_row(row)
            res = table.get_string()
        except ImportError as e:
            print("Unable to import prettytable module.  Outputting in TSV format")
            csv = True
    if csv:
        lines = ["\t".join(field_names)]
        for row in rows:
            line = "\t".join([str(f) for f in row])
            lines.append(line)

        res = "\n".join(lines) 
        
    return res  + "\n"            

