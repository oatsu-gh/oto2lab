#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) oatsu
"""
歌唱DBをUTAU音源化する
wavファイルと同じディレクトリにoto.iniを生成する。
"""
import os
from glob import glob
from pprint import pprint

import utaupy as up
PATH_TABLE = './romaji2kana_sjis.table'
CONSONANTS = ['b', 'by', 'ch', 'd', 'dy', 'f', 'g', 'gy', 'h', 'hy', 'j',
              'k', 'ky', 'm', 'my', 'n', 'ny', 'p', 'py', 'r', 'ry', 's',
              'sh', 't', 'ts', 'ty', 'v', 'w', 'y', 'z']
VOWELS = ['a', 'i', 'u', 'e', 'o', 'N']
# VOWELS = ['a', 'i', 'u', 'e', 'o', 'N', 'cl']


def label2otoini_for_utau(label, name_wav, table, dt=100, threshold=300):
    """
    LabelオブジェクトをOtoIniオブジェクトに変換
    UTAU音源として使えるようにチューニングする。

    |   dt      |     子音      |   dt    |  残りの母音   |
    |左ブランク |オーバーラップ |先行発声 |子音部固定範囲 |右ブランク
    """
    # time_order_ratio = label_time_order / otoini_time_order
    time_order_ratio = 10**(-4)

    l = []  # Otoオブジェクトを格納するリスト
    phonemes = label.values

    # ラベルの各PhoenmeオブジェクトをOtoオブジェクトに変換して、リストにまとめる。
    tmp = []
    prev_vowel = '-'
    for phoneme in phonemes:
        if phoneme.symbol in CONSONANTS:
            tmp.append(phoneme)
        elif phoneme.symbol in VOWELS:
            if time_order_ratio * (phoneme.end - phoneme.start) > threshold:
                tmp.append(phoneme)
                oto = up.otoini.Oto()
                oto.filename = name_wav
                try:
                    kana = table[''.join([ph.symbol for ph in tmp])][0]
                    oto.alias = '{} {}'.format(prev_vowel, kana)
                    # oto.alias = '{}'.format(''.join([ph.symbol for ph in tmp]))
                    oto.offset = (time_order_ratio * tmp[0].start) - dt
                    oto.overlap = dt
                    oto.preutterance = (time_order_ratio * tmp[-1].start) - oto.offset
                    oto.consonant = oto.preutterance + dt
                    oto.cutoff2 = time_order_ratio * tmp[-1].end - dt
                    l.append(oto)
                except KeyError as err:
                    print('[ERROR]:', err)
            tmp = []
            prev_vowel = phoneme.symbol.replace('N', 'n')
        else:
            tmp = []
            prev_vowel = '-'

    # Otoiniオブジェクト化
    otoini = up.otoini.OtoIni()
    otoini.values = l
    return otoini


def labfiles2inifile_for_utau(path_labdir, path_table, dt=100, kiritan=False):
    """
    ファイル入出力とオブジェクト変換処理
    """
    labfiles = glob(f'{path_labdir}/**/*.lab', recursive=True)
    pprint(labfiles)
    table = up.table.load(path_table)
    l = []
    for path_lab in labfiles:
        basename_wav = os.path.basename(path_lab).replace('.lab', '.wav')
        label = up.label.load(path_lab, kiritan=kiritan)
        otoini = label2otoini_for_utau(label, basename_wav, table, dt=dt)
        l += otoini.values
    total_otoini = up.otoini.OtoIni()
    total_otoini.values = l
    print('登録エイリアス数:', len(total_otoini.values))
    total_otoini.write(path_labdir + '/oto.ini')


def main():
    """
    パラメータとパスを指定して実行
    """
    path_labdir = input('path_labdir: ')
    # 左ブランクとかのずらす長さ
    dt = float(input('dt_shift: '))
    path_table = PATH_TABLE
    labfiles2inifile_for_utau(path_labdir, path_table, dt=dt, kiritan=False)


if __name__ == '__main__':
    main()
    print()
    input('Press Enter to exit')
