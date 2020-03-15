#!/usr/bin/env python3
# coding: utf-8
"""
単独ファイルについて lab → ini 変換をします。
"""

# import os
# from subprocess import Popen
# from pprint import pprint

import lab2ini as l2i

# from pysnooper import snoop

TEST_MODE = True

# @snoop()
def lab2ini_solo_cv():
    """
    全体の処理を実行
    """
    # oto.iniファイルを指定
    print('LAB ファイルを指定してください。')
    path_lab = input('>>>').strip('"')

    print('\nLAB -> INI 変換します。')
    # print('read_lab()')
    mono_oto = l2i.read_lab(path_lab)

    # print('\nmono_oto---')
    # pprint(mono_oto)

    path_vcs = './table/vowel_consonant_sinsy.txt'
    # path_japanesetable = './table/japanese_sinsy_sjis.table'
    cv_oto = l2i.mono_oto2cv_oto(mono_oto, path_vcs)
    # pprint(cv_oto)

    name_wav = l2i.simple_filename(path_lab).replace('.lab', '.wav')
    print(name_wav)
    otolist = l2i.cv_oto2otolist(cv_oto, name_wav)
    # print('\notolist---')
    # pprint(otolist)

    # otolist = l2i.otolist_for_utau(otolist)
    # print('\notolist_utau---')
    # pprint(otolist_utau)

    filename = path_lab.split('\\')[-1].rstrip('.lab')
    print('入力ファイル(LAB):', filename)
    path_ini = l2i.write_ini(otolist, filename)

    print('出力ファイル(INI):', path_ini)

# @snoop()
def lab2ini_solo_mono():
    """
    全体の処理を実行
    """
    # oto.iniファイルを指定
    print('LAB ファイルを指定してください。')
    path_lab = input('>>>').strip('"')

    print('\nLAB -> INI 変換します。')
    # print('read_lab()')
    mono_oto = l2i.read_lab(path_lab)

    # print('\nmono_oto---')
    # pprint(mono_oto)

    # path_vcs = './table/vowel_consonant_sinsy.txt'
    # path_japanesetable = './table/japanese_sinsy_sjis.table'

    name_wav = l2i.simple_filename(path_lab).replace('.lab', '.wav')
    print(name_wav)
    otolist = l2i.mono_oto2otolist(mono_oto, name_wav)
    # print('\notolist---')
    # pprint(otolist)

    # otolist = l2i.otolist_for_utau(otolist)
    # print('\notolist_utau---')
    # pprint(otolist_utau)

    filename = path_lab.split('\\')[-1].rstrip('.lab')
    print('入力ファイル(LAB):', filename)
    path_ini = l2i.write_ini(otolist, filename)

    print('出力ファイル(INI):', path_ini)


def main():
    print('モード選択')
    print('  1: 単独音 (CV)')
    print('  2: モノフォン')
    mode = input('>>>')
    if mode == '1':
        lab2ini_solo_cv()
    elif mode == '2':
        lab2ini_solo_mono()
    else:
        main()

if __name__ == '__main__':
    main()
    input()
