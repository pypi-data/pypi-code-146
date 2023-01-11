
# 特徴量定義ファイル [features.py]

from ezpip import load_develop
# ftable特徴量生成ツール [ffeature]
ffeature = load_develop("ffeature", "../", develop_flag = True)

# 特徴量定義 [ffeature]
@ffeature.add_feature("player_score")
def player_score_feature(rec, ftable_dic):
	one_player = ftable_dic["player_ft"].cfilter("name", rec["name"])
	if len(one_player.data) != 1: raise Exception("[error] player unique constraint error")
	return one_player.data[0]["player_score"]

# 特徴量定義 [ffeature]
@ffeature.add_feature("field")
def field_feature(rec, ftable_dic):
	return rec["field"]
