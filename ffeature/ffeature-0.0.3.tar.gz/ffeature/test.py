
# ftable特徴量生成ツール [ffeature]
# 【動作確認 / 使用例】

import sys
import ftable
import features	# 特徴量定義ファイル [features.py]
from sout import sout
from ezpip import load_develop
# ftable特徴量生成ツール [ffeature]
ffeature = load_develop("ffeature", "../", develop_flag = True)

# 特徴量作成に利用するテーブルの一覧
ftable_dic = {
	"game_ft": ftable.FTable([
		{"name": "taro", "game_difficulty": 1.2, "field": "A"},
		{"name": "yusuke", "game_difficulty": 1.5, "field": "A"},
		{"name": "yusuke", "game_difficulty": 1.3, "field": "B"},
		{"name": "taro", "game_difficulty": 1.3, "field": "B"},
		{"name": "taro", "game_difficulty": 1.0, "field": None},
	]),
	"player_ft": ftable.FTable([
		{"name": "taro", "player_score": 120},
		{"name": "yusuke", "player_score": 150},
	])
}

# 全量に対する特徴量テーブルを作成 (add_feature デコレータに従って作成) [ffeature]
feature_ft = ffeature.gen_feature_table(
	ftable_dic = ftable_dic,	# 特徴量作成に利用するテーブルの一覧
	rec_table = ftable_dic["game_ft"],	# 作成するデータのレコード単位を規定するテーブル
	sorted_keys = []	# ftableのsorted_keysの指定
)
print(feature_ft)

# 欠損値を処理 [ffeature]
feature_ft = ffeature.handle_missing(
	feature_ft,
	mode = "delete",	# delete: 1つでも欠損値がある行をスキップする
	missing_values = [None]	# 欠損値として扱う値
)
print(feature_ft)

# データの分割
rec_filter = lambda rec: (rec["field"] == "A")
partial_ft = ffeature.data_filter(feature_ft, rec_filter)	# ftから条件を満たすレコードを抽出 [ffeature]
print(partial_ft)
