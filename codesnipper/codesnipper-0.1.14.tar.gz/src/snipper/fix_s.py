from collections import defaultdict
import os
from snipper.block_parsing import block_iterate
from snipper.snipper_main import full_strip

def get_s(lines):
    """ Return snips from 'lines' """
    blocks = defaultdict(list)
    for c in block_iterate(lines, "#!s"):
        # c['start_tag_args']
        if not c['start_tag_args'].get('keeptags', False):
            c['block'] = full_strip(c['block'])
        else:
            # In this case the #! tags are kept in.
            pass
            # print("keepting tags.")
        blocks[c['name']].append(c)

    output = {}
    for name, co in blocks.items():
        slines = [l for c in co for l in c['block']]
        # full_strip("")
        # c['block']['args']
        # slines = slines[ 23]
        # co.
        output[name] = slines
    return output

# def _s_block_process():
#
#     pass

def save_s(lines, output_dir, file_path): # save file snips to disk
    content = get_s(lines)
    # Only make output dir if needed.
    if len(content) > 0 and not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    for name, ll in content.items():
        if file_path is not None:
            file_path = file_path.replace("\\", "/")
            ll = [f"# {file_path}"] + ll
        out = "\n".join(ll)

        with open(output_dir + "/" + os.path.basename(file_path)[:-3] + ("_" + name if len(name) > 0 else name) + ".py", 'w') as f:
            f.write(out)


s1 = """
L1
L2 #!s=a
L3 #!s=b
L4
L5 
L6 
L7 #!s=a
L8 
L9 #!s=b
went
"""
if __name__ == "__main__":
    # for c in block_iterate(s1.splitlines(), tag="#!s"):
    #     print(c['block'])
    output = get_s(s1.splitlines())
    for k, v in output.items():
        print("name:", k)
        print("\n".join(v))
        print("="*10)

