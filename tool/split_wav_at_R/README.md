# split_wav_at_R
休符位置でWAVファイルを切断する。

## 方針
1. すべてのUSTとWAVを休符位置で分割して、一時フォルダに格納する
2. 分割したUSTから、ラベリング用INIファイルを生成する。（出力しないで結合してもOK）
3. ラベリング用INIファイルのデータを oto.ini にまとめて出力する。
4. 出力した oto.ini を moresampler でパラメータ推定する。ファイルがたくさんあるほど推定しやすそう。

# 断念しました
- moresampler の update 機能がわからない
- moresampler の overwrite 機能だと誤推定が多いのと、wavファイル名を歌詞にする必要がある。
