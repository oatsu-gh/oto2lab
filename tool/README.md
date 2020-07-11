# oto2lab / tools

歌唱DBまわりのちょっとしたツール。

[utaupy](https://github.com/oatsu-gh/utaupy) が必要です。

## ツール紹介

### audacitylabel2lab.py

Audacityでラベリングしたいときのツール。
Audacityのラベルファイル（txt）を歌唱DBのモノラベルファイル（lab）に変換します。

### convert_label_time_unit

モノラベルファイル（lab）の時刻のフォーマットの相互変換をします。

相互変換対象は以下の２種類です。

- Sinsy（時間単位 [100ns]）
- 東北きりたん歌唱DB（時間単位 [s]） 

### generate_label_from_xml

pysinsyとかを使って、楽譜情報のxmlからモノラベルとフルラベルを生成します。

pysinsyの環境が無いと使えません。

### phoneme_complete_checker

歌唱DBのモノラベルをすべて取得して、音素の網羅状況をチェックします。

検査結果を Excel 用の xlsx に出力します。

### ust2shiroindex

複数のustファイルから、[SHIRO](https://github.com/Sleepwalking/SHIRO) 用の Index file（txt）を生成します。



## モノラベルの仕様比較

### Sinsy のモノラベル
- 拡張子は lab
- 時間単位は 100ns
- 整数
- 区切り文字は 半角スペース
```plain txt (.lab)
0 5000000 pau
5000000 5500000 h
5500000 12500000 o
12500000 15000000 g
15000000 30000000 e
...
3939000000 4000000000 pau

```

### 東北きりたん歌唱DB のモノラベル
- 拡張子は lab
- 時間単位は 1s
- 小数ゼロ埋めあり
- 区切り文字は 半角スペース
```plain txt (.lab)
0.0000000 0.5000000 pau
0.5000000 0.5500000 h
0.5500000 1.2500000 o
1.2500000 1.5000000 g
1.5000000 3.0000000 e
...
393.9000000 400.0000000 pau

```

### Audacityのラベルファイル

- 拡張子は txt
- 時間単位は 1s
- 小数ゼロ埋めなし
- 区切り文字は Tab文字

```plain txt (.txt)
0\t0.5\tpau
0.5\t0.55\th
0.55\t1.25\to
1.25\t1.5\tg
1.5\t3\te
...
393.9\t400

```


---

Copyright (c) oatsu 2020