
# ftable特徴量生成ツール [ffeature]

import sys
import erf
import ftable
import random
from sout import sout, souts
from tqdm import tqdm

# 特徴量登録情報 (add_featureデコレータで追加できる)
feature_def_ls = []

# 名称重複チェック (重複の場合は落ちる)
def check_dub_name(feature_name):
	for e in feature_def_ls:
		if feature_name == e["feature_name"]:
			raise Exception("[ffeature error] Duplicate feature_name.")

# 特徴量定義 [ffeature]
def add_feature(feature_name):
	# 引数が処理されたあとのデコレータ本体
	def decorator_func(org_func):
		# 名称重複チェック (重複の場合は落ちる)
		check_dub_name(feature_name)
		# 特徴量定義情報を登録
		feature_def_ls.append({
			"feature_name": feature_name,
			"def_func": org_func,
		})
		# 改変せずに返す
		return org_func
	return decorator_func

# 全量に対する特徴量テーブルを作成 (add_feature デコレータに従って作成) [ffeature]
def gen_feature_table(
	ftable_dic,	# 特徴量作成に利用するテーブルの一覧
	rec_table,	# 作成するデータのレコード単位を規定するテーブル
	sorted_keys = []	# ftableのsorted_keysの指定
):
	feature_ft = ftable.FTable([
		{
			f_def["feature_name"]: f_def["def_func"](rec, ftable_dic)
			for f_def in feature_def_ls
		}
		for rec in tqdm(rec_table.data)
	], sorted_keys = sorted_keys)
	return feature_ft

# 欠損値が1つでも含まれるか判定
def judge_missing(rec, missing_values):
	for k in rec:
		if rec[k] in missing_values: return True
	return False

# 欠損値を処理 [ffeature]
def handle_missing(
	feature_ft,
	mode,	# delete: 1つでも欠損値がある行をスキップする
	missing_values = [None]	# 欠損値として扱う値
):
	if mode == "delete":
		def rec_filter(rec):
			flag = judge_missing(rec, missing_values)	# 欠損値が1つでも含まれるか判定
			return (not flag)
		# ftから条件を満たすレコードを抽出 [ffeature]
		ret_ft = data_filter(feature_ft, rec_filter)
		# 欠損率の表示
		all_n, non_missing_n = len(feature_ft.data), len(ret_ft.data)
		missing_n = all_n - non_missing_n
		print("欠損レコード: %d/%d (欠損率: %.3f%%)"%(missing_n, all_n, missing_n / all_n * 100))
		return ret_ft
	else:
		raise Exception("[ffeature error] invalid mode.")

# ftから条件を満たすレコードを抽出 [ffeature]
def data_filter(
	feature_ft,
	rec_filter
):
	return ftable.FTable([
		rec for rec in feature_ft.data
		if rec_filter(rec) is True
	], sorted_keys = feature_ft.sorted_keys)

# 値の割合リストの生成
@erf(unhashable = "(unhashable values)")
def gen_values_ratio_rank(values_ls):
	cnt_dic = {}
	for e in values_ls:
		if e not in cnt_dic: cnt_dic[e] = 0
		cnt_dic[e] += 1
	raw_rank = [
		(e, cnt_dic[e])
		for e in cnt_dic
	]
	raw_rank.sort(key = lambda e: e[1], reverse = True)
	top_rank = raw_rank[:10]
	return [
		"%s: %.2f%% (%d records)"%(e[0], e[1]/len(values_ls)*100, e[1])
		for e in top_rank
	]

# 1つのkeyに対してアセスメント結果
def one_key_assessment(arg_ft, key, missing_values, sample_idx_ls):
	if len(arg_ft.data) == 0: return "(zero records)"
	res_dic = {}
	values_ls = [e[key] for e in arg_ft.data]
	# 欠損率
	is_missing_ls = [int(e in missing_values) for e in values_ls]
	res_dic["missing_ratio"] = "%.3f%%"%(sum(is_missing_ls) / len(is_missing_ls) * 100)
	# ランダム値サンプル
	res_dic["random_index_examples"] = [arg_ft.data[i][key] for i in sample_idx_ls]
	# 値の割合リスト
	res_dic["values_ratio_rank"] = gen_values_ratio_rank(values_ls)	# 値の割合リストの生成
	return res_dic

# データアセスメント [ffeature]
def assessment(
	arg_ft,
	missing_values = [None],	# 欠損値として扱う値
	show = True,	# 文字列としての結果表示だけでなく標準出力に結果を見せる
	seed = 23
):
	# ランダムサンプリングのインデックスを確定させる
	idx_ls = list(range(len(arg_ft.data)))
	r = random.Random(seed)
	r.shuffle(idx_ls)
	sample_idx_ls = idx_ls[:10]
	# assessment結果を作る
	res_dic = {
		key: one_key_assessment(arg_ft, key, missing_values, sample_idx_ls)	# 1つのkeyに対してアセスメント結果
		for key in arg_ft.data[0]
	}
	assessment_res = souts(res_dic, None)
	# 表示
	if show is True:
		print("■■■■ [ffeature] assessment result ■■■■")
		print(assessment_res)
	return assessment_res
