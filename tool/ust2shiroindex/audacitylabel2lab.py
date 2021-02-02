#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
txt (Audacityのラベル) -> lab (歌唱DBモノフォンラベル) の変換
読み取って、時間単位と区切り文字変えて保存するだけ。
"""
import os
from glob import glob
from pprint import pprint

import utaupy as up


def audacitylabelfile2labfile(path_audacitylabel_in:str, path_lab_out:str):
    """
    txt (Audacityのラベル) -> lab (歌唱DBモノフォンラベル)
    単一ファイルを変換
    """
    label = up.label.load(path_audacitylabel_in, time_unit='s')
    # ファイル出力
    label.write(path_lab_out, time_unit='100ns')


def main():
    """
    フォルダを指定して処理
    """
    path_in = input('Input Audacity label txt path (file or dir)\n>>> ').strip('"')
    if os.path.isdir(path_in):
        txt_files = glob('{}/*.{}'.format(path_in, 'txt'))
    else:
        if not path_in.endswith('.txt'):
            raise ValueError('txt ではないファイルが入力されました。終了します。')
        txt_files = [path_in]

    print('\n処理対象ファイル')
    pprint(txt_files)
    print('\n始めます')
    for path_txt in txt_files:
        print('  processing:', path_txt)
        path_lab = path_txt.replace('.txt', '.lab')
        audacitylabelfile2labfile(path_txt, path_lab)
    print('終わりました')


if __name__ == '__main__':
    print('---Audacity用ラベルを歌唱DB用ラベルにするツール(20210202)---')
    main()
    print('Press Enter to exit')
