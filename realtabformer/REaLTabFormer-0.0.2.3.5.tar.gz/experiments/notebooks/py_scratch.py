# >>> samples = rtf_model.sample(n_samples=1000, device="cpu")
#   0%|                                                                                                                                                                                                                                                     | 0/1000 [00:01<?, ?it/s]
# Traceback (most recent call last):
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3803, in get_loc
#     return self._engine.get_loc(casted_key)
#   File "pandas/_libs/index.pyx", line 138, in pandas._libs.index.IndexEngine.get_loc
#   File "pandas/_libs/index.pyx", line 165, in pandas._libs.index.IndexEngine.get_loc
#   File "pandas/_libs/hashtable_class_helper.pxi", line 5745, in pandas._libs.hashtable.PyObjectHashTable.get_item
#   File "pandas/_libs/hashtable_class_helper.pxi", line 5753, in pandas._libs.hashtable.PyObjectHashTable.get_item
# KeyError: 0

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/realtabformer/rtf_sampler.py", line 106, in _convert_to_table
#     series = synth_df[c]
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/frame.py", line 3805, in __getitem__
#     indexer = self.columns.get_loc(key)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3805, in get_loc
#     raise KeyError(key) from err
# KeyError: 0

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3803, in get_loc
#     return self._engine.get_loc(casted_key)
#   File "pandas/_libs/index.pyx", line 138, in pandas._libs.index.IndexEngine.get_loc
#   File "pandas/_libs/index.pyx", line 165, in pandas._libs.index.IndexEngine.get_loc
#   File "pandas/_libs/hashtable_class_helper.pxi", line 5745, in pandas._libs.hashtable.PyObjectHashTable.get_item
#   File "pandas/_libs/hashtable_class_helper.pxi", line 5753, in pandas._libs.hashtable.PyObjectHashTable.get_item
# KeyError: 0

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/realtabformer/realtabformer.py", line 610, in sample
#     synth_df = tabular_sampler.sample_tabular(
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/realtabformer/rtf_sampler.py", line 517, in sample_tabular
#     synth_sample = self._processes_sample(
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/realtabformer/rtf_sampler.py", line 374, in _processes_sample
#     synth_df = self._convert_to_table(synth_df)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/realtabformer/rtf_sampler.py", line 147, in _convert_to_table
#     _synth_df.append(synth_df[c])
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/frame.py", line 3805, in __getitem__
#     indexer = self.columns.get_loc(key)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3805, in get_loc
#     raise KeyError(key) from err
# KeyError: 0
# >>> df.head()
#    0                  1       2           3   4                    5                   6               7       8        9     10  11  12              13      14
# 0  39          State-gov   77516   Bachelors  13        Never-married        Adm-clerical   Not-in-family   White     Male  2174   0  40   United-States   <=50K
# 1  50   Self-emp-not-inc   83311   Bachelors  13   Married-civ-spouse     Exec-managerial         Husband   White     Male     0   0  13   United-States   <=50K
# 2  38            Private  215646     HS-grad   9             Divorced   Handlers-cleaners   Not-in-family   White     Male     0   0  40   United-States   <=50K
# 3  53            Private  234721        11th   7   Married-civ-spouse   Handlers-cleaners         Husband   Black     Male     0   0  40   United-States   <=50K
# 4  28            Private  338409   Bachelors  13   Married-civ-spouse      Prof-specialty            Wife   Black   Female     0   0  40            Cuba   <=50K
# >>> df.head().dtypes
# 0      int64
# 1     object
# 2      int64
# 3     object
# 4      int64
# 5     object
# 6     object
# 7     object
# 8     object
# 9     object
# 10     int64
# 11     int64
# 12     int64
# 13    object
# 14    object
# dtype: object
# >>> df.head().dtypes.index
# Int64Index([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], dtype='int64')
# >>> rtf_model.column_dtypes
# {0: 'int64', 1: 'object', 2: 'int64', 3: 'object', 4: 'int64', 5: 'object', 6: 'object', 7: 'object', 8: 'object', 9: 'object', 10: 'int64', 11: 'int64', 12: 'int64', 13: 'object', 14: 'object'}
# >>> rtf_model.processed_columns
# ['00___NUMERIC___0_00', '01___CATEGORICAL___1', '02___NUMERIC___2_00', '02___NUMERIC___2_01', '02___NUMERIC___2_02', '02___NUMERIC___2_03', '03___CATEGORICAL___3', '04___NUMERIC___4_00', '05___CATEGORICAL___5', '06___CATEGORICAL___6', '07___CATEGORICAL___7', '08___CATEGORICAL___8', '09___CATEGORICAL___9', '10___NUMERIC___10_00', '10___NUMERIC___10_01', '10___NUMERIC___10_02', '11___NUMERIC___11_00', '11___NUMERIC___11_01', '12___NUMERIC___12_00', '13___CATEGORICAL___13', '14___CATEGORICAL___14']
# >>> rtf_model.column_dtypes[0]
# 'int64'
# >>> rtf_model.column_dtypes = {str(i): j for i, j in rtf_model.column_dtypes.items()}
# >>> samples = rtf_model.sample(n_samples=1000, device="cpu")
#   0%|                                                                                                                                                                                                                                                     | 0/1000 [00:01<?, ?it/s]
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/realtabformer/realtabformer.py", line 610, in sample
#     synth_df = tabular_sampler.sample_tabular(
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/realtabformer/rtf_sampler.py", line 517, in sample_tabular
#     synth_sample = self._processes_sample(
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/realtabformer/rtf_sampler.py", line 375, in _processes_sample
#     synth_df = self._validate_missing(synth_df)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/realtabformer/rtf_sampler.py", line 395, in _validate_missing
#     return synth_df.dropna(subset=self.drop_na_cols)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/util/_decorators.py", line 331, in wrapper
#     return func(*args, **kwargs)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/frame.py", line 6558, in dropna
#     raise KeyError(np.array(subset)[check].tolist())
# KeyError: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# >>> rtf_model.drop_na_cols
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# >>> rtf_model.drop_na_cols = list(map(str, rtf_model.drop_na_cols))
# >>> samples = rtf_model.sample(n_samples=1000, device="cpu")
# 1024it [00:08, 114.81it/s]
# >>> samples.head()
#     0                  1       2         3  4                    5                   6               7       8        9     10  11  12              13      14
# 0  52   Self-emp-not-inc  163439   HS-grad  9   Married-civ-spouse               Sales            Wife   White   Female      0   0  15   United-States   <=50K
# 1  50            Private  154950   HS-grad  9   Married-civ-spouse     Exec-managerial         Husband   White     Male  15024   0  40   United-States    >50K
# 2  30            Private  172582      11th  7        Never-married   Handlers-cleaners   Not-in-family   Black     Male      0   0  40   United-States   <=50K
# 3  36   Self-emp-not-inc  207802   HS-grad  9             Divorced    Transport-moving   Not-in-family   White     Male      0   0  35   United-States   <=50K
# 4  28            Private  205374   HS-grad  9        Never-married   Machine-op-inspct       Own-child   White   Female      0   0  35   United-States   <=50K
# >>> test_df = pd.read_csv("adult.test")
# >>> test_df.head()
#                                                                                                                                 |1x3 Cross validator
# 25  Private   226802  11th         7   Never-married       Machine-op-inspct  Own-child  Black  Male   0    0 40  United-States               <=50K.
# 38  Private   89814   HS-grad      9   Married-civ-spouse  Farming-fishing    Husband    White  Male   0    0 50  United-States               <=50K.
# 28  Local-gov 336951  Assoc-acdm   12  Married-civ-spouse  Protective-serv    Husband    White  Male   0    0 40  United-States                >50K.
# 44  Private   160323  Some-college 10  Married-civ-spouse  Machine-op-inspct  Husband    Black  Male   7688 0 40  United-States                >50K.
# 18  ?         103497  Some-college 10  Never-married       ?                  Own-child  White  Female 0    0 30  United-States               <=50K.
# >>> test_df = pd.read_csv("adult.test", header=1)
# >>> test_df.head()
#    25     Private   226802           11th   7        Never-married   Machine-op-inspct       Own-child   Black     Male     0   0.1   40   United-States   <=50K.
# 0  38     Private    89814        HS-grad   9   Married-civ-spouse     Farming-fishing         Husband   White     Male     0     0   50   United-States   <=50K.
# 1  28   Local-gov   336951     Assoc-acdm  12   Married-civ-spouse     Protective-serv         Husband   White     Male     0     0   40   United-States    >50K.
# 2  44     Private   160323   Some-college  10   Married-civ-spouse   Machine-op-inspct         Husband   Black     Male  7688     0   40   United-States    >50K.
# 3  18           ?   103497   Some-college  10        Never-married                   ?       Own-child   White   Female     0     0   30   United-States   <=50K.
# 4  34     Private   198693           10th   6        Never-married       Other-service   Not-in-family   White     Male     0     0   30   United-States   <=50K.
# >>> test_df = pd.read_csv("adult.test", header=None)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/util/_decorators.py", line 211, in wrapper
#     return func(*args, **kwargs)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/util/_decorators.py", line 331, in wrapper
#     return func(*args, **kwargs)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/io/parsers/readers.py", line 950, in read_csv
#     return _read(filepath_or_buffer, kwds)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/io/parsers/readers.py", line 611, in _read
#     return parser.read(nrows)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/io/parsers/readers.py", line 1778, in read
#     ) = self._engine.read(  # type: ignore[attr-defined]
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/io/parsers/c_parser_wrapper.py", line 230, in read
#     chunks = self._reader.read_low_memory(nrows)
#   File "pandas/_libs/parsers.pyx", line 808, in pandas._libs.parsers.TextReader.read_low_memory
#   File "pandas/_libs/parsers.pyx", line 866, in pandas._libs.parsers.TextReader._read_rows
#   File "pandas/_libs/parsers.pyx", line 852, in pandas._libs.parsers.TextReader._tokenize_rows
#   File "pandas/_libs/parsers.pyx", line 1973, in pandas._libs.parsers.raise_parser_error
# pandas.errors.ParserError: Error tokenizing data. C error: Expected 1 fields in line 2, saw 15

