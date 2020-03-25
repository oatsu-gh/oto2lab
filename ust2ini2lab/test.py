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

# from utaupy import label
# from utaupy import otoini
from utaupy import convert, otoini, table, ust


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
    特定の拡張子のファイルを退避させる。
    上書きによるファイル消滅回避が目的。
    path_dir: 処理対象フォルダ
    ext     : 処理対象拡張子
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


def read_japanesetable(path_table):
    """
    平仮名-ローマ字変換表を読み取って変換用の辞書を返す。
    {'変換元': ['母音', '子音'], ...}
    """
    d = table.load(path_table).get_values()
    d.update({'R': 'pau', 'B': 'br', '息': 'br'})
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
        try:
            # 連続音を単独音化
            kana = v['エイリアス'].split()[-1]
            # [発音開始時刻, 発音記号] の形式にする
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
            print('\n[KeyError]----------------------')
            print('エイリアスをモノフォン化する過程でエラーが発生しました。')
            print('ノートの歌詞が想定外です。iniを編集してください。')
            print('使用可能な歌詞は japanese_sjis.table に記載されている平仮名と、br、pau、cl です。')
            print('\nエラー項目    :', e)
            print('該当エイリアス:', v['エイリアス'])
            print('--------------------------------\n')
            print('プログラムを終了します。ファイル破損の心配は無いはずです。')
            input('Press enter to exit.')
            sys.exit()
        except IndexError as e:
            print('\n[IndexError]----------------------')
            print('エイリアスをモノフォン化する過程でエラーが発生しました。')
            print('ノートの歌詞が空欄な可能性が高いです。')
            print('該当ノートをスキップして続行します。')
            print('\nエラー内容    :', e)
            print('該当エイリアス:', v['エイリアス'])
            print('--------------------------------\n')
            continue

    return l  # mono_otoに相当


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


def ust2ini_solo(path_ust, outdir):
    """
    USTファイルをINIファイルに変換
    """
    basename = os.path.basename(path_ust)  # '<name>.ust'
    name_wav = basename.replace('.ust', '.wav')  # '<name>.wav'
    path_ini = outdir + basename.replace('.ust', '.ini')  # 'outdir/<name>.ini'
    print('converting UST->INI:', basename)
    # UST を読み取り
    u = ust.load(path_ust)
    u.replace_lyrics('息', 'br').replace('R', 'pau')
    # 変換
    o = convert.ust2otoini(u, name_wav)
    # INI を書き出し
    o.write(path_ini)
    print('converted  UST->INI:', path_ini)
    return path_ini


def ini2lab_solo(path_ini, outdir):
    """
    oto->lab 変換を単独ファイルに実行
    """
    basename = os.path.basename(path_ini)
    path_lab = outdir + basename.replace('.ini', '.lab')
    print('converting INI->LAB:', basename)
    # INI を読み取り
    o = otoini.load(path_ini)
    mono_oto = monophonize_oto(o)
    # 変換
    lab = convert.otoini2label(o)
    # LAB を書き出し
    lab.write(path_lab)
    print('converted  INI->LAB:', path_lab)
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
    print('3 ... UST -> INI -> LAB の変換')
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
