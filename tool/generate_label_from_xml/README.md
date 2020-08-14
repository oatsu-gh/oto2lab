# generate_label_from_xml

musicxml から 音素ラベルとフルコンテキストラベルを生成する。

## 動作環境

- Windows 10 2004
  - WSL2 (Ubuntu-20.04 LTS)
    - WSL1でもOK
    - たぶん Debian でもOK
- Sinsy と Pysinsy のセットアップを済ませておくこと。

## 使い方

1. WSL を起動
2. oto2lab のリポジトリを複製 `git clone https://github.com/oatsu-gh/oto2lab`
3. Pysinsy にパスを通すために `export LD_LIBRARY_PATH=/usr/local/lib`
4. 変換するスクリプトを起動 `python3 oto2lab/tool/generate_label/from_xml/generate_label_from_xml.py`
5. musicxml があるフォルダのパスを入力（Window形式のパスでOK）
6. musicxml があるフォルダに 音素ラベル lab と フルコンテキストラベル full が生成される。



