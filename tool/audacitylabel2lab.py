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
from sys import exit

import utaupy as up


def audacitylabelfile2labfile(inpath, outpath):
    """
    txt (Audacityのラベル) -> lab (歌唱DBモノフォンラベル)
    単一ファイルを変換
    """
    l = up.label.load_as_plainlist(inpath, kiritan=True)
    lines = ['{}\t{}\t{}'.format(*v) for v in l]
    # ファイル出力
    with open(path, mode=mode, encoding=encoding, newline=newline) as f:
        f.write('\n'.join(lines))


def main():
    p = input('Input Audacity label txt path (file or dir)\n>>> ')
    if os.path.isdir(p):
        txtfiles = glob('{}/*.{}'.format(p, 'txt'))
    else:
        if not p.endswith('.txt'):
            print('[ERROR] txt ではないファイルが入力されました。終了します。')
            input('Press Enter to exit')
            exit()
        txtfiles = [p]
    print('\n処理対象ファイル')
    pprint(txtfiles)
    print('\n始めます')
    for path_txt in txtfiles:
        print('  processing:', path_txt)
        path_lab = path_txt.replace('.txt', '.lab')
        audacitylabelfile2labfile(path_txt, path_lab)
    print('終わりました')


if __name__ == '__main__':
    print('---Audacity用ラベルを歌唱DB用ラベルにするツール(20200711)---')
    main()
    print('Press Enter to exit')
