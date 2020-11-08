# lab_insert_sil

lab_set_start_sil の強化版。Sinsyで生成したLABを参照して、oto2labなどで生成したLABにsilやpauを挿入する。

## 開発環境

- Windos 10 2004
- Python 3.9

### 使用ライブラリ

- utaupy 1.8

## 設計

1. oto2labで生成したLABファイルと、Sinsyで生成したLABファイルを読み取る。
2. oto2labで生成したLABの sil と pau をすべて削除する。
3. Sinsyで生成したLABの sil と pau をすべて oto2lab のLABに挿入する。
4. oto2labのLABの pau の時間データがずれるので、復元する。
5. 修正されたoto2labのLABをファイル出力する。

## 使い方

1. Sinsyが生成したLABを **lab_input_sinsy** に入れる。ファイル名は **{songname}\_sinsy.lab** または **{musicname}.lab** としておく。
1. oto2labが生成したLABを **lab_input_oto2lab** に入れる。ファイル名は **{songname}.lab** としておく。
1. **lab_insert_sil** を起動して実行。
1. **lab_output** に出力される。
