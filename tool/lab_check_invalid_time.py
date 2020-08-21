#!python
# coding: utf-8
# Copyright (c) oatsu
"""
発声区間がマイナス値なラベルがないか検査
"""
from glob import glob
import utaupy as up

def main():
    path_lab_dir = input('path_lab_dir: ')
    l_path_lab = glob(f'{path_lab_dir}/**/*.lab', recursive=True)
    for path_lab in l_path_lab:
        print(path_lab)
        label = up.label.load(path_lab)
        for phoneme in label.values:
            duration = phoneme.end - phoneme.start
            if duration <= 20000:
                print(f'  [ERROR] 発声時間が2ms未満です : {phoneme.start} {phoneme.end} {phoneme.symbol}')

if __name__ == '__main__':
    main()
    input('Press Enter to exit.')
