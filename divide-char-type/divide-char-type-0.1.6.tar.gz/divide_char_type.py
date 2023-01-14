import re

##########################################################
# 字種分割
##########################################################
def divide_char_type(document, concat_conj_in_ja=True):
    re_kana = re.compile("[ぁ-ゖー～]")         # 平仮名の正規表現
    re_kata = re.compile("[ァ-ヴｦ-ｯｱ-ﾝー～]")   # カタカナの正規表現
    re_cjk = re.compile("[一-龠々]")     # 漢字の正規表現
    re_alpha = re.compile("[A-Za-zＡ-Ｚａ-ｚ]")     # アルファベットの正規表現
    re_digit = re.compile("[0-9０-９]")    # 数字の正規表現
    re_punc = re.compile("[,，][^0-9０-９]|[^0-9０-９][,，]|、") # 読点の正規表現
    re_point = re.compile("[.．。!?！？]") # 句点の正規表現
    re_break = re.compile("\r?\n")   # 段落の正規表現
    re_empty = re.compile("[^A-Za-zＡ-Ｚａ-ｚ0-9０-９ぁ-ゖァ-ヴｦ-ｯｱ-ﾝ一-龠々ー～.,，、．。　\s]")            # 上記以外の正規表現    
    re_word = re.compile("[a-zA-ZＡ-Ｚａ-ｚ0-9０-９ぁ-ゖァ-ヴｦ-ｯｱ-ﾝー一-龠々][a-zA-ZＡ-Ｚａ-ｚ0-9０-９ぁ-ゖァ-ヴｦ-ｯｱ-ﾝ一-龠々ー～・'&.,]*$")

    text1 = document  # 全文
    text2 = re.split(re_break, text1)   # 段落単位
    text3 = []                          # センテンス単位

    num_kana_words = 0      # 平仮名の分割語数
    num_kata_words = 0      # カタカナの分割語数
    num_cjk_words = 0       # 漢字の分割語数
    num_alpha_words = 0     # アルファベットの分割語数
    num_digit_words = 0     # 数字の分割語数

    list_kana_words = []        # 平仮名の分割語長リスト
    list_kata_words = []        # カタカナの分割語長リスト
    list_cjk_words = []         # 漢字の分割語長リスト
    list_alpha_words = []       # アルファベットの分割語長リスト
    list_digit_words = []       # 数字の分割語長リスト
    len_list_kana_words = 0     # 平仮名の分割語長リストの長さ
    len_list_kata_words = 0     # カタカナの分割語長リストの長さ
    len_list_cjk_words = 0      # 漢字の分割語長リストの長さ
    len_list_alpha_words = 0    # アルファベットの分割語長リストの長さ
    
    avg_len_kana_words = 0      # 平仮名の平均分割語長
    avg_len_kata_words = 0      # カタカナの平均分割語長
    avg_len_cjk_words = 0       # 漢字の平均分割語長
    avg_len_alpha_words = 0     # アルファベットの平均分割語長

    tmp_char_class = None   # 一つ前の文字の字種
    conj = None             # 接続記号
    conjlist = ".,&．＆"    # 接続記号の一覧
    end_period = ["e.g", "u.s", "u.s.a"]

    span = []       # センテンスリスト
    allwords = []   # 分割語リスト
    tmp_char_class = None   # 一つ前の文字の字種
    conj = None             # 接続記号

    # 字種分割処理
    for i in text1:
        # 一つ前が接続記号の場合
        if conj != None:
            # 平仮名の場合
            if re_kana.match(i) != None:
                if concat_conj_in_ja == True:
                    del allwords[-1]
                    allwords[-1] += conj
                allwords.append(i)          # 分割語の追加
                list_kana_words.append(1)   # 分割語長の追加
                tmp_char_class = "kana"     # 現在の文字の字種
                conj = None                 # conjの初期化
            # カタカナの場合
            elif re_kata.match(i) != None:
                if concat_conj_in_ja == True:
                    del allwords[-1]
                    allwords[-1] += conj
                allwords.append(i)          # 分割語の追加
                list_kata_words.append(1)   # 分割語長の追加
                tmp_char_class = "kata"     # 現在の文字の字種
                conj = None                 # conjの初期化
            # 漢字の場合
            elif re_cjk.match(i) != None:
                if concat_conj_in_ja == True:
                    del allwords[-1]
                    allwords[-1] += conj
                allwords.append(i)          # 分割語の追加
                list_cjk_words.append(1)    # 分割語長の追加
                tmp_char_class = "cjk"      # 現在の文字の字種
                conj = None                 # conjの初期化
            # アルファベットの場合
            elif re_alpha.match(i) != None:
                # 二つ前がアルファベットの場合    
                if tmp_char_class == "alpha":
                    del allwords[-1]
                    allwords[-1] += conj + i
                    list_alpha_words[-1] += 1   # 分割語長の追加
                elif conj == ".":
                    del allwords[-1]
                    allwords[-1] += conj + i
                    list_alpha_words.append(1)  # 分割語長の追加
                else:
                    allwords.append(i)          # 分割語の追加
                    list_alpha_words.append(1)  # 分割語長の追加
                tmp_char_class = "alpha"    # 現在の文字の字種
                conj = None                 # conjの初期化
            # 数字の場合
            elif re_digit.match(i) != None:
                # 二つ前が数字の場合
                if tmp_char_class == "digit":
                    del allwords[-1]
                    allwords[-1] += conj + i
                    list_digit_words[-1] += 1   # 分割語長の追加
                else:
                    allwords.append(i)          # 分割語の追加
                    list_digit_words.append(1)  # 分割語長の追加
                tmp_char_class = "digit"    # 現在の文字の字種
                conj = None                 # conjの初期化
            # それ以外の場合
            else:
                # 後置ピリオドの場合
                if conj == "." and allwords[-2] in end_period:
                    del allwords[-1]
                    allwords[-1] += conj
                allwords.append(i)          # 分割語の追加
                tmp_char_class = None       # 現在の文字の字種
                conj = None                 # conjの初期化
        # 一つ前が平仮名
        elif tmp_char_class == "kana":
            # 平仮名の場合
            if re_kana.match(i) != None:
                allwords[-1] += i           # 分割語の追加
                list_kana_words[-1] += 1    # 分割語長の追加
            # カタカナの場合
            elif re_kata.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_kata_words.append(1)   # 分割語長の追加
                tmp_char_class = "kata"     # 現在の文字の字種
            # 漢字の場合
            elif re_cjk.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_cjk_words.append(1)    # 分割語長の追加
                tmp_char_class = "cjk"      # 現在の文字の字種
            # アルファベットの場合
            elif re_alpha.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_alpha_words.append(1)  # 分割語長の追加
                tmp_char_class = "alpha"    # 現在の文字の字種
            # 数字の場合
            elif re_digit.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_digit_words.append(1)  # 分割語長の追加
                tmp_char_class = "digit"    # 現在の文字の字種
            # それ以外の場合
            else:
                allwords.append(i)          # 分割語の追加
                tmp_char_class = None       # 現在の文字の字種
        # 一つ前がカタカナ
        elif tmp_char_class == "kata":
            # カタカナの場合
            if re_kata.match(i) != None or i == "-":
                allwords[-1] += i           # 分割語の追加
                list_kata_words[-1] += 1    # 分割語長の追加
            # 平仮名の場合
            elif re_kana.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_kana_words.append(1)   # 分割語長の追加
                tmp_char_class = "kana"     # 現在の文字の字種
            # 漢字の場合
            elif re_cjk.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_cjk_words.append(1)    # 分割語長の追加
                tmp_char_class = "cjk"      # 現在の文字の字種
            # アルファベットの場合
            elif re_alpha.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_alpha_words.append(1)  # 分割語長の追加
                tmp_char_class = "alpha"    # 現在の文字の字種
            # 数字の場合
            elif re_digit.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_digit_words.append(1)  # 分割語長の追加
                tmp_char_class = "digit"    # 現在の文字の字種
            # それ以外の場合
            else:
                allwords.append(i)          # 分割語の追加
                tmp_char_class = None       # 現在の文字の字種
        # 一つ前が漢字
        elif tmp_char_class == "cjk":
            # 漢字の場合
            if re_cjk.match(i) != None:
                allwords[-1] += i           # 分割語の追加
                list_cjk_words[-1] += 1     # 分割語長の追加
            # 平仮名の場合
            elif re_kana.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_kana_words.append(1)   # 分割語長の追加
                tmp_char_class = "kana"     # 現在の文字の字種
            # カタカナの場合
            elif re_kata.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_kata_words.append(1)   # 分割語長の追加
                tmp_char_class = "kata"     # 現在の文字の字種
            # アルファベットの場合
            elif re_alpha.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_alpha_words.append(1)  # 分割語長の追加
                tmp_char_class = "alpha"    # 現在の文字の字種
            # 数字の場合
            elif re_digit.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_digit_words.append(1)  # 分割語長の追加
                tmp_char_class = "digit"    # 現在の文字の字種
            # それ以外の場合
            else:
                allwords.append(i)          # 分割語の追加
                tmp_char_class = None       # 現在の文字の字種
        # 一つ前がアルファベット
        elif tmp_char_class == "alpha":
            # アルファベットの場合
            if re_alpha.match(i) != None:
                allwords[-1] += i           # 分割語の追加
                list_alpha_words[-1] += 1   # 分割語長の追加
            # 数字の場合
            elif re_digit.match(i) != None:
                #allwords[-1] += i           # 分割語の追加
                allwords.append(i)          # 分割語の追加
                list_digit_words.append(1)  # 分割語長の追加
                tmp_char_class = "digit"    # 現在の文字の字種
            # 平仮名の場合
            elif re_kana.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_kana_words.append(1)   # 分割語長の追加
                tmp_char_class = "kana"     # 現在の文字の字種
            # カタカナの場合
            elif re_kata.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_kata_words.append(1)   # 分割語長の追加
                tmp_char_class = "kata"     # 現在の文字の字種
            # 漢字の場合
            elif re_cjk.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_cjk_words.append(1)    # 分割語長の追加
                tmp_char_class = "cjk"      # 現在の文字の字種
            # 接続記号の場合
            elif i in conjlist:
                conj = i
                allwords.append(i)          # 分割語の追加 
            # それ以外の場合
            else:
                allwords.append(i)          # 分割語の追加
                tmp_char_class = None       # 現在の文字の字種
        # 一つ前が数字
        elif tmp_char_class == "digit":
            # 数字の場合
            if re_digit.match(i) != None:
                allwords[-1] += i           # 分割語の追加
                list_digit_words[-1] += 1   # 分割語長の追加
            # アルファベットの場合
            elif re_alpha.match(i) != None:
                #allwords[-1] += i           # 分割語の追加
                allwords.append(i)          # 分割語の追加
                list_alpha_words.append(1)  # 分割語長の追加
                tmp_char_class = "alpha"    # 現在の文字の字種
            # 平仮名の場合
            elif re_kana.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_kana_words.append(1)   # 分割語長の追加
                tmp_char_class = "kana"     # 現在の文字の字種
            # カタカナの場合
            elif re_kata.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_kata_words.append(1)   # 分割語長の追加
                tmp_char_class = "kata"     # 現在の文字の字種
            # 漢字の場合
            elif re_cjk.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_cjk_words.append(1)    # 分割語長の追加
                tmp_char_class = "cjk"      # 現在の文字の字種
            # 接続記号の場合
            elif i in conjlist:
                conj = i
                allwords.append(i)          # 分割語の追加
            # それ以外の場合
            else:
                allwords.append(i)          # 分割語の追加
                tmp_char_class = None       # 現在の文字の字種            
        # 一つ前がそれ以外
        else:
            # 平仮名の場合
            if re_kana.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_kana_words.append(1)   # 分割語長の追加
                tmp_char_class = "kana"     # 現在の文字の字種
            # カタカナの場合
            elif re_kata.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_kata_words.append(1)   # 分割語長の追加
                tmp_char_class = "kata"     # 現在の文字の字種
            # 漢字の場合
            elif re_cjk.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_cjk_words.append(1)    # 分割語長の追加
                tmp_char_class = "cjk"      # 現在の文字の字種
            # アルファベットの場合
            elif re_alpha.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_alpha_words.append(1)  # 分割語長の追加
                tmp_char_class = "alpha"    # 現在の文字の字種
            # 数字の場合
            elif re_digit.match(i) != None:
                allwords.append(i)          # 分割語の追加
                list_digit_words.append(1)  # 分割語長の追加
                tmp_char_class = "digit"    # 現在の文字の字種
            # それ以外の場合
            else:
                allwords.append(i)          # 分割語の追加
                tmp_char_class = None       # 現在の文字の字種

        #print(allwords)

    # 戻り値（字種分割語リスト、平仮名連リスト，カタカナ連リスト，漢字連リスト，アルファベット連リスト）
    return (allwords, list_kana_words, list_kata_words, list_cjk_words, list_alpha_words)


if __name__=="__main__":
    print(divide_char_type("1.0 is number.")[0])
    print(divide_char_type("1,000 is number.")[0])
    print(divide_char_type("u.s.a. is state.")[0])
    print(divide_char_type("u.k. is state.")[0])
    print(divide_char_type("e.g., th, ch, sh, ph, gh, ng, qu")[0])
    print(divide_char_type("state include u.s. u.s. is state.")[0])
    print(divide_char_type("state include u.k. u.k. is state.")[0])
    print(divide_char_type("u.s.は国です。")[0])
    print(divide_char_type("u.s.は国です。", concat_conj_in_ja=False)[0])
    print(divide_char_type("あいうえおーかきくけこ")[0])
    print(divide_char_type("アイウエオーカキクケコ")[0])
    print(divide_char_type("今日の天気は晴れです。\n明日の天気は曇りです。\n")[0])
