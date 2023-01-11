
# 高速テーブル [ftable]
# 【動作確認 / 使用例】

import sys
from sout import sout
from ezpip import load_develop
# 深層分位点回帰 [deep_q_reg]
ftable = load_develop("ftable", "../", develop_flag = True)

raw_data = [
	{"date": "20450105", "name": "taro", "score": 22.5},
	{"date": "20450206", "name": "hanako", "score": 12.6},
	{"date": "20450206", "name": "taro", "score": 3.5},
]

# 高速テーブル型 [ftable]
ft = ftable.FTable(
	raw_data,	# 原型となるテーブルデータ
	sorted_keys = ["date"]	# 整序軸の指定
)

# cacheされたフィルタ機能 [ftable]
filtered_ft = ft.cfilter("name", "taro")
# フィルタ結果の表示
print(filtered_ft)

# cacheされたフィルタ機能 [ftable]
def judge_score(rec): return ("high" if rec["score"] > 15 else "low")
filtered_ft = ft.cfilter(judge_score, "high")
# フィルタ結果の表示
print(filtered_ft)

# 二分探索 (条件を満たす最後のインデックスを見つける; 最初からFalseの場合は-1を返す) [ftable]
idx = filtered_ft.bfind("date",
	cond = lambda date: (date < "20450110"))

# 元データの直接参照
print(idx)
if idx == -1: idx = None
sout(filtered_ft.data[idx])

# 高速合計関数 (2項演算で集計) [ftable]
res = ft.csum(0, 2, "score")
print(res)

# 合計ではない2項演算 (max等) も可能
res = ft.csum(0, 2, "score", lambda a, b: max(a, b))	# 高速合計関数 (2項演算で集計)
print(res)

# 集計対象の値がレコード値そのものではなく、少し加工が必要な場合
res = ft.csum(	# 高速合計関数 (2項演算で集計)
	0, 2,
	lambda rec: len(rec["name"]),
	lambda a, b: max(a, b)
)
print(res)

# ランダムなレコードを選定 (seed固定) [ftable]
print(ft.rget(2))
