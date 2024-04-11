#!/usr/bin/env python3
# Copyright (c) 2022 oatsu
"""
USTファイルをREAPERのマーカーCSVファイルに変換する。
utaupyがリージョンにしか対応していないので、いったんリージョンとして作成してからマーカーに変換して出力する。
"""
from os.path import dirname, join

import utaupy

PATH_TABLE = join(dirname(__file__),
                  'kana2phonemes_003_oto2lab.table')


def calculate_marker_time_from_ust(ust: utaupy.ust.Ust):
    """ノート開始時刻のリストを返す。一番最後だけ終了時刻。
    """
    t = 0
    l = [t]
    for note in ust.notes:
        t += note.length_ms / 1000
        l.append(t)
    return l


def get_marker_strings_from_ust(ust: utaupy.ust.Ust, table: dict):
    """ノート情報から歌詞を抜き出して、音素記号に変換してリストで返す。
    ノートごとに複数の音素があると思うので、2次元リストで返す。
    """
    l_2d = []
    for note in ust.notes:
        lyric = note.lyric
        phonemes = table.get(note.lyric, lyric.split())
        l_2d.append(phonemes)
    return l_2d


def convert_ust_file_to_marker_csv_file(path_ust, path_marker_csv, path_table):
    """USTファイルをREAPERのマーカー用のCSVファイルに変換する。
    """
    # USTファイルを読み取る
    ust = utaupy.ust.load(path_ust)
    # 歌詞→音素 の変換テーブルを読み取る
    table = utaupy.table.load(path_table)
    # リージョン・マーカーCSVファイル用のインスタンスを生成する
    regions = utaupy.reaper.RegionCsv()
    # USTから時刻と音素情報を生成
    times = calculate_marker_time_from_ust(ust)
    phonemes_2d = get_marker_strings_from_ust(ust, table)
    # 終端時刻のデータがあることを考慮して長さがおかしくないか比較する
    assert len(times) - 1 == len(phonemes_2d)
    # 音素ごとにマーカー情報を作成
    for t, phonemes_1d in zip(times, phonemes_2d):
        len_phonemes_1d = len(phonemes_1d)
        for i, ph in enumerate(phonemes_1d):
            region = utaupy.reaper.Region()
            region.name = ph
            region.start = t - (len_phonemes_1d - i - 1) * 0.05
            regions.append(region)
    # 最終ノートの終了位置のマーカーを登録
    region = utaupy.reaper.Region()
    region.name = 'END'
    region.start = times[-1]
    regions.append(region)

    # ファイル出力
    regions.write(path_marker_csv)


def region2marker(path_csv):
    """リージョンCSVをマーカーCSVにする
    """
    with open(path_csv, 'r') as f:
        lines = f.readlines()
    lines = [lines[0]] + [f'M{line[1:]}' for line in lines[1:]]
    with open(path_csv, 'w') as f:
        f.writelines(lines)


def main():
    path_ust = input('USTファイルを指定してください: ').strip('"')
    path_table = PATH_TABLE
    path_marker_csv = path_ust.replace('.ust', '_ReaperRegionMarker.csv')
    convert_ust_file_to_marker_csv_file(path_ust, path_marker_csv, path_table)
    region2marker(path_marker_csv)


if __name__ == "__main__":
    main()
