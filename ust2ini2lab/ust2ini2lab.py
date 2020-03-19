#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 oatsu
"""
setParam での音声ラベリング支援ツールです。
ファイル形式を変換できます。
・ust → ini （ExcelVBA を使用）
・ini → lab （Python 標準ライブラリのみで実行可能）
"""
import os
import re
import shutil
import sys
from datetime import datetime
from glob import glob
from pathlib import Path
from pprint import pprint

import win32com.client  # Excel操作に使用

import UtauPy as up

TEST_MODE = False


def run_ExecuteUstToOto(path_xlsm):
    """
    ust→ini 用のExcelVBAを実行する
    """
    abspath = str(Path(path_xlsm).resolve())  # 絶対パスに変換
    excel = win32com.client.Dispatch('Excel.Application')
    excel.Visible = 0  # Excelの表示設定（0:非表示, 1:表示）
    excel.Workbooks.Open(abspath, UpdateLinks=0, ReadOnly=True)  # 読み取り専用で開く

    excel.Application.Run('ExecuteUstToOto')  # マクロを実行
    excel.Workbooks(1).Close(SaveChanges=0)  # ブックを保存せずに閉じる
    excel.Application.Quit()


def evacuate_files(path_dir, ext):
    """
    指定したフォルダにある指定した拡張子のファイルを退避させる。
    上書きによるファイル消滅回避が目的。
    """
    ext = ext.replace('.', '')
    old_files = glob('{}/*.{}'.format(path_dir, ext))
    # 退避先のフォルダを作成
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_dir = '{}/old__{}'.format(path_dir, now)
    os.mkdir(new_dir)
    # 移動
    for p in old_files:
        shutil.move(p, new_dir)


def ust2ini_solo(path_ust):
    """
    USTを読み取ってINI向けリスト(otolist)に変換する
    """
    otolist = []
    t = 0
    ust = up.Ust()
    ust.read_ust(path_ust)
    bpm = ust.get_tempo()
    for note in ust.values()[2:]:
        tmp = [t]
        t = note.length()
        tmp.append(t)
        tmp.append(note.lyric().replace('R', 'pau'))
        otolist.append(tmp)
    return otolist


def read_ini(path_ini):
    """
    iniを読み取って辞書のリストを返す
    """
    with open(path_ini, 'r') as f:
        l = [re.split('[=,]', s.strip()) for s in f.readlines()]

    # 入力ファイル末尾の空白行を除去
    while l[-1] == ['']:
        del l[-1]

    # 配列を辞書に変換(覚えられないので)
    keys = ('ファイル名', 'エイリアス', '左ブランク', '固定範囲', '右ブランク', '先行発声', 'オーバーラップ')
    otolist = [dict(zip(keys, v)) for v in l]

    return otolist


def read_japanesetable(path_table):
    """
    平仮名-ローマ字変換表を読み取って変換用の辞書を返す。
    {'変換元': ['母音', '子音'], ...}
    """
    # 平仮名とローマ字の対応表を辞書にする
    with open(path_table, 'r') as f:
        l = [v.split() for v in f.readlines()]
    # d = {}
    d = {'R': 'pau', 'B': 'br', '息': 'br'}
    for v in l:
        d[v[0]] = v[1:]
    return d


def monophonize_oto(otolist):
    """
    ・入力iniは辞書のリスト[{}]
    ・iniのエイリアスをモノフォン化
    ・ラベルに不要なデータを破棄
    必要: オーバーラップ, 先行発声
    変換: エイリアス(→モノフォン)
    不要: 左ブランク, ファイル名, 固定範囲, 右ブランク
    ・リストを返す [[発音開始時刻, 発音記号], ...]
    """
    table = read_japanesetable('./table/japanese_sjis.table')  # {平仮名: [母音, 子音]} の辞書
    mono_kana = ['あ', 'い', 'う', 'え', 'お', 'ん', 'っ']  # モノフォン平仮名
    special = ['br', 'pau', 'cl', 'k', 's']  # 休符と無声子音
    # NOTE:「す」の無声化は「sU」と表現するらしい。

    l = []
    for v in otolist:
        # 連続音を単独音化
        kana = v['エイリアス'].split()[-1]

        # [発音開始時刻, 発音記号] の形式にする
        try:
            # モノフォン平仮名歌詞
            if kana in mono_kana:
                t_start = float(v['左ブランク']) + float(v['オーバーラップ'])
                l.append([t_start / 1000, table[kana][0]])
            # 想定内アルファベット歌詞
            elif kana in special:
                t_start = float(v['左ブランク']) + float(v['オーバーラップ'])
                l.append([t_start / 1000, kana])
            # ダイフォン平仮名歌(子音と母音に分割)
            else:
                t_start = float(v['左ブランク']) + float(v['オーバーラップ'])
                l.append([t_start / 1000, table[kana][0]])

                t_start = float(v['左ブランク']) + float(v['先行発声'])
                l.append([t_start / 1000, table[kana][1]])

        except KeyError as e:
            print('\n--[KeyError]--------------------')
            print('エイリアスをモノフォン化する過程でエラーが発生しました。')
            print('ノートの歌詞が想定外です。iniを編集してください。')
            print('使用可能な歌詞は japanese_sjis.table に記載されている平仮名と、br、pau、cl です。')
            print('\nエラー項目:', e)
            print('--------------------------------\n')
            print('プログラムを終了します。ファイル破損の心配は無いはずです。')
            sys.exit()

    return l  # mono_otoに相当


