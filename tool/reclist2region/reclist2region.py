#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) oatsu
"""
録音リストからReaper用のリージョンCSVを生成するツール
【更新履歴】
- v0.0.0 初リリース
- v0.0.1
    - reclist2regioncsv() をutaupyから切り離し。
    - リージョンの End を指定するようにした。(マーカーとして扱われてしまう対策)
"""

import os
from pprint import pprint

import utaupy as up


def reclist2regioncsv(reclist, a, b):
    """
    reclist: 録音リストの配列
    a: 1行ごとの発声部分の長さ （小節）
    b: 1行ごとの余白部分の長さ （小節）

    実際はbを2等分する必要がありそうだけど
    DAWで音声ファイル移動させるほうが実装が楽

    |______a_________|___b____|______a_________|___b____|
    |ああいあうえあー|　　　　|いいうあえいえー|　　　　|
    | 2小節          | 1小節  | 2小節          | 1小節  |

    """
    duration = a + b
    t = 1  # 開始位置を記録するやつ
    l = []
    for v in reclist:
        t += duration
        region = up.reaper.Region()
        region.name = v
        region.start = '{}.1.00'.format(t)
        region.end = '{}.1.00'.format(t + duration)
        region.length = '{}.0.00'.format(duration)
        l.append(region)

    regioncsv = up.reaper.RegionCsv()
    regioncsv.values = l
    return regioncsv


def main():
    a = int(input('1行ごとの発声長さ（小節）を入力してください: '))
    b = int(input('1行ごとの余白長さ（小節）を入力してください: '))
    inpath = input('録音リストのパスを指定してください: ').strip(r'"')
    print()

    reclist = up.reclist.load(inpath)
    regioncsv = reclist2regioncsv(reclist, a, b)
    for region in regioncsv.values:
        print(region.values)
    outpath = os.path.splitext(inpath)[0] + '_発声{}小節_余白{}小節.csv'.format(a, b)
    regioncsv.write(outpath)


if __name__ == '__main__':
    print('_____ξ・ヮ・) < reclist2region v0.0.2 ________')
    print('録音リストからリージョンCSVを生成するツール')
    print('Copyright (c) 2001-2020 Python Software Foundation')
    print('Copyright (c) 2020 oatsu\n')
    main()
    input('Press Enter to exit')
