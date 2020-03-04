#!/usr/bin/env python3
# coding: utf-8
"""
単独ファイルについて lab → ini 変換をします。
"""

# import os
# from subprocess import Popen
from pprint import pprint

import lab2ini as l2i

TEST_MODE = True


def main():
    """
    全体の処理を実行
    """
    # oto.iniファイルを指定
    print('LAB ファイルを指定してください。')
    path_lab = input('>>>').strip('"')

    print('\nLAB -> INI 変換します。')
    mono_oto = l2i.read_lab(path_lab)
    pprint(mono_oto)
    # # path_ini = u2l.lab2ini_solo(path_ini)
    # print('\nINI -> LAB 変換しました。')
    # print('\n出力ファイルのPATHは {} です。'.format(path_ini))
    # print('ファイルを開いて終端時刻を書き込んでください。')

    # Windows, WSLで実行された場合に限り、出力結果をメモ帳で開く。
    # if os.name in ('nt', 'posix'):
    #     print('メモ帳で開きます。')
    #     Popen([r'notepad.exe', path_lab])
    #
    # print('\n----鋭意開発中です！----')


if __name__ == '__main__':
    main()
    while input('Press Enter to exit.') == 'r':
        main()
