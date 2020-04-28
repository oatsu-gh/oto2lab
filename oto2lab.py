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
# import re
import sys
from datetime import datetime
from glob import glob
from shutil import copy2, move

from utaupy import convert, label, otoini, ust

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
        move(p, new_dir)


def backup_files(path_dir, ext):
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
    backup_dir = '{}/old__{}'.format(path_dir, now)
    os.mkdir(backup_dir)
    # 移動
    for p in old_files:
        copy2(p, backup_dir)


def ustfile_to_inifile_solo(path_ustfile, outdir, path_tablefile, mode='romaji_cv'):
    """
    USTファイルをINIファイルに変換
    """
    allowed_modes = ['mono', 'romaji_cv']
    if mode not in allowed_modes:
        raise ValueError('argument \'mode\' must be in {}'.format(allowed_modes))

    basename = os.path.basename(path_ustfile)  # '<name>.ust'
    name_wav = basename.replace('.ust', '.wav')  # '<name>.wav'
    path_inifile = '{}/{}'.format(outdir, basename.replace('.ust', '.ini'))
    # 'outdir/<name>.ini'
    print('converting UST to INI :', path_ustfile)
    # UST を読み取り
    ustobj = ust.load(path_ustfile)
    ustobj.replace_lyrics('息', 'br')
    ustobj.replace_lyrics('R', 'pau')
    # 変換
    otoiniobj = convert.ust2otoini(ustobj, name_wav, path_tablefile)
    # INI を書き出し
    otoiniobj.write(path_inifile)
    print('converted  UST to INI :', path_inifile)
    return path_inifile


def inifile_to_labfile_solo(path_inifile, outdir):
    """
    oto->lab 変換を単独ファイルに実行
    """
    basename = os.path.basename(path_inifile)
    path_labfile = '{}/{}'.format(outdir, basename.replace('.ini', '.lab'))
    print('converting INI to LAB :', path_inifile)
    # INI を読み取り
    o = otoini.load(path_inifile)
    # モノフォン化
    o.monophonize()
    # 変換
    lab = convert.otoini2label(o)
    # LAB を書き出し
    lab.write(path_labfile)
    print('converted  INI to LAB :', path_labfile)
    return path_labfile


def labfile_to_inifile_solo(path_labfile, outdir):
    """
    lab->ini 変換
    """
    # 各種pathの設定
    basename = os.path.basename(path_labfile)
    path_inifile = '{}/{}'.format(outdir, basename.replace('.lab', '.ini'))
    name_wav = basename.replace('.lab', '.wav')
    # 変換開始
    print('converting LAB to INI :', path_labfile)
    lab = label.load(path_labfile)
    o = convert.label2otoini(lab, name_wav)
    o.write(path_inifile)
    print('converted  LAB to INI :', path_inifile)
    return path_inifile


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


# def ustfile_to_inifile_Excel(dir_ust):
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


def main_cli():
    """
    全体の処理を実行
    """
    path_tablefile = './table/japanese_sinsy_sjis.table'
    print('実行内容を数字で選択してください。')
    print('1 ... UST -> INI の変換（ひとつ）')
    print('2 ... INI -> LAB の変換（ひとつ）')
    print('3 ... INI <- LAB の変換（ひとつ）')
    mode = input('>>> ')
    # ustファイルを変換
    if mode in ['1', '１']:
        path_ustfile = ''
        while not path_ustfile.endswith('.ust'):
            print('USTファイルを指定してください。')
            path_ustfile = input('>>> ')
        outdir = os.path.dirname(path_ustfile)
        evacuate_files(outdir, 'ini')
        ustfile_to_inifile_solo(path_ustfile, outdir, path_tablefile)

    # iniファイルを変換
    elif mode in ['2', '２']:
        while not path_ustfile.endswith('.ini'):
            print('INIファイルを指定してください。')
            path_inifile = input('>>> ')
        outdir = os.path.dirname(path_inifile)
        evacuate_files(outdir, 'lab')
        inifile_to_labfile_solo(path_inifile, outdir)

    # labファイルをiniファイルに変換
    elif mode in ['3', '３']:
        while not path_ustfile.endswith('.lab'):
            print('LABファイルを指定してください。')
            path_labfile = input('>>> ')
        outdir = os.path.dirname(path_labfile)
        evacuate_files(outdir, 'ini')
        labfile_to_inifile_solo(path_labfile, outdir)

    # elif mode in ['4', '４']:
    #     labfile_to_inifile_solo('lab')

    else:
        print('1 か 2 か 3 で選んでください。\n')
        main_cli()


def main_gui(path, mode):
    """
    oto2lab_gui.exe から呼び出されたときの処理
    """
    path_tablefile = './table/japanese_sinsy_sjis.table'

    # ustファイルを変換
    if mode == '1':
        path_ustfile = path
        outdir = os.path.dirname(path_ustfile)
        evacuate_files(outdir, 'ini')
        ustfile_to_inifile_solo(path_ustfile, outdir, path_tablefile)

    # iniファイルを変換
    elif mode == '2':
        path_inifile = path
        outdir = os.path.dirname(path_inifile)
        evacuate_files(outdir, 'lab')
        inifile_to_labfile_solo(path_inifile, outdir)

    # labファイルをiniファイルに変換
    elif mode == '3':
        path_labfile = path
        outdir = os.path.dirname(path)
        evacuate_files(outdir, 'ini')
        labfile_to_inifile_solo(path_labfile, outdir)


if __name__ == '__main__':
    print('_____ξ・ヮ・) < oto2lab v1.1.0________\n')
    args = sys.argv
    if len(args) == 1:
        main_cli()
        input('Press Enter to exit.')

    else:
        main_gui(path=args[1], mode=args[3])