# >>> test_df = pd.read_csv("adult.test", header=None, skiprows=1)
# >>> test_df.head()
#    0           1       2              3   4                    5                   6           7       8        9     10  11  12              13       14
# 0  25     Private  226802           11th   7        Never-married   Machine-op-inspct   Own-child   Black     Male     0   0  40   United-States   <=50K.
# 1  38     Private   89814        HS-grad   9   Married-civ-spouse     Farming-fishing     Husband   White     Male     0   0  50   United-States   <=50K.
# 2  28   Local-gov  336951     Assoc-acdm  12   Married-civ-spouse     Protective-serv     Husband   White     Male     0   0  40   United-States    >50K.
# 3  44     Private  160323   Some-college  10   Married-civ-spouse   Machine-op-inspct     Husband   Black     Male  7688   0  40   United-States    >50K.
# 4  18           ?  103497   Some-college  10        Never-married                   ?   Own-child   White   Female     0   0  30   United-States   <=50K.
# >>> test_df[1].value_counts(normalize=True)
#  Private             0.688533
#  Self-emp-not-inc    0.081138
#  Local-gov           0.064062
#  ?                   0.059149
#  State-gov           0.041951
#  Self-emp-inc        0.035563
#  Federal-gov         0.028991
#  Without-pay         0.000430
#  Never-worked        0.000184
# Name: 1, dtype: float64
# >>> samples[1].value_counts(normalize=True)
# Traceback (most recent call last):
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3803, in get_loc
#     return self._engine.get_loc(casted_key)
#   File "pandas/_libs/index.pyx", line 138, in pandas._libs.index.IndexEngine.get_loc
#   File "pandas/_libs/index.pyx", line 165, in pandas._libs.index.IndexEngine.get_loc
#   File "pandas/_libs/hashtable_class_helper.pxi", line 5745, in pandas._libs.hashtable.PyObjectHashTable.get_item
#   File "pandas/_libs/hashtable_class_helper.pxi", line 5753, in pandas._libs.hashtable.PyObjectHashTable.get_item
# KeyError: 1

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/frame.py", line 3805, in __getitem__
#     indexer = self.columns.get_loc(key)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3805, in get_loc
#     raise KeyError(key) from err
# KeyError: 1
# >>> samples["1"].value_counts(normalize=True)
#  Private             0.751
#  Self-emp-not-inc    0.061
#  Local-gov           0.057
#  State-gov           0.042
#  ?                   0.039
#  Self-emp-inc        0.034
#  Federal-gov         0.016
# Name: 1, dtype: float64
# >>> df["1"].value_counts(normalize=True)
# Traceback (most recent call last):
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3803, in get_loc
#     return self._engine.get_loc(casted_key)
#   File "pandas/_libs/index.pyx", line 138, in pandas._libs.index.IndexEngine.get_loc
#   File "pandas/_libs/index.pyx", line 146, in pandas._libs.index.IndexEngine.get_loc
#   File "pandas/_libs/index_class_helper.pxi", line 49, in pandas._libs.index.Int64Engine._check_type
# KeyError: '1'

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/frame.py", line 3805, in __getitem__
#     indexer = self.columns.get_loc(key)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3805, in get_loc
#     raise KeyError(key) from err
# KeyError: '1'
# >>> df[1].value_counts(normalize=True)
#  Private             0.697030
#  Self-emp-not-inc    0.078038
#  Local-gov           0.064279
#  ?                   0.056386
#  State-gov           0.039864
#  Self-emp-inc        0.034274
#  Federal-gov         0.029483
#  Without-pay         0.000430
#  Never-worked        0.000215
# Name: 1, dtype: float64
# >>> test_df.shaoe
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/generic.py", line 5902, in __getattr__
#     return object.__getattribute__(self, name)
# AttributeError: 'DataFrame' object has no attribute 'shaoe'. Did you mean: 'shape'?
# >>> test_df.shape
# (16281, 15)
# >>> samples = rtf_model.sample(n_samples=test_df.shape[0], device="cpu")
# 16384it [02:21, 116.11it/s]
# >>> samples.head()
#     0         1       2              3   4                    5                   6               7       8        9  10  11  12              13      14
# 0  22   Private  314620   Some-college  10        Never-married        Adm-clerical       Own-child   White   Female   0   0  40   United-States   <=50K
# 1  38   Private  180686        HS-grad   9        Never-married       Other-service   Not-in-family   White     Male   0   0  60   United-States   <=50K
# 2  37   Private  228251   Some-college  10        Never-married        Craft-repair   Not-in-family   White     Male   0   0  40   United-States   <=50K
# 3  36   Private  105801     Assoc-acdm  12   Married-civ-spouse   Machine-op-inspct         Husband   White     Male   0   0  70   United-States    >50K
# 4  23   Private  196675      Bachelors  13        Never-married       Other-service       Own-child   Black   Female   0   0  20   United-States   <=50K
# >>> samples.columns = df.columns
# >>> samples[1].value_counts(normalize=True)
#  Private             0.729132
#  Self-emp-not-inc    0.069467
#  Local-gov           0.060561
#  ?                   0.046005
#  State-gov           0.038081
#  Self-emp-inc        0.029912
#  Federal-gov         0.026657
#  Without-pay         0.000184
# Name: 1, dtype: float64
# >>> df[1].value_counts(normalize=True)
#  Private             0.697030
#  Self-emp-not-inc    0.078038
#  Local-gov           0.064279
#  ?                   0.056386
#  State-gov           0.039864
#  Self-emp-inc        0.034274
#  Federal-gov         0.029483
#  Without-pay         0.000430
#  Never-worked        0.000215
# Name: 1, dtype: float64
# >>> test_df[1].value_counts(normalize=True)
#  Private             0.688533
#  Self-emp-not-inc    0.081138
#  Local-gov           0.064062
#  ?                   0.059149
#  State-gov           0.041951
#  Self-emp-inc        0.035563
#  Federal-gov         0.028991
#  Without-pay         0.000430
#  Never-worked        0.000184
# Name: 1, dtype: float64
# >>> col = 13
# >>> samples[col].value_counts(normalize=True)
#  United-States                 0.913212
#  Mexico                        0.019041
#  ?                             0.014803
#  Jamaica                       0.004791
#  Philippines                   0.004177
#  South                         0.003992
#  Germany                       0.003870
#  Puerto-Rico                   0.002887
#  China                         0.002580
#  Cuba                          0.002395
#  Canada                        0.002211
#  Italy                         0.002088
#  England                       0.001904
#  Columbia                      0.001781
#  Haiti                         0.001658
#  Vietnam                       0.001658
#  Guatemala                     0.001597
#  Japan                         0.001536
#  India                         0.001536
#  Iran                          0.001474
#  Poland                        0.001290
#  Taiwan                        0.001167
#  El-Salvador                   0.001044
#  Dominican-Republic            0.000921
#  France                        0.000798
#  Nicaragua                     0.000798
#  Ecuador                       0.000614
#  Thailand                      0.000491
#  Hungary                       0.000491
#  Portugal                      0.000430
#  Yugoslavia                    0.000430
#  Ireland                       0.000369
#  Trinadad&Tobago               0.000307
#  Hong                          0.000307
#  Greece                        0.000246
#  Outlying-US(Guam-USVI-etc)    0.000246
#  Honduras                      0.000246
#  Cambodia                      0.000184
#  Laos                          0.000184
#  Holand-Netherlands            0.000123
#  Scotland                      0.000123
# Name: 13, dtype: float64
# >>> df[col].value_counts(normalize=True)
#  United-States                 0.895857
#  Mexico                        0.019748
#  ?                             0.017905
#  Philippines                   0.006081
#  Germany                       0.004207
#  Canada                        0.003716
#  Puerto-Rico                   0.003501
#  El-Salvador                   0.003255
#  India                         0.003071
#  Cuba                          0.002918
#  England                       0.002764
#  Jamaica                       0.002488
#  South                         0.002457
#  China                         0.002303
#  Italy                         0.002242
#  Dominican-Republic            0.002150
#  Vietnam                       0.002058
#  Guatemala                     0.001966
#  Japan                         0.001904
#  Poland                        0.001843
#  Columbia                      0.001812
#  Taiwan                        0.001566
#  Haiti                         0.001351
#  Iran                          0.001321
#  Portugal                      0.001136
#  Nicaragua                     0.001044
#  Peru                          0.000952
#  France                        0.000891
#  Greece                        0.000891
#  Ecuador                       0.000860
#  Ireland                       0.000737
#  Hong                          0.000614
#  Cambodia                      0.000584
#  Trinadad&Tobago               0.000584
#  Laos                          0.000553
#  Thailand                      0.000553
#  Yugoslavia                    0.000491
#  Outlying-US(Guam-USVI-etc)    0.000430
#  Honduras                      0.000399
#  Hungary                       0.000399
#  Scotland                      0.000369
#  Holand-Netherlands            0.000031
# Name: 13, dtype: float64
# >>> test_df[col].value_counts(normalize=True)
#  United-States                 0.900559
#  Mexico                        0.018918
#  ?                             0.016829
#  Philippines                   0.005958
#  Puerto-Rico                   0.004299
#  Germany                       0.004238
#  Canada                        0.003747
#  India                         0.003132
#  El-Salvador                   0.003010
#  China                         0.002887
#  Cuba                          0.002641
#  England                       0.002273
#  South                         0.002150
#  Dominican-Republic            0.002027
#  Italy                         0.001965
#  Haiti                         0.001904
#  Portugal                      0.001843
#  Japan                         0.001843
#  Poland                        0.001658
#  Columbia                      0.001597
#  Jamaica                       0.001536
#  Guatemala                     0.001474
#  Greece                        0.001228
#  Vietnam                       0.001167
#  Ecuador                       0.001044
#  Iran                          0.000983
#  Peru                          0.000921
#  Nicaragua                     0.000921
#  Taiwan                        0.000860
#  Ireland                       0.000798
#  Thailand                      0.000737
#  Hong                          0.000614
#  Outlying-US(Guam-USVI-etc)    0.000553
#  France                        0.000553
#  Scotland                      0.000553
#  Cambodia                      0.000553
#  Trinadad&Tobago               0.000491
#  Yugoslavia                    0.000430
#  Honduras                      0.000430
#  Hungary                       0.000369
#  Laos                          0.000307
# Name: 13, dtype: float64
# >>> tr_df = df.sample(n=test_df.shape[0], random_state=1029, replace=False)
# >>> tr_df.head()
#        0         1       2              3   4                    5                  6                7       8        9   10  11  12              13      14
# 4306   30   Private   65278        HS-grad   9   Married-civ-spouse       Tech-support          Husband   White     Male   0   0  40   United-States    >50K
# 18718  40   Private  163455   Some-college  10   Married-civ-spouse       Tech-support          Husband   White     Male   0   0  55   United-States    >50K
# 27527  34   Private  173495   Some-college  10   Married-civ-spouse       Craft-repair          Husband   White     Male   0   0  48   United-States    >50K
# 24110  19   Private   87497           11th   7        Never-married   Transport-moving   Other-relative   White     Male   0   0  10   United-States   <=50K
# 7887   25   Private   34803      Bachelors  13        Never-married    Exec-managerial        Own-child   White   Female   0   0  20   United-States   <=50K
# >>> from sklearn.ensemble import RandomForestClassifier


