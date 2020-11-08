# lab_insert_sil

lab_set_start_sil の強化版。Sinsyで生成したLABを参照して、oto2labなどで生成したLABにsilを挿入する。

## 開発環境

- Windos 10 2004
- Python 3.9

### 使用ライブラリ

- utaupy 1.8

## 設計

1. oto2labで生成したLABと、Sinsyで生成したLABを読み取る。
2. 行数差を検出する。
3. 数値無視して音素のみ比較、一致しなければsilとみなして挿入。
   - 最初の行はsil-pau
   - 中間はpau-sil-pau（このときのpauは複製） 
   - 最後はpauのまま放置
4. silの値を差し込む。前後のpauの値も同時にいじる。
5. 行数差がsilによって改善されるのを確認する。

## 使い方

1. sinsyが生成したLABを lab_input_sinsy に入れる。ファイル名は {songname}\_sinsy.lab または {musicname}.lab としておく。
1. oto2labが生成したLABを lab_input_oto2lab に入れる。ファイル名は {songname}.lab としておく。
1. lab_insert_sil を起動して実行。
