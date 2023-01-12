import datetime, os,shutil
import numpy as np
import pandas as pd
from importlib.resources import files
from random import choices, randrange, random
from pathlib import Path

pet_home = Path.home() / 'pet_home'
pet_home.mkdir(parents=True, exist_ok=True)
pet_desktop= Path.home() / 'Desktop/Python与数据分析及可视化教学案例'

def gen_iid(init=220151000, number=40):
    """ 生成从init起始的一批学号
    init:起始学号
    number:元素个数
    """
    init = 220151000 if not isinstance(init, int) else init
    return pd.Series(data=range(init, init + number))


def gen_name(xm, number=40):
    """ 生成姓名，
    xm=['姓字符串','名字字符串],若传入的是空字符串"",则生成默认姓名
    根据姓，名，生成n个假名字
    number:元素个数
    """
    xm = [
        '赵钱孙李周吴郑王冯陈褚蒋沈韩杨朱秦尤许何吕施刁张孔曹严华金魏陶姜戚谢邹喻柏窦章苏潘葛奚范彭郎鲁韦昌马苗方俞任袁柳',
        "群平风华正茂仁义礼智媛强天霸红和丽平世莉界中华正义伟岸茂盛繁望印树枝松涛圆一懿贵妃彭桂花民凤春卿玺波嬴政荣群智慧睿兴平风清扬自成世民嬴旺品网红丽文天学与翔斌霸学花文教学忠谋书"
    ] if not isinstance(xm, (list, tuple)) else xm

    names = ["".join(choices(xm[0], k=1) + choices(xm[1], k=randrange(1, 3))) for _ in range(number)]
    return pd.Series(names)


def gen_int_series(int_range_lst=[0, 100], name='mark', number=40):
    '''  生成整数随机series
       int_range_lst：[start，end]
        记录条数：number
    '''
    int_range_lst = [0, 100] if not isinstance(int_range_lst, (list, tuple)) else int_range_lst
    low, high = int_range_lst
    return pd.Series(np.random.randint(low, high, number), name=name)


def gen_float_series(float_range_lst=[0, 100, 2], name='mark', number=40):
    '''  生成浮点数 series
        float_range_lst：[start，end，length] ，length:小数点的位数
        记录条数：number

    '''
    float_range_lst = [0, 100, 2] if not isinstance(float_range_lst, (list, tuple)) else float_range_lst
    low, high, length = float_range_lst
    out = map(lambda x: round(x, length), (np.random.rand(number) * (high - low) + low))
    return pd.Series(out, name=name)


def gen_date_time_series(period=['2020-2-24 00:00:00', '2022-12-31 00:00:00'], number=40, frmt="%Y-%m-%d %H:%M:%S"):
    '''
    print(gen_date_time_series('2022-1-01 07:00:00', '2020-11-01 09:00:00', 10))
    随机生成某一时间段内的日期,时刻：
    :param start: 起始时间
    :param end:   结束时间
    :param number: 记录数
    :param frmt: 格式
    :return: series
    '''
    period = ['2020-2-24 00:00:00', '2022-12-31 00:00:00'] if not isinstance(period, (list, tuple)) else period
    start, end = period
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    time_datetime = [random() * (etime - stime) + stime for _ in range(number)]
    time_str = [t.strftime(frmt) for t in time_datetime]
    return pd.Series(time_str)


def gen_date_series(date_period=['2020-2-24', '2024-12-31'], number=40, frmt="%Y-%m-%d"):
    '''
    随机生成某一时间段内的日期：
    print(gen_date_time_series('2022-1-01', '2020-11-01', 10))
     :param start: 起始时间
    :param end:   结束时间
    :param number: 记录数
    :param frmt: 格式
    :return: series
    '''
    date_period = ['2020-2-24', '2024-12-31'] if not isinstance(date_period, (list, tuple)) else date_period
    return gen_date_time_series(date_period, number, frmt="%Y-%m-%d")


