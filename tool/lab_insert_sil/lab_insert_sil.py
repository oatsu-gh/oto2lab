#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
lab_set_start_sil の強化版。Sinsyで生成したLABを参照して、oto2labなどで生成したLABにsilを挿入する。

# 使い方
1. sinsyが生成したLABを lab_input_sinsy に入れる。ファイル名は {songname}_sinsy.lab または {musicname}.lab としておく。
2. oto2labが生成したLABを lab_input_oto2lab に入れる。ファイル名は {songname}.lab としておく。
3. lab_insert_sil を起動して実行。
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
    oto2lab_sil = [phoneme for phoneme in labobj_oto2lab if phoneme.symbol == 'sil']
    sinsy_sil = [phoneme for phoneme in labobj_sinsy if phoneme.symbol == 'sil']
    oto2lab_pau = [phoneme for phoneme in labobj_oto2lab if phoneme.symbol == 'pau']
    sinsy_pau = [phoneme for phoneme in labobj_sinsy if phoneme.symbol == 'pau']
    oto2lab_br = [phoneme for phoneme in labobj_oto2lab if phoneme.symbol == 'br']
    sinsy_br = [phoneme for phoneme in labobj_sinsy if phoneme.symbol == 'br']
    oto2lab_cl = [phoneme for phoneme in labobj_oto2lab if phoneme.symbol == 'cl']
    sinsy_cl = [phoneme for phoneme in labobj_sinsy if phoneme.symbol == 'cl']
    oto2lab_w = [phoneme for phoneme in labobj_oto2lab if phoneme.symbol == 'w']
    sinsy_w = [phoneme for phoneme in labobj_sinsy if phoneme.symbol == 'w']
    print('  oto2labのラベルの音素数   :', len(labobj_oto2lab))
    print('  Sinsy  のラベルの音素数   :', len(labobj_sinsy))
    print('  oto2labのラベル中のpauの数:', len(oto2lab_pau))
    print('  Sinsy  のラベル中のpauの数:', len(sinsy_pau))
    print('  oto2labのラベル中のsilの数:', len(oto2lab_sil))
    print('  Sinsy  のラベル中のsilの数:', len(sinsy_sil))
    print('  oto2labのラベル中のbrの数 :', len(oto2lab_br))
    print('  Sinsy  のラベル中のbrの数 :', len(sinsy_br))
    print('  oto2labのラベル中のclの数 :', len(oto2lab_cl))
    print('  Sinsy  のラベル中のclの数 :', len(sinsy_cl))
    print('  oto2labのラベル中のwの数 :', len(oto2lab_w))
    print('  Sinsy  のラベル中のwの数 :', len(sinsy_w))
    assert len(oto2lab_br) == len(sinsy_br), 'br の個数が一致しません。'
    assert len(oto2lab_w) == len(sinsy_w), 'w の個数が一致しません。'
    assert len(labobj_oto2lab) - len(oto2lab_pau) - len(oto2lab_sil) \
        == len(labobj_sinsy) - len(sinsy_pau) - len(sinsy_sil), \
        'pau, sil 以外の音素で登録ミスが存在するようです。'


def compare_all_phonemes(labobj_oto2lab, labobj_sinsy):
    """
    すべての音素が一致するかチェックする。
    """
    len_labobj_oto2lab = len(labobj_oto2lab)
    len_labobj_sinsy = len(labobj_sinsy)
    assert len_labobj_oto2lab == len_labobj_sinsy, \
        f'音素数が一致しません。出力するLABの音素数: {len_labobj_oto2lab}, Sinsyの音素数 {len_labobj_sinsy}'
    oto2lab_all_phonemes = [phoneme.symbol for phoneme in labobj_oto2lab]
    sinsy_all_phonemes = [phoneme.symbol for phoneme in labobj_sinsy]
    for i, (ph_oto2lab, ph_sinsy) in enumerate(zip(oto2lab_all_phonemes, sinsy_all_phonemes)):
        assert ph_oto2lab == ph_sinsy, \
            f'{i+1} 行目付近の音素が一致しません。oto2labの音素: {ph_oto2lab}, Sinsyの音素: {ph_sinsy}'

def check_start_end_match(labobj):
    end = 0
    for phoneme in labobj:
        start = phoneme.start
        assert end == start
        end = phoneme.end


def delete_pau_and_sil(labobj):
    """
    pauとsilを全部消す
    """
    labobj.data = [phoneme for phoneme in labobj if phoneme.symbol not in ('pau', 'sil')]


def insert_pau_and_sil(labobj_oto2lab, labobj_sinsy):
    """
    pauとsilを入れる。それ以外の音素は完璧に一致している前提とする。
    """
    for i, phoneme_sinsy in enumerate(labobj_sinsy):
        if phoneme_sinsy.symbol in ('pau', 'sil'):
            labobj_oto2lab.insert(i, deepcopy(phoneme_sinsy))


def restore_pau_time(labobj_oto2lab):
    """
    一度削除されたことによってpauの開始時刻と終了時刻が崩れているため、
    前後の音符の音素の終了時刻と開始時刻から、本来の値を復元する。
    """
    rest_symbols = ('pau', 'sil')
    for i, current_phoneme in enumerate(labobj_oto2lab[1:], 1):
        if current_phoneme.symbol == 'pau':
            previous_phoneme = labobj_oto2lab[i - 1]
            if previous_phoneme.symbol not in rest_symbols:
                current_phoneme.start = previous_phoneme.end
    for i, current_phoneme in enumerate(labobj_oto2lab[:-1]):
        if current_phoneme.symbol == 'pau':
            next_phoneme = labobj_oto2lab[i + 1]
            if next_phoneme.symbol not in rest_symbols:
                current_phoneme.end = next_phoneme.start


def main_wrap(path_lab_oto2lab, path_lab_sinsy, path_lab_out):
    """
    間奏の処理とか前奏の処理とかクラスオブジェクト化とかをまとめて実行する。
    path_lab_oto2lab: oto2lab で作ったLABファイルのパス
    path_lab_sinsy  : Sinsy で作ったLABファイルのパス
    path_lab_out    : 処理結果の出力パス
    """
    # 前処理
    labobj_oto2lab = utaupy.label.load(path_lab_oto2lab)
    labobj_sinsy = utaupy.label.load(path_lab_sinsy)
    print('  処理前-------------------------')
    check_label_diff_for_debug(labobj_oto2lab, labobj_sinsy)
    # oto2labのラベルのsilを全部消す
    delete_pau_and_sil(labobj_oto2lab)
    # oto2labのラベルとSinsyのラベルを比較してsilを挿入する
    insert_pau_and_sil(labobj_oto2lab, labobj_sinsy)
    # pauが失った時間情報を復元する
    restore_pau_time(labobj_oto2lab)
    print('  処理後-------------------------')
    check_label_diff_for_debug(labobj_oto2lab, labobj_sinsy)
    labobj_oto2lab.check_invalid_time(threshold=5)
    # ファイル出力
    labobj_oto2lab.write(path_lab_out)
    compare_all_phonemes(labobj_oto2lab, labobj_sinsy)
    check_start_end_match(labobj_oto2lab)


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
    len_sinsy_labels = len(sinsy_labels)
    len_oto2lab_labels = len(oto2lab_labels)
    print('len_sinsy_labels  :', len_sinsy_labels)
    print('len_oto2lab_labels:', len_sinsy_labels)
    assert len_sinsy_labels == len_oto2lab_labels, 'sinsyのラベルファイル数とoto2labのラベルファイル数が一致しません。'
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
