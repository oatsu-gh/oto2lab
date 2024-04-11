#!/usr/bin/env python3
# Copyright (c) 2021 oatsu
"""
oto2labで子音開始時刻が直前の母音開始時刻より昔になっているのを修正する。
setParamではなくPraatなどでラベリングするときに、
UST->INI->LAB変換した際の不具合対策を想定している。
"""

from glob import glob
from os import makedirs
from os.path import basename, isfile, join

import utaupy


def fix_labelobj(label):
    """
    ラベルオブジェクトを直す。
    """
    previous_phoneme = label[0]
    for phoneme in label[1:]:
        if phoneme.start < previous_phoneme.start:
            print('  なおすよ')
            phoneme.start = round((previous_phoneme.start + phoneme.end) / 2)
        previous_phoneme = phoneme
    label.reload()
    label.is_valid()


def main():
    """
    ファイル入出力と読み取りする
    """
    in_dir = input('入力ファイルまたはフォルダを指定してください。\n>>> ').strip()
    out_dir = 'result'
    makedirs(out_dir, exist_ok=True)

    if isfile(in_dir):
        lab_files = [in_dir]
    else:
        lab_files = glob(f'{in_dir}/*.lab') + glob(f'{in_dir}/*/*.lab')
    for path_lab_in in lab_files:
        print(basename(path_lab_in))
        path_lab_out = join(out_dir, basename(path_lab_in))
        label = utaupy.label.load(path_lab_in)
        fix_labelobj(label)
        label.write(path_lab_out)


if __name__ == '__main__':
    main()
