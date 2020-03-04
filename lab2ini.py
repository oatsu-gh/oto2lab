#!/usr/bin/env python3
# coding: utf-8
"""
・lab→iniの変換ツール
・きりたんDBをUTAU化するとか。
"""
# import os
# import re
# import sys
from datetime import datetime
# from glob import glob
# from pathlib import Path
# from pprint import pprint


def read_lab(path_lab):
    """
    labファイルを読み取ってリストにする。
    [[開始時刻, 終了時刻, 発音], [], ...]
    """
    # LABファイルを読み取り
    with open(path_lab, 'r') as f:
        l = [s.strip().split() for s in f.readlines()]

    # 入力ファイル末尾の空白行を除去
    while l[-1] == ['']:
        del l[-1]

    # リストにする [[開始時刻, 終了時刻, 発音], [], ...]
    mono_oto = []
    for v in l:
        mono_oto.append([float(v[0]), float(v[1]), v[2]])

    return mono_oto  # mono_otoに相当


def mono_oto2otolist(mono_oto, name_wav):
    """
    LAB 用データのリスト [[開始時刻, 終了時刻, 発音], [], ...] を
    INI 用データのリスト [{key: value, {}, ...}, ...] に変換
    """
    otolist = []
    keys = ('ファイル名', 'エイリアス', '左ブランク', '固定範囲', '右ブランク', '先行発声', 'オーバーラップ')
    for v in mono_oto:
        l = list(map(str, [name_wav, v[2], v[0] * 1000, 200, -500, 100, 0]))
        d = dict(zip(keys, l))
        otolist.append(d)

    return otolist


def write_ini(otolist, name_lab):
    """
    INI 用データのリストを文字列に変換してファイル出力
    """
    # データを文字列に変換
    s = ''
    for d in otolist:
        l = [d['ファイル名'], d['エイリアス'], d['左ブランク'], d['固定範囲'], d['右ブランク'], d['先行発声'], d['オーバーラップ']]
        s += '{}={},{},{},{},{},{}\n'.format(*l) # l[0]=l[1],l[2],...

    # ファイル作成とデータ書き込み
    path_ini = './ini/' + name_lab + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.ini'
    with open(path_ini, 'w', encoding='shift-jis') as f:
        f.write(s)

    return path_ini


def main():
    """
    デバッグ終わるまで未実装
    """
    print('lab2ini_solo でデバッグしてください。')


if __name__ == '__main__':
    main()
