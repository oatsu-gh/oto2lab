# generate_random_ust

音程と歌詞がランダムなUSTを生成する。最後は必ず休符になるようにする。

## 使い方

-   使える歌詞（単独音）の一覧を読み取る
    -   R も書いておく
    -   同じ歌詞を重ねてもOK
-   音程の範囲を設定する
    -   最低音の鍵盤番号
    -   最高音の鍵盤番号
-   BPMを設定する
    -   途中で変化してもたぶんOK
-   USTの長さ（ノート数）を設定する
-   ノート長を設定する
    -   同じノート長を重ねて出現回数を調整する
-   出力するファイル数を設定する

## generate_random_ust_config.json に書く内容

-   必須パラメーター
    -   aliases (list of str)
    -   max_notenum (int)
    -   min_notenum (int)
    -   bpm (list of int, or list of float)
    -   ust_length (int)
        - BPM120の場合1800程度が上限（wavが100MBを超えるため）
        - BPM240の場合3600程度
        - UTAUの仕様で9999が上限
    -   note_length (list of int)
    -   file_number (int)
-   任意パラメーター
    -   voicedir (str)
    -   tool1 (str)
    -   tool2 (str)
