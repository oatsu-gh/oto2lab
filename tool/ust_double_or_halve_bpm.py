#!python
# coding: utf-8
# Copyright (c) oatsu
"""
ピッチを変えずにUSTのテンポを倍にしたり半分にしたりする。
エンベロープがどうなるかは知らん。
"""
import os

import utaupy


def double_tempo_ust(ust):
    """
    ピッチそのままでUSTのテンポを倍にする
    """
    ust.tempo *= 2
    notes = ust.notes
    for note in notes:
        note.length *= 2
        note.pbs = [v * 2 for v in note.pbs]
        note.pbw = [v * 2 for v in note.pbw]


def halve_tempo_ust(ust):
    """
    ピッチそのままでUSTのテンポを倍にする
    """
    ust.tempo /= 2
    notes = ust.notes
    for note in notes:
        note.length /= 2
        note.pbs = [v / 2 for v in note.pbs]
        note.pbw = [v // 2 for v in note.pbw]


def main():
    """
    機能選択とファイル入出力
    """
    path_ust_in = input('USTファイルのパスを入力してください\n>>> ')
    ust = utaupy.ust.load(path_ust_in)
    print('どちらの機能を使いますか？( 1 / 2 )')
    print('1) ピッチを保って BPMを２倍にする')
    print('2) ピッチを保って BPMを半分にする')
    mode = input()

    # 機能の分岐
    if mode in ['1', '１']:
        double_tempo_ust(ust)
    elif mode in ['2', '２']:
        halve_tempo_ust(ust)

    # 実行ファイルの隣に出力
    path_ust_out = os.path.basename(path_ust_in)
    ust.write(f'./{path_ust_out}')


if __name__ == '__main__':
    main()
    input('Press Enter to exit.')
