#!/usr/bin/env python3
# coding: utf-8
"""
about module
"""

# from pprint import pprint
import os

from utaupy import utaupy as up


def test_1():
    """UstとOtoIniクラスのテスト"""
    path_ust = input('USTのパス: ').strip('"')

    basename = os.path.basename(path_ust)

    ust = up.Ust()
    ust.new_from_ustfile(path_ust)
    # print('ust.getvalues()----')
    # pprint(ust.get_values())
    # print('ust.getvalues()----\n')
    # print('note.getvalues()----')
    # for note in ust.get_values():
    #     pprint(note.get_values())
    # print('note.getvalues()----\n')
    otoini = up.new_otoiniobj_from_ustobj(ust, basename)
    # print('otoini-------------')
    # pprint(otoini)
    # print('otoini-------------\n')
    # print('otoini.getvalues()-------------')
    # pprint(otoini.get_values())
    outpath = basename.replace('.wav', '') + '_test.ini'
    up.write_inifile(otoini, outpath)

if __name__ == '__main__':
    test_1()