# >>>
# >>>
# >>> rf = RandomForestClassifier()
# >>> rf
# RandomForestClassifier()
# >>> rf.fit(tr_df.drop(14, axis=1), tr_df[14])
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/ensemble/_forest.py", line 331, in fit
#     X, y = self._validate_data(
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/base.py", line 596, in _validate_data
#     X, y = check_X_y(X, y, **check_params)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/utils/validation.py", line 1074, in check_X_y
#     X = check_array(
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/utils/validation.py", line 856, in check_array
#     array = np.asarray(array, order=order, dtype=dtype)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/generic.py", line 2070, in __array__
#     return np.asarray(self._values, dtype=dtype)
# ValueError: could not convert string to float: ' Private'
# >>> from sklearn.preprocessing import LabelEncoder, OneHotEncoder
# >>> le = OneHotEncoder()
# >>> ohe = OneHotEncoder()
# >>> ohe.fit(tr_df)
# OneHotEncoder()
# >>> ohe.transform(tr_df)
# <16281x13302 sparse matrix of type '<class 'numpy.float64'>'
#         with 244215 stored elements in Compressed Sparse Row format>
# >>> ohe.transform(tr_df)[:10]
# <10x13302 sparse matrix of type '<class 'numpy.float64'>'
#         with 150 stored elements in Compressed Sparse Row format>
# >>> ohe.transform(tr_df)[:10].asarray()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/scipy/sparse/_base.py", line 771, in __getattr__
#     raise AttributeError(attr + " not found")
# AttributeError: asarray not found. Did you mean: 'toarray'?
# >>> ohe.transform(tr_df)[:10].toarray()
# array([[0., 0., 0., ..., 0., 0., 1.],
#        [0., 0., 0., ..., 0., 0., 1.],
#        [0., 0., 0., ..., 0., 0., 1.],
#        ...,
#        [0., 0., 0., ..., 0., 1., 0.],
#        [0., 0., 0., ..., 0., 1., 0.],
#        [0., 0., 0., ..., 0., 1., 0.]])
# >>> objects = tr_df.select_dtypes(include="object")
# >>> numeric = tr_df.select_dtypes(include=np.number))
#   File "<stdin>", line 1
#     numeric = tr_df.select_dtypes(include=np.number))
#                                                     ^
# SyntaxError: unmatched ')'
# >>> import numpy as np
# >>> numeric = tr_df.select_dtypes(include=np.number)
# >>> len(numeric.columns)
# 6
# >>> numeric.shape
# (16281, 6)
# >>> objects.shape
# (16281, 9)
# >>> df.shape
# (32561, 15)
# >>> objects = tr_df.drop(14, axis=1).select_dtypes(include="object")
# >>> objects
#                  1              3                    5                   6                7       8        9               13
# 4306        Private        HS-grad   Married-civ-spouse        Tech-support          Husband   White     Male   United-States
# 18718       Private   Some-college   Married-civ-spouse        Tech-support          Husband   White     Male   United-States
# 27527       Private   Some-college   Married-civ-spouse        Craft-repair          Husband   White     Male   United-States
# 24110       Private           11th        Never-married    Transport-moving   Other-relative   White     Male   United-States
# 7887        Private      Bachelors        Never-married     Exec-managerial        Own-child   White   Female   United-States
# ...             ...            ...                  ...                 ...              ...     ...      ...             ...
# 3324        Private        Masters              Widowed      Prof-specialty    Not-in-family   White   Female   United-States
# 20006       Private        HS-grad        Never-married   Machine-op-inspct        Unmarried   Black   Female   United-States
# 29899   Federal-gov   Some-college   Married-civ-spouse        Adm-clerical          Husband   White     Male   United-States
# 14072       Private   Some-college   Married-civ-spouse    Transport-moving          Husband   White     Male   United-States
# 10885       Private   Some-college        Never-married     Exec-managerial   Other-relative   Black   Female   United-States

