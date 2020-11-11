# dic

「かな → 音素」変換辞書

## フォルダ説明

### sinsy

- Sinsy に使用されるデフォルトの辞書を微改変
  - 「を」が必ず「o」に変換されるように修正

### sinsy_cl_disabled

- 現時点では使いません（2020/09/26）
- sinsy フォルダのものを、促音の扱いを変更
  - japanese.*.conf を改変
    - `PHONEME_CL="cl"` → `PHONEME_CL="cl_is_treated_as_normal_phoneme"`
  - musicxmlにおいて、「っ」を独立した音符として扱えることを期待