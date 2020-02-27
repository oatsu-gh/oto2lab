#!/usr/bin/env python3
# coding: utf-8
"""
oto.ini → oto.lab の変換ツール

oto2lab v002 をもとに
ちていこさんの ust→oto.ini 変換ツールの自動実行機能追加
"""
# import os
import re
import sys
from datetime import datetime
from glob import glob
from pathlib import Path
from pprint import pprint

import win32com.client  # Excel操作に使用

# from time import sleep


# from subprocess import Popen


TEST_MODE = False


def run_ExecuteUstToOto(path_xlsm):
    """
    ust→otoini 用のExcelVBAを実行する
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


def read_otoini(path_otoini):
    """
    otoiniを読み取って辞書を返す
    """
    with open(path_otoini, 'r') as f:
        l = [re.split('[=,]', s.strip()) for s in f.readlines()]

    # 入力ファイル末尾の空白行を除去
    while l[-1] == ['']:
        del l[-1]

    # 配列を辞書に変換(覚えられないので)
    keys = ('ファイル名', 'エイリアス', '左ブランク', '固定範囲', '右ブランク', '先行発声', 'オーバーラップ')
    l = [dict(zip(keys, v)) for v in l]

    return l


def read_japanesetable(path_table):
    """
    平仮名-ローマ字変換表を読み取って辞書を返す。
    子音と母音に分けて、リストを返す。
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
    ・入力otoiniは辞書のリスト[{}]
    ・otoiniのエイリアスをモノフォン化
    ・ラベルに不要なデータを破棄
    必要: オーバーラップ, 先行発声
    変換: エイリアス(→モノフォン)
    不要: 左ブランク, ファイル名, 固定範囲, 右ブランク
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
                l.append([float(v['オーバーラップ']) / 1000, table[kana][0]])
            # 想定内アルファベット歌詞
            elif kana in special:
                l.append([float(v['オーバーラップ']) / 1000, kana])
            # ダイフォン平仮名歌(子音と母音に分割)
            else:
                l.append([float(v['オーバーラップ']) / 1000, table[kana][0]])
                l.append([float(v['先行発声']) / 1000, table[kana][1]])

        except KeyError as e:
            print('\n--[KeyError in monophonize_oto]--------')
            print('エイリアスをモノフォン化する過程でエラーが発生しました。')
            print('ノートの歌詞が想定外です。otoiniを編集してください。')
            print('使用可能な歌詞は japanese_sjis.table に記載されている平仮名と、br、pau、cl です。')
            print('\nエラー項目:', e)
            print('---------------------------------------\n')
            print('プログラムを終了します。ファイル破損の心配は無いはずです。')
            sys.exit()

    return l


def write_otolab(mono_otoini, name_otoini):
    """
    format_otoini でフォーマットした二次元リスト [[発音開始時刻, 発音記号], ...] から、
    きりたんDB式音声ラベルで oto_日付.lab に出力する
    """
    s = ''
    for i, v in enumerate(mono_otoini):
        try:
            s += '{:.6f} {:.6f} {}\n'.format(v[0], mono_otoini[i + 1][0], v[1])
        except IndexError:
            s += '{:.6f} {} {}\n'.format(v[0], '[ここに終端時刻を手入力]', v[1])

    # ファイル作成とデータ書き込み
    path_otolab = './lab/' + name_otoini + '_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.lab'
    with open(path_otolab, 'w') as f:
        f.write(s)

    return path_otolab


def oto2lab(path_otoini):
    """
    otoini→otolab 変換本体
    """
    # oto.ini を読み取り
    otolist = read_otoini(path_otoini)
    if TEST_MODE:
        pprint(otolist)

    # 読み取ったデータを整形
    mono_oto = monophonize_oto(otolist)
    if TEST_MODE:
        print('mono_oto------------')
        pprint(mono_oto)
        print('--------------------')

    # oto.lab を書き出し
    filename = path_otoini.split('\\')[-1].rstrip('.ini')
    path_otolab = write_otolab(mono_oto, filename)

    # print('出力ファイルのPATHは {} です。'.format(path_otolab))
    return path_otolab


def main():
    """
    全体の処理を実行
    """

    print('ust→ini 変換します。数秒かかります。')
    ust_files = glob('ust/*.ust')
    if ust_files == []:
        print('[ERROR] ustファイルを設置してください。')
        input('Press Enter to exit.')
        sys.exit()

    print('対象UST一覧-------------------')
    pprint(ust_files)
    print('------------------------------')
    run_ExecuteUstToOto('歌声DBラベリング用ust→oto変換ツール.xlsm')
    print('ust→ini 変換しました。')

    print()

    ini_files = glob('oto/*.ini')
    print('ini→lab 変換します。')
    print('対象INI一覧-------------------')
    pprint(ini_files)
    print('------------------------------')
    print('ini→lab 変換しました。')

    print()

    lab_files = []
    for ini in ini_files:
        lab = oto2lab(ini)
        lab_files.append(lab)
    print('出力LAB一覧-------------------')
    pprint(lab_files)
    print('------------------------------')



if __name__ == '__main__':
    main()
    while input('Press Enter to exit.') == 'r':
        main()
