#!/usr/bin/env python3
# coding: utf-8
"""
ラベルファイルの時間単位を変えるやつ。
きりたんDBは  s (小数点以下6桁)
HTSサンプルは 100ns (整数)
"""

import os
from datetime import datetime
from glob import glob
from pprint import pprint
from shutil import copy2


def s_to_subus(path_labfile):
    """上書きするので注意"""
    time_order_ratio = 10 ** 7
    with open(path_labfile, 'r') as f:
        lines = [s.strip().split() for s in f.readlines()]
    # この時点で [[発声開始, 発声終了, 発音記号], ]
    s = ''
    for l in lines:
        # print(l, end='\t ->  ')
        tmp = (int(float(l[0]) * time_order_ratio), int(float(l[1]) * time_order_ratio), l[2])
        # print(tmp)
        s += '{} {} {}\n'.format(*tmp)
    with open(path_labfile, 'w') as f:
        f.write(s)


def subus_to_s(path_labfile):
    """HTSのをきりたんの形式に変換"""
    time_order_ratio = 10 ** (-7)
    with open(path_labfile, 'r') as f:
        lines = [s.strip().split() for s in f.readlines()]
    # この時点で [[発声開始, 発声終了, 発音記号], ]
    s = ''
    for l in lines:
        # print(l, end='\t ->  ')
        tmp = (float(l[0]) * time_order_ratio, float(l[1]) * time_order_ratio, l[2])
        # print(tmp)
        s += '{:.7f} {:.7f} {}\n'.format(*tmp)
    with open(path_labfile, 'w') as f:
        f.write(s)


def backup_files(path_dir, ext):
    """
    特定の拡張子のファイルを退避させる。
    上書きによるファイル消滅回避が目的。
    path_dir: 処理対象フォルダ
    ext     : 処理対象拡張子
    """
    ext = ext.replace('.', '')
    old_files = glob('{}/*.{}'.format(path_dir, ext))
    # 退避先のフォルダを作成
    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = '{}/old__{}'.format(path_dir, now)
    os.mkdir(backup_dir)
    # 移動
    for p in old_files:
        copy2(p, backup_dir)


def wrapper(path, mode):
    """
    機能選択するやつ
    """
    if mode in ['1', '１']:
        s_to_subus(path)
    elif mode in ['2', '２']:
        subus_to_s(path)
    else:
        print('モードは2つしかありません。')
        main()


def main():
    """
    ファイルをバックアップしたうえで単位換算する。
    """
    print('換算機能の選択をしてください----------')
    print('1) きりたんDB [s] → HTS [100ns]')
    print('2) HTS [100ns]    → きりたんDB [s]')
    print('--------------------------------------')
    mode = input('>>> ')
    print('\ninput target filepath or dirpath')
    path = input('>>> ')
    if os.path.isdir(path):
        # 破損対策でコピー
        backup_files(path, 'lab')
        # labファイル一覧を取得
        target_file_paths = glob('{}/*.{}'.format(path, 'lab'))
        print('\n処理対象ファイル---------')
        pprint(target_file_paths)
        print('-------------------------\n')
        for p in target_file_paths:
            wrapper(p, mode)
    else:
        backup_files(os.path.dirname(path), 'lab')
        wrapper(path, mode)
    print('完了しました。')
    input('press enter to exit')


if __name__ == '__main__':
    main()
