#!/usr/bin/env python3
# Copyright (c) 2020 oatsu
"""
音素の長さの分布を調査する。
指定したフォルダ内にあるモノラベルファイルをすべて取得して、csvか何かにして出力する。

とりあえず、
音素,duration
だけの大きいcsvを作ってExcelで処理させてみる？
"""

from glob import glob
from statistics import median, mode
from typing import Dict

import pandas as pd
import utaupy

# from typing import List


def load_mono_label_files(path_dir):
    """
    モノラベルを一括で読み取る
    """
    lab_files = glob(f'{path_dir}/**/*.lab', recursive=True)
    label_objects = [utaupy.label.load(path_lab) for path_lab in lab_files]
    return label_objects


def export_phoneme_duration_csv(label_objects, path_csv_out):
    """
    音素記号,duration
    のみのCSV出力
    """
    lines = []
    for label in label_objects:
        line = '\n'.join([f'{phoneme.symbol},{phoneme.duration // 10000}' for phoneme in label])
        lines.append(line)
    s = '\n'.join(lines)
    with open(path_csv_out, 'w', encoding='utf-8') as f:
        f.write(s)


def phoneme_duration_dict(label_objects) -> dict:
    """
    音素:[duration, duration]
    な辞書にする
    """
    d: Dict[str, list] = {}
    for label in label_objects:
        for phoneme in label:
            if phoneme.symbol in d:
                d[phoneme.symbol].append(round(phoneme.duration / 10000))
            else:
                d[phoneme.symbol] = [round(phoneme.duration / 10000)]
    for key, value in d.items():
        d[key] = sorted(value)
    return d


def export_discribed_data_txt(label_objects, path_out):
    """
    {音素: durationの最頻値}
    な辞書にする
    """
    d: Dict[str, list] = {}
    for label in label_objects:
        for phoneme in label:
            if phoneme.symbol in d:
                d[phoneme.symbol].append(phoneme.duration)
            else:
                d[phoneme.symbol] = [phoneme.duration]
    s = ''
    for k, v in d.items():
        s += '-----------------------------------\n'
        s += f'{k}\n'
        df = pd.DataFrame(v)
        s += str(df.describe())
        s += '\n'
    with open(path_out, 'w', encoding='utf-8')as f:
        f.write(s)


def export_phoneme_median_json(label_objects, path_json_out):
    """
    {音素: durationの最頻値}
    な辞書にする
    """
    d: Dict[str, list] = {}
    for label in label_objects:
        for phoneme in label:
            if phoneme.symbol in d:
                d[phoneme.symbol].append(round(phoneme.duration))
            else:
                d[phoneme.symbol] = [round(phoneme.duration)]
    d_median = {key: round(median(value) / 50000) * 5 for key, value in d.items()}
    with open(path_json_out, 'w', encoding='utf-8')as f:
        f.write(str(d_median).replace('\'', '"'))


def main():
    path_dir = input('path_dir: ').strip('"')
    label_objects = load_mono_label_files(path_dir)
    # export_phoneme_duration_csv(label_objects, 'result_all_durations.csv')
    export_phoneme_median_json(label_objects, 'result_median.json')
    # export_discribed_data_txt(label_objects, 'result_discribed.txt')


if __name__ == '__main__':
    main()
