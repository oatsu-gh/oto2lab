#!/usr/bin/env python3
# coding: utf-8
"""
oto.ini → oto.lab の変換ツール
"""
import re
from pprint import pprint
from datetime import datetime

import pyperclip

TEST_MODE = False


def read_otoini(path):
    """
    otoiniを読み取って辞書を返す
    """
    with open(path, 'r') as f:
        l = [re.split('[=,]', s.strip()) for s in f.readlines()]

    # 入力ファイル末尾の空白行を除去
    while l[-1] == ['']:
        del l[-1]

    # 配列を辞書に変換(覚えられないので)
    keys = ['ファイル名', 'エイリアス', '左ブランク', '固定範囲', '右ブランク', '先行発声', 'オーバーラップ']
    l = [dict(zip(keys, v)) for v in l]

    return l


def format_otoini(otoini):
    """
    otoiniを元にした配列をotolab用に整形する
    必要: 左ブランク, 先行発声
    不要: ファイル名, エイリアス, 固定範囲, 右ブランク, オーバーラップ
    変換: エイリアス→発音

    ブレスは「B」で休符では「R」にする？
    """
    # 「母音のみor子音のみorブレスor休符」の判定に使用
    onesign = ['あ', 'い', 'う', 'え', 'お', 'ん', 'っ', 'R', 'B']

    l = []
    for v in otoini:
        # 連続音を単独音化
        kana = v['エイリアス'].split()[-1]

        if kana in onesign:
            roma = kana2roma(kana)
            # [オーバーラップ, 発音文字]
            l.append([v['ファイル名'], v['オーバーラップ'], roma[0]])

        else:
            roma = kana2roma(kana)
            # [オーバーラップ, 子音文字]
            l.append([v['ファイル名'], v['オーバーラップ'], roma[0]])
            # [先行発声, 母音文字]
            l.append([v['ファイル名'], v['先行発声'], roma[1]])

    result = []
    for i, v in enumerate(l):
        try:
            tmp = [v[0], v[1], l[i+1][1], v[2]]
        except IndexError:
            tmp = [v[0], v[1], 'ここに終端時刻を入力', v[2]]
        result.append(tmp)

    return result


def kana2roma(kana):
    """
    平仮名をローマ字に変換する。
    子音と母音に分けて、リストを返す。
    """
    # 平仮名とローマ字の対応表を辞書にする
    with open('japanese_sjis.table', 'r') as f:
        l = [v.split() for v in f.readlines()]
    d = {}
    for v in l:
        d[v[0]] = v[1:]

    return d[kana]


def write_otolab(dataset):
    """
    整形済みデータから oto.lab ファイルを書き出します。
    """
    s = ''
    now = datetime.now()
    path = './output/oto_' + now.strftime('%Y%m%d_%H%M%S') + '.lab'
    with open(path, 'w') as f:
        for l in dataset:
            tmp = '{} {} {} {}\n'.format(l[0], l[1], l[2], l[3])
            s += tmp
        f.write(s)
    return path, s


def main():
    """
    全体の処理を実行
    """
    # oto.iniファイルを指定
    print('oto.iniファイルを指定してください。')
    path = input('>>>').strip('""')

    print('oto.ini を読み取ります。')
    otoini = read_otoini(path)
    # if TEST_MODE:
    #     pprint(otoini)
    print('oto.ini を読み取りました。')

    print('\nデータを整形します。')
    dataset = format_otoini(otoini)
    if TEST_MODE:
        pprint(dataset)
    print('データを整形しました。')

    print('\noto.lab を書き出します。')
    labname, result = write_otolab(dataset)
    pyperclip.copy(str(result))
    print('oto.lab を書き出しました。')
    print('\nファイル名は {} です。'.format(labname))
    print('ファイル内容をクリップボードにコピーしました。')
    print('ファイルを開いて終端時刻を書き込んでください。')
    print('----鋭意開発中です！----')


if __name__ == '__main__':
    main()
    input('Press Enter to exit.')
