#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) oatsu
"""
歌唱DBのモノフォンラベルファイルをREAPERのリージョン用CSVに変換する
【更新履歴】
v0.0.1 ... utaupy.label の仕様変更に対応
"""

import datetime
import os
from pprint import pprint

import utaupy as up


def label2regioncsv(label):
    """
    ラベルオブジェクト（？）をリージョンCSV用のオブジェクトに変換する。
    """
    phonemes = label.values
    regioncsv = up.reaper.RegionCsv()
    for phoneme in phonemes:
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
    # 入力パス
    inpath = input('labファイルのパスを入力してください。\n>>> ').strip(r'"')
    # 出力パス
    outpath = os.path.splitext(inpath)[0] + '.csv'
    # ファイル変換
    labfile2regionfile(inpath, outpath)


if __name__ == '__main__':
    print('_____ξ・ヮ・) < lab2region v0.0.1 ________')
    print('音素ラベルからリージョンCSVを生成するツール')
    print('Copyright (c) 2001-2020 Python Software Foundation')
    print('Copyright (c) 2020 oatsu\n')
    main()
    input('Press Enter to exit')
