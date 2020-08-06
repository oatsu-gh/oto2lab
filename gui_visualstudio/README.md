# oto2labGUI

IDE is Microsoft Visual Studio Community 2017

## Haruqaさんが書いてくれた仕様

### Input File or Folder

D&Dでファイルもしくはフォルダー指定可能
「File Browse」ボタンでファイル選択ダイアログ
「Folder Browse」ボタンでフォルダー選択ダイアログ
※「Folder Browse」のダイアログのファイル名に「SelectFolder」が出るけど無視して大丈夫
　Windows標準のフォルダー選択ダイアログも使えるけど、使いづらいのでファイルダイアログを使用してます
　使いづらい：パスが入力できなかったり、ツリーを開いてくのが面倒だったり

\--input [ファイル/フォルダパス]

### Option

実行オプションに `--mode`

-   ust to oto：`1`
-   oto to lab：`2`
-   lab to oto：`3`
-   svp to oto：`4`  

を付加します

### Append option

実行オプションに付加します。

-   Debug：`--debug`
-   Kana Alias：`--kana`

### oto2lab.exeの起動時

「oto2lab.exe」の固定文字列でハードコードしてます。
存在しないとエラーします。

### 標準出力エリア

帰ってくる標準出力を表示します

### リターンコード

リターンコード0以外はエラーとして「error occured from oto2lab.exe」を
標準出力エリアに表示します

## 更新履歴

-   2.1.0

    -   Debug mode を削除
    -   Kana Alias は残してあるけどoto2lab本体は未実装

-   2.0.0
    -   オプション「svp to oto」を追加
    -   追加オプション「Debug mode」「Kana Alias」を追加
    -   ウィンドウサイズを変更可能に更新
