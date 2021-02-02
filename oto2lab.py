#! /usr/bin/env python3
# coding: utf-8
# Copyright 2020 oatsu
"""
setParam での音声ラベリング支援ツールです。
ファイル形式を変換できます。
・ust → ini
・svp → ini
・ini → lab
・lab → ini
"""
import argparse
import os
# import re
# import sys
from datetime import datetime
from glob import glob
# from pathlib import Path
from pprint import pprint
from shutil import copy2

import utaupy as up

DEBUG_MODE = False
PATH_TABLE = './dic/kana2phonemes_utf8_for_oto2lab.table'


def backup_io(path_file, outdirname):
    """
    ファイル名に時刻を組み込んでバックアップ
    入出力ファイル向け。
    """
    basename, ext = os.path.splitext(os.path.basename(path_file))
    now = datetime.now().strftime('%Y%m%d_%H%M%S')

    copy2(path_file, f'backup/{outdirname}/{basename}__{now}{ext}')


def split_cl_note_of_ust(ust):
    """
    Ustオブジェクト中のNoteのうち、促音を含むノートを半分に割る。
    「かっ」→「か」「っ」
    促音のみのノートはそのままにすることに注意。
    """
    new_notes = []
    for note in ust.notes:
        lyric = note.lyric
        if ('っ' in lyric) and (lyric != 'っ'):
            # もとのノートを半分にして、促音を削ってリストに追加
            half_length = note.length // 2
            note.lyric = lyric.strip('っ')
            note.length = half_length
            new_notes.append(note)
            # もう半分の長さの促音のノートをリストに追加
            note_cl = up.ust.Note()
            note_cl.lyric = 'っ'
            note_cl.length = half_length
            # 分割した2つのノートをリストに追加
            new_notes.append(note_cl)
        else:
            new_notes.append(note)
    # ノートを上書き
    ust.notes = new_notes
    ust.reload_tempo()


def ustfile_to_inifile(path:str, path_tablefile:str, mode='romaji_cv'):
    """
    USTファイルをINIファイルに変換
    """
    allowed_modes = ['mono', 'romaji_cv']
    if mode not in allowed_modes:
        raise ValueError('argument \'mode\' must be in {}'.format(allowed_modes))

    # かな→ローマ字変換テーブルを読み取り
    d_table = up.table.load(path_tablefile)  # kana-romaji table

    # ファイルを指定した場合
    if os.path.isfile(path):
        l = [path]
        outdir = os.path.dirname(path)
    # フォルダを指定した場合
    else:
        l = glob('{}/*.{}'.format(path, 'ust'))
        outdir = path

    print('\n処理対象ファイル---------')
    pprint(l)
    print('-------------------------\n')
    # USTファイルをINIファイルに変換して保存する処理
    for path_ustfile in l:
        print('converting UST to INI :', path_ustfile)  # 'outdir/name.ini'
        backup_io(path_ustfile, 'in')
        basename = os.path.basename(path_ustfile)  # 'name.ust'
        name_wav = basename.replace('.ust', '.wav')  # 'name.wav'
        # 出力するINIファイルのパス
        path_inifile = '{}/{}'.format(outdir, basename.replace('.ust', '.ini'))
        # UST を読み取り
        ust = up.ust.load(path_ustfile)
        # 促音を含むノートを分割
        split_cl_note_of_ust(ust)
        # 変換
        otoini = up.convert.ust2otoini(ust, name_wav, d_table, mode=mode, debug=DEBUG_MODE)
        otoini.write(path_inifile)
        backup_io(path_inifile, 'out')
        print('converted  UST to INI :', path_inifile)


def inifile_to_labfile(path_dir_in, mode='auto'):
    """
    oto->lab 変換を単独ファイルに実行
    """

    # ファイルを指定した場合
    if os.path.isfile(path_dir_in):
        l = [path_dir_in]
        outdir = os.path.dirname(path_dir_in)
    # フォルダを指定した場合
    else:
        l = glob('{}/*.{}'.format(path_dir_in, 'ini'))
        outdir = path_dir_in

    print('\n処理対象ファイル---------')
    pprint(l)
    print('-------------------------\n')
    # ファイル変換処理
    for path_inifile in l:
        print('converting INI to LAB :', path_inifile)
        backup_io(path_inifile, 'in')

        basename = os.path.basename(path_inifile)
        path_labfile = '{}/{}'.format(outdir, basename.replace('.ini', '.lab'))

        # INI を読み取り
        otoini = up.otoini.load(path_inifile)
        # 変換
        lab = up.convert.otoini2label(otoini, mode=mode, debug=DEBUG_MODE)
        # LAB を書き出し
        lab.write(path_labfile)
        backup_io(path_labfile, 'out')
        print('converted  INI to LAB :', path_labfile)


