import re
import os
import sys
import argparse
import subprocess
import pandas as pd


# This scripts was depend on entrez direct software, for more information and documentation on EDirect, please see:
# https://www.ncbi.nlm.nih.gov/books/NBK179288/
# This script was used to download biosample metadata based on the biosample accession.
# Before run, you should put all acc number in a txt file, one acc per line
# Test env
# python=3.6
# pandas=0.25.3
# author： Qingpo Cui
# email：B20193050449@cau.edu.cn


def args_parse():
    "Parse the input argument, use '-h' for help."
    parser = argparse.ArgumentParser(
        usage='download_biosample.py -list <biosample_acc_list> -outdir <output>\n\nAuthor: Qingpo Cui(SZQ Lab, China Agricultural University)\n')
    parser.add_argument("-list", help="<file>: biosample_acc_list, one accession per line")
    parser.add_argument("-outdir", help="<path>: output directory name")
    parser.add_argument('-v', '--version', action='version',
                        version='Version: ' + get_version("__init__.py"), help='Display version')
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()

def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

def parse_meta(file):
    temp_dict = {}
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if re.search(r'="', line):
                temp_dict[line.split('=')[0].replace(
                    '/', '')] = line.split('=')[1].replace('"', '')
            elif re.search(r'Accession: ', line):
                temp_dict['BioSample'] = line.split(
                    '\t')[0].replace('Accession: ', '')

    df_meta = pd.DataFrame.from_dict(temp_dict, orient='index')
    return df_meta


def get_biosample_list(file):
    bs = []
    with open(file, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            bs.append(line)
    return bs


def download_meta(biosample_acc, outdir):
    outdir = os.path.abspath(outdir)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    # print(outdir)
    output_file = os.path.join(outdir, str(biosample_acc + '.txt'))
    # print(output_file)
    command = "esearch -db biosample -query " + biosample_acc + " | efetch "
    # print(command)
    with open(output_file, 'w') as outfile:
        subprocess.run(command, shell=True, stdout=outfile)
    outfile.close()
    df_tmp = parse_meta(output_file)
    return df_tmp


def main():
    df_metainfo = pd.DataFrame()
    args = args_parse()
    biosample_list_file = os.path.abspath(args.list)
    outdir = os.path.abspath(args.outdir)
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for i in get_biosample_list(biosample_list_file):
        # print(i)
        df_biosample = download_meta(i, outdir)
        print('Downloading ' + i + ' metadata...')
        df_metainfo = pd.concat(
            [df_metainfo, df_biosample], axis=1, sort=False)
    metainfo_outfile = os.path.join(outdir, 'final_metainfo.csv')
    df_metainfo.T.to_csv(metainfo_outfile)


if __name__ == '__main__':
    main()
