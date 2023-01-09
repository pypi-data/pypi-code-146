#! /usr/bin/env python3
#import requests
import requests, sys, ftplib, os, subprocess, gzip, shutil
import pandas as pd
from easyterm import *
from ._version import __version__

def_opt={'i':'',
         'n':'',
         'otab':'',
         'of':'',
         'd':'',
         'markup':'yellow,,magenta,red',
         'f':'default',
         'max_down':4,
         'force':False,
         'ngz':False}

default_fields_displayed=['name', 'taxon_id', 'division', 'accession', 'release']
ftp_path_templates={'dna': 'ftp://ftp.ensembl.org/pub/release-{release}/fasta/{name}/dna/{name_capitalized}.{assembly}.dna.toplevel.fa.gz',
             'pep': 'ftp://ftp.ensembl.org/pub/release-{release}/fasta/{name}/pep/{name_capitalized}.{assembly}.pep.all.fa.gz',
             'cds': 'ftp://ftp.ensembl.org/pub/release-{release}/fasta/{name}/cds/{name_capitalized}.{assembly}.cds.all.fa.gz',
             'cdn':'ftp://ftp.ensembl.org/pub/release-{release}/fasta/{name}/cdna/{name_capitalized}.{assembly}.cdna.all.fa.gz',
             'gff': 'ftp://ftp.ensembl.org/pub/release-{release}/gff3/{name}/{name_capitalized}.{assembly}.{release}.gff3.gz'                }
file_code_description={'dna':'ensembl_genome.fa',
                      'pep':'ensembl_proteome.fa',
                      'cds':'ensembl_cds.fa',
                      'cdn':'ensembl_cdna.fa',
                      'gff':'ensembl_annotation.gff'}
ensembl_file_codes=sorted(file_code_description.keys())

help_msg="""ensembl_assembly.py: Program to check or download genomes and related files from the Ensembl FTP website.

Normally the program retrieves on the fly information for all Ensembl assemblies online.

## Output and input:
-n     +   only filter this assembly name, or multiple names as comma-sep
-otab  +   output assembly info table with *all* available fields to this file
-i     +   read a tsv file with assembly info (same type as written with -otab) instead of downloading on the fly

## Show to screen:
-f     +   comma-sep fields to display. Use 'all' for all fields. Prefix with "+" to add to default fields. Use "0" for no output.  
 Default:   """ +' '.join(default_fields_displayed) + """
 Available beyond Ensembl-provided:
   f:XXX  path to file in ftp server
   s:XXX  file size. It is 0 if file is not found
   h:XXX  human readable file size
  where XXX is any file code among: """+' '.join(ensembl_file_codes)+ """; use "any" for all)

-markup  comma-sep terminal codes used for printing columns. Available codes:
           """ +' '.join(markup_codes) + """

## Download files:
-d        +   comma-sep file code (see XXX above) to download
-of       +   output folder for downloading (required if any download is done)
-force        force overwrite even if local files are found
-max_down +   max number of attempts to download if checksum does not match
-ngz      +   do not gunzip and link files with a standard name (e.g. ensembl_genome.fa for dna)

### Other options:
-print_opt      print currently active options
-h OR --help    print this help and exit
"""

command_line_synonyms={}