def labfile_to_inifile(path):
    """
    lab->ini 変換
    """
    if os.path.isfile(path):
        l = [path]
    else:
        l = glob('{}/**/*.{}'.format(path, 'lab'), recursive=True)

    # ファイル変換処理
    print('\n処理対象ファイル---------')
    pprint(l)
    print('-------------------------\n')
    for path_labfile in l:
        # 各種pathの設定
        basename = os.path.basename(path_labfile)
        path_inifile = os.path.splitext(path_labfile)[0] + '_review.ini'
        name_wav = basename.replace('.lab', '.wav')
        # 変換開始
        print('converting LAB to INI :', path_labfile)
        backup_io(path_labfile, 'in')
        label = up.label.load(path_labfile)
        otoini = up.convert.label2otoini(label, name_wav)
        otoini.write(path_inifile)
        backup_io(path_inifile, 'out')
        print('converted  LAB to INI :', path_inifile)


def inifile_kana2romaji(path_input, path_tablefile):
    """
    複数のiniファイルの平仮名エイリアスをローマ字にする
    """
    if os.path.isdir(path_input):
        l = glob('{}/*.{}'.format(path_input, 'ini'))
    else:
        l = [path_input]

    # かな→ローマ字変換テーブル
    d_table = up.table.load(path_tablefile)

    # ファイル変換処理
    print('\n処理対象ファイル---------')
    pprint(l)
    print('-------------------------\n')
    for path_ini in l:
        backup_io(path_ini, 'in')
        otoini = up.otoini.load(path_ini)
        for oto in otoini:
            try:
                oto.alias = ' '.join(d_table[oto.alias])
            except KeyError as err:
                print('[WARNING] KeyError in oto2lab.inifile_kana2ramaji')
                print('  詳細:', err)
        print(path_ini)
        otoini.write(path_ini)
        backup_io(path_ini, 'out')


def svpfile_to_inifile(path, path_tablefile, mode='romaji_cv'):
    """
    SVPファイルをINIファイルに変換する。
    Ustオブジェクトを中間フォーマットにする。
    """
    allowed_modes = ['mono', 'romaji_cv']
    if mode not in allowed_modes:
        raise ValueError('argument \'mode\' must be in {}'.format(allowed_modes))

    # かな→ローマ字変換テーブル
    d_table = up.table.load(path_tablefile)

    # ファイルを指定した場合
    if os.path.isfile(path):
        l = [path]
        outdir = os.path.dirname(path)
    # フォルダを指定した場合
    else:
        l = glob('{}/*.{}'.format(path, 'svp'))
        outdir = path

    print('\n処理対象ファイル---------')
    pprint(l)
    print('-------------------------\n')
    for path_svpfile in l:
        print('converting SVP to INI :', path_svpfile)  # 'outdir/<name>.ini'
        # 入力ファイルをバックアップ
        backup_io(path_svpfile, 'in')
        # 出力パスを決める
        basename = os.path.basename(path_svpfile)  # '<name>.ust'
        name_wav = basename.replace('.svp', '.wav')  # '<name>.wav'
        path_inifile = '{}/{}'.format(outdir, basename.replace('.svp', '.ini'))
        # SvpをUstに変換
        svp = up.svp.load(path_svpfile)
        ust = up.convert.svp2ust(svp, debug=DEBUG_MODE)
        # 促音を含むノートを分割
        split_cl_note_of_ust(ust)
        # UstをOtoIniに変換してファイル出力
        otoini = up.convert.ust2otoini(ust, name_wav, d_table, mode=mode, debug=DEBUG_MODE)
        otoini.write(path_inifile)
        # 出力ファイルをバックアップ
        backup_io(path_inifile, 'out')
        print('converted  SVP to INI :', path_inifile)


