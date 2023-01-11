
# 高速テーブル [ftable]

import sys
import random
from sout import sout, souts
from tqdm import tqdm

# cfilter_cacheの生成
def gen_cfilter_cache(ft, key):
	show_key = (key if type(key) == type("") else "<custom_function>")
	print("[ftable] generating cache (key = %s)..."%show_key)
	# 情報を取り出す関数
	def pickup_func(rec):
		if type(key) == type(""): return rec[key]
		return key(rec)	# 関数による指定の場合
	# 情報を分割格納
	prepare_dic = {}
	for rec in tqdm(ft.data):
		value = pickup_func(rec)
		if value not in prepare_dic: prepare_dic[value] = []
		prepare_dic[value].append(rec)
	# cacheの値をFTabel型として格納
	one_cache = {
		value: FTable(
			prepare_dic[value],
			ft.sorted_keys,
			_already_sorted = True
		)
		for value in tqdm(prepare_dic)
	}
	return one_cache

# インデックスを所定範囲内にクリッピング
def idx_clipping(org_idx, clipping_range):
	r0, r1 = clipping_range
	if org_idx < r0: return r0
	if org_idx > r1: return r1
	return org_idx

# csumの要素数0個の集計結果を表現する特殊オブジェクト
class _Empty_Sum:
	pass

# recをtargetで指定された方法でvalue化
def pickup_value(rec, target):
	if type(target) == type(""): return rec[target]
	return target(rec)

# 高速テーブル型 [ftable]
class FTable:
	# 初期化処理
	def __init__(self,
		raw_data,	# 原型となるテーブルデータ
		sorted_keys = [],	# 整序軸の指定
		_already_sorted = False	# (内部機能) すでにソートされている場合
	):
		# 整序軸の処理
		self.sorted_keys = sorted_keys
		if len(self.sorted_keys) == 0:
			pass
		elif len(self.sorted_keys) == 1:
			if _already_sorted is False:
				# 外側のリストのみ新たに生成される (シャローコピーに対応)
				raw_data = sorted(raw_data,
					key = lambda rec: rec[self.sorted_keys[0]])
		else:
			# 未実装の機能
			raise Exception("[ftable error] The current version does not allow more than two sorted_keys to be specified.")
		# データ登録
		self.data = raw_data	# データ登録
		# cfilterのキャッシュ
		self.cfilter_cache = {}
		# csumのキャッシュ
		self.csum_cache = {}
	# cacheされたフィルタ機能 [ftable]
	def cfilter(self, key, value):
		if key not in self.cfilter_cache:
			# cfilter_cacheの生成
			self.cfilter_cache[key] = gen_cfilter_cache(self, key)
		# filterした結果を返す
		filtered_ft = self.cfilter_cache[key][value]
		return filtered_ft
	# 二分探索 (条件を満たす最後のインデックスを見つける; 最初からFalseの場合は-1を返す) [ftable]
	def bfind(self, key, cond):
		# keyの適格性判断
		if key not in self.sorted_keys: raise Exception("[ftable error] The bfind function can only compute on keys specified in sorted_keys.")
		# 二分探索
		left = 0
		right = len(self.data) - 1
		while left <= right:
			mid = (left + right) // 2
			if cond(self.data[mid][key]) is True:
				left = mid + 1
			else:
				right = mid - 1
		idx = right
		if idx < 0: return -1
		return idx
	# 高速合計関数 (2項演算で集計) [ftable]
	def csum(self,
		start_idx,	# 集計範囲開始インデックス
		end_idx,	# 集計範囲終了インデックス (自身は含まない)
		target,	# 集計対象 (key名もしくはrecを受け取って値を返す関数で指定)
		func = (lambda a, b: a + b)	# 集計方法 (2項演算; 値2つを受け取って値を返す)
	):
		# start_idx, end_idx がftableインデックス範囲外の場合は実装ミス防止の意味で落とす
		if start_idx < 0: raise Exception("[ftable error] index out of range.")
		if end_idx > len(self.data): raise Exception("[ftable error] index out of range.")
		if start_idx > end_idx: raise Exception("[ftable error] start_idx > end_idx")
		# 再帰的にcsumを計算
		raw_res = self._rec_csum(
			start_idx,	# 集計範囲開始インデックス
			end_idx,	# 集計範囲終了インデックス (自身は含まない)
			target,	# 集計対象 (key名もしくはrecを受け取って値を返す関数で指定)
			func,	# 集計方法 (2項演算; 値2つを受け取って値を返す)
			block_start = 0,	# 被覆範囲開始インデックス
			block_end = len(self.data),	# 被覆範囲終了インデックス
		)
		if type(raw_res) == _Empty_Sum:
			raise Exception("[ftable error] csum() is only available for ranges containing one or more elements.")
		return raw_res
	# 再帰的にcsumを計算
	def _rec_csum(self,
		start_idx,	# 集計範囲開始インデックス
		end_idx,	# 集計範囲終了インデックス (自身は含まない)
		target,	# 集計対象 (key名もしくはrecを受け取って値を返す関数で指定)
		func,	# 集計方法 (2項演算; 値2つを受け取って値を返す)
		block_start,	# 被覆範囲開始インデックス
		block_end,	# 被覆範囲終了インデックス
	):
		# インデックスの範囲外の部分をカットする
		start_idx = idx_clipping(start_idx, (block_start, block_end))	# インデックスを所定範囲内にクリッピング
		end_idx = idx_clipping(end_idx, (block_start, block_end))	# インデックスを所定範囲内にクリッピング
		# 要素が0個の場合 (クリッピングの作用により、範囲を外れている場合もこの場合に集約される)
		if end_idx - start_idx == 0: return _Empty_Sum()
		# block範囲全体の場合
		csum_key = (block_start, block_end, target, func)
		is_whole_block = (start_idx == block_start) and (block_end == end_idx)
		if is_whole_block is True:
			if csum_key in self.csum_cache: return self.csum_cache[csum_key]
		# 要素が1個の場合
		if end_idx - start_idx == 1:
			res_value = pickup_value(self.data[start_idx], target)	# recをtargetで指定された方法でvalue化
		else:
			# 分割計算
			block_med = (block_start + block_end) // 2	# 中央インデックス
			left_res = self._rec_csum(start_idx, end_idx, target, func, block_start, block_med)	# 左側を計算
			right_res = self._rec_csum(start_idx, end_idx, target, func, block_med, block_end)	# 右側を計算
			# 集計して返す
			if type(left_res) == _Empty_Sum:
				res_value = right_res
			elif type(right_res) == _Empty_Sum:
				res_value = left_res
			else:
				res_value = func(left_res, right_res)
		# キャッシュの登録
		if is_whole_block is True:
			self.csum_cache[csum_key] = res_value
		return res_value
	# 文字列化
	def __str__(self):
		return "<ftable %s>"%souts(self.data, 10)
	# 文字列化その2
	def __repr__(self):
		return str(self)
	# ランダムなレコードを選定 (seed固定) [ftable]
	def rget(self, num, seed = 23):
		# 局所的にシードが固定された乱数生成器
		rd = random.Random(seed)
		return FTable(
			rd.sample(self.data, num),
			self.sorted_keys
		)
