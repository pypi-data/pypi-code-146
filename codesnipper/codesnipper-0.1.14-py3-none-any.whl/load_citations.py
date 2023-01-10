import os
import io
import glob
from pybtex import plugin
from pybtex.database.input import bibtex
from warnings import warn

### Newstyle loading.
def get_aux(auxfile):
    # paths = get_paths()
    # auxfile = os.path.join(paths['02450public'], auxfile)
    auxfile = os.path.normpath(auxfile) # Unsure if this is required. But had problems finding the auxfile on git.
    # auxfile = auxfile.replace(os.sep, '/')
    auxfile = auxfile.replace("\\", '/') # Fucking windows.

    if not os.path.exists(auxfile):
        # print(auxfile)
        warn("Could not find bibtex file: " + auxfile + " testing for troubles")
        auxdir = os.path.dirname(auxfile)
        # os.path.curdir

        print("The current working directory (os.getcwd()) is ", os.getcwd() )
        try:
            print("Trying to list files in builds dir")
            for f in glob.glob("/builds/02465material/*"):
                print(f)
        except Exception as e:
            print(e)

        if not os.path.dirname(auxdir):
            print("Directory for auxfile does not exist:", auxdir)
        else:
            print("Auxfile did not exist, but directory did. Printing the contents:")
            for f in glob.glob(os.path.dirname(auxfile) + "/*"):
                print(f)

        return {}

    with open(auxfile, 'r') as f:
        items = f.readlines()
    entries = {}
    for e in items:
        e = e.strip()
        if e.startswith("\\newlabel") and "@cref" in e:
            # print(e)
            i0 = e.find("{")
            i1 = e.find("@cref}")
            key = e[i0+1:i1]

            j0 = e.find("{{[", i0)+3
            j1 = e.find("}", j0)

            val = e[j0:j1]

            label = val[:val.find("]")]
            number = val[val.rfind("]")+1:]

            if label == "equation":
                nlabel = f"eq. ({number})"
            else:
                nlabel = label.capitalize() + " " + number

            # coderef = "\\cite[%s]{%s}"%(nlabel, bibtex) if bibtex is not None else None

            entries[key] = {'nicelabel': nlabel, 'rawlabel': label, 'number': number}
    return entries


def get_bibtex(bibfile):
    """
    all references.
    """
    if not os.path.exists(bibfile):
        return None

    pybtex_style = plugin.find_plugin('pybtex.style.formatting', 'alpha')()
    pybtex_html_backend = plugin.find_plugin('pybtex.backends', 'html')()
    pybtex_plain_backend = plugin.find_plugin('pybtex.backends', 'plaintext')()
    pybtex_parser = bibtex.Parser()

    with open(bibfile, 'r', encoding='utf8') as f:
        data = pybtex_parser.parse_stream(f)

    data_formatted = pybtex_style.format_entries(data.entries.values())
    refs = {}

    # if 'auxfile' in gi:
    #     all_references = parse_aux(gi['auxfile'], bibtex=gi['bibtex'])
    # else:
    #     all_references = {}

    for entry in data_formatted:
        output = io.StringIO()
        output_plain = io.StringIO()
        pybtex_plain_backend.output = output_plain.write
        pybtex_html_backend.output = output.write
        pybtex_html_backend.write_entry(entry.key, entry.label, entry.text.render(pybtex_html_backend))

        pybtex_plain_backend.write_entry(entry.key, entry.label, entry.text.render(pybtex_plain_backend))

        html = output.getvalue()
        plain = output_plain.getvalue()

        entry.text.parts[-2].__str__()
        url = ""
        for i,p in enumerate(entry.text.parts):
            if "\\url" in p.__str__():
                url = entry.text.parts[i+1]
                break
        url = url.__str__()
        i1 = html.find("\\textbf")
        i2 = html.find("</span>", i1)
        dht = html[i1:i2]
        dht = dht[dht.find(">")+1:]
        html = html[:i1] + " <b>"+dht+"</b> " + html[i2+7:]

        plain = plain.replace("\\textbf ", "")
        iu = plain.find("URL")
        if iu > 0:
            plain = plain[:iu]

        refs[entry.key] = {'html': html,
                           'plain': plain,
                           'label': entry.label,
                           'filename': url,
                           }

    return refs


