#!/usr/bin/env python3
# coding: utf-8
"""
・lab→iniの変換ツール
・きりたんDBをUTAU化するとか。
"""

import os
import re
# import sys
from datetime import datetime
from glob import glob
# from pathlib import Path
from pprint import pprint


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
    開始時刻 → 左ブランク=オーバーラップ=先行発声
    終了時刻 → 右ブランク
    発音     → エイリアス
    """
    otolist = []

    for v in mono_oto:
        d = {}
        t_start = v[0] * 1000
        t_length = round((v[0] - v[1]) * 1000, 4)

        d['ファイル名'] = name_wav
        d['エイリアス'] = v[2]
        d['左ブランク'] = t_start
        d['固定範囲'] = 0
        d['右ブランク'] = t_length
        d['先行発声'] = 0
        d['オーバーラップ'] = 0
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


def read_vowel_consonant(path_vowel_consonant):
    """
    母音, 子音, 特殊文字列 の判定用ファイルを読み取って辞書を返す。
    """
    with open(path_vowel_consonant, 'r') as f:
        l = [v.split() for v in f.readlines()]
    d = {'Vowel': l[0], 'Consonant': l[1], 'Special': l[2]}

    return d


def mono_oto2cv_oto(mono_oto, path_vowel_consonant):
    """
    モノフォンの LAB 用リストを
    単独音(ローマ字CV)の リストに変換
    [[子音開始時刻(=オーバーラップ), 母音開始時刻(=先行発声), 終了時刻=右ブランク], [], ...]
    """
    d = read_vowel_consonant(path_vowel_consonant)
    l = []
    cv_oto = []
    s_prev = 's_prev'  # 直前の発音記号
    t_prev = 0  # 直前のノート長

    # 平仮名に変換する前に、子音と母音のデータを結合する。
    # NOTE: 各値が右ブランクを超えないように気を付ける
    for v in mono_oto:
        s = v[2]  # 発音記号
        t = (v[1] - v[0]) * 1000  # ノート長
        onset = 50  # 先行発声のデフォルト値(ms)

        # 一時ファイルを初期化 [子音開始時刻, 終了時刻, 発音(CV), 子音母音境界時刻]
        l = []

        if s in d['Special']:
            # 特殊文字はそのまま入れる
            l.append(round(v[0] * 1000, 4))
            l.append(round(v[1] * 1000, 4))
            l.append(s)
            l.append(min(v[0] * 1000 + t + onset, l[0]))
        elif s in d['Consonant']:
            # 子音はスキップ
            s_prev = s  # 発音記号を引き継ぎ
            t_prev = t  # ノート長を引き継ぎ
            continue
        elif s in d['Vowel'] and s_prev in d['Consonant']:
            # 子音+母音の組み合わせ
            cv = s_prev + s
            l.append(round(v[0] * 1000 - t_prev, 4))
            l.append(round(v[1] * 1000, 4))
            l.append(cv)
            l.append(round(v[0] * 1000, 4))
        elif s in d['Vowel'] and s_prev in d['Vowel']:
            # 母音→母音はそのまま入れる
            l.append(round(v[0] * 1000, 4))
            l.append(round(v[1] * 1000, 4))
            l.append(s)
            l.append(min(v[0] * 1000 + t + onset, l[0]))
        elif s in d['Vowel'] and s_prev in d['Special']:
            # 特殊→母音はそのまま入れる
            l.append(round(v[0] * 1000, 4))
            l.append(round(v[1] * 1000, 4))
            l.append(s)
            l.append(min(v[0] * 1000 + t + onset, l[0]))
        else:
            print('\n[ERROR]------------------------------------------------')
            print('子音の連続 あるいは 想定外の発音文字 が含まれています。')
            print('直前の文字列: {}'.format(s_prev))
            print('対象の文字列: {}'.format(s))
            print('特殊文字として処理し、続行します。')
            print('-------------------------------------------------------\n')
            l.append(round(v[0] * 1000, 4))
            l.append(round(t, 4))
            l.append(s)
            l.append(min(v[0] * 1000 + t + onset, l[0]))

        s_prev = s  # 直前の発音記号に引き継ぎ
        t_prev = t  # 直前のノート長に引き継ぎ
        cv_oto.append(l)

    return cv_oto


def cv_oto2otolist(cv_oto, name_wav, fix=50):
    """
    ローマ字CV形式のデータをINI用に変換する。
    utauモードではUTAU音源として使えるように 左右ブランクを補正する。
    fix: 子音部の後の固定範囲の長さ
    # NOTE: 発音記号は平仮名の方が良いよね。
    """
    l = []
    keys = ('ファイル名', 'エイリアス', '左ブランク', '固定範囲', '右ブランク', '先行発声', 'オーバーラップ')

    for v in cv_oto:
        t = round(v[1] - v[0])  # ノート長
        onset = round(v[3] - v[0], 4)  # 先行発声の相対時刻
        tmp = []
        tmp.append(name_wav)  # ファイル名
        tmp.append(v[2])  # エイリアス
        tmp.append(round(v[0], 4))  # 左ブランク
        if v[2] == 'br':
            tmp.append(t)  # ブレスの時は全体を子音部固定範囲にする
        else:
            tmp.append(min(t, round(onset + fix, 4)))  # 固定範囲 = s先行発声 + 100ms
        tmp.append(- t)  # 右ブランク
        tmp.append(onset)  # 先行発声
        tmp.append(0)  # オーバーラップ
        l.append(tmp)

    # 二次元リストを辞書のリストに変換
    otolist = [dict(zip(keys, v)) for v in l]
    return otolist


def otolist_for_utau(otolist, overlap=10):
    """
    UTAU音源にするために
    ・オーバーラップ領域を作る（dt[ms]）
    ・右ブランクを削る
    """
    dt = overlap

    otolist_utau = []
    for d in otolist:
        # 数値以外は引き継ぎ
        d_new = {'ファイル名': d['ファイル名'], 'エイリアス': d['エイリアス']}
        # 左ブランクは左に移動、それ以外は移動しないように補正
        d_new['左ブランク'] = round(d['左ブランク'] - dt, 4)
        d_new['オーバーラップ'] = round(d['オーバーラップ'] + dt, 4)
        d_new['先行発声'] = round(d['先行発声'] + dt, 4)
        if d['エイリアス'] == 'br':
            d_new['エイリアス'] = '息'
            d_new['固定範囲'] = d['固定範囲']
            d_new['右ブランク'] = d['右ブランク']
        elif d['エイリアス'] == 'pau':
            d_new['エイリアス'] = 'R'
            d_new['固定範囲'] = d['固定範囲']
            d_new['右ブランク'] = d['右ブランク']
        else:
            d_new['固定範囲'] = round(d['固定範囲'] + dt, 4)
            d_new['右ブランク'] = max(- round(200 + dt, 4), d['右ブランク'] + 20)
        otolist_utau.append(d_new)

    return otolist_utau


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
    path_ini = './ini/{}__{}.ini'.format(name_lab.rstrip('.lab'), datetime.now().strftime('%Y%m%d_%H%M%S'))
    with open(path_ini, 'w', encoding='shift-jis') as f:
        f.write(s)

    return path_ini


def simple_filename(filepath):
    """
    name__YYYYmmDD_HHMMSS.ext や
    name__YYYYmmDD_HHMMSS__YYYYmmDD_HHMMSS.ext のような文字列を
    name.ext に変換
    """
    basename = os.path.basename(filepath)
    basename_without_ext, ext = os.path.splitext(basename)
    simple_name = re.split(r'__\d+_\d+', basename_without_ext, 1)[0] + ext
    return simple_name


def lab2ini_solo(path_lab, alies='mono', utau=False):
    """
    ini->lab 変換を単独ファイルに実行
    filepath: labファイルのパス
    alies: iniのエイリアス形式 ('mono', 'cv', 'vcv')
    """
    # iniファイル名を取得
    name_lab = os.path.basename(path_lab)
    # iniに登録するwavファイル名を決定
    name_wav = simple_filename(path_lab).replace('.lab', '.wav')
    # labを読み取り
    mono_oto = read_lab(path_lab)
    # ini用のデータ構造に変換
    if alies == 'mono':
        otolist = mono_oto2otolist(mono_oto, name_wav)
    elif alies == 'cv':
        path_vcs = './table/vowel_consonant_sinsy.txt'
        cv_oto = mono_oto2cv_oto(mono_oto, path_vcs)
        otolist = cv_oto2otolist(cv_oto, name_wav)
    elif alies == 'vcv':
        print('\n[MATTE] 連続音形式は未対応です。\n')
    elif alies == 'cvvc':
        print('\n[SUMAN] CVVC形式は未対応です。\n')
    else:
        print('\n[ERROR] 開発者はlab2iniのモードを設定し直してください。')
    # iniファイル書き出し
    path_ini = write_ini(otolist, name_lab)

    # 出力ファイルの相対パスを返す
    return path_ini


def lab2ini_multi(dir_ini, alies='mono', utau=False):
    """
    lab -> ini 変換を複数ファイルに実行
    """
    print('変換モード: {}'.format(alies))
    print('UTAUモード: {}'.format(utau))

    if alies == 'mono':
        print('モノフォン形式のINIに変換します。')
    elif alies == 'cv':
        print('単独音形式のINIに変換します。')
    elif alies == 'vcv':
        print('連続音形式のINIに変換します。')
    elif alies == 'cvvc':
        print('CV-VC形式のINIに変換します')
    if utau is True:
        print('UTAU音源化モードで実行します。')

    # labファイルを一括取得
    lab_files = glob('{}/*.lab'.format(dir_ini))
    print('\nlab -> ini 一括変換します。')
    print('入力LAB一覧-------------------')
    pprint(lab_files)
    print('------------------------------')

    # 出力したiniファイルのリスト
    ini_files = []
    # ファイルをひとつずつ変換
    for path_lab in lab_files:
        path_ini = lab2ini_solo(path_lab, alies=alies, utau=utau)
        ini_files.append(path_ini)
    print('\nlab -> ini 一括変換しました。')
    print('出力INI一覧-------------------')
    pprint(ini_files)
    print('------------------------------')


def main():
    """
    デバッグ終わるまで未実装
    """
    print('実行内容を数字で選択してください。')
    print('1 ... LAB -> INI の変換 (単独ファイル)')
    print('2 ... LAB -> INI の変換 (複数ファイル)')

    mode = input('>>> ')
    # 指定ファイルを変換
    if mode in ['1', '１']:
        print('\nLAB ファイルを指定してください。')
        path_lab = input('>>> ').strip('""')
        print('\nLAB -> INI 変換します。')
        path_ini = lab2ini_solo(path_lab, alies='mono', utau=False)
        print('\nINI ファイルを出力しました。')
        print('出力ファイル:', path_ini)

    # 'lab'フォルダ内にあるlabファイルを変換
    elif mode in ['2', '２']:
        lab2ini_multi('lab', alies='mono', utau=False)

    else:
        print('1 か 2 で選んでください。\n')
        main()


if __name__ == '__main__':
    main()
    input('\nPress enter to exit.')
