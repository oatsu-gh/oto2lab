#!/usr/bin/env python3
# coding: utf-8
"""
oto.ini → oto.lab の変換ツール

oto2lab v002 をもとに
ちていこさんの ust→oto.ini 変換ツールの自動実行機能追加
"""
import os
import re
import sys
from datetime import datetime
from pprint import pprint
from subprocess import Popen
from pathlib import Path
import win32com.client # Excel操作に使用

TEST_MODE = False


def run_ExecuteUstToOto(path_xlsm):
    """
    ust→otoini 用のExcelVBAを実行する
    """
    abspath = str(Path(path_xlsm).resolve()) # 絶対パスに変換
    excel = win32com.client.Dispatch('Excel.Application')
    excel.Visible = 0 # Excelの表示設定（0:非表示, 1:表示）
    excel.Workbooks.Open(abspath, UpdateLinks=0, ReadOnly=True) # 読み取り専用で開く

    excel.Application.Run('ExecuteUstToOto') # マクロを実行
    excel.Workbooks(1).Close(SaveChanges=1) # ブックを保存せずに閉じる
    excel.Application.Quit()

def glob()

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
    d = {}
    for v in l:
        d[v[0]] = v[1:]
    return d


def monorize_oto(otolist):
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
            print('\n--[KeyError]--------------------')
            print('エイリアスをモノフォン化する過程でエラーが発生しました。')
            print('ノートの歌詞が想定外です。otoiniを編集してください。')
            print('使用可能な歌詞は japanese_sjis.table に記載されている平仮名と、br、pau、cl です。')
            print('\nエラー項目:', e)
            print('--------------------------------\n')
            print('プログラムを終了します。ファイル破損の心配は無いはずです。')
            sys.exit()

    return l


def write_otolab(mono_otoini):
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
    path_otolab = './lab/oto_' + datetime.now().strftime('%Y%m%d_%H%M%S') + '.lab'
    with open(path_otolab, 'w') as f:
        f.write(s)

    return path_otolab


def main():
    """
    全体の処理を実行
    """
    # oto.iniファイルを指定
    print('oto.iniファイルを指定してください。')
    path_otoini = input('>>>').strip('"')

    print('oto.ini を読み取ります。')
    otolist = read_otoini(path_otoini)
    if TEST_MODE:
        pprint(otolist)
    print('oto.ini を読み取りました。')

    print('\n読み取ったデータを整形します。')
    mono_oto = monorize_oto(otolist)
    if TEST_MODE:
        pprint(mono_oto)
    print('読み取ったデータを整形しました。')

    print('\noto.lab を書き出します。')
    path_otolab = write_otolab(mono_oto)
    print('oto.lab を書き出しました。')

    print('\n出力ファイルのPATHは {} です。'.format(path_otolab))
    print('ファイルを開いて終端時刻を書き込んでください。')
    # Windows, WSLで実行された場合に限り、出力結果をメモ帳で開く。
    if os.name in ('nt', 'posix'):
        print('メモ帳で開きます。')
        Popen([r'notepad.exe', path_otolab])

    print('\n----鋭意開発中です！----')


if __name__ == '__main__':
    main()
    while input('Press Enter to exit.') == 'r':
        main()
