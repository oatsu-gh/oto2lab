# compare_tempo_xml_ust

歌唱データベース内のMusicXMLとUSTのテンポ情報を比較して、一致していない場合に修正を促す。

## 動作環境

- Windows 10 2004
- Python 3.9
  - utaupy 1.8
- WSLは不要

## 使い方

1. PowerShell上で `Python compare_tempo_xml_ust.py`
2. MusicXMLやUSTが入っているフォルダを指定（再帰的に取得できます）
3. PowerShell上での出力を読んで不整合を探す

## TODO（開発）

- いずれ改造してログファイル出力したい

- 順に表示するだけでなく不一致を一覧にしたい