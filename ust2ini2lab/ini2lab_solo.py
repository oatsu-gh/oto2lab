#!/usr/bin/env python3
# coding: utf-8
# Copyright 2020 oatsu
"""
v0.0.1 ~ v0.1.1 の仕様に併せたツールです。
単独ファイルについて ini → lab 変換をします。
"""

import os
from subprocess import Popen

import ust2ini2lab as u2l

TEST_MODE = True


def main():
    """
    全体の処理を実行
    """
    # oto.iniファイルを指定
    print('INI ファイルを指定してください。')
    path_ini = input('>>>').strip('"')

    print('\nINI -> LAB 変換します。')
    path_lab = u2l.ini2lab_solo(path_ini)
    print('\nINI -> LAB 変換しました。')
    print('\n出力ファイルのPATHは {} です。'.format(path_lab))
    print('ファイルを開いて終端時刻を書き込んでください。')

    # Windows, WSLで実行された場合に限り、出力結果をメモ帳で開く。
    if os.name in ('nt', 'posix'):
        print('メモ帳で開きます。')
        Popen([r'notepad.exe', path_lab])

    print('\n----鋭意開発中です！----')


if __name__ == '__main__':
    main()
    while input('Press Enter to exit.') == 'r':
        main()
