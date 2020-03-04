#!/usr/bin/env python3
# coding: utf-8
"""
単独ファイルについて lab → ini 変換をします。
"""

# import os
# from subprocess import Popen
from pprint import pprint

# from pysnooper import snoop

import lab2ini as l2i

TEST_MODE = True

# @snoop()
def main():
    """
    全体の処理を実行
    """
    # oto.iniファイルを指定
    print('LAB ファイルを指定してください。')
    path_lab = input('>>>').strip('"')

    print('\nLAB -> INI 変換します。')
    print('read_lab()')
    mono_oto = l2i.read_lab(path_lab)

    print('\nmono_oto---')
    pprint(mono_oto)

    name_wav = '大きなのっぽの古時計.wav'
    otolist = l2i.mono_oto2otolist(mono_oto, name_wav)
    print('\notolist---')
    pprint(otolist)

    filename = path_lab.split('\\')[-1].rstrip('.lab')
    print(filename)
    path_ini = l2i.write_ini(otolist, filename)

    print('ini---')
    pprint(path_ini)



if __name__ == '__main__':
    main()
    while input('Press Enter to exit.') == 'r':
        main()