def labfile_to_inifile_revise(path):
    """
    lab->ini 変換
    """
    if os.path.isfile(path):
        l = [path]
    else:
        l = glob('{}/**/*.{}'.format(path, 'lab'), recursive=True)

    # ファイル変換処理
    print('\n処理対象ファイル---------')
    pprint(l)
    print('-------------------------\n')
    for path_labfile in l:
        # 各種pathの設定
        basename = os.path.basename(path_labfile)
        path_inifile = os.path.splitext(path_labfile)[0] + '_revise.ini'
        name_wav = basename.replace('.lab', '.wav')
        # 変換開始
        print('converting LAB to INI :', path_labfile)
        backup_io(path_labfile, 'in')
        label = up.label.load(path_labfile)
        otoini = up.convert.label2otoini(label, name_wav)
        for oto in otoini:
            oto.offset -= 100
            oto.overlap = 0
            oto.preutterance += 100
            oto.consonant += 100
            oto.cutoff2 += 100
        otoini.write(path_inifile)
        backup_io(path_inifile, 'out')
        print('converted  LAB to INI :', path_inifile)


def main_cli():
    """
    全体の処理を実行
    """
    path_tablefile = PATH_TABLE
    print('実行内容を数字で選択してください。')
    print('1 ... UST -> INI の変換')
    print('2 ... INI -> LAB の変換')
    print('3 ... LAB -> INI の変換（点検用）')
    print('4 ... SVP -> INI の変換')
    print('5 ... INI ファイルのエイリアス置換（かな -> ローマ字）')
    print('6 ... LAB -> INI の変換（再編集用）')
    mode = input('>>> ')
    print('処理対象ファイルまたはフォルダを指定してください。')
    path = input('>>> ').strip(r'"')

    # ustファイルを変換
    if mode in ['1', '１']:
        ustfile_to_inifile(path, path_tablefile)
    # iniファイルを変換
    elif mode in ['2', '２']:
        inifile_to_labfile(path, mode='auto')
    # labファイルをiniファイルに変換
    elif mode in ['3', '３']:
        labfile_to_inifile(path)
    # svpファイルをiniファイルに変換(ustオブジェクト経由)
    elif mode in ['4', '４']:
        svpfile_to_inifile(path, path_tablefile)
    elif mode in ['5', '５']:
        # iniファイルをひらがなCV→romaCV変換
        inifile_kana2romaji(path, path_tablefile)
    elif mode in ['6', '６']:
        # labファイルを再編集用のモノフォンiniファイルに変換
        labfile_to_inifile_revise(path)
    else:
        # 想定外のモードが指定されたとき
        print('1 から 5 で選んでください。\n')
        main_cli()


def main_gui(path, mode):
    """
    oto2lab_gui.exe から呼び出されたときの処理
    """
    path_tablefile = PATH_TABLE
    path = path.strip(r'"')
    if mode == '1':
        # ustファイルを変換
        ustfile_to_inifile(path, path_tablefile)
    elif mode == '2':
        # iniファイルを変換
        inifile_to_labfile(path)
    elif mode == '3':
        # labファイルをiniファイルに変換
        labfile_to_inifile(path)
    elif mode == '4':
        # svpファイルをiniファイルに変換(ustオブジェクト経由)
        svpfile_to_inifile(path, path_tablefile)
    elif mode is None:
        print('mode番号が設定されてないみたい。')


if __name__ == '__main__':
    print('_____ξ・ヮ・) < oto2lab v2.2.5 ________')
    print('Copyright (c) 2020 oatsu')
    print('Copyright (c) 2020 Haruqa')
    print('Copyright (c) 2001-2020 Python Software Foundation\n')

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='入力ファイルかフォルダ input path\t(file or dir)')
    parser.add_argument('-m', '--mode', help='モード選択 mode selection\t(1~5)')
    parser.add_argument('--table', help='変換テーブルのパス table path\t(file)')
    parser.add_argument('--debug', help='デバッグモード debug flag\t(bool)', action='store_true')
    parser.add_argument('--gui', help='executed by oto2labGUI\t(bool)', action='store_true')
    parser.add_argument('--kana', help='日本語のINIエイリアスの時に有効にしてね\t(bool)', action='store_true')

    args = parser.parse_args()
    DEBUG_MODE = args.debug
    if not args.table is None:
        PATH_TABLE = args.table

    # バックアップ用のフォルダを生成
    os.makedirs('backup/in', exist_ok=True)
    os.makedirs('backup/out', exist_ok=True)

    if args.gui is False:
        if DEBUG_MODE:
            print('args:', args)
        main_cli()
        input('Press Enter to exit.')

    else:
        # NOTE: GUI呼び出しでデバッグモードにすると実行失敗することが判明。
        # args は 扱えるがprintしようとすると落ちる。
        # args をつかうのやめてもなんか落ちる。標準出力が多いせいか。
        main_gui(path=args.input, mode=args.mode)
