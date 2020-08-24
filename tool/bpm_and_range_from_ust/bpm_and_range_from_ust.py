#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) oatsu
"""
指定フォルダ内にあるustファイルの音域とBPM情報を取得するツール
"""

import csv
import os
from glob import glob
from pprint import pprint

import utaupy as up


def get_param(path_ust):
    """
    ustのパスを受け取って、BPM情報と最高音、最低音を返す
    """
    ust = up.ust.load(path_ust)
    bpm = ust.tempo
    notes = ust.values[2:-1]

    # 最初のノートをとりあえず基準にする
    highest_note = None
    lowest_note = None
    # 残りのノートをチェック
    for note in notes[1:]:
        if note.lyric in ['pau', 'br', 'R', '息', '吸', 'sil']:
            continue
        if highest_note == None:
            highest_note = note
        elif highest_note.notenum < note.notenum:
            highest_note = note
        if lowest_note == None:
            lowest_note = note
        elif lowest_note.notenum > note.notenum:
            lowest_note = note
    l = [os.path.basename(path_ust), bpm,
         up.ust.notenum_as_abc(highest_note.notenum), highest_note.lyric,
         up.ust.notenum_as_abc(lowest_note.notenum), lowest_note.lyric]
    return l


def main():
    path_dir = input('ustファイルがあるフォルダを指定してください。孫フォルダ以降も探索します。\n>>> ')
    paths = glob('{}/**/*.ust'.format(path_dir), recursive=True)
    l = [['ファイル名', 'BPM', '最高音', '最高音の歌詞', '最低音', '最低音の歌詞']]
    for p in paths:
        l.append(get_param(p))
    pprint(l)

    path_csv = f'result(ust_bpm_and_range).csv'
    with open(path_csv, mode='w', newline='\n', encoding='shift-jis') as f:
        writer = csv.writer(f)
        writer.writerows(l)
    print('CSVファイルを出力しました。:', path_csv)


if __name__ == '__main__':
    print('_____ξ・ヮ・) < ust_bpm_and_range v0.0.0 ________')
    print('USTのBPMと音域を取得するツール')
    main()
    print('press enter to exit')