# [16281 rows x 8 columns]
# >>> ohe = OneHotEncoder()
# >>> ohe.fit(objects)
# OneHotEncoder()
# >>> o_features = ohe.transform(objects)
# >>> features = np.concatenate([o_features, numeric.values], axis=1)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "<__array_function__ internals>", line 180, in concatenate
# ValueError: zero-dimensional arrays cannot be concatenated
# >>> numeric.values
# array([[    30,  65278,      9,      0,      0,     40],
#        [    40, 163455,     10,      0,      0,     55],
#        [    34, 173495,     10,      0,      0,     48],
#        ...,
#        [    42, 460214,     10,      0,      0,     40],
#        [    27, 183523,     10,      0,      0,     40],
#        [    23, 141264,     10,      0,      0,     40]])
# >>> o_features
# <16281x101 sparse matrix of type '<class 'numpy.float64'>'
#         with 130248 stored elements in Compressed Sparse Row format>
# >>> o_features.toarray()
# array([[0., 0., 0., ..., 1., 0., 0.],
#        [0., 0., 0., ..., 1., 0., 0.],
#        [0., 0., 0., ..., 1., 0., 0.],
#        ...,
#        [0., 1., 0., ..., 1., 0., 0.],
#        [0., 0., 0., ..., 1., 0., 0.],
#        [0., 0., 0., ..., 1., 0., 0.]])
# >>> features = np.concatenate([o_features.toarray(), numeric.values], axis=1)
# >>> features.shape
# (16281, 107)
# >>> s_features = np.concatenate([ohe.transform(samples[objects.columns]).toarray(), samples[numeric.columns].values], axis=1)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/preprocessing/_encoders.py", line 882, in transform
#     X_int, X_mask = self._transform(
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/preprocessing/_encoders.py", line 160, in _transform
#     raise ValueError(msg)
# ValueError: Found unknown categories [' Holand-Netherlands'] in column 7 during transform
# >>> ohe = OneHotEncoder(drop="first", handle_unknown="ignore")
# >>> ohe.fit(objects)
# OneHotEncoder(drop='first', handle_unknown='ignore')
# >>> features = np.concatenate([ohe.transform(tr_df[objects.columns]).toarray(), tr_df[numeric.columns].values], axis=1)
# >>> s_features = np.concatenate([ohe.transform(samples[objects.columns]).toarray(), samples[numeric.columns].values], axis=1)
# /Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/preprocessing/_encoders.py:188: UserWarning: Found unknown categories in columns [7] during transform. These unknown categories will be encoded as all zeros
#   warnings.warn(
# >>> d = pd.DataFrame(features)
# >>> d.shape
# (16281, 99)
# >>> s_features.shape
# (16281, 99)
# >>> d = pd.concat([d, s_features])
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/util/_decorators.py", line 331, in wrapper
#     return func(*args, **kwargs)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/reshape/concat.py", line 368, in concat
#     op = _Concatenator(
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/reshape/concat.py", line 458, in __init__
#     raise TypeError(msg)
# TypeError: cannot concatenate object of type '<class 'numpy.ndarray'>'; only Series and DataFrame objs are valid
# >>> d = pd.concat([d, pd.DataFrame(s_features)])
# >>> d.shape
# (32562, 99)
# >>> d.iloc[:16281].shape
# (16281, 99)
# >>> d.iloc[:16281, "label"] = 1
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexing.py", line 818, in __setitem__
#     iloc._setitem_with_indexer(indexer, value, self.name)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexing.py", line 1797, in _setitem_with_indexer
#     self._setitem_single_block(indexer, value, name)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexing.py", line 2078, in _setitem_single_block
#     self.obj._mgr = self.obj._mgr.setitem(indexer=indexer, value=value)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/internals/managers.py", line 393, in setitem
#     return self.apply("setitem", indexer=indexer, value=value)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/internals/managers.py", line 352, in apply
#     applied = getattr(b, f)(**kwargs)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/internals/blocks.py", line 986, in setitem
#     values[indexer] = casted
# IndexError: only integers, slices (`:`), ellipsis (`...`), numpy.newaxis (`None`) and integer or boolean arrays are valid indices
# >>> d["label"] = list(range(len(d))
# ... )
# >>> d.tail()
#          0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22  ...   77   78   79   80   81   82   83   84   85   86   87   88   89   90   91   92    93        94    95       96   97    98  label
# 16276  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  33.0  112841.0   9.0      0.0  0.0  45.0  32557
# 16277  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  42.0  108632.0  15.0  15024.0  0.0  38.0  32558
# 16278  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  38.0  165737.0  10.0      0.0  0.0  40.0  32559
# 16279  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  27.0  257294.0   9.0      0.0  0.0  38.0  32560
# 16280  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  59.0  443269.0   9.0      0.0  0.0  44.0  32561

