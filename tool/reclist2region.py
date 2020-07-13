#!python3
# coding: utf-8
# Copyright (c) oatsu
"""
録音リストからReaper用のリージョンCSVを生成するツール
"""
import os
from pprint import pprint

import utaupy as up


# def reclist2rows(reclist, a, b):
#     """
#     reclist: 録音リストの配列
#     a: 1行ごとの発声部分の長さ （小節）
#     b: 1行ごとの余白部分の長さ （小節）
#
#     実際はbを2等分する必要がありそうだけど
#     DAWで音声ファイル移動させるほうが実装が楽
#
#     |______a_________|___b____|______a_________|___b____|
#     |ああいあうえあー|　　　　|いいうあえいえー|　　　　|
#     | 2小節          | 1小節  | 2小節          | 1小節  |
#
#     クラスを使わない方の実装
#     """
#     l = []  # CSV生成用の二次元リスト
#     duration = a + b
#     t = 1  # 開始位置を記録するやつ
#     for i, v in enumerate(reclist):
#         t += duration
#         tag = 'R{}'.format(i)
#         name = v
#         start = '{}.1.00'.format(t)
#         end = None
#         length = '{}.0.00'.format(duration)
#         l.append([tag, v, start, end, length])
#     return l



def main():
    a = int(input('1行ごとの発声長さ（小節）を入力してください: '))
    b = int(input('1行ごとの余白長さ（小節）を入力してください: '))
    inpath = input('録音リストのパスを指定してください: ')
    print()

    reclist = up.reclist.load(inpath)
    regioncsv = up.convert.reclist2regioncsv(reclist, a, b)
    for region in regioncsv.values:
        print(region.values)

    outpath = os.path.splitext(inpath)[0] + '_発声{}小節_余白{}小節.csv'.format(a, b)
    regioncsv.write(outpath)


if __name__ == '__main__':
    print('---録音リストからReaper用のリージョンCSVを生成するツール---')
    main()
    input('Press Enter to exit')
