#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
lab_set_start_sil の強化版。Sinsyで生成したLABを参照して、oto2labなどで生成したLABにsilを挿入する。

# 使い方
1. sinsyが生成したLABを lab_input_sinsy に入れる。ファイル名は {songname}_sinsy.lab または {musicname}.lab としておく。
1. oto2labが生成したLABを lab_input_oto2lab に入れる。ファイル名は {songname}.lab としておく。
1. lab_insert_sil を起動して実行。
"""
from copy import deepcopy
from glob import glob
from os.path import basename

import utaupy

PATH_SINSY_LABEL_DIR = 'lab_input_sinsy'
PATH_OTO2LAB_LABEL_DIR = 'lab_input_oto2lab'
PATH_OUTPUT_LABEL_DIR = 'lab_output'


def check_label_diff_for_debug(labobj_oto2lab, labobj_sinsy):
    """
    デバッグ用に音素数を数える
    1つ違うとき・・・前奏または後奏のsilが一致しない
    2つ違うとき・・・前奏と構想の両方、または間奏のsilが一致しない
    """
    oto2lab_sil = [phoneme for phoneme in labobj_sinsy if phoneme.symbol == 'sil']
    sinsy_sil = [phoneme for phoneme in labobj_oto2lab if phoneme.symbol == 'sil']
    oto2lab_br = [phoneme for phoneme in labobj_oto2lab if phoneme.symbol == 'br']
    sinsy_br = [phoneme for phoneme in labobj_sinsy if phoneme.symbol == 'br']
    print('  oto2labのラベルの音素数   :', len(labobj_oto2lab))
    print('  Sinsy  のラベルの音素数   :', len(labobj_sinsy))
    print('  oto2labのラベル中のsilの数:', len(oto2lab_sil))
    print('  Sinsy  のラベル中のsilの数:', len(sinsy_sil))
    print('  oto2labのラベル中のbrの数 :', len(oto2lab_br))
    print('  Sinsy  のラベル中のbrの数 :', len(sinsy_br))


def delete_sil(labobj):
    """
    silを全部消す
    """
    labobj.data = [phoneme for phoneme in labobj if phoneme.symbol != 'sil']
    labobj[0].start = 0
    labobj.reload()


def insert_sil(labobj_oto2lab, labobj_sinsy):
    """
    間奏部分のsilを挿入する
    1. Sinsyのラベル中のsilな音素を検出
    2. silを挿入する前に、manualのラベルへの挿入部分の前後のpauを複製する
    3. silを挿入する
    """
    # 一番最初のpauを処理する
    if labobj_oto2lab[0].symbol == 'pau' and labobj_sinsy[0].symbol == 'sil':
        # silを挿入する
        labobj_oto2lab.insert(0, deepcopy(labobj_sinsy[0]))
        # silの直後のpauの時刻を調整する
        labobj_oto2lab[1].start = labobj_oto2lab[1].end
    # 前奏の最初以外と間奏のsilを挿入する
    for i, phoneme_sinsy in enumerate(labobj_sinsy[1:-1], 1):
        if phoneme_sinsy.symbol == 'sil':
            if labobj_oto2lab[i - 1] != 'pau':
                if labobj_oto2lab[i - 1].symbol != 'sil':
                    # pauを複製する
                    labobj_oto2lab.insert(i, deepcopy(labobj_oto2lab[i - 1]))
                # silを挿入する
                labobj_oto2lab.insert(i, deepcopy(phoneme_sinsy))
                # silの直前のpauの時刻を調整する
                labobj_oto2lab[i - 1].end = labobj_oto2lab[i].start
                # silの直後のpauの時刻を調整する
                labobj_oto2lab[i + 1].start = labobj_oto2lab[i].end
            else:
                raise ValueError('sil を挿入したい場所にある音素が pau 以外です。:', str(labobj_oto2lab[i]))


def main_wrap(path_lab_oto2lab, path_lab_sinsy, path_lab_out):
    """
    間奏の処理とか前奏の処理とかクラスオブジェクト化とかをまとめて実行する。
    path_lab_oto2lab: oto2lab で作ったLABファイルのパス
    path_lab_sinsy  : Sinsy で作ったLABファイルのパス
    path_lab_out    : 処理結果の出力パス
    """
    # 前処理
    labobj_oto2lab = utaupy.label.load(path_lab_oto2lab)
    labobj_oto2lab.check_invalid_time()
    labobj_sinsy = utaupy.label.load(path_lab_sinsy)
    labobj_sinsy.check_invalid_time()
    print('  処理前------------------------')
    check_label_diff_for_debug(labobj_oto2lab, labobj_sinsy)
    # oto2labのラベルのsilを全部消す
    delete_sil(labobj_oto2lab)
    # oto2labのラベルとSinsyのラベルを比較してsilを挿入する
    insert_sil(labobj_oto2lab, labobj_sinsy)
    print('  処理後------------------------')
    check_label_diff_for_debug(labobj_oto2lab, labobj_sinsy)
    labobj_oto2lab.check_invalid_time()
    # ファイル出力
    labobj_oto2lab.write(path_lab_out)


def main():
    """
    PATHを指定して全体の処理をする。
    """
    path_sinsy_label_dir = PATH_SINSY_LABEL_DIR
    path_oto2lab_label_dir = PATH_OTO2LAB_LABEL_DIR
    path_output_label_dir = PATH_OUTPUT_LABEL_DIR

    # LABファイルを取得
    sinsy_labels = glob(f'{path_sinsy_label_dir}/*.lab')
    oto2lab_labels = glob(f'{path_sinsy_label_dir}/*.lab')
    len_sinsny_labels = len(sinsy_labels)
    len_oto2lab_labels = len(oto2lab_labels)
    print('len_sinsny_labels :', len_sinsny_labels)
    print('len_oto2lab_labels:', len_sinsny_labels)
    if len_sinsny_labels != len_oto2lab_labels:
        raise ValueError('sinsyのラベルファイル数とoto2labのラベルファイル数が一致しません。')
    # 書き換えを始める。
    for path_lab_sinsy in sinsy_labels:
        print('--------------------------------------------------')
        songname = basename(path_lab_sinsy).replace('_sinsy.lab', '').replace('.lab', '')
        path_lab_oto2lab = f'{path_oto2lab_label_dir}/{songname}.lab'
        print('path_lab_oto2lab:', path_lab_oto2lab)
        print('path_lab_sinsy  :', path_lab_sinsy)
        path_lab_out = f'{path_output_label_dir}/{songname}.lab'
        main_wrap(path_lab_oto2lab, path_lab_sinsy, path_lab_out)


if __name__ == '__main__':
    main()