def write_lab(mono_oto, name_ini):
    """
    monophonize_ini でフォーマットした二次元リスト [[発音開始時刻, 発音記号], ...] から、
    きりたんDB式音声ラベルで oto_日付.lab に出力する
    """
    s = ''
    for i, v in enumerate(mono_oto):
        try:
            s += '{:.6f} {:.6f} {}\n'.format(v[0], mono_oto[i + 1][0], v[1])
        except IndexError:
            s += '{:.6f} {} {}\n'.format(v[0], v[0] + 1.0, v[1])

    # ファイル作成とデータ書き込み
    path_lab = './lab/{}__{}.lab'.format(name_ini, datetime.now().strftime('%Y%m%d_%H%M%S'))
    with open(path_lab, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)

    return path_lab


def ust2ini_Excel(dir_ust):
    """
    Excelのツールを使用してUST→INI変換
    """
    print('\nust -> ini 変換します。数秒かかります。')
    ust_files = glob('{}/*.ust'.format(dir_ust))
    if ust_files == []:
        print('[ERROR] ustファイルを設置してください。')
        input('Press Enter to exit.')
        sys.exit()

    print('入力UST一覧-------------------')
    pprint(ust_files)
    print('------------------------------')
    run_ExecuteUstToOto('歌声DBラベリング用ust→oto変換ツール.xlsm')
    print('ust -> ini 変換しました。')


def ini2lab_solo(path_ini):
    """
    oto->lab 変換を単独ファイルに実行
    """
    # oto.ini を読み取り
    otolist = read_ini(path_ini)
    if TEST_MODE:
        pprint(otolist)
        # 読み取ったデータを整形
    mono_oto = monophonize_oto(otolist)
    if TEST_MODE:
        print('mono_oto------------')
        pprint(mono_oto)
        print('--------------------')
    # lab を書き出し
    filename = path_ini.split('\\')[-1].rstrip('.ini')
    path_lab = write_lab(mono_oto, filename)
    return path_lab


def ini2lab_multi(dir_ini):
    """
    ini -> lab 変換を複数ファイルに実行
    """
    ini_files = glob('{}/*.ini'.format(dir_ini))
    print('\nini -> lab 変換します。')
    print('入力INI一覧-------------------')
    pprint(ini_files)
    print('------------------------------')
    lab_files = []
    for path_ini in ini_files:
        lab_files.append(ini2lab_solo(path_ini))
    print('\nini -> lab 変換しました。')

    print('出力LAB一覧-------------------')
    pprint(lab_files)
    print('------------------------------')


def main():
    """
    全体の処理を実行
    """
    print('実行内容を数字で選択してください。')
    print('1 ... UST -> INI の変換')
    print('2 ... INI -> LAB の変換')
    print('3 ... UST -> LAB の変換（INIも生成されます）')
    # print('3 ... INI <- LAB の変換')
    mode = input('>>> ')

    # 'ust'フォルダ内にあるustファイルを変換
    if mode in ['1', '１']:
        evacuate_files('ini', 'ini')
        ust2ini_Excel('ust')

    # 'ini'フォルダ内にあるiniファイルを変換
    elif mode in ['2', '２']:
        evacuate_files('lab', 'lab')
        ini2lab_multi('ini')

    # 'ust' フォルダにあるustファイルを一気にLABまで変換
    elif mode in ['3', '３']:
        evacuate_files('ini', 'ini')
        ust2ini_Excel('ust')
        evacuate_files('lab', 'lab')
        ini2lab_multi('ini')

    # elif mode in ['4', '４']:
    #     lab2ini_solo('lab')

    else:
        print('1 か 2 か 3 で選んでください。\n')
        main()


if __name__ == '__main__':
    main()
    while input('Press Enter to exit.') == 'r':
        main()
