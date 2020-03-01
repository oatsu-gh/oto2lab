#!/usr/bin/env python3
# coding: utf-8
"""
setParam での音声ラベリング支援ツールです。
ファイル形式を変換できます。
・ust → ini （ExcelVBA を使用）
・ini → lab （Python 標準ライブラリのみで実行可能）
"""
# import os
import re
import sys
from datetime import datetime
from glob import glob
from pathlib import Path
from pprint import pprint

import win32com.client  # Excel操作に使用

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
    # sleep(0.1)
    excel.Application.Quit()
    # sleep(0.1)


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
                t_start = float(v['左ブランク']) / 1000 + float(v['オーバーラップ']) / 1000
                l.append([t_start, table[kana][0]])
            # 想定内アルファベット歌詞
            elif kana in special:
                t_start = float(v['左ブランク']) / 1000 + float(v['オーバーラップ']) / 1000
                l.append([t_start, kana])
            # ダイフォン平仮名歌(子音と母音に分割)
            else:
                t_start = float(v['左ブランク']) / 1000 + float(v['オーバーラップ']) / 1000
                l.append([t_start, table[kana][0]])

                t_start = float(v['先行発声']) / 1000 + float(v['オーバーラップ']) / 1000
                l.append([t_start, table[kana][1]])

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
            s += '{:.6f} {} {}\n'.format(v[0], '[ここに終端時刻を手入力]', v[1])

    # ファイル作成とデータ書き込み
    path_otolab = './lab/' + name_ini + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.lab'
    with open(path_otolab, 'w') as f:
        f.write(s)

    return path_otolab


def ust2ini(dir_ust):
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
    oto->lab 変換を1ファイルに実行
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
    outpath = path_ini.split('\\')[-1].rstrip('.ini')
    filename = write_lab(mono_oto, outpath)
    return filename


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
    print('ini -> lab 変換しました。')

    print('\n出力LAB一覧-------------------')
    pprint(lab_files)
    print('------------------------------')


def main():
    """
    全体の処理を実行
    """
    print('実行内容を数字で選択してください。')
    print('1 ... UST -> INI の変換')
    print('2 ... INI -> LAB の変換')
    mode = input('>>> ')

    if mode in ['1', '１']:
        # 'ust'フォルダ内にあるustファイルを変換
        ust2ini('ust')
    elif mode in ['2', '２']:
        # 'ini'フォルダ内にあるiniファイルを変換
        ini2lab_multi('ini')
    else:
        print('1 か 2 で選んでください。\n')
        main()


if __name__ == '__main__':
    main()
    while input('Press Enter to exit.') == 'r':
        main()
