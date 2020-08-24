#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) oatsu
"""
歌唱DBのモノフォンラベルファイルをREAPERのリージョンようCSVに変換する
v0.0.1
- フォルダごと処理できるようにした。
"""

import datetime
import os
from glob import glob
from pprint import pprint

import utaupy as up


def label2regioncsv(label):
    """
    ラベルオブジェクト（？）をリージョンCSV用のオブジェクトに変換する。
    """
    l = label.values
    regioncsv = up.reaper.RegionCsv()
    for phoneme in l:
        region = up.reaper.Region()
        region.name = phoneme.symbol
        region.start = datetime.timedelta(seconds = phoneme.start * (10**(-7)))
        region.end = datetime.timedelta(seconds = phoneme.end * (10**(-7)))
        regioncsv.append(region)
    return regioncsv


def labfile2regionfile(inpath, outpath):
    """
    ファイル変換をする。
    """
    print('converting LAB to CSV :', inpath)
    label = up.label.load(inpath)
    regioncsv = label2regioncsv(label)
    regioncsv.write(outpath)
    print('converted  LAB to CSV :', outpath)


def main():
    """
    パスを入力させて処理を実行する
    """
    path_labdir = input('labfileがあるフォルダのパスを入力してください。（再帰的に取得します。）\n>>> ').strip('\"')
    l = glob(f'{path_labdir}/**/*.lab')
    pprint(l)
    for path_lab in l:
        path_outcsv = os.path.splitext(path_lab)[0] + '.csv'
        # ファイル変換
        labfile2regionfile(path_lab, path_outcsv)



if __name__ == '__main__':
    print('_____ξ・ヮ・) < lab2region v0.0.1 ________')
    print('音素ラベルからリージョンCSVを生成するツール')
    print('Copyright (c) 2001-2020 Python Software Foundation')
    print('Copyright (c) 2020 oatsu\n')
    main()
    input('Press Enter to exit')