def find_tex_cite(s, start=0, key="\\cite"):
    txt = None
    i = s.find(key, start)
    if i < 0:
        return (i,None), None, None
    j = s.find("}", i)
    cite = s[i:j + 1]

    if cite.find("[") > 0:
        txt = cite[cite.find("[") + 1:cite.find("]")]

    reference = cite[cite.find("{") + 1:cite.find("}")]
    return (i, j), reference, txt

### Oldstyle loading
# def get_references(bibfile, gi):
#     """
#     all references.
#     """
#     if not os.path.exists(bibfile):
#         return None
#
#     pybtex_style = plugin.find_plugin('pybtex.style.formatting', 'alpha')()
#     pybtex_html_backend = plugin.find_plugin('pybtex.backends', 'html')()
#     pybtex_plain_backend = plugin.find_plugin('pybtex.backends', 'plaintext')()
#     pybtex_parser = bibtex.Parser()
#
#     with open(bibfile, 'r', encoding='utf8') as f:
#         data = pybtex_parser.parse_stream(f)
#
#     data_formatted = pybtex_style.format_entries(data.entries.values())
#     refs = {}
#
#     if 'auxfile' in gi:
#         all_references = parse_aux(gi['auxfile'], bibtex=gi['bibtex'])
#     else:
#         all_references = {}
#
#     for entry in data_formatted:
#         output = io.StringIO()
#         output_plain = io.StringIO()
#         pybtex_plain_backend.output = output_plain.write
#         pybtex_html_backend.output = output.write
#         pybtex_html_backend.write_entry(entry.key, entry.label, entry.text.render(pybtex_html_backend))
#
#         pybtex_plain_backend.write_entry(entry.key, entry.label, entry.text.render(pybtex_plain_backend))
#
#         html = output.getvalue()
#         plain = output_plain.getvalue()
#
#         entry.text.parts[-2].__str__()
#         url = ""
#         for i,p in enumerate(entry.text.parts):
#             if "\\url" in p.__str__():
#                 url = entry.text.parts[i+1]
#                 break
#         url = url.__str__()
#         i1 = html.find("\\textbf")
#         i2 = html.find("</span>", i1)
#         dht = html[i1:i2]
#         dht = dht[dht.find(">")+1:]
#         html = html[:i1] + " <b>"+dht+"</b> " + html[i2+7:]
#
#         plain = plain.replace("\\textbf ", "")
#         iu = plain.find("URL")
#         if iu > 0:
#             plain = plain[:iu]
#
#         refs[entry.key] = {'html': html,
#                            'plain': plain,
#                            'label': entry.label,
#                            'filename': url,
#                            'references': all_references}
#
#     newref = {}
#     ls = lambda x: x if isinstance(x, list) else [x]
#     if 'tex_command' in gi:
#         for cmd, aux, display in zip( ls(gi['tex_command']), ls(gi['tex_aux'] ), ls( gi['tex_display'] ) ):
#             ax = parse_aux(aux, bibtex=gi['bibtex'])
#             for k in ax:
#                 ax[k]['pyref'] = display%(ax[k]['nicelabel'],)
#             newref[cmd] = ax
#
#     return refs, newref
#
#
# def parse_aux(auxfile, bibtex=None):
#     # paths = get_paths()
#     paths = {}
#     auxfile = os.path.join(paths['02450public'], auxfile)
#     if not os.path.exists(auxfile):
#         print(auxfile)
#         from warnings import warn
#         warn("Could not find file")
#         return {}
#
#     with open(auxfile, 'r') as f:
#         items = f.readlines()
#     entries = {}
#     for e in items:
#         e = e.strip()
#         if e.startswith("\\newlabel") and "@cref" in e:
#             # print(e)
#             i0 = e.find("{")
#             i1 = e.find("@cref}")
#             key = e[i0+1:i1]
#
#             j0 = e.find("{{[", i0)+3
#             j1 = e.find("}", j0)
#
#             val = e[j0:j1]
#
#             label = val[:val.find("]")]
#             number = val[val.rfind("]")+1:]
#
#             if label == "equation":
#                 nlabel = f"eq. ({number})"
#             else:
#                 nlabel = label.capitalize() + " " + number
#
#             coderef = "\\cite[%s]{%s}"%(nlabel, bibtex) if bibtex is not None else None
#             entries[key] = {'pyref': coderef, 'nicelabel': nlabel, 'rawlabel': label, 'number': number}
#     return entries

