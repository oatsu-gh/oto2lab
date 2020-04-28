#!/usr/bin/env python3
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

VOWELS = ['a', 'i', 'u', 'e', 'o']
CONSONANTS = ['k', 's', 't', 'n', 'h', 'm', 'y', 'r', 'w',
              'g', 'z', 'j', 'd', 'b', 'p',
              'ky', 'sh', 'ch', 'ts', 'ty', 'ny', 'hy',
              'by', 'py', 'my', 'ry', 'v', 'gy', 'dy', 'f']
SPECIALS = ['pau', 'cl', 'N', 'br', 'sil', 'TRACKSTART', 'TRACKEND']


def read_labels(path_labeldir):
    """
    複数のモノフォンラベルを読み取って、音素を一次元のリストにする
    """
    labfiles = glob('{}/*.lab'.format(path_labeldir))
    print('\n対象ファイル')
    pprint(labfiles)

    l = []
    for labfile in labfiles:
        l.append('TRACKSTART')
        with open(labfile) as f:
            l += [s.strip().split()[2] for s in f.readlines()]
        l.append('TRACKEND')
    return l


def check_mono(l):
    """
    単音でチェック
    """
    # モノフォン用の表（一次元の辞書）をつくる
    keys = VOWELS + CONSONANTS + SPECIALS
    zerolist = [0] * len(keys)
    d = dict(zip(keys, zerolist))
    # カウント
    for v in l:
        d[v] += 1
    return d


def main():
    """
    機能選択とパス指定
    """
    print('まだテスト中')
    # 処理対象フォルダ指定
    path = input('path: ')
    # モード選択
    mode = input('mode: ')
    if mode == 'mono':
        # ここから本処理開始
        l = read_labels(path)
        d = check_mono(l)
        print('\n数え上げ結果')
        for k, v in d.items():
            print('  {}\t: {}'.format(k, v))
    else:
        print('未実装')




if __name__ == '__main__':
    main()
    input('press enter')
