#!/usr/bin/env python3
# encoding: UTF-8
# 2022.12.1 by ganjun

import os
import shutil

def link_pics(inprefix, outprefix):
    os.system("ln -srf %s.png %s.png" %(inprefix, outprefix))
    os.system("ln -srf %s.pdf %s.pdf" %(inprefix, outprefix))

def convert_pics(inprefix, outprefix):
    os.system("convert -resize 800 %s.png %s.png" %(inprefix, outprefix))
    os.system("ln -srf %s.pdf %s.pdf" %(inprefix, outprefix))

def qc_supp(yaml_dict, pro_dir , odir):
    """Summarize clean stat for report generation

    :Args:
        * yaml_dict (dict): yaml.load(open(yaml),Loader=yamlFullload)
        * prodir (str): directory of project
        * odir (str): directory of output
    :Returns:
        Null
    """
    qc_dir_new = os.path.join(odir, "QC")
    if os.path.exists(qc_dir_new):
        shutil.rmtree(qc_dir_new)
    os.makedirs(qc_dir_new)

    os.system('ln -srf %s %s' %(os.path.join(pro_dir,"QC","qc.stat.xls") , os.path.join(qc_dir_new,"qc.stat.xls")))

    for sample in yaml_dict["samples"]:
        raw_dir = os.path.join(pro_dir, "QC", sample)
        res_dir = os.path.join(qc_dir_new,sample)
        os.makedirs(res_dir)

        convert_pics(os.path.join(raw_dir, "%s.reads.filter"%(sample)), os.path.join(res_dir, "%s.reads.filter"%(sample)))
        convert_pics(os.path.join(raw_dir, "%s.bases.quality"%(sample)), os.path.join(res_dir, "%s.bases.quality"%(sample)))
        convert_pics(os.path.join(raw_dir, "%s.bases.content"%(sample)), os.path.join(res_dir, "%s.bases.content"%(sample)))
        convert_pics(os.path.join(raw_dir, "%s.GC.distribution"%(sample)), os.path.join(res_dir, "%s.GC.distribution"%(sample)))

def uid_supp(prodir, odir):
    """Summarize UID stat for report generation

    :Args:
        * prodir: directory of project
        * odir: directory of output
    :Returns:
        Null
    """
    uid_dir_new = os.path.join(odir, "UID")
    if os.path.exists(uid_dir_new):
        shutil.rmtree(uid_dir_new)
    os.makedirs(uid_dir_new)
    uid_stat = os.path.join(uid_dir_new, "uid.stat.xls")
    file_dir = os.path.join(prodir, "UID", "uid.stat.xls")
    os.system("ln -srf %s %s" %(file_dir, uid_stat))

def qc_release(yaml_dict,prodir, odir):
    raw_dir_new = os.path.join(odir,"RawData")
    qc_dir_new = os.path.join(odir, "CleanData")
    md5_new = os.path.join(odir, "MD5.txt")
    md5_out = open(md5_new,'w')
    for dir in [raw_dir_new,qc_dir_new]:
        os.system("mkdir -p %s" %(dir))
    # RawData
    for sample in yaml_dict["samples"]:
        for end in ["R1","R2"]:
            raw_md5 = os.path.join(prodir,"RawData","%s.%s.fastq.gz.md5" %(sample, end))
            md5,path = open(raw_md5).readlines()[0].split()
            md5_out.write(md5+"  RawData/"+os.path.basename(path)+'\n')
            os.system("ln -srf %s %s" %(path,raw_dir_new))
    # CleanData
    for sample in yaml_dict["samples"]:
        for end in ["R1","R2"]:
            qc_md5 = os.path.join(prodir,"QC",sample,"%s.clean.%s.fastq.gz.md5" %(sample,end))
            md5,path = open(qc_md5).readlines()[0].split()
            md5_out.write(md5+"  CleanData/"+os.path.basename(path)+'\n')
            os.system("ln -srf %s %s" %(path,qc_dir_new))

def uid_release(yaml_dict, prodir, odir):
    uid_dir_new = os.path.join(odir,"UID")
    md5_new = os.path.join(odir, "MD5.txt")
    md5_out = open(md5_new, "a")
    os.system("mkdir -p %s" %(uid_dir_new))
    for sample in yaml_dict["samples"]:
        for end in ["R1","R2"]:
            uid_md5 = os.path.join(prodir,"UID","%s.dedup.%s.fastq.gz.md5" %(sample,end))
            md5,path = open(uid_md5).readlines()[0].split()
            md5_out.write(md5+"  UID/"+os.path.basename(path)+'\n')
            os.system("ln -srf %s %s" %(path,uid_dir_new))