###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
""" Collection of user jobs for testing purposes
"""
import os
import time
import errno

from DIRAC import rootPath
from DIRAC.DataManagementSystem.Utilities.DMSHelpers import DMSHelpers
from DIRAC.tests.Utilities.testJobDefinitions import baseToAllJobs, endOfAllJobs, find_all
from DIRAC.Core.Utilities.Proxy import executeWithUserProxy
from LHCbDIRAC.Interfaces.API.LHCbJob import LHCbJob
from LHCbDIRAC.Interfaces.API.DiracLHCb import DiracLHCb
from LHCbDIRAC.tests.Workflow import createJob

# parameters

jobClass = LHCbJob
diracClass = DiracLHCb

try:
    tier1s = DMSHelpers().getTiers(tier=(0, 1))
except AttributeError:
    tier1s = [
        "LCG.CERN.cern",
        "LCG.CNAF.it",
        "LCG.GRIDKA.de",
        "LCG.IN2P3.fr",
        "LCG.NIKHEF.nl",
        "LCG.PIC.es",
        "LCG.RAL.uk",
        "LCG.RRCKI.ru",
        "LCG.SARA.nl",
    ]

# List of jobs
wdir = os.getcwd()


@executeWithUserProxy
def helloWorldTestT2s():

    job = baseToAllJobs("helloWorldTestT2s", jobClass)
    job.setInputSandbox([find_all("exe-script.py", rootPath, ".")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setBannedSites(tier1s)
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestCERN():

    job = baseToAllJobs("helloWorld-test-CERN", jobClass)
    job.setInputSandbox([find_all("exe-script.py", rootPath, ".")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination("LCG.CERN.cern")
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestIN2P3():
    job = baseToAllJobs("helloWorld-test-IN2P3", jobClass)
    job.setInputSandbox([find_all("exe-script.py", rootPath, ".")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination("LCG.IN2P3.fr")
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestGRIDKA():
    job = baseToAllJobs("helloWorld-test-GRIDKA", jobClass)
    job.setInputSandbox([find_all("exe-script.py", rootPath, ".")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination("LCG.GRIDKA.de")
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestARC():

    job = baseToAllJobs("helloWorld-test-ARC", jobClass)
    job.setInputSandbox([find_all("exe-script.py", rootPath, ".")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination(["LCG.RAL.uk"])
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestSSHCondor():

    job = baseToAllJobs("helloWorld-test-SSHCondor", jobClass)
    job.setInputSandbox([find_all("exe-script.py", rootPath, ".")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination(["DIRAC.Sibir.ru"])
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestCLOUD():

    job = baseToAllJobs("helloWorld-test-CLOUD", jobClass)
    job.setInputSandbox([find_all("exe-script.py", rootPath, ".")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setDestination(["CLOUD.CERN.cern"])
    return endOfAllJobs(job)


@executeWithUserProxy
def helloWorldTestCentos7():

    job = baseToAllJobs("helloWorld-test-CentOS7", jobClass)
    job.setInputSandbox([find_all("exe-script.py", rootPath, ".")[0]])
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setPlatform("x86_64-centos7-gcc9-opt")
    return endOfAllJobs(job)


@executeWithUserProxy
def jobWithOutput():

    timenow = time.strftime("%s")
    with open(os.path.join(wdir, timenow + "testFileUpload.txt"), "w") as f:
        f.write(timenow)
    inp1 = [find_all(timenow + "testFileUpload.txt", ".")[0]]
    inp2 = [find_all("exe-script.py", rootPath, ".")[0]]
    job = baseToAllJobs("jobWithOutput", jobClass)
    job.setInputSandbox(inp1 + inp2)
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setOutputData([timenow + "testFileUpload.txt"])
    res = endOfAllJobs(job)
    try:
        os.remove(os.path.join(wdir, timenow + "testFileUpload.txt"))
    except OSError as e:
        return e.errno == errno.ENOENT
    return res


@executeWithUserProxy
def jobWithOutputAndPrepend():

    timenow = time.strftime("%s")
    with open(os.path.join(wdir, timenow + "testFileUploadNewPath.txt"), "w") as f:
        f.write(timenow)
    job = baseToAllJobs("jobWithOutputAndPrepend", jobClass)
    inp1 = [find_all(timenow + "testFileUploadNewPath.txt", ".")[0]]
    inp2 = [find_all("exe-script.py", rootPath, ".")[0]]
    job.setInputSandbox(inp1 + inp2)
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setOutputData([timenow + "testFileUploadNewPath.txt"], filePrepend="testFilePrepend")
    res = endOfAllJobs(job)
    try:
        os.remove(os.path.join(wdir, timenow + "testFileUploadNewPath.txt"))
    except OSError as e:
        return e.errno == errno.ENOENT
    return res


@executeWithUserProxy
def jobWithOutputAndPrependWithUnderscore():

    timenow = time.strftime("%s")
    with open(os.path.join(wdir, timenow + "testFileUpload_NewPath.txt"), "w") as f:
        f.write(timenow)
    job = baseToAllJobs("jobWithOutputAndPrependWithUnderscore", jobClass)
    inp1 = [find_all(timenow + "testFileUpload_NewPath.txt", ".")[0]]
    inp2 = [find_all("exe-script.py", rootPath, ".")[0]]
    job.setInputSandbox(inp1 + inp2)
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    res = job.setOutputData([timenow + "testFileUpload_NewPath.txt"], filePrepend="testFilePrepend")
    if not res["OK"]:
        return 0
    res = endOfAllJobs(job)
    try:
        os.remove(os.path.join(wdir, timenow + "testFileUpload_NewPath.txt"))
    except OSError as e:
        return e.errno == errno.ENOENT
    return res


@executeWithUserProxy
def jobWithOutputAndReplication():

    timenow = time.strftime("%s")
    with open(os.path.join(wdir, timenow + "testFileReplication.txt"), "w") as f:
        f.write(timenow)
    job = baseToAllJobs("jobWithOutputAndReplication", jobClass)
    inp1 = [find_all(timenow + "testFileReplication.txt", ".")[0]]
    inp2 = [find_all("exe-script.py", rootPath, ".")[0]]
    job.setInputSandbox(inp1 + inp2)
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setOutputData([timenow + "testFileReplication.txt"], replicate="True")
    res = endOfAllJobs(job)
    try:
        os.remove(os.path.join(wdir, timenow + "testFileReplication.txt"))
    except OSError as e:
        return e.errno == errno.ENOENT
    return res


@executeWithUserProxy
def jobWith2OutputsToBannedSE():

    timenow = time.strftime("%s")
    with open(os.path.join(wdir, timenow + "testFileUploadBanned-1.txt"), "w") as f:
        f.write(timenow)
    with open(os.path.join(wdir, timenow + "testFileUploadBanned-2.txt"), "w") as f:
        f.write(timenow)
    job = baseToAllJobs("jobWith2OutputsToBannedSE", jobClass)
    inp1 = [find_all(timenow + "testFileUploadBanned-1.txt", ".")[0]]
    inp2 = [find_all(timenow + "testFileUploadBanned-2.txt", ".")[0]]
    inp3 = [find_all("exe-script.py", rootPath, ".")[0]]
    inp4 = [find_all("partialConfig.cfg", "..", ".")[0]]
    job.setInputSandbox(inp1 + inp2 + inp3 + inp4)
    job.setExecutable("exe-script.py", "", "helloWorld.log")
    job.setConfigArgs("partialConfig.cfg")
    job.setDestination("LCG.PIC.es")
    job.setOutputData(
        [timenow + "testFileUploadBanned-1.txt", timenow + "testFileUploadBanned-2.txt"], OutputSE=["PIC-USER"]
    )
    res = endOfAllJobs(job)
    try:
        os.remove(os.path.join(wdir, timenow + "testFileUploadBanned-1.txt"))
    except OSError as e:
        return e.errno == errno.ENOENT
    try:
        os.remove(os.path.join(wdir, timenow + "testFileUploadBanned-2.txt"))
    except OSError as e:
        return e.errno == errno.ENOENT
    return res


@executeWithUserProxy
def jobWithSingleInputData():

    job = baseToAllJobs("jobWithSingleInputData-shouldGoToCERN", jobClass)
    job.setInputSandbox([find_all("exe-script-with-input-single-location.py", "..", ".")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("download")
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataCERN():

    job = baseToAllJobs("jobWithSingleInputDataCERN-shouldSucceed", jobClass)
    job.setInputSandbox([find_all("exe-script-with-input-single-location.py", "..", ".")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("download")
    job.setDestination(["LCG.CERN.cern"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataRAL():

    job = baseToAllJobs("jobWithSingleInputDataRAL-shouldFailOptimizers", jobClass)
    job.setInputSandbox([find_all("exe-script-with-input-single-location.py", "..", ".")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("protocol")
    job.setDestination(["LCG.RAL.uk"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataIN2P3():

    job = baseToAllJobs("jobWithSingleInputDataIN2P3-shouldFailOptimizers", jobClass)
    job.setInputSandbox([find_all("exe-script-with-input-single-location.py", "..", ".")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("protocol")
    job.setDestination(["LCG.IN2P3.fr"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataRRCKI():

    job = baseToAllJobs("jobWithSingleInputDataRRCKI-shouldFailOptimizers", jobClass)
    job.setInputSandbox([find_all("exe-script-with-input-single-location.py", "..", ".")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("protocol")
    job.setDestination(["LCG.RRCKI.ru"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataSARA():

    job = baseToAllJobs("jobWithSingleInputDataSARA-shouldFailOptimizers", jobClass)
    job.setInputSandbox([find_all("exe-script-with-input-single-location.py", "..", ".")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("protocol")
    job.setDestination(["LCG.SARA.nl"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataPIC():

    job = baseToAllJobs("jobWithSingleInputDataPIC-shouldFailOptimizers", jobClass)
    job.setInputSandbox([find_all("exe-script-with-input-single-location.py", "..", ".")[0]])
    job.setExecutable("exe-script-with-input-single-location.py", "", "exeWithInput.log")
    # this file should be at CERN-USER only
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFileSingleLocation.txt")
    job.setInputDataPolicy("protocol")
    job.setDestination(["LCG.PIC.es"])
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithSingleInputDataSpreaded():

    job = baseToAllJobs("jobWithSingleInputDataSpreaded", jobClass)
    job.setInputSandbox([find_all("exe-script-with-input.py", "..", ".")[0]])
    job.setExecutable("exe-script-with-input.py", "", "exeWithInput.log")
    # this file should be at CERN-USER and IN2P3-USER
    job.setInputData("/lhcb/user/f/fstagni/test/testInputFile.txt")
    job.setInputDataPolicy("download")
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def jobWithInputDataAndAncestor():

    job = baseToAllJobs("jobWithInputDataAndAncestor", jobClass)
    job.setInputSandbox([find_all("exe-script-with-input-and-ancestor.py", "..", ".")[0]])
    job.setExecutable("exe-script-with-input-and-ancestor.py", "", "exeWithInput.log")
    # WARNING: Collision10!!
    job.setInputData("/lhcb/data/2010/SDST/00008375/0005/00008375_00053941_1.sdst")  # this file should be at SARA-RDST
    # the ancestor should be /lhcb/data/2010/RAW/FULL/LHCb/COLLISION10/81616/081616_0000000213.raw (CERN and SARA)
    job.setAncestorDepth(1)  # pylint: disable=no-member
    job.setInputDataPolicy("download")
    res = endOfAllJobs(job)
    return res


@executeWithUserProxy
def gaussMPJob():

    job = baseToAllJobs("GaussMP_v54r3", jobClass)

    job.setInputSandbox([find_all("prodConf_Gauss_MP_test.py", "..", ".")[0]])
    job.setOutputSandbox("Gauss_MP_test.sim")

    options = "$APPCONFIGOPTS/Gauss/Beam7000GeV-mu100-nu7.6-HorExtAngle.py;"
    options += "$APPCONFIGOPTS/Gauss/EnableSpillover-25ns.py;"
    options += "$DECFILESROOT/options/12143001.py;"
    options += "$LBPYTHIA8ROOT/options/Pythia8.py;"
    options += "$APPCONFIGOPTS/Gauss/Gauss-Upgrade-Baseline-20150522.py;"
    options += "$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmOpt2.py;"
    options += "$APPCONFIGOPTS/Gauss/GaussMPpatch20200701.py;"
    options += "$APPCONFIGOPTS/Persistency/Compression-LZMA-4.py"

    job.setApplication(
        "Gauss",
        "v54r3",
        options,  # pylint: disable=no-member
        extraPackages="AppConfig.v3r400;Gen/DecFiles.v30r42;ProdConf.v3r0",
        systemConfig="x86_64-centos7-gcc9-opt",
    )
    job.setDIRACPlatform()  # pylint: disable=no-member
    job.setCPUTime(172800)
    job.setNumberOfProcessors(4)

    return endOfAllJobs(job)
