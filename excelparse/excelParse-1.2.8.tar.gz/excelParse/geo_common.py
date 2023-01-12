#!/usr/bin/env python3
"""
Usage: 根据excel创建的各流程共用的对象
Author: Gj
Last update: 2022.11.15
"""
import os
import math
import collections
import shutil
from excelParse import ParserXLS, FastqToFC



def ding_talk(msn, mobiles, access_token = 'e20f01ecb7d4cb1c78975d0946667f934092043c4d11e855a397bf4ad1a84ef1'):
    talk = """curl 'https://oapi.dingtalk.com/robot/send?access_token=%s' \
-H 'Content-Type: application/json' -d '{"msgtype": "text","text": {"content":"%s"},"at":{"atMobiles":%s}}'
"""%(access_token, msn, mobiles)
    return talk

def get_oss_path(contract_number):
    """Get OSS path for uploading based on contract number
    """
    year = contract_number.split("-")[0][2:]
    num = int(contract_number.split("-")[1][1:])
    floor = str(math.floor(num/100) * 100 + 1).zfill(4)
    ceil = str(math.ceil(num/100) * 100).zfill(4)
    oss_path = "/%s/%s-%s/%s/Data/"%(year, floor, ceil, contract_number)
    return oss_path

class Geo_common:
    """
    这个对象定义了:
    1. init: main页面所有块, 和project页面的公共块(analysis_steps, adapter, parameters, pipeline_control)
    2. singularity容器挂载参数
    3. 分析脚本, report脚本, upload脚本
    """
    def __init__(self, excel, main_name, project_name, pipe_dir):
        self.excel = excel
        self.main_name = main_name
        self.project_name = project_name
        ######## 以下是main页面的解析
        # series: 合同信息 , dict = {key:value}
        self.series = {}
        for k,v in ParserXLS.fetch_col(excel, main_name, "SERIES").items():
            self.series[k] = v
        # samples: 样本信息 ,  dict = {sample:{group:x, IP/Input:x, raw_file_r1:x, raw_file_r2:x}}
        self.samples = collections.defaultdict(dict)
        which_sheet = main_name
        if project_name in ["WES","WGS"]:         # 这些项目的样本信息在自己的项目页面
            which_sheet = project_name
        data = ParserXLS.fetch_row(excel, which_sheet, "SAMPLES")        # sample name 必须在第一列
        for line in data[1:]:
            # 跳过空行
            if_empty = True
            for s in line:
                if s.strip():
                    if_empty = False
            if if_empty:
                continue

            for head in data[0][1:]:
                tmp = line[data[0].index(head)]
                if head in ["group","raw_file_r1","raw_file_r2"]:      # 这三个key允许多个值, 一致使用列表元素
                    tmp = tmp.strip().split(";")                           # group , raw_file_r1 , raw_file_r2 可以输入多个值, 用 ; 分割
                    self.samples[line[0]][head] = []
                    for i in tmp:
                        self.samples[line[0]][head].append(i)
                else:
                    self.samples[line[0]][head] = tmp
            # 判断R1和R2是否对应
            r1s = self.samples[line[0]]["raw_file_r1"]
            r2s = self.samples[line[0]]["raw_file_r2"]
            if len(r1s) != len(r2s):
                exit("错误: %s 的R1和R2文件数量不相等" %(line[0]))
            l1 = 0                                                      # read测序长度, 只取R1的第一个数据
            for r1,r2 in zip(r1s,r2s):
                if not l1:
                    f1,i1,l1 = FastqToFC.flowcell_lane(r1)                  
                if_same = FastqToFC.diff_r1_r2(r1,r2)
                if not if_same:
                    exit("错误: %s 与 %s 不是对应的双端序列!" %(r1,r2))
                # 测序reads长度 
            self.samples[line[0]]["length"] = str(l1)
        # groups: 每个比对组包含的样本 , dict = {group1 : [sample1 , smaple2] , group2 : [sample3 , sample4]}
        self.groups = collections.defaultdict(list)
        for sample in self.samples:
            for group in self.samples[sample]["group"]:
                self.groups[group].append(sample)
        # compare_group: 比对组信息 , list = [treat__control]
        self.compare_group = []
        for line in ParserXLS.fetch_row(excel, main_name, "COMPARE_GROUP")[1:]:
            self.compare_group.append(line[0]+"__"+line[1])
        # protocol: 基因组信息 , dict = {key:value}
        self.protocol = {}
        for k,v in ParserXLS.fetch_col(excel, main_name, "PROTOCOL").items():
            self.protocol[k] = v
        # phone : 分析人员手机号码
        self.analyst_phone_number = int(ParserXLS.fetch_row(excel, main_name, "ANALYST_PHONE_NUMBER")[0][0])

        ############ 以下是project页面的解析, 仅解析公共部分, 比如: ANALYSIS_STEPS , ADAPTER , PARAMETERS , PIPELINE_CONTROL
        # analysis_steps: 分析步骤 , list = [QC,Mapping,...]
        self.analysis_steps = []
        for k,v in ParserXLS.fetch_col(excel, project_name, "ANALYSIS_STEPS").items():
            if v == "True":
                self.analysis_steps.append(k)
        # adapter: 接头 , dict = {key:value}
        self.adapter = {}
        for k,v in ParserXLS.fetch_col(excel, project_name, "ADAPTER").items():
            self.adapter[k] = v
        # parameters: 流程的部分参数, 经常修改的, 比如pvalue, FDR等, dict = {key:value}
        self.parameters = {}
        for k,v in ParserXLS.fetch_col(excel, project_name, "PARAMETERS").items():
            self.parameters[k] = v
        # pipeline_control: 流程控制参数, 如抽数据, 去污染等, dict = {key:value}
        self.pipeline_control = {}
        for k,v in ParserXLS.fetch_col(excel, project_name, "PIPELINE_CONTROL").items():
            self.pipeline_control[k] = v

        #### 常用变量:
        pro_dir = self.protocol["project_dir"]
        contract_number = self.series["contract_number"]
        self.yaml = os.path.join(pro_dir,contract_number+"."+project_name+'.yaml')
        ############ singularity 挂载信息
        roots= []
        self.singularity_args = ''
        for i in [pipe_dir , pro_dir , 'abc'] + [self.samples[sample]["raw_file_r1"][0] for sample in self.samples]:
            i = i.split("/")[1]
            roots.append(i)
        roots = set(roots)
        for i in roots:
            self.singularity_args += "-B /%s:/%s " %(i,i)
        ########## 生成目录, 拷贝pipeline.yaml
        os.system("mkdir -p %s/log/slurmlog" %(pro_dir))
        shutil.copy(os.path.join(pipe_dir,"pipeline.yaml"),pro_dir)
        ########## 分析脚本
        n = 1
        shells = []
        for stage in self.analysis_steps:
            shell = os.path.join(pro_dir, "%s.%s.sh" %(n,stage))
            n += 1
            shells.append("sh %s" %(shell))
            success_msn = "hello, %s 的 %s 已完成，路径为 %s ."%(contract_number, stage, pro_dir)
            fail_msn = "hello, %s 的 %s 分析失败，请检查, 路径为 %s ."%(contract_number, stage, pro_dir)
            success_talk = ding_talk(success_msn, self.analyst_phone_number)
            fail_talk = ding_talk(fail_msn, self.analyst_phone_number)
            with open(shell,'w') as f:
                f.write("""
snakemake --cluster-config %s/pipeline.yaml --cluster "sbatch -c {cluster.c} -o {cluster.o} -e {cluster.e} --parsable " --cluster-cancel scancel --use-singularity --singularity-args "%s" -j 20 -ps %s/master/master_%s.smk --configfile %s --directory %s --latency-wait 300 

if [ $? -eq 0 ];
then
#DingTalk
%s
else
#Fail DingTalk
%s
fi

""" %(pro_dir, self.singularity_args,pipe_dir, stage, self.yaml, pro_dir,
    success_talk,
    fail_talk))

        ######### 生成报告 和 上传 脚本
        report_shell = os.path.join(pro_dir, "report.sh")
        with open(report_shell,'w') as f:
            f.write("""
    %s/script/SuppGenerate.py --yaml %s --odir %s/Report/supp/ && \\

    %s/script/Report.py --odir %s/Report --yaml %s
    """%(pipe_dir, self.yaml, pro_dir,
    pipe_dir, pro_dir, self.yaml))

        upload_shell = os.path.join(pro_dir, "upload.sh")
        oss_path = get_oss_path(contract_number)
        msn = "hello, %s 的 上传已完成，路径为 %s ."%(contract_number, oss_path)
        talk = ding_talk(msn, self.analyst_phone_number)
        fail_msn = "hello, %s 的 上传失败! 路径为 %s ."%(contract_number, oss_path)
        fail_talk = ding_talk(fail_msn, self.analyst_phone_number)
        with open(upload_shell,"w") as f:
            f.write("""
cd %s

%s/script/DataRelease.py --yaml %s --odir %s/Upload/ && \\

python3 -m excelParse.upload -i %s/Upload/ -o %s 

if [ $? -eq 0 ];
then
#DingTalk
%s
else
#Fail DingTalk
%s
fi

""" %(pro_dir,
        pipe_dir, self.yaml, pro_dir,
        pro_dir , oss_path,
        talk,
        fail_talk))

        # 打印运行命令
        msn = "\n\033[34m%s\033[0m 的shell脚本已生成。shell脚本路径为: \033[34m%s\033[0m .\n\n您可以选择运行以下命令：\n%s"%(contract_number, pro_dir , "\n".join(shells))
        print(msn)