def gen_time_series(time_period=['00:00:00', '23:59:59'], number=40, frmt="%H:%M:%S"):
    '''
    随机生成某一时间段内的时刻：
    print(gen_time_series('07:00:00', '12:00:00', 10))
     :param start: 起始时间
    :param end:   结束时间
    :param number: 记录数
    :param frmt: 格式
    :return: series
    '''
    time_period = ['00:00:00', '23:59:59'] if not isinstance(time_period, (list, tuple)) else time_period
    return gen_date_time_series(time_period, number, frmt="%H:%M:%S")


def gen_category_series(lst, number=40):
    '''  生成category数据 series
        lst:可选数据列表
        记录条数：number

    '''

    return pd.Series(np.random.choice(lst, size=number))


'''
对上述函数做简化名称，目的为了选择解析模板数据后调用函数名称。自动实现一一对应。
'''

func_dict={
    'iid':gen_iid,
    'n':gen_name,
    'i':gen_int_series,
    'f':gen_float_series,
    'd':gen_date_series,
    't':gen_time_series,
    'dt':gen_date_time_series,
    'c':gen_category_series

}


sample_order = {

    '学号.iid': 220151000,
    '考号.i': [151000, 789000],
    '姓名.n': '',  # ""生成默认的随机名字，也可以设置姓名字符串，['赵钱孙李','微甜地平天下'],
    '性别.c': ['男', '女'],
    '报名时间.d': ['2016-1-1', '2021-12-31'],
    '录入时间.t': ['00:00:00', '23:59:59'],
    '年龄.i': [18, 34],
    '政治面貌.c': ['中共',  '群众', '民革', '九三'],
    '专业.c': ['计算机科学与技术', '人工智能', '软件工程', '自动控制', '机械制造', '自动控制'],
    '学校.c': ['清华大学', '北京大学', '复旦大学', '上海交通大学', '华东理工大学','中山大学','上海师范大学', '中国科技大学', '上海大学'],
    '政治成绩.i': [36, 100],
    '英语成绩.i': [29, 100],
    '英语类别.c': ['英语一', '英语二'],
    '数学成绩.i': (40, 150),
    '数学类别.c': ['数学一', '数学二', '数学三'],
    '专业课成绩.i': [55, 150],
    '六级证书.c': ['是','否'],
    '在线时长.f': (1000.3, 9999.55, 2)
}


def add_noise(df, noise=0.1, repeat=2) -> pd.DataFrame:
    '''
    对 DataFrame加入噪声，非法数据
    :param df:
    :return:
    '''
    scope_n = int(df.shape[0]*df.shape[1])
    noise_n = int(scope_n * noise)
    df = pd.concat([df] * repeat)
    df = df.sample(frac=1 / repeat).reset_index(drop=True)

    for i in df.columns:
        df[i] = df[i].apply(lambda x: None if np.random.randint(1, scope_n) in range(noise_n) else x)

    return df


def generator(order: dict = sample_order,
              number: int = 40,
              dst: str = f'{pet_home}/generated_dataset_{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.xlsx',
              noise: float = 0,
              repeat: int = 1):
    '''
    根据订单生成数据
    :param order: 订单字典
    :param number: 数据元素个数
    :return:
    订单字典格式：
    sample_order = {

    '学号.iid': 220151000,
    '考号.i': [151000, 789000],
    '姓名.n': '',  # ""生成默认的随机名字，也可以设置姓名字符串，['赵钱孙李','微甜地平天下'],
    '性别.c': ['男', '女'],
    '日期.d': ['2020-2-24', '2024-12-31'],
    '时间.t': ['00:00:00', '23:59:59'],
    '年龄.i': [18, 24],
    '政治面貌.c': ['党员', '团员', '群众'],
    '专业.c': ['计算机科学与技术', '人工智能', '软件工程', '自动控制', '机械制造', '自动控制'],
    '学校.c': ['清华大学', '北京大学', '复旦大学', '上海交通大学', '上海师范大学', '中国科技大学', '上海大学'],
    '政治.i': [19, 100],
    '英语.i': [29, 100],
    '英语类别.c': ['英语一', '英语二'],
    '高等数学.i': [30, 140],
    '数学类别.c': ['数学一', '数学二', '数学三'],
    '专业课.i': [30, 150],
    '净收入.f': [30.3, 150.55, 3],
}

   func_dict={
    'iid':gen_iid,
    'n':gen_name,
    'i':gen_int_series,
    'f':gen_float_series,
    'd':gen_date_series,
    't':gen_time_series,
    'dt':gen_date_time_series,
    'c':gen_category_series

}



    '''
    df = pd.DataFrame()
    for k, v in order.items():
        na, func = k.split('.')
        #df[na] = eval(func)(v, number=number)
        df[na] = func_dict[func](v, number=number)
    if noise > 0.0:
        df = add_noise(df, noise=noise, repeat=repeat)
    df.to_excel(dst, index=None)
    print(f'Dataset is generated in {dst} ！！！')

    return df


