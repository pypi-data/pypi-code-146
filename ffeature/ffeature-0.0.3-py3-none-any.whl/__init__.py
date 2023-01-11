
# ftable特徴量生成ツール [ffeature]

import sys
import ftable
from sout import sout
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
