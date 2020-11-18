#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
休符音素の連続を検知する。
"""

import utaupy as up
from glob import glob

def check_label(path_lab:str) -> list:
    """
    utaupy.label.Label オブジェクト内の休符連続を検査
    """
    label = up.label.load(path_lab)
    l_outer = []
    rest_phoneme = ('pau', 'sil')
    previous_phoneme = label[0]
    for phoneme in label[1:]:
        if (previous_phoneme.symbol in rest_phoneme) and (phoneme.symbol in rest_phoneme):
            l_inner = [previous_phoneme, phoneme]
            l_outer.append('\t'.join((str(lab) for lab in l_inner)))
            print('休符音素連続を検出しました。')
            print(previous_phoneme)
            print(phoneme)
            print('--------------------------------------------')
        previous_phoneme = phoneme
    return l_outer

def main():
    path_dir_lab = input('path_dir_lab: ').strip('"')
    lab_files = glob(f'{path_dir_lab}/**/*.lab', recursive=True)
    total_result = []
    for path_lab in lab_files:
        print(path_lab)
        result = check_label(path_lab)
        if len(result) != 0:
            total_result.append(f'\n{path_lab}')
            total_result.append('\n'.join(result))


    str_total_result = '\n'.join(total_result)

    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write(str_total_result)

if __name__ == '__main__':
    main()
