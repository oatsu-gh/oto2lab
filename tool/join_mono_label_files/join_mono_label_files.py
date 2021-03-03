#!/usr/bin/env python3
# coding: utf-8
"""
複数のモノラベルを結合する。
前のファイルの終了時刻を次のファイルの開始時刻にする。
"""
from glob import glob

import utaupy as up


def main():
	"""
    複数のファイルをドラッグアンドドロップで指定？して結合したい。
    フォルダ内でいいかなあ
    """
    path_dir_in = input('path_dir_in: ').strip('"')
    labfiles = glob('path_dir_in/*.lab').sorted()
    label_objects = [up.label.load(path) for path in path_dir_in]
    new_label = up.label.Label()
    new_label += label_objects[0]
    for i, label in enumerate(label_objects[1:], 1):
        # オフセット設定するメソッドが欲しいと思った。
        # t_start = label.global_start
        offset = label[i-1][-1].end
        print(f'{i}\toffset[100ns]: {offset}')
        for phoneme in label:
            phoneme.start += offset
            phoneme.end += offset
        new_label += label

if __name__ == '__main__':
    main()
