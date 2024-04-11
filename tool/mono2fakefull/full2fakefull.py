#!/usr/bin/env python3
# Copyright (c) 2020 oatsu
"""
フルラベルをフルラベルっぽいやつに変換する。
いったんモノラベル作って作り直すのと同義。
指定したフォルダにあるフルラベルをすべて偽フルラベルとして上書きする。
"""

from glob import glob

import utaupy as up
from mono2fakefull import monolabel_file_to_fulllabel_file
from tqdm import tqdm


def full_to_mono(path_true_full_in, path_mono_out):
    """
    フルラベルをモノラベルとして上書きするだけ
    """
    up.hts.load(path_true_full_in).as_mono().write(path_mono_out)


def main():
    path_hts_conf = input('path_hts_conf: ')
    full_lab_dir = input('path_full_lab_dir: ')
    full_label_files = glob(f'{full_lab_dir}/**/*.lab', recursive=True)
    for path_lab in tqdm(full_label_files):
        full_to_mono(path_lab, path_lab)
    for path_lab in tqdm(full_label_files):
        monolabel_file_to_fulllabel_file(path_lab, path_lab, path_hts_conf)

if __name__ == '__main__':
    main()
