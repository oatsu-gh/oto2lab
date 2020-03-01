# oto2lab

SetParamで作った oto.ini をきりたん歌唱DB式ラベル oto.lab に変換するツール。


## 目的

UTAUにおける既存インフラとノウハウの流用で、歌唱DBの充実を図る。

## 注意事項
- 「japanese.table」 を[きりたん歌唱DB](https://github.com/mmorise/kiritan_singing)からお借りしています。
- 「歌声DBラベリング用ust→oto変換ツール」については作者が異なるため、[別個の注意書き](歌声DBラベリング用ust→oto変換ツールについて.txt)を読んでください。
- バージョンアップでスクリプト名が変わることがあるのでご注意ください。

## 開発環境

-   Windows 10 Education 1909
-   Python 3.8.2

## 手順（全体）

1.  歌唱を録音する。
2.  音声ファイルに合わせてMIDIを作る。
3.  MIDIをもとにUSTを作る。
4.  ust2ini2lab（本ツール）を使って UST を INI に変換する。
5.  音声ファイルに合わせて INI を SetParam で編集して保存する。
6.  ust2ini2lab（本ツール）を使って oto.lab に変換する。

* * *

## 手順（詳細）

### SetParamでのパラメータ設定

ラベル変換目的のため、UTAUの原音設定とは違う使い方をします。  
以下のように設定してください。

-   左ブランク: 不使用
-   オーバーラップ: 発声開始位置
-   先行発声: 子音と母音の切れ目
-   固定範囲: 不使用
-   右ブランク: 不使用

### 本ツールの使い方

1.  初めて実行する場合は コマンドラインで `pip install pywin32` を実行。
2.  ust フォルダに変換元の UST を置く。
3.  コマンドラインから `python ust2ini2lab.py` を実行し、モード選択で 1 を入力。
4.  ini フォルダに INI が生成される。
5.  生成された INI をsetParamで編集する。（上書きしないために別のフォルダで作業すると吉）
6.  コマンドラインから `python ust2ini2lab.py` を実行し、モード選択で 2 を入力。
7.  lab フォルダに LAB が生成される。

---
### oto2lab.pyについて
oto2lab0.0.3以前の仕様になれた方のために、同じ操作感で実行できるスクリプトを同梱しています。デバッグ以外での更新予定はありません。
