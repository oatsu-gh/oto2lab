#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
モノフォンラベルをかな文字ラベルに変換する。
UTAU連続音の思想のラベリングにより、滑らかな発声の歌声モデル構築を目指す。

動作モード
- 子音の開始位置を発声開始位置にする。（オーバーラップ終了時刻の思想）←こっちを実装した。
- 子音と母音の区切り位置を発声開始位置にする（先行発声終了時刻の思想）
"""

import json
from datetime import datetime
from glob import glob
from os import makedirs
from os.path import basename, isfile, splitext

import utaupy as up


def monolabel_to_intermediate(mono_label, d_phoneme_category):
    """
    モノフォンラベルをいったん2次元リストにする
    [[子音のラベル, 母音のラベル], [子音のラベル, 母音のラベル], [母音のラベル], ...]
    """
    # 子音一覧のリスト
    consonants = d_phoneme_category['consonants']
    # 母音一覧のリスト
    vowels = d_phoneme_category['vowels']
    # [[子音のラベル, 母音のラベル], [子音のラベル, 母音のラベル], [母音のラベル], ...]
    l_temp_2d = []
    # [子音のラベル, 母音のラベル]
    l_temp_inner = []
    for mono_phoneme in mono_label:
        if mono_phoneme.symbol in consonants:
            l_temp_inner.append(mono_phoneme)
        elif mono_phoneme.symbol in vowels:
            l_temp_inner.append(mono_phoneme)
            l_temp_2d.append(l_temp_inner)
            l_temp_inner = []
        else:
            l_temp_inner.append(mono_phoneme)
            l_temp_2d.append(l_temp_inner)
            l_temp_inner = []
    return l_temp_2d


def intermadiate_to_kanalabel(intermadiate_2dlist, d_roma2kana):
    """
    intermadiate_2dlist:
        [[子音のラベル, 母音のラベル], [子音のラベル, 母音のラベル], [母音のラベル], ...]
    return:
        [かなラベル, かなラベル, かなラベル, ...]
    """
    kana_label = up.label.Label()
    for inner_list in intermadiate_2dlist:
        kana_phoneme = up.label.Phoneme()
        kana_phoneme.start = inner_list[0].start
        kana_phoneme.end = inner_list[-1].end
        kana_phoneme.symbol = d_roma2kana[''.join(ph.symbol for ph in inner_list)]
        kana_label.append(kana_phoneme)
    return kana_label


def main():
    """
    ファイル入出力のパスを指定する。
    """
    with open('./config.json', 'r') as f:
        config = json.load(f)
    d_phoneme_category = config['phoneme_category']
    d_roma2kana = config['roma2kana']

    # 変換元のモノフォンラベルのパスを入力させる
    path_input = input('Input path of mono-label directory\n>>> ')
    if isfile(path_input):
        path_mono_label_dir = [path_input]
    else:
        path_mono_label_dir = glob(f'{path_input}/**/*.lab', recursive=True)

    now = datetime.now().strftime('%Y%m%d_%H%M%S')
    makedirs(f'out/{now}', exist_ok=True)
    # モノフォンラベルをかなラベルにする。
    for path_mono_label in path_mono_label_dir:
        print(f'  {path_mono_label}')
        # 変換元のモノフォンラベル
        mono_label = up.label.load(path_mono_label)
        # いったん中間フォーマットとして二次元リストにする
        intermadiate = monolabel_to_intermediate(mono_label, d_phoneme_category)
        # 変換先のかな文字ラベル
        kana_label = intermadiate_to_kanalabel(intermadiate, d_roma2kana)
        # ファイル出力
        path_kana_label = f'out/{now}/{splitext(basename(path_mono_label))[0]}_kana.lab'
        kana_label.write(path_kana_label)


if __name__ == '__main__':
    main()
    input('Press Enter to exit.')
