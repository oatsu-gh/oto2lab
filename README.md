# oto2lab

SetParamで作った oto.ini をきりたん歌唱DB式ラベル oto.lab に変換するツール。
'japanese.table' のファイルをきりたん歌唱DBからお借りしています。

## 目的

UTAUにおける既存インフラとノウハウの流用で、歌唱DBの充実を図る。

## 開発環境

-   Windows 10 Education 1909
-   Python 3.8.2

## 手順（全体）

1.  音声ファイルを休符で切断する
2.  音声ファイル名には該当部分の歌詞を使う。
3.  音声ファイル群に対してSetParamでラベリングして oto.ini で保存する。
4.  oto2lab（本ツール）を使って oto.lab に変換する。

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

### ファイル変換作業

<!---実装目標
1. oto.ini を oto2lab.py にドラッグ&ドロップ。（ini, txt, lab対応）
2.  oto.iniをフルパス指定してEnter
3.  oto.ini と同じフォルダに oto_yyyyMMdd_hhmmss.lab ファイルが生成されます。
-->

#### oto2labの使い方

1.  コマンドラインから `python oto2lab.py` を実行
2.  oto.ini をフルパス指定してEnter
3.  oto\_日付\_時刻.lab ファイルが生成されて、自動的にメモ帳で開きます。この時点で保存済みです。

#### ust2labの使い方

1.  初めて ust2lab を実行する場合は コマンドラインで `pip install pywin32` を実行。
2.  ust2lab フォルダに ちていこさんのUST→OTO変換ツールを置く。
3.  ust2lab 内の ust フォルダに変換元の UST ファイルを置く。（複数可）
4.  コマンドラインから `python ust2lab.py` を実行。
5.  ust2lab 内の oto フォルダに INI ファイルが仮生成される。
6.  ust2lab 内の labフォルダにLABファイルが生成される。
