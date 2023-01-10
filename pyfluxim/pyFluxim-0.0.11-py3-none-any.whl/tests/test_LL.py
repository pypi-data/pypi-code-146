from pyFluxim import LL
import numpy as np
import matplotlib.pyplot as plt


def test_getStartStopData():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PSC9"
    result_id = 0
    start_stop = A.getStartStopData(sample_name, result_id)
    assert list(start_stop.keys())[0] == 'Sample holder climate : temperature'

def test_getSampleList():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sl = A.getSampleList()
    assert len(sl) == 9

def test_getResultTimestamp():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PSC9"
    result_id = 0
    st_raw = A.getResultTimestamp(sample_name, result_id, raw=True)
    st_nraw = A.getResultTimestamp(sample_name, result_id, raw=False)
    assert type(st_raw) == str and type(st_nraw) == float

def test_getSampleList():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sl = A.getSampleList()
    assert len(sl) == 9 and sl[0] == {'name': 'PSC9', 'devices': 3, 'sampleID': 7}

def test_getResultStartTime():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PSC9"
    result_id = 0
    t0 = A.getResultStartTime(sample_name, result_id)
    assert str(t0) == '2022-11-16 13:27:11'

def test_getResultsIndicesByType():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PSC9"
    res_CV = A.getResultsIndicesByType(sample_name, 'CV')
    assert len(res_CV) == 46

def test_getResultsTypes():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PSC9"
    r_hr = A.getResultsTypes(sample_name, hr=True)
    r_nhr = A.getResultsTypes(sample_name, hr=False)
    assert type(r_hr[0]) == str and type(r_nhr[0]) == int

def test_listSensors():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PSC9"
    result_id = 0
    sl = A.listSensors(sample_name, result_id)
    assert sl[0][0] == 'IR temperature [0]'

def test_getSensorResultByName():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PSC9"
    result_id = 0
    sr = A.getSensorResultByName(sample_name, result_id, 'IR temperature [0]')
    assert sr['data'][0] == np.float32(309.84) and sr['data'][20] == np.float32(310.48)

def test_getDevices():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PSC9"
    dev = A.getDevices(sample_name)
    assert dev[0]['sampleID'] == 7

def test_getMeasurements():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    meas = A.getMeasurements()
    assert len(meas) == 94

def test_getResult():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PSC9"
    result_id = 0
    pixel_id = 0
    res = A.getResult(sample_name, pixel_id, result_id)
    ls = ['type', 't', 'voltage', 'current', 'start_time']
    assert list(res.keys()) == ls and res['current'][-1] == np.float32(-6.574143e-07)

def test_getResultData():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PSC9"
    result_id = 0
    res = A.getResultData(sample_name, result_id)
    assert res['Light intensity']['start'] == np.float32(100.0)

def test_plotJVparams():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PHD1"
    pixel_id = 1

    exp_list = ['MPP', 'FF', 'Voc', 'Isc', 'Vmpp', 'Impp']
    axis = plt.gca()
    for exp in exp_list:
        res = A.plotJVparams(sample_name, pixel_id)
        assert type(res) == type(axis)

def test_getJVparams():
    path = r'C:\Users\Paios\Desktop\pyfluxim_test\data_test.lls'
    A = LL.Result(path)
    sample_name = "PHD1"
    pixel_id = 1
    params = A.getJVparams(sample_name, pixel_id)
    assert params[1]['up']['MPP'][-1][0] == np.float32(-6.173304e-05)