# [5 rows x 100 columns]
# >>> d["label"] // samples.shape[0]
# 0        0
# 1        0
# 2        0
# 3        0
# 4        0
#         ..
# 16276    1
# 16277    1
# 16278    1
# 16279    1
# 16280    1
# Name: label, Length: 32562, dtype: int64
# >>> 1 - (d["label"] // samples.shape[0])
# 0        1
# 1        1
# 2        1
# 3        1
# 4        1
#         ..
# 16276    0
# 16277    0
# 16278    0
# 16279    0
# 16280    0
# Name: label, Length: 32562, dtype: int64
# >>> d["label"] = 1 - (d["label"] // samples.shape[0])
# >>> rf = RandomForestClassifier(oob_score=True)
# >>> rf.fit(d.drop("label", axis=1), d["label"])
# RandomForestClassifier(oob_score=True)
# >>> rf.oob_score_
# 0.5646459062711136
# >>>
# >>> objects = tr_df.select_dtypes(include="object")
# >>> ohe = OneHotEncoder()
# >>> ohe = OneHotEncoder(drop="first", handle_unknown="ignore")
# >>> ohe.fit(objects)
# OneHotEncoder(drop='first', handle_unknown='ignore')
# >>> features = np.concatenate([ohe.transform(tr_df[objects.columns]).toarray(), tr_df[numeric.columns].values], axis=1)
# >>> s_features = np.concatenate([ohe.transform(samples[objects.columns]).toarray(), samples[numeric.columns].values], axis=1)
# /Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/preprocessing/_encoders.py:188: UserWarning: Found unknown categories in columns [7] during transform. These unknown categories will be encoded as all zeros
#   warnings.warn(
# >>> d = pd.concat([pd.DataFrame(features), pd.DataFrame(s_features)])
# >>> d["label"] = 1 - (np.arange(len(d)) // samples.shape[0])
# >>> df.head()
#    0                  1       2           3   4                    5                   6               7       8        9     10  11  12              13      14
# 0  39          State-gov   77516   Bachelors  13        Never-married        Adm-clerical   Not-in-family   White     Male  2174   0  40   United-States   <=50K
# 1  50   Self-emp-not-inc   83311   Bachelors  13   Married-civ-spouse     Exec-managerial         Husband   White     Male     0   0  13   United-States   <=50K
# 2  38            Private  215646     HS-grad   9             Divorced   Handlers-cleaners   Not-in-family   White     Male     0   0  40   United-States   <=50K
# 3  53            Private  234721        11th   7   Married-civ-spouse   Handlers-cleaners         Husband   Black     Male     0   0  40   United-States   <=50K
# 4  28            Private  338409   Bachelors  13   Married-civ-spouse      Prof-specialty            Wife   Black   Female     0   0  40            Cuba   <=50K
# >>> d.head()
#      0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22   23  ...   77   78   79   80   81   82   83   84   85   86   87   88   89   90   91   92   93    94        95    96   97   98    99  label
# 0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  30.0   65278.0   9.0  0.0  0.0  40.0      1
# 1  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  40.0  163455.0  10.0  0.0  0.0  55.0      1
# 2  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  34.0  173495.0  10.0  0.0  0.0  48.0      1
# 3  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  19.0   87497.0   7.0  0.0  0.0  10.0      1
# 4  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  25.0   34803.0  13.0  0.0  0.0  20.0      1

