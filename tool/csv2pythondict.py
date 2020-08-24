#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) oatsu
"""
音階番号をC4みたいな表記にするときに使う辞書を作るために、
Excelから書きだしたCSVをPythonの辞書にしようと思って作ったやつ

コンマ区切りCSVをPythonの辞書にします。
"""
from pprint import pprint


def main():
    path = input('path: ')
    with open(path) as f:
        s = f.read()
    pprint(s)
    s = s.replace(',', '\':\'')
    s = s.replace('\n', '\',\'')
    s = '{' + s[:-1] + '}'
    print('---------------------------------------------------')
    pprint(s)
    outpath = path + '_edit.txt'
    with open(outpath, 'w') as f:
        f.write(s)
    input('press enter to exit')


if __name__ == '__main__':
    main()