def main(args={}):
    if not args: opt=command_line_options(def_opt, help_msg, '', synonyms=command_line_synonyms )
    write(f'  ensembl_assembly v.{__version__}  '.center(50, '='))
    #write(  opt  )
    write('='*50+'\n')

    if opt['d'] and not opt['of']:
        raise(NoTracebackError('ERROR to download with -d, you must specify a folder with -of'))
    
    if opt['i']:
        write(f"Reading Ensembl assembly metadata from file {opt['i']} ... ")
        check_file_presence(opt['i'], 'input file (opt -i)')
        full_ensembl_assembly_data=pd.read_csv( opt['i'], sep='\t', header=0)
    else: 
        write(f"Fetching Ensembl assembly metadata ...")
        server = "http://rest.ensembl.org"
        ext = "/info/species?"
        r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
            
        decoded = r.json()
        fields=set()
        for species_e in decoded['species']:
              for field in species_e: fields.add(field)
        full_ensembl_assembly_data=pd.DataFrame()
        for field in sorted(fields):
            full_ensembl_assembly_data[field]= [species_e[field] for species_e in decoded['species']  ]
    write(f"Ensembl metadata collected: {full_ensembl_assembly_data.shape[0]} species", how='reverse')

    if opt['n']:
        this_query=f"name in {opt['n'].split(',')}"
        ensembl_assembly_data=full_ensembl_assembly_data.query(this_query).copy()
        write(f"Filtering to these (n={ensembl_assembly_data.shape[0]}) assemblies collected: {opt['n']}")
    else:
        ensembl_assembly_data=full_ensembl_assembly_data
        
    if opt['f']:
        
        if   opt['f']=='default':        fields_displayed=default_fields_displayed
        elif opt['f']=='all':            fields_displayed=[i for i in ensembl_assembly_data.columns]
        elif opt['f'].startswith('+'):   fields_displayed=default_fields_displayed + opt['f'][1:].split(',')
        else:                            fields_displayed=opt['f'].split(',')
        
        for i in range(len(fields_displayed)-1, -1, -1):
            f=fields_displayed[i]
            if f.endswith(':any'):
                fields_displayed.pop(i)
                for fc in ensembl_file_codes:    fields_displayed.insert(i, f[0]+':'+fc)
    
    
    write(f'Determining FTP file paths and sizes...  ')
    compute_size={}
    for k in ensembl_file_codes:
        compute_size[k]='s:'+k in fields_displayed or 'h:'+k in fields_displayed            
    
    ftp_path_data={}
    filesize_data={}
    filesizeh_data={}
        
    for i, r in ensembl_assembly_data.iterrows():
        service(f"Processing {r['name']}")

        for k in ftp_path_templates:
            x=ftp_path_templates[k].format(**r, name_capitalized=r['name'].capitalize() )    
            ftp_path_data.setdefault(k,  []).append( x )

            if compute_size[k]:
              ftp_handler=get_ftp_handler() # lazy connection            
              try:
                  s=ftp_handler.size(   strip_ftp_root(x)   )
              except ftplib.error_perm:
                  s=0
              h=human_readable_size(s)

              filesize_data.setdefault(k,  []).append( s )
              filesizeh_data.setdefault(k, []).append( h )

    for k in ftp_path_data:
        ensembl_assembly_data['f:'+k] =ftp_path_data[k]
        if compute_size[k]:
            ensembl_assembly_data['s:'+k] =filesize_data[k]
            ensembl_assembly_data['h:'+k] =filesizeh_data[k]        

        
    ### DISPLAY
    if opt['f']:
        max_length_per_fields={}
        for field in fields_displayed:
            max_length_per_fields[field]= max( [  len(str(r[field]))
                     for i, r in ensembl_assembly_data.iterrows()] + [len(field)])

        ### start printing
        table_width=sum(max_length_per_fields.values()) + len(max_length_per_fields)
        write(f'{" Summary table ":=^{table_width}}')        
        # header
        markup=opt['markup'].split(',')
        for i,field in enumerate(fields_displayed):
            write(field.ljust(max_length_per_fields[field]), end=' ',  how=  markup[i%len(markup)] )
        write('')
        # rows
        for i, r in ensembl_assembly_data.iterrows():
            for i,field in enumerate(fields_displayed):
                write( str(r[field]).ljust(max_length_per_fields[field]), end=' ',  how=  markup[i%len(markup)] )
            write('')
        write('='*table_width)

        file_codes_requested_size=  set([f[2:]  for f in fields_displayed if f.startswith('s:') or f.startswith('h:')])
        if file_codes_requested_size:
            tot_size=sum(   [ ensembl_assembly_data [ 's:'+k ].sum()   for k in file_codes_requested_size] ) 
            write(f"Total size: {tot_size} bytes, approximately {human_readable_size(tot_size)}")
            write('='*table_width)        
        
    if opt['otab']:
        write(f"Printing table with all available fields to -> {opt['otab']}")
        ensembl_assembly_data.to_csv(opt['otab'], sep='\t', index=False)

    if opt['d']:
        types_to_download=opt['d'].split(',')  if opt['d']!='any' else  ensembl_file_codes
        
        table2_width=max_length_per_fields['name']+ 4 + 9*len(types_to_download)
        output_folder=opt['of'].rstrip('/')+'/'
        if not os.path.isdir(output_folder):    os.mkdir(output_folder)
        
        write(f'\n{f" Downloading -> {output_folder} ":=^{table2_width}}')
        
        for i, r in ensembl_assembly_data.iterrows():
            name=r['name']
            message=f"{name:<{max_length_per_fields['name']}}    "

            assembly_folder=output_folder+name+'/'            
            if not os.path.isdir(assembly_folder):    os.mkdir(assembly_folder)
            
            ftp_handler=get_ftp_handler() # lazy connection            
            for k in types_to_download:
                
                ftp_path=strip_ftp_root(r['f:'+k])
                basename_ftp_path=os.path.basename(ftp_path)
                file_destination= assembly_folder + basename_ftp_path
                file_destination_tmp=file_destination +'.downloading'
                gunzipped_file= file_destination.split('.gz')[0]
                gunzipped_file_tmp=gunzipped_file+'.gunzipping'                
                file_link=assembly_folder+file_code_description[k]
                
                message+= k+' '

                lets_unzip= not opt['gz']
                lets_link=  not opt['gz']
                lets_download=True
                if os.path.isfile(file_link):     
                    if lets_link  and opt['force']:
                        printerr(f"Removing existing link to replace it: {file_link}");
                        os.remove(file_link)
                    else:
                        lets_download, lets_unzip, lets_link=(False, False, False)
                if os.path.isfile(gunzipped_file):     
                    if lets_unzip and opt['force']:
                        printerr(f"Removing existing file to replace it: {gunzipped_file}")
                        os.remove(gunzipped_file)
                    else:
                        lets_download, lets_unzip=(False, False)
                if os.path.isfile(file_destination):
                    if opt['force']:
                        printerr(f"Removing existing file.gz to replace it: {file_destination}")
                        os.remove(file_destination)          
                    else:
                        lets_download=False                

                if lets_download:
                    ## downloading checksum file
                    ftp_checksum_file=os.path.dirname(ftp_path) + '/CHECKSUMS'
                    checksum_file_content=''
                    def store_checksum_file_content(line):
                        nonlocal checksum_file_content
                        checksum_file_content+=str(line, 'utf-8')
                    ftp_handler.retrbinary("RETR " + ftp_checksum_file, store_checksum_file_content)

                    ## getting checksum of file we want
                    website_checksum=None                
                    for line in checksum_file_content.split('\n'):                
                        s=line.strip().split()
                        if len(s)<3: continue
                        if s[2]==  basename_ftp_path:
                            website_checksum=(int(s[0]), int(s[1]) )
                    if website_checksum is None: raise(Exception(f"ERROR I did not find the checksum for {basename_ftp_path}"))

                    #### downloading actual target file
                    for download_attempt in range(opt['max_down']):
                        service(message+  f" downloading (attempt n.{download_attempt+1})")
                        fh = open( '{}'.format(file_destination_tmp), "wb")            #fh = open( '{}'.format(file_destination_tmp), "w")
                        ftp_handler.retrbinary("RETR " + ftp_path, fh.write)       #ftp_handler.retrlines("RETR " + ftp_path_cut, fh.write) #, 8*1024)
                        fh.close()

                        downloaded_checksum=checksum_of_file(file_destination_tmp)

                        if downloaded_checksum!=website_checksum:
                            printerr('checksum did not match for {} at download attempt {}'.format(basename_ftp_path, download_attempt+1) )
                        else:
                            break  #ok, no more download attempts

                    os.rename(file_destination_tmp,  file_destination)

                if lets_unzip:
                    ## gunzipping
                    if lets_unzip:
                      service(message+  f" gunzipping")
                      with gzip.open(file_destination, 'rb') as f_in:
                        with open(gunzipped_file_tmp, 'wb') as f_out:
                          shutil.copyfileobj(f_in, f_out)
                          os.rename(gunzipped_file_tmp,  gunzipped_file)
                          os.remove(file_destination)
                          
                if lets_link:
                    ## linking 
                    if lets_link:
                      service(message+  f" linking")                    
                      os.symlink( os.path.basename(gunzipped_file),  file_link) 

                
                message+='OK   '
            write(message)
        write('='*table2_width)
        



