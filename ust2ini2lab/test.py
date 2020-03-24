#!/usr/bin/env python3
# coding: utf-8
"""
about module
"""

# from pprint import pprint
import os
from pprint import pprint

# from utaupy import utaupy as up
from utaupy import convert, otoini, ust


def test_1():
    """UstとOtoIniクラスのテスト"""
    path_ust = input('USTのパス: ').strip('"')

    basename = os.path.basename(path_ust)

    u = ust.load(path_ust)
    # print('ust.getvalues()----')
    # pprint(ust.get_values())
    # print('ust.getvalues()----\n')
    # print('note.getvalues()----')
    # for note in ust.get_values():
    #     pprint(note.get_values())
    # print('note.getvalues()----\n')
    o = convert.ust2otoini(u, basename)
    # print('otoini-------------')
    # pprint(otoini)
    # print('otoini-------------\n')
    # print('otoini.getvalues()-------------')
    # pprint(otoini.get_values())
    outpath = basename.replace('.ust', '') + '_test.ini'
    o.write(outpath)


def test_2():
    """OtoIniクラスのテスト"""
    path_ini = input('INIのパス: ').strip('"')
    o = otoini.load(path_ini)
    print('o.get_values----------------------------')
    pprint(o.get_values())
    print(type(o))
    print('----------------------------------------')
    # for oto in o.get_values():
    #     pprint(oto.get_values())
    lab = convert.otoini2label(o)
    print(lab.get_values())
    s = lab.write(path_ini.replace('.ini', '.lab'))
    print('\n')
    print(s)


if __name__ == '__main__':
    test_2()
