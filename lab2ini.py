#!/usr/bin/env python3
# coding: utf-8
"""
・lab→iniの変換ツール
・きりたんDBをUTAU化するとか。
"""

# import re
# import sys
from datetime import datetime

# import os
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


def read_japanesetable(path_japanesetable):
    """
    平仮名-ローマ字変換表を読み取って変換用の辞書を返す。
    {'変換元': ['母音', '子音'], ...}
    """
    # 平仮名とローマ字の対応表を辞書にする
    with open(path_japanesetable, 'r') as f:
        l = [v.split() for v in f.readlines()]

    d = {}
    for v in l:
        d[v[0]] = v[1:]

    return d


def read_vowel_consonant_special(path_vowel_consonant_special):
    """
    母音, 子音, 特殊文字列 の判定用ファイルを読み取って辞書を返す。
    """
    with open(path_vowel_consonant_special, 'r') as f:
        l = [v.split() for v in f.readlines()]
    d = {'Vowel': l[0], 'Consonant': l[1], 'Special': l[2]}

    return d


def mono_oto2cv_oto(mono_oto, path_vowel_consonant_special):
    """
    モノフォンの LAB 用リストを
    単独音(ローマ字CV)の リストに変換
    [[子音開始時刻(=オーバーラップ), 母音開始時刻(=先行発声), 終了時刻=右ブランク], [], ...]
    """
    d = read_vowel_consonant_special(path_vowel_consonant_special)
    l = []
    cv_oto = []
    s_prev = 's_prev'  # 直前の発音記号
    t_prev = 0  # 直前のノート長

    # 平仮名に変換する前に、子音と母音のデータを結合する。
    # NOTE: 各値が右ブランクを超えないように気を付ける
    for v in mono_oto:
        s = v[2]  # 発音記号
        t = (v[1] - v[0]) * 1000  # ノート長

        # 一時ファイルを初期化
        # [子音開始時刻, 終了時刻, 発音(CV), 子音母音境界時刻]
        l = []

        if s in d['Special']:
            # 特殊文字はそのまま入れる
            l.append(round(v[0] * 1000, 3))
            l.append(round(v[1] * 1000, 3))
            l.append(s)
            l.append(l[0])

        elif s in d['Consonant']:
            # 子音はスキップ
            s_prev = s  # 直前の発音記号に引き継ぎ
            t_prev = t  # 直前のノート長に引き継ぎ
            continue

        elif s in d['Vowel'] and s_prev in d['Consonant']:
            # 子音+母音の組み合わせ
            cv = s_prev + s
            l.append(round(v[0] * 1000 - t_prev, 3))
            l.append(round(v[1] * 1000 + t_prev, 3))
            l.append(cv)
            l.append(round(v[1] * 1000, 3))

        elif s in d['Vowel'] and s_prev in d['Vowel']:
            # 母音→母音はそのまま入れる
            l.append(round(v[0] * 1000, 3))
            l.append(round(v[1] * 1000, 3))
            l.append(s)
            l.append(l[0])

        elif s in d['Vowel'] and s_prev in d['Special']:
            # 特殊→母音はそのまま入れる
            l.append(round(v[0] * 1000, 3))
            l.append(round(v[1] * 1000, 3))
            l.append(s)
            l.append(l[0])

        else:
            print('\n[ERROR]------------------------------------------------')
            print('子音の連続 あるいは 想定外の発音文字 が含まれています。')
            print('直前の文字列: {}'.format(s_prev))
            print('対象の文字列: {}'.format(s))
            print('特殊文字として処理し、続行します。')
            print('-------------------------------------------------------\n')
            l.append(round(v[0] * 1000, 3))
            l.append(round(t, 3))
            l.append(s)
            l.append(l[0])

        s_prev = s  # 直前の発音記号に引き継ぎ
        t_prev = t  # 直前のノート長に引き継ぎ
        cv_oto.append(l)

    print('\nl--------------------')
    return cv_oto


def write_ini(otolist, name_lab):
    """
    INI 用データのリストを文字列に変換してファイル出力
    """
    # データを文字列に変換
    s = ''
    for d in otolist:
        l = [d['ファイル名'], d['エイリアス'], d['左ブランク'], d['固定範囲'], d['右ブランク'], d['先行発声'], d['オーバーラップ']]
        s += '{}={},{},{},{},{},{}\n'.format(*l)  # l[0]=l[1],l[2],...

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
