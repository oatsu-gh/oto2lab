#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
モノフォンラベルの休符連続を検出する。Sinsy準拠に改変されていることが条件。
"""

from glob import glob

import utaupy as up
from tqdm import tqdm


def load_all_labels(path_dir):
    """
    対象のラベルを一気にロードする。
    """
    all_paths = glob(f'{path_dir}/**/*.lab', recursive=True)
    labels = [up.label.load(path) for path in all_paths]
    return labels


def detect_paupau(label):
    """
    pau-pau, sil-sil, pau-sil, sil-pau の並びを検出する。
    """
    pau_and_sil = ('pau', 'sil')

    pau_pau = 0
    pau_sil = 0
    sil_sil = 0
    sil_pau = 0

    for i, phoneme in enumerate(label[:-1]):
        current_symbol = phoneme.symbol
        next_symbol = label[i + 1].symbol
        if not (current_symbol in pau_and_sil and next_symbol in pau_and_sil):
            continue
        if current_symbol == 'pau' and next_symbol == 'pau':
            pau_pau += 1
        elif current_symbol == 'pau' and next_symbol == 'sil':
            pau_sil += 1
        elif current_symbol == 'sil' and next_symbol == 'sil':
            sil_sil += 1
        elif current_symbol == 'sil' and next_symbol == 'pau':
            sil_pau += 1
        else:
            print('は？')
    return pau_pau, pau_sil, sil_sil, sil_pau


def main():
    path_dir = input('path_dir: ').strip('"')
    labels = load_all_labels(path_dir)
    pau_pau, pau_sil, sil_sil, sil_pau = (0, 0, 0, 0)
    for label in tqdm(labels):
        l = detect_paupau(label)
        pau_pau += l[0]
        pau_sil += l[1]
        sil_sil += l[2]
        sil_pau += l[3]

    s = f'pau_pau: {pau_pau}\npau_sil: {pau_sil}\nsil_sil: {sil_sil}\nsil_pau: {sil_pau}\n'
    print(s)
    with open('result.txt', mode='w', encoding='utf-8') as f:
        f.write(s)

if __name__ == '__main__':
    main()