# [5 rows x 101 columns]
# >>> d.tail()
#          0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22  ...   78   79   80   81   82   83   84   85   86   87   88   89   90   91   92   93    94        95    96       97   98    99  label
# 16276  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  33.0  112841.0   9.0      0.0  0.0  45.0      0
# 16277  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  42.0  108632.0  15.0  15024.0  0.0  38.0      0
# 16278  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  38.0  165737.0  10.0      0.0  0.0  40.0      0
# 16279  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  27.0  257294.0   9.0      0.0  0.0  38.0      0
# 16280  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  59.0  443269.0   9.0      0.0  0.0  44.0      0

# [5 rows x 101 columns]
# >>> d["label"].meean()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/generic.py", line 5902, in __getattr__
#     return object.__getattribute__(self, name)
# AttributeError: 'Series' object has no attribute 'meean'. Did you mean: 'mean'?
# >>> d["label"].mean()
# 0.5
# >>> rf = RandomForestClassifier(oob_score=True, n_estimators=85, max_depth=12)
# >>> rf.fit(d.drop("label", axis=1), d["label"])
# RandomForestClassifier(max_depth=12, n_estimators=85, oob_score=True)
# >>> rf.oob_score
# True
# >>> rf.oob_score_
# 0.579294883606658
# >>> t_features = np.concatenate([ohe.transform(test_df[objects.columns]).toarray(), test_df[numeric.columns].values], axis=1)
# /Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/preprocessing/_encoders.py:188: UserWarning: Found unknown categories in columns [8] during transform. These unknown categories will be encoded as all zeros
#   warnings.warn(
# >>> d_test = pd.concat([pd.DataFrame(t_features), pd.DataFrame(s_features)])
# >>> d_test["label"] = 1 - (np.arange(len(d_test)) // samples.shape[0])
# >>> e = rf.predict(d_test.drop("label", axis=1))
# >>> e
# array([0, 1, 1, ..., 1, 0, 1])
# >>> e.mean()
# 0.436183281125238
# >>> 1 - e.mean()
# 0.563816718874762
# >>> e == d_test["label"]
# 0        False
# 1         True
# 2         True
# 3         True
# 4        False
#          ...
# 16276     True
# 16277     True
# 16278    False
# 16279     True
# 16280    False
# Name: label, Length: 32562, dtype: bool
# >>> (e == d_test["label"]).mean()
# 0.6605859590934218
# >>>
# >>> samples_test = rtf_model.sample(n_samples=test_df.shape[0], device="cpu")
# 16384it [02:25, 112.31it/s]
# >>> st_features = np.concatenate([ohe.transform(samples_test[objects.columns]).toarray(), samples_test[numeric.columns].values], axis=1)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/frame.py", line 3811, in __getitem__
#     indexer = self.columns._get_indexer_strict(key, "columns")[1]
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 6113, in _get_indexer_strict
#     self._raise_if_missing(keyarr, indexer, axis_name)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 6173, in _raise_if_missing
#     raise KeyError(f"None of [{key}] are in the [{axis_name}]")
# KeyError: "None of [Int64Index([1, 3, 5, 6, 7, 8, 9, 13, 14], dtype='int64')] are in the [columns]"
# >>> samples_test.columns = df.columns
# >>> st_features = np.concatenate([ohe.transform(samples_test[objects.columns]).toarray(), samples_test[numeric.columns].values], axis=1)
# >>> d_test = pd.concat([pd.DataFrame(t_features), pd.DataFrame(st_features)])
# >>> d_test["label"] = 1 - (np.arange(len(d_test)) // test_df.shape[0])
# >>> e = rf.predict(d_test.drop("label", axis=1))
# >>> e.mean()
# 0.4907868067072047
# >>> (e == d_test["label"]).mean()
# 0.6059824335114551
# >>>
# >>> from sklearn.model_selection import train_test_split
# >>> X_train, X_test, y_train, y_test = train_test_split(d_test.drop("label", axis=1), d_test["label"], stratify=d_test["label"], test_size=0.2)
# >>> X_train.shape
# (26049, 100)
# >>> X_test.shape
# (6513, 100)
# >>> X_test.head()
#        0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19   20   21   22  ...   77   78   79   80   81   82   83   84   85   86   87   88   89   90   91   92   93    94        95    96       97      98    99
# 7069  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  31.0  206609.0  13.0      0.0  1876.0  40.0
# 2690  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  37.0  130805.0  12.0      0.0     0.0  99.0
# 7993  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  31.0  213172.0  10.0      0.0     0.0  50.0
# 6905  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  52.0  145179.0  13.0  15024.0     0.0  40.0
# 77    0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  33.0  118027.0   9.0      0.0     0.0  65.0