def gen_sample_series(number: int = 40,
                      dst=f'{pet_home}/generated_sample_series_{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.xlsx',
                      noise=0,
                      repeat=1):
    order = {
        '姓名.n': '',  # ""生成默认的随机名字，也可以设置姓名字符串，['赵钱孙李','微甜地平天下'],
        '成绩.i': ''
    }
    df = generator(order, number, dst)
    df = pd.concat([df] * repeat)
    df = df.sample(frac=1 / repeat).reset_index(drop=True)

    df.set_index(df['姓名'], inplace=True)
    df['成绩'] = df['成绩'].apply(lambda x: None if np.random.randint(1, len(df)) in range(int(noise * len(df))) else x)

    return df['成绩']


def gen_sample_dataframe(sample_order=sample_order,
                         number: int = 40,
                         dst=f'{pet_home}/generated_sample_dataframe_{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.xlsx',
                         noise=0,
                         repeat=1):
    print('*' * number)
    from pprint import pprint
    print('订单格式：')
    pprint(sample_order)
    print("*" * number)
    os.startfile(pet_home)
    return generator(order=sample_order, number=number, dst=dst, noise=noise, repeat=repeat)


def show_order_sample():
    from pprint import pprint
    pprint(sample_order)


'''

def add_noise(df) -> pd.DataFrame:
   
    for i in df.columns:
        df[i] = df[i].apply(lambda x: None if np.random.randint(1, 12) == 2 else x)

    return df
'''
datafile_dict = {
    'ip地址分类': 'ip_address.xlsx',
    '研究生初试成绩': 'st.xlsx',
    '上海地铁线路': 'subway.xlsx',
    '北京公交车': 'beijing_bus.xlsx',
    '通识课': '2022tsk.xlsx',
    '优秀毕业论文': '2022pst.xlsx',
    '太乙金华宗旨': 'tyjhzz.txt',
    '微信接龙投票': 'votes.txt',
    'cookie样例': 'sample_cookies.txt',
    '道德经': 'ddj.txt',
    '双色球': 'ssq_22134.xlsx'
}


def get_datasets_list():
    return datafile_dict.keys()


def load_data(key='道德经',prompt=True):
    #默认提示 数据集可选项
    print(f'可选数据集: {get_datasets_list()}') if prompt else print('-'*20)
    file_name = datafile_dict.get(key, "ddj.txt")
    data_file = files('pet.datasets.database').joinpath(file_name)

    if file_name.split('.')[-1] == 'xlsx':
        return pd.read_excel(data_file)

    elif file_name.split('.')[-1] == 'txt':
        return open(data_file, encoding="UTF-8").read().replace('\n', '')

    elif file_name.split('.')[-1] == 'csv':
        return pd.read_csv(data_file)

    else:
        '''
        如果文件名非法，则默认线上《道德经》
        '''
        print('目前仅支持 txt，xlsx，csv 文件类型')
        f = files('pet.datasets.database.ddj.txt')
        return open(data_file, encoding="UTF-8").read()


def download_textbook1(dst=pet_desktop):
    src = files('pet.textbook1')
    print('Please wait....')
    shutil.copytree(src, dst, dirs_exist_ok=True)
    print('done!!')
    os.startfile(dst)


if __name__ == '__main__':
    df = gen_sample_dataframe(number=500, noise=.08, repeat=2)
    print(df)

    #print(gen_sample_series(number=30, noise=0.1, repeat=2))

    print(gen_sample_series())
