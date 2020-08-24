#! /usr/bin/env python3
# coding: utf-8
"""
音素網羅チェッカー！
フォルダ内にあるモノフォンラベルを全部取得して、
モノフォン、ダイフォン、トライフォンで網羅度をチェックします。
- 日本語 CV
- 日本語 CV / VV / VC
- 日本語 VV / VCV / CVC
- CC は歌唱内で使わなそうな気がするけどどうなんすか
- 中間母音はどうするんすか
- VCV, VCVC (a か k), CVCV (k ak i)

任意長さでできるといいなあ
先頭と末尾の無音を含めるのを忘れないように。
Excelで可視化できるようにしたいですね。
音程遷移のチェック機能はありません。
"""

from glob import glob
from pprint import pprint

import numpy as np

# import openpyxl

VOWELS = ['a', 'i', 'u', 'e', 'o']
CONSONANTS = ['k', 's', 't', 'n', 'h', 'm', 'y', 'r', 'w',
              'g', 'z', 'j', 'd', 'b', 'p',
              'ky', 'sh', 'ch', 'ts', 'ty', 'ny', 'hy',
              'by', 'py', 'my', 'ry', 'v', 'gy', 'dy', 'f']
SPECIALS = ['pau', 'cl', 'N', 'br', 'sil', 'TRACKSTART', 'TRACKEND', 'DUMMY']


def read_labels(path_labeldir):
    """
    複数のモノフォンラベルを読み取って、トラック x 音素列 の二次元音素リストにする。
    """
    labfiles = glob('{}/*.lab'.format(path_labeldir))
    print('対象ファイル')
    pprint(labfiles)

    l = []
    for labfile in labfiles:
        with open(labfile) as f:
            tmp = [s.strip().split()[2] for s in f.readlines()]
            l.append(['TRACKSTART'] + tmp + ['TRACKEND'])
    return l


def phonemes_as_number(keys, tracks, dimension=1):
    """
    ラベルの発音記号を数字にする
    numpy.arrayで扱うために発音記号を数字に置き換える。
    """
    dummy_list = ['DUMMY'] * (dimension - 1)
    d = dict(zip(keys, range(len(keys))))
    # l = [[dummy_list + [d[v] for v in track] + dummy_list] for track in tracks]
    # リスト内包表記を展開-------------
    l = []
    for track in tracks:
        tmp = dummy_list + track + dummy_list
        tmp = [d[v] for v in tmp]
        l.append(tmp)
    # ----------------------------------
    return l


def count_how_often(keys, tracks, dimension):
    """
    l 数字化した音素: ラベル中の発音記号リストを数字のリストにしたやつ
    dimension 次元数: モノフォンなら1, ダイフォンなら2, トライフォンなら3。
    length  辺の長さ: 発音記号の種類数。
    """
    length = len(keys)
    a = np.zeros((length, ) * dimension, dtype=np.int)  # 整数ゼロで初期化した多次元配列

    # numpy.array は tuple = (0, 1) とすれば a[tuple] で座標指定取得できる
    if dimension == 1:
        for track in tracks:
            for v in track:
                a[v] += 1
    elif dimension == 2:
        for track in tracks:
            for i, _ in enumerate(track[:-1]):
                tmp = track[i:(i + 2)]
                a[tmp[0], tmp[1]] += 1
    elif dimension == 3:
        for track in tracks:
            for i, _ in enumerate(track[:-2]):
                tmp = track[i:(i + 3)]
                a[tmp[0], tmp[1], tmp[2]] += 1
    elif dimension == 4:
        for track in tracks:
            for i, _ in enumerate(track[:-3]):
                tmp = track[i:(i + 4)]
                a[tmp[0], tmp[1], tmp[2], tmp[3]] += 1
    elif dimension == 5:
        for track in tracks:
            for i, _ in enumerate(track[:-4]):
                tmp = track[i:(i + 5)]
                a[tmp[0], tmp[1], tmp[2], tmp[3], tmp[4]] += 1
    elif dimension == 6:
        for track in tracks:
            for i, _ in enumerate(track[:-5]):
                tmp = track[i:(i + 6)]
                a[tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5]] += 1

    # pprint(a)
    return a


def main():
    """
    機能選択とパス指定
    """
    np.set_printoptions(threshold=10000, linewidth=100)
    print('まだテスト中')
    # 処理対象フォルダ指定
    path = input('path     : ').strip(r'"')
    # モード選択
    dimension = int(input('dimension: '))
    if not isinstance(dimension, int):
        print('数字で')

    keys = VOWELS + CONSONANTS + SPECIALS
    tracks = read_labels(path)
    tracks = phonemes_as_number(keys, tracks, dimension)
    a = count_how_often(keys, tracks, dimension)
    np.set_printoptions(threshold=100000, linewidth=2000)
    s = ' '.join(keys) + '\n' + str(a)
    with open('result.txt', 'w') as f:
        f.write(s)


if __name__ == '__main__':
    main()
    input('press enter')
