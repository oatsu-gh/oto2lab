#!python
# coding: utf-8
# Copyright (c) oatsu
"""
発声区間がマイナス値なラベルがないか検査
"""
from glob import glob
from pprint import pprint

import utaupy as up


def main():
    path_lab_dir = input('path_lab_dir: ')
    l_path_lab = glob(f'{path_lab_dir}/**/*.lab', recursive=True)
    pprint(l_path_lab)
    for path_lab in l_path_lab:
        print(path_lab)
        label = up.label.load(path_lab)
        label.check_invalid_time()


if __name__ == '__main__':
    main()
    input('Press Enter to exit.')
