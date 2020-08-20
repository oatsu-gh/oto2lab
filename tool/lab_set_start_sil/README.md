# lab_set_start_sil

LABファイルの最初の音素をするツール。LABファイルが上書きされるのでバックアップを取ること。

## 使い方

1. PySinsy を使って MusicXMLからLABファイルを生成する。
   自分はこれで生成 https://github.com/oatsu-gh/oto2lab/tree/master/tool/generate_label_from_xml
2. 生成した LAB ファイルの名前を 楽曲名_sinsy.lab にする。
3. 上書きされたいLAB（楽曲名.lab）と、PySinsyで生成したLAB（楽曲名_sinsy.lab）を同じフォルダにまとめる。
4. `python lab_set_start_sil` で本ツールを起動し、表示に従って操作する。
5. 処理が終わると上書き保存される。