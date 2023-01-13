
# 分位点散布図 [quantile_scatter]
# 【動作確認 / 使用例】

import sys
import numpy as np
from sout import sout

# xの型に応じて処理を分岐
def judge_x_type(x_ls):
	if type(x_ls[0]) == type(""):
		for x in x_ls:
			if type(x) != type(""): raise Exception("[error] Consistency error in the type of x value.")
		return "nominal"
	return "number"

# 数値横軸をグループに分割
def num_grouping(arg_ls, group_n):
	ret_ls = [[] for _ in range(group_n)]
	for i, e in enumerate(arg_ls):
		th = i / len(arg_ls)	# 無次元化インデックス
		group_idx = int(th * group_n)
		# 格納
		ret_ls[group_idx].append(e)
	return ret_ls

# 各名義の出現頻度を調べる
def gen_rank_ls(x_ls):
	cnt_dic = {}
	for x in x_ls:
		if x not in cnt_dic: cnt_dic[x] = 0
		cnt_dic[x] += 1
	rank_ls = [(k, cnt_dic[k]) for k in cnt_dic]
	rank_ls.sort(key = lambda e: e[1], reverse = True)
	return rank_ls

# 横軸値に従ってグルーピング
def x_grouping(x_ls, y_ls, group_n):
	# xの型に応じて処理を分岐
	x_type = judge_x_type(x_ls)
	if x_type == "number":	# 数値
		# x昇順に整序
		zip_ls = list(zip(x_ls, y_ls))
		zip_ls.sort(key = lambda e: e[0])
		# 数値横軸をグループに分割
		grouped_zip_ls = num_grouping(zip_ls, group_n)
		# 各グループの横軸値を集約
		group_ls = [
			{
				"x": np.mean([x for x, y in group]),
				"y_ls": [y for x, y in group]
			}
			for group in grouped_zip_ls
		]
	elif x_type == "nominal":	# 名義尺度
		# 各名義の出現頻度を調べる
		rank_ls = gen_rank_ls(x_ls)
		# ランキング上位のkeyを一覧
		top_keys = [k for k, cnt in rank_ls[:(group_n-1)]]
		top_keys_dic = {k: True for k in top_keys}
		# 値の一覧をグループにくくる
		group_dic = {}
		for x, y in zip(x_ls, y_ls):
			key = (x if x in top_keys_dic else "others")
			if key not in group_dic: group_dic[key] = []
			group_dic[key].append(y)
		# 成果物の形を整える
		keys = (top_keys + ["others"] if "others" in group_dic else top_keys)
		group_ls = [
			{"x": key, "y_ls": group_dic[key]}
			for key in keys	# top_keys の順序に従う
		]
	else:
		raise Exception("[error] invalid x_type.")
	return group_ls, x_type

# matplotlibで可視化 [quantile_scatter]
def visualize(arg_data, x_type):
	from matplotlib import pyplot as plt
	for one_data in arg_data:
		# 描画
		plt.plot(
			one_data["x"], one_data["y"],
			label = one_data["label"],
			marker = ".", markersize = 8
		)
	# 描画処理
	plt.legend()
	if x_type == "nominal":
		plt.xticks(rotation=90)
		plt.tight_layout()
	plt.show()

# 1ラベル分のグラフデータ生成
def one_label_sum(
	group_ls,	# グループ化されたデータ
	sum_func,	# データ集計関数
	label	# 凡例に掲載するデータ説明
):
	# xの取り出し
	show_x_ls = [group["x"] for group in group_ls]
	# yの計算 (sum_funcでgroup内y値を集計)
	show_y_ls = [
		sum_func(group["y_ls"])
		for group in group_ls
	]
	# データをパッケージングして返却
	return {
		"label": label,
		"x": show_x_ls,
		"y": show_y_ls,
	}

# 分位点散布図の描画 [quantile_scatter]
def plot(
	x,	# 横軸数値リスト
	y,	# 縦軸数値リスト
	group_n = 20,	# 分割グループ数
	ile_ls = [0.25, 0.5, 0.75],	# どこの分位点を出すか
	mean = False,	# 平均も出力する
	show = True,	# False指定でグラフを出力しない (データ集計のみ)
):
	# 横軸値に従ってグルーピング
	group_ls, x_type = x_grouping(x, y, group_n)
	# 返却するデータ
	ret_data = []
	# 各分位点を集計
	for ile in ile_ls:
		# 今回のデータ集計方法
		sum_func = lambda arg_y_ls: np.quantile(arg_y_ls, ile)
		# 1ラベル分のグラフデータ生成
		ret_data.append(one_label_sum(
			group_ls,	# グループ化されたデータ
			sum_func,	# データ集計関数
			label = str(ile)	# 凡例に掲載するデータ説明
		))
	# 平均を集計
	if mean is True:
		# 1ラベル分のグラフデータ生成
		ret_data.append(one_label_sum(
			group_ls,	# グループ化されたデータ
			sum_func = lambda arg_y_ls: np.mean(arg_y_ls),	# データ集計関数
			label = "mean"	# 凡例に掲載するデータ説明
		))
	# matplotlibで可視化 [quantile_scatter]
	if show is True:
		visualize(ret_data, x_type)
	return ret_data
