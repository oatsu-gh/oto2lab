# split_wav_and_lab

休符でフルコンテキストラベルと音声ファイルを分割する。

## 分割パターン

### sil-pau（前奏）

何もしない

### pau-pau

pau と pau の境界で分割する。

### pau-sil-pau

sil と pau の境界で分割する。

### pau-sil-sil-pau

sil と sil の境界で分割する。

### pau-sil-sil-sil-sil-pau

sil と sil の境界で分割し、単独となったsilの部分は破棄する。

### pau-sil（後奏）

何もしない

## 処理手順

1. モノラベルの数値をフルラベルに転写する。
2. フルラベル中の休符連続を検出する。
3. フルラベルを分割する。このとき、sil のみのラベル（前奏を除く）は破棄する。
4. 