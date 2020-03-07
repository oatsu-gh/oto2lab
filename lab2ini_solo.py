#!/usr/bin/env python3
# coding: utf-8
"""
単独ファイルについて lab → ini 変換をします。
"""

# import os
# from subprocess import Popen
from pprint import pprint

import lab2ini as l2i

# from pysnooper import snoop


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

    path_vcs = './table/vowel_consonant_sinsy.txt'
    # path_japanesetable = './table/japanese_sinsy_sjis.table'
    cv_oto = l2i.mono_oto2cv_oto(mono_oto, path_vcs)
    pprint(cv_oto)

    name_wav = '01.wav'
    otolist = l2i.cv_oto2otolist(cv_oto, name_wav)
    print('\notolist---')
    pprint(otolist)

    otolist_utau = l2i.otolist_for_utau(otolist)
    print('\notolist_utau---')
    pprint(otolist_utau)

    filename = path_lab.split('\\')[-1].rstrip('.lab')
    print(filename)
    path_ini = l2i.write_ini(otolist_utau, filename)

    print('ini---')
    pprint(path_ini)


if __name__ == '__main__':
    main()
    while input('Press Enter to exit.') == 'r':
        main()