# [5 rows x 100 columns]
# >>> rf = RandomForestClassifier(oob_score=True, n_estimators=85, max_depth=12)
# >>> rf.fit(X_train, y_train)
# RandomForestClassifier(max_depth=12, n_estimators=85, oob_score=True)
# >>> rf.oob_score_
# 0.677262082997428
# >>> rf.predict(X_test)
# array([0, 1, 1, ..., 0, 0, 0])
# >>> rf.predict(X_test).mean()
# 0.6307385229540918
# >>> rf.predict(X_test) == y_test
# 7069     False
# 2690      True
# 7993     False
# 6905      True
# 77       False
#          ...
# 10518     True
# 6629      True
# 4931      True
# 10136     True
# 6279      True
# Name: label, Length: 6513, dtype: bool
# >>> (rf.predict(X_test) == y_test).mean()
# 0.6744971595270997
# >>> d_test["label"].mean()
# 0.5
# >>> d_test.shape
# (32562, 101)
# >>> rf = RandomForestClassifier(oob_score=True, n_estimators=85, max_samples_leaf=30)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: RandomForestClassifier.__init__() got an unexpected keyword argument 'max_samples_leaf'
# >>> rf = RandomForestClassifier(oob_score=True, n_estimators=85, min_samples_leaf=30)
# >>> rf.fit(X_train, y_train)
# RandomForestClassifier(min_samples_leaf=30, n_estimators=85, oob_score=True)
# >>> rf.oob_score_
# 0.6791815424776383
# >>> (rf.predict(X_test) == y_test).mean()
# 0.6784891754951635
# >>> rf.fit(d.drop("label", axis=1), d["label"])
# RandomForestClassifier(min_samples_leaf=30, n_estimators=85, oob_score=True)
# >>> d.shape
# (32562, 101)
# >>> rf.oob_score_
# 0.5875253362815552
# >>> (rf.predict(X_test) == y_test).mean()
# 0.6095501305082144
# >>> (rf.predict(X_train) == y_train).mean()
# 0.6108103957925448
# >>> rf = RandomForestClassifier(oob_score=True, n_estimators=85, min_samples_leaf=30, bootstrap=True)
# >>> rf.fit(d.drop("label", axis=1), d["label"])
# RandomForestClassifier(min_samples_leaf=30, n_estimators=85, oob_score=True)
# >>> rf = RandomForestClassifier(oob_score=True, n_estimators=85, min_samples_leaf=30, bootstrap=False)
# >>> rf.fit(d.drop("label", axis=1), d["label"])
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/ensemble/_forest.py", line 437, in fit
#     raise ValueError("Out of bag estimation only available if bootstrap=True")
# ValueError: Out of bag estimation only available if bootstrap=True
# >>> rf = RandomForestClassifier(oob_score=False, n_estimators=85, min_samples_leaf=30, bootstrap=False)
# >>> rf.fit(d.drop("label", axis=1), d["label"])
# RandomForestClassifier(bootstrap=False, min_samples_leaf=30, n_estimators=85)
# >>> (rf.predict(X_train) == y_train).mean()
# 0.6138431417712772
# >>> (rf.predict(X_test) == y_test).mean()
# 0.6074005834484877
# >>> rf.predict(X_test)
# array([1, 1, 0, ..., 0, 0, 1])
# >>> rf.feature_importances_
# array([1.59166112e-03, 4.17673450e-03, 0.00000000e+00, 2.04968006e-02,
#        3.77595618e-03, 5.68503554e-03, 2.23788047e-03, 0.00000000e+00,
#        2.08095515e-03, 4.36738879e-04, 3.65172916e-04, 5.21512335e-04,
#        1.22673152e-03, 4.10178767e-03, 3.74341163e-03, 1.92928210e-03,
#        2.12474642e-02, 4.80869055e-04, 1.02778014e-02, 2.65664834e-03,
#        2.09276888e-05, 8.80961545e-04, 8.54831014e-03, 0.00000000e+00,
#        1.08826814e-02, 7.05400592e-04, 1.22984716e-02, 1.72350638e-03,
#        4.45318011e-03, 5.97322081e-03, 0.00000000e+00, 1.25166307e-02,
#        6.72175472e-03, 2.63823065e-03, 6.00590753e-03, 3.77250898e-03,
#        7.06157860e-03, 1.52135704e-05, 6.60730137e-03, 1.66387285e-03,
#        3.95763648e-02, 1.61538815e-03, 3.04343439e-03, 1.60171060e-02,
#        4.22145156e-03, 8.90315399e-03, 2.44880893e-02, 1.97176397e-03,
#        7.03998529e-03, 5.78330064e-03, 1.22918331e-04, 8.04946013e-03,
#        9.90963566e-03, 0.00000000e+00, 0.00000000e+00, 5.15642233e-05,
#        0.00000000e+00, 0.00000000e+00, 8.62481872e-05, 0.00000000e+00,
#        1.57818818e-03, 1.89495731e-05, 0.00000000e+00, 6.07036048e-06,
#        0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
#        0.00000000e+00, 0.00000000e+00, 2.02318680e-04, 0.00000000e+00,
#        0.00000000e+00, 0.00000000e+00, 2.58558039e-04, 0.00000000e+00,
#        0.00000000e+00, 3.06565724e-03, 0.00000000e+00, 0.00000000e+00,
#        0.00000000e+00, 9.46736134e-04, 1.16442677e-05, 0.00000000e+00,
#        1.82026989e-05, 0.00000000e+00, 3.38644542e-04, 0.00000000e+00,
#        0.00000000e+00, 0.00000000e+00, 9.14586225e-03, 4.07880297e-05,
#        0.00000000e+00, 1.39537363e-02, 2.17237218e-01, 3.09947192e-01,
#        3.71423963e-02, 2.10924612e-02, 1.32585619e-02, 6.13348470e-02])
# >>> from sklearn.model_selection import cros
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ImportError: cannot import name 'cros' from 'sklearn.model_selection' (/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/model_selection/__init__.py)
# >>> d
#          0    1    2    3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22  ...   78   79   80   81   82   83   84   85   86   87   88   89   90   91   92   93    94        95    96       97   98    99  label
# 0      0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  30.0   65278.0   9.0      0.0  0.0  40.0      1
# 1      0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  40.0  163455.0  10.0      0.0  0.0  55.0      1
# 2      0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  34.0  173495.0  10.0      0.0  0.0  48.0      1
# 3      0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  19.0   87497.0   7.0      0.0  0.0  10.0      1
# 4      0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  25.0   34803.0  13.0      0.0  0.0  20.0      1
# ...    ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...   ...       ...   ...      ...  ...   ...    ...
# 16276  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  33.0  112841.0   9.0      0.0  0.0  45.0      0
# 16277  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  42.0  108632.0  15.0  15024.0  0.0  38.0      0
# 16278  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0  38.0  165737.0  10.0      0.0  0.0  40.0      0
# 16279  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  27.0  257294.0   9.0      0.0  0.0  38.0      0
# 16280  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  59.0  443269.0   9.0      0.0  0.0  44.0      0

