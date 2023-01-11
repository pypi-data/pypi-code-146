
# 高速テーブル [ftable]
# csumのテスト

import sys
import random
from sout import sout
from tqdm import tqdm
from ezpip import load_develop
# 深層分位点回帰 [deep_q_reg]
ftable = load_develop("ftable", "../../", develop_flag = True)

def randint(num, r): return int(r.random() * num)

rand = random.Random(23)	# シード固定乱数発生器

raw_data = [
	{"idx": i, "value": randint(100, rand)}
	for i in range(100000)
]

# 検算用関数
def true_summer(i0, i1, raw_data, func):
	if i0 < 0: return "error"
	if i1 > len(raw_data): return "error"
	if i1 < i0: return "error"
	if i0 == i1: return "error"	# 今回は0個のsumはerror
	pre_value = raw_data[i0]["value"]
	for e in raw_data[i0+1:i1]:
		pre_value = func(pre_value, e["value"])
	return pre_value

# 高速テーブル型 [ftable]
ft = ftable.FTable(
	raw_data,	# 原型となるテーブルデータ
	sorted_keys = ["idx"]	# 整序軸の指定
)

def func(a, b): return max(a, b)

rand = random.Random(23)	# シード固定乱数発生器
for _ in tqdm(range(100000)):
	i0 = randint(10200, rand) - 100
	i1 = randint(10200, rand) - 100
	true_res = true_summer(i0, i1, raw_data, func)

rand = random.Random(23)	# シード固定乱数発生器
for _ in tqdm(range(100000)):
	i0 = randint(10200, rand) - 100
	i1 = randint(10200, rand) - 100
	try:
		csum_res = ft.csum(i0, i1, "value", func)
	except:
		csum_res = "error"

rand = random.Random(23)	# シード固定乱数発生器
for _ in tqdm(range(100000)):
	i0 = randint(10200, rand) - 100
	i1 = randint(10200, rand) - 100
	try:
		csum_res = ft.csum(i0, i1, "value", func)
	except:
		csum_res = "error"
	true_res = true_summer(i0, i1, raw_data, func)
	if csum_res != true_res:
		print(error)
		print(i0)
		print(i1)
		print(csum_res)
		print(true_res)
		sys.exit()