###  A few functions
        
ftp_handler=None
def get_ftp_handler(url='ftp.ensembl.org',  force=False): #'ftp.ncbi.nlm.nih.gov'
    global ftp_handler
    if ftp_handler is None or force:
        printerr('FTP: establishing connection with {}'.format(url))
        ftp_handler=ftplib.FTP(host=url)
        ftp_handler.login()
        ftp_handler.set_pasv(False) ## added
    return(ftp_handler)


def strip_ftp_root(url):
    """ Go from ftp://ftp.ensembl.org/pub/release-...
         to:  pub/release-...
    """
    return(url[6+ url[6:].index('/') +1 : ])

size_names = [    (1024 ** 5, 'P'),    (1024 ** 4, 'T'),     (1024 ** 3, 'G'),     (1024 ** 2, 'M'),     (1024 ** 1, 'K'),    (1024 ** 0, 'B')    ]
def human_readable_size(bytes, system=size_names):
    """Human-readable file size.
    Using the traditional system, where a factor of 1024 is used::     >>> size(10)    '10B'
    >>> size(20000)    '19K'       >>> size(100000)    '97K'           >>> size(200000)    '195K'        """
    for factor, suffix in system:
        if bytes >= factor:            break
    amount = int(bytes/factor)
    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:    suffix = singular
        else:              suffix = multiple
    return(str(amount) + suffix)


def checksum_of_file(filename):
    csplit=['sum', filename]
    p = subprocess.Popen(csplit, 
                         stderr=subprocess.STDOUT, stdout=subprocess.PIPE,
                         env=os.environ)
    stdout, _  = p.communicate()
    int1, int2=map(int, stdout.strip().split())    
    return( (int1, int2) )


if __name__ == "__main__":
    main()
