#!python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
USTからSHIRO用のCSVを生成するツール
"""

import os
import sys
from datetime import datetime
from glob import glob
from pprint import pprint

import utaupy as up


def ustfiles2shiroindexfile(ust_dir, d):
    """
    ust_dir: ustファイルがあるディレクトリパス、
    d: かなローマ変換辞書
    """
    ustfiles = glob('{}/*.{}'.format(ust_dir, 'ust'))
    pprint(ustfiles)

    l = []  # indexの元にするリスト
    for ustfile in ustfiles:
        print(f'    processing: {ustfile}')
        ust = up.ust.load(ustfile)  # Ustオブジェクトを生成
        kana_lyrics = [note.lyric for note in ust.values[2:-1]]
        romaji_lyrics = [' '.join(d[v]) for v in kana_lyrics]
        songname = os.path.splitext(os.path.basename(ustfile))[0]
        l.append([songname] + romaji_lyrics)
    # pprint(l)
    index = up.shiro.Index()
    index.values = l  # Indexに値を代入
    now = datetime.now().strftime('%Y%m%d_%H%M%S')  # 出力ファイルにつける時刻文字列
    csv_path = f'{ust_dir}/shiro_index__{now}.csv'  # 出力パス
    index.write(csv_path, encoding='shift-jis')     # 出力
    print(f'IndexFile was successfully exported as \"{csv_path}\"')


def main():
    """
    各種パスを標準入力で指定
    """
    ust_dir = input('Input path of USTs directory\n>>> ')

    if not os.path.isdir(ust_dir):
        print('フォルダを指定してください。')
        input('Press enter to exit')
        sys.exit()
    tablepath = input('Input path of tablefile\n>>> ')
    d = up.table.load(tablepath)  # かなローマ辞書
    d.update({'R': ['pau'], 'br': ['br'], '息': ['br'], 'pau': ['pau'], 'sil': ['sil']})
    ustfiles2shiroindexfile(ust_dir, d)


if __name__ == '__main__':
    print('---USTからSHIRO用のCSVを生成するツール(20200711)---')
    main()
    input('Press enter to exit')
