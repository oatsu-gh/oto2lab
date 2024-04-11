#!/usr/bin/env python3
# Copyright (c) 2021 oatsu
"""
DB中のラベルの音素数をカウントする。
"""

PHONEME_IGNORE = {'pau', 'sil', 'br'}

import utaupy
from glob import glob

def main():
    path_database = input('path_database: ').strip('"')
    lab_files = glob(f'{path_database}/**/*.lab', recursive=True)
    all_phonemes = []
    for path_lab in lab_files:
        all_phonemes += utaupy.label.load(path_lab).data
    # 発生時間の合計
    total_duration = sum(phoneme.duration for phoneme in all_phonemes
                         if phoneme.symbol not in PHONEME_IGNORE)
    n_phonemes = len([phoneme for phoneme in all_phonemes
                     if phoneme.symbol not in PHONEME_IGNORE])
    print('n_phonemes:', n_phonemes)
    print('total_duration:', round(total_duration / 10000000), '[s]')
    print('PHONEME_IGNORE:', PHONEME_IGNORE)

if __name__ == '__main__':
    main()
