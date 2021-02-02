#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) oatsu
"""
歌唱データベースの発声時間の和を求めるツール
複数または単一のlabファイルから計算します。
"""
import csv
import os
from glob import glob
from pprint import pprint

import utaupy as up


def get_voiced_part_length(label):
    """
    utaupy.label.Label オブジェクトの発声区間の和を求める。
    """
    non_voice = ('br', 'cl', 'pau', 'sil')
    t = 0  # 発声時間を蓄える変数
    for phoneme in label:
        if phoneme.symbol not in non_voice:
            t += phoneme.end - phoneme.start  # 発声時間を加算
    return t


def main():
    """
    pathを渡して結果をファイル出力
    """
    path_labdir = input('LABファイルがあるフォルダを指定してください。\n>>> ').strip('"')
    path_labfiles = glob(f'{path_labdir}/**/*.lab', recursive=True)
    print('処理対象ラベルファイル一覧----')
    pprint(path_labfiles)
    print('------------------------------')

    result = []  # LAB解析結果を蓄える変数
    t_total = 0  # 合計時間を蓄える変数
    for path_lab in path_labfiles:
        label = up.label.load(path_lab)
        name = os.path.basename(path_lab)
        length = int(get_voiced_part_length(label) / 10**7)
        t_total += length
        result.append([name, length])

    print(f'total: {t_total} seconds')
    result = [['TOTAL_VOICED_PART_LENGTH[seconds]', t_total]] + result

    basename_labdir = os.path.basename(path_labdir)
    with open(f'./result__{basename_labdir}.csv', mode='w', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerows(result)


if __name__ == '__main__':
    print('_____ξ・ヮ・) < voiced part length from lab v0.0.1 ________')
    print('Copyright (c) 2001-2020 Python Software Foundation')
    print('Copyright (c) 2020 oatsu\n')
    main()
    input('Press Enter to exit')