# [32562 rows x 101 columns]
# >>> objects = tr_df.drop(14, axis=1).select_dtypes(include="object")
# >>> numeric = tr_df.select_dtypes(include=np.number)
# >>> ohe = OneHotEncoder(drop="first", handle_unknown="ignore")
# >>> ohe.fit(objects)
# OneHotEncoder(drop='first', handle_unknown='ignore')
# >>> features = np.concatenate([ohe.transform(tr_df[objects.columns]).toarray(), tr_df[numeric.columns].values], axis=1)
# >>> rf = RandomForestClassifier(oob_score=True, n_estimators=85, max_depth=12)
# >>> le = LabelEncoder()
# >>> le.fit(tr_df[14])
# LabelEncoder()
# >>> target = le.transform(tr_df[14])
# >>> target
# array([1, 1, 1, ..., 1, 1, 0])
# >>> rf.fit(features, target)
# RandomForestClassifier(max_depth=12, n_estimators=85, oob_score=True)
# >>> rf.oob_score_
# 0.8570726613844358
# >>> tr_df.shape
# (16281, 15)
# >>> s_features = np.concatenate([ohe.transform(samples[objects.columns]).toarray(), samples[numeric.columns].values], axis=1)
# /Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/preprocessing/_encoders.py:188: UserWarning: Found unknown categories in columns [7] during transform. These unknown categories will be encoded as all zeros
#   warnings.warn(
# >>> s_features.shape
# (16281, 99)
# >>> features.shape
# (16281, 99)
# >>> y_pred = rf.predict(s_features)
# >>> t_features = np.concatenate([ohe.transform(test_df[objects.columns]).toarray(), test_df[numeric.columns].values], axis=1)
# >>> y_pred = rf.predict(t_features)
# >>> y_pred == le.transform(test_df[14])
# Traceback (most recent call last):
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/utils/_encode.py", line 224, in _encode
#     return _map_to_integer(values, uniques)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/utils/_encode.py", line 164, in _map_to_integer
#     return np.array([table[v] for v in values])
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/utils/_encode.py", line 164, in <listcomp>
#     return np.array([table[v] for v in values])
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/utils/_encode.py", line 158, in __missing__
#     raise KeyError(key)
# KeyError: ' <=50K.'

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/preprocessing/_label.py", line 138, in transform
#     return _encode(y, uniques=self.classes_)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/sklearn/utils/_encode.py", line 226, in _encode
#     raise ValueError(f"y contains previously unseen labels: {str(e)}")
# ValueError: y contains previously unseen labels: ' <=50K.'
# >>> test_df[14].value_counts()
#  <=50K.    12435
#  >50K.      3846
# Name: 14, dtype: int64
# >>> tr_df[14].value_counts()
#  <=50K    12328
#  >50K      3953
# Name: 14, dtype: int64
# >>> tr_df[14].value_counts()["<=50K"]
# Traceback (most recent call last):
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3803, in get_loc
#     return self._engine.get_loc(casted_key)
#   File "pandas/_libs/index.pyx", line 138, in pandas._libs.index.IndexEngine.get_loc
#   File "pandas/_libs/index.pyx", line 165, in pandas._libs.index.IndexEngine.get_loc
#   File "pandas/_libs/hashtable_class_helper.pxi", line 5745, in pandas._libs.hashtable.PyObjectHashTable.get_item
#   File "pandas/_libs/hashtable_class_helper.pxi", line 5753, in pandas._libs.hashtable.PyObjectHashTable.get_item
# KeyError: '<=50K'

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/series.py", line 981, in __getitem__
#     return self._get_value(key)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/series.py", line 1089, in _get_value
#     loc = self.index.get_loc(label)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 3805, in get_loc
#     raise KeyError(key) from err
# KeyError: '<=50K'
# >>> tr_df[14].value_counts()[" <=50K"]
# 12328
# >>> y_pred == le.transform(test_df[14].str.strip("."))
# array([ True,  True, False, ..., False,  True,  True])
# >>> (y_pred == le.transform(test_df[14].str.strip("."))).mean()
# 0.8603279896812235
# >>> rf.fit(s_features, le.transform(samples[14]))
# RandomForestClassifier(max_depth=12, n_estimators=85, oob_score=True)
# >>> rf.oob_score
# True
# >>> rf.oob_score_
# 0.8699097107057306
# >>> (le.transform(test_df[14].str.strip(".")))
# array([0, 0, 1, ..., 0, 0, 1])
# >>> (le.transform(test_df[14].str.strip(".")) == rf.predict(t_features))
# array([ True,  True, False, ..., False, False,  True])
# >>> (le.transform(test_df[14].str.strip(".")) == rf.predict(t_features)).mean()
# 0.8537559117990295
# >>> samples = rtf_model.sample(n_samples=df.shape[0], device="cpu", gen_batch=512)
# 32768it [04:08, 132.07it/s]
# >>> samples.head()
#     0         1       2         3   4                    5                   6               7       8      9  10    11  12              13      14
# 0  21   Private  129612   HS-grad   9        Never-married       Other-service   Not-in-family   White   Male   0     0  40   United-States   <=50K
# 1  27   Private   56396   HS-grad   9   Married-civ-spouse   Machine-op-inspct         Husband   White   Male   0  1579  40   United-States   <=50K
# 2  28         ?   78313   Masters  14   Married-civ-spouse                   ?         Husband   White   Male   0     0   5   United-States   <=50K
# 3  63   Private  250676      10th   6   Married-civ-spouse        Craft-repair         Husband   White   Male   0     0  40   United-States   <=50K
# 4  18   Private   47655      12th   8        Never-married       Other-service       Own-child   White   Male   0     0  32   United-States   <=50K
# >>> objects = df.drop(14, axis=1).select_dtypes(include="object")
# >>>
# >>> numeric = df.select_dtypes(include=np.number)
# >>> ohe = OneHotEncoder(drop="first", handle_unknown="ignore")
# >>> ohe.fit(objects)
# OneHotEncoder(drop='first', handle_unknown='ignore')
# >>> features = np.concatenate([ohe.transform(df[objects.columns]).toarray(), df[numeric.columns].values], axis=1)
# >>> rf = RandomForestClassifier(oob_score=True, n_estimators=85, max_depth=12)
# >>> le = LabelEncoder()
# >>> target = le.fit_transform(df[14])
# >>> rf.fit(features, target)
# RandomForestClassifier(max_depth=12, n_estimators=85, oob_score=True)
# >>> rf.oob_score_
# 0.8595559104450109
# >>> t_features = np.concatenate([ohe.transform(test_df[objects.columns]).toarray(), test_df[numeric.columns].values], axis=1)
# >>> y_pred = rf.predict(t_features)
# >>> (y_pred == le.transform(test_df[14].str.strip("."))).mean()
# 0.8600823045267489
# >>> s_features.shape
# (16281, 99)
# >>> s_features = np.concatenate([ohe.transform(samples[objects.columns]).toarray(), samples[numeric.columns].values], axis=1)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/frame.py", line 3811, in __getitem__
#     indexer = self.columns._get_indexer_strict(key, "columns")[1]
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 6113, in _get_indexer_strict
#     self._raise_if_missing(keyarr, indexer, axis_name)
#   File "/Users/avsolatorio/.local/share/virtualenvs/DevRealTabFormer-e8cwROrn/lib/python3.10/site-packages/pandas/core/indexes/base.py", line 6173, in _raise_if_missing
#     raise KeyError(f"None of [{key}] are in the [{axis_name}]")
# KeyError: "None of [Int64Index([1, 3, 5, 6, 7, 8, 9, 13], dtype='int64')] are in the [columns]"
# >>> samples.shape
# (32561, 15)
# >>> samples.columns = df.columns
# >>> s_features = np.concatenate([ohe.transform(samples[objects.columns]).toarray(), samples[numeric.columns].values], axis=1)
# >>> rf.fit(s_features, le.transform(samples[14]))
# RandomForestClassifier(max_depth=12, n_estimators=85, oob_score=True)
# >>> rf.oob_score_
# 0.8669266914406806
# >>> (le.transform(test_df[14].str.strip(".")) == rf.predict(t_features)).mean()
# 0.857379767827529
# >>>
