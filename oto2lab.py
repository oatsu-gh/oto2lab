#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 oatsu
"""
setParam での音声ラベリング支援ツールです。
ファイル形式を変換できます。
・ust → ini
・ini → lab
・lab → ini
"""
import os
import shutil
from datetime import datetime
from glob import glob

from utaupy import convert, label, otoini, ust

# import re
# import sys
# from pathlib import Path
# from pprint import pprint


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


def ust2ini_solo(path_ust, outdir, path_table):
    """
    USTファイルをINIファイルに変換
    """
    basename = os.path.basename(path_ust)  # '<name>.ust'
    name_wav = basename.replace('.ust', '.wav')  # '<name>.wav'
    path_ini = '{}/{}'.format(outdir, basename.replace('.ust', '.ini'))  # 'outdir/<name>.ini'
    print('converting UST->INI:', path_ust)
    # UST を読み取り
    u = ust.load(path_ust)
    u.replace_lyrics('息', 'br')
    u.replace_lyrics('R', 'pau')
    # 変換
    o = convert.ust2otoini(u, name_wav)
    o.romanize(path_table)
    # INI を書き出し
    o.write(path_ini)
    print('converted  UST->INI:', path_ini)
    return path_ini


def ini2lab_solo(path_ini, outdir):
    """
    oto->lab 変換を単独ファイルに実行
    """
    basename = os.path.basename(path_ini)
    path_lab = '{}/{}'.format(outdir, basename.replace('.ini', '.lab'))
    print('converting INI->LAB:', path_ini)
    # INI を読み取り
    o = otoini.load(path_ini)
    # モノフォン化
    o.monophonize()
    # 変換
    lab = convert.otoini2label(o)
    # LAB を書き出し
    lab.write(path_lab)
    print('converted  INI->LAB:', path_lab)
    return path_lab


def lab2ini_solo(path_lab, outdir):
    """
    lab->ini 変換
    """
    # 各種pathの設定
    basename = os.path.basename(path_lab)
    path_ini = '{}/{}'.format(outdir, basename.replace('.lab', '.ini'))
    name_wav = basename.replace('.lab', '.wav')
    # 変換開始
    print('converting LAB->INI:', basename)
    lab = label.load(path_lab)
    o = convert.label2otoini(lab, name_wav)
    o.write(path_ini)
    print('converted  LAB->INI:', path_ini)


# def run_ExecuteUstToOto(path_xlsm):
#     """
#     ust→ini 用のExcelVBAを実行する
#     """
#     abspath = str(Path(path_xlsm).resolve())  # 絶対パスに変換
#     excel = win32com.client.Dispatch('Excel.Application')
#     excel.Visible = 0  # Excelの表示設定（0:非表示, 1:表示）
#     excel.Workbooks.Open(abspath, UpdateLinks=0, ReadOnly=True)  # 読み取り専用で開く
#
#     excel.Application.Run('ExecuteUstToOto')  # マクロを実行
#     excel.Workbooks(1).Close(SaveChanges=0)  # ブックを保存せずに閉じる
#     excel.Application.Quit()


# def ust2ini_Excel(dir_ust):
#     """
#     Excelのツールを使用してUST→INI変換
#     """
#     import win32com.client  # Excel操作に使用
#     print('\nust -> ini 変換します。数秒かかります。')
#     ust_files = glob('{}/*.ust'.format(dir_ust))
#     if ust_files == []:
#         print('[ERROR] ustファイルを設置してください。')
#         input('Press Enter to exit.')
#         sys.exit()
#
#     print('入力UST一覧-------------------')
#     pprint(ust_files)
#     print('------------------------------')
#     run_ExecuteUstToOto('歌声DBラベリング用ust→oto変換ツール.xlsm')
#     print('ust -> ini 変換しました。')


def main():
    """
    全体の処理を実行
    """
    path_table = './table/japanese_sinsy_sjis.table'
    print('実行内容を数字で選択してください。')
    print('1 ... UST -> INI の変換（ひとつ）')
    print('2 ... INI -> LAB の変換（ひとつ）')
    print('3 ... INI <- LAB の変換（ひとつ）')
    mode = input('>>> ')
    # ustフォルダ内にあるustファイルを変換
    if mode in ['1', '１']:
        print('USTファイルを指定してください。')
        path_ust = input('>>>')
        outdir = os.path.dirname(path_ust)
        evacuate_files(outdir, 'ini')
        ust2ini_solo(path_ust, outdir, path_table)

    # iniファイルを変換
    elif mode in ['2', '２']:
        print('INIファイルを指定してください。')
        path_ini = input('>>> ')
        outdir = os.path.dirname(path_ini)
        evacuate_files(outdir, 'lab')
        ini2lab_solo(path_ini, outdir)

    # labファイルをiniファイルに変換
    elif mode in ['3', '３']:
        print('LABファイルを指定してください。')
        path_lab = input('>>> ')
        outdir = os.path.dirname(path_lab)
        evacuate_files(outdir, 'ini')
        lab2ini_solo(path_lab, outdir)

    # elif mode in ['4', '４']:
    #     lab2ini_solo('lab')

    else:
        print('1 か 2 か 3 で選んでください。\n')
        main()


if __name__ == '__main__':
    main()
    while input('Press Enter to exit.') == 'r':
        main()
