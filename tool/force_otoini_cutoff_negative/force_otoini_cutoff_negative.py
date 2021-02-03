#!/usr/bin/env python3
# Copyright (c) 2020 oatsu
"""
oto.iniの右ブランクを負の値に強制する。
"""
from sys import argv
from os.path import dirname, join

from pydub import AudioSegment
import utaupy as up


def force_otoinifile_cutoff_negative(path_otoini_in, path_otoini_out):
    """
    指定されたoto.iniを読んで、右ブランクが正の値なときはwavファイルの長さを調べて負にする。
    """
    otoini = up.otoini.load(path_otoini_in)
    voice_dir = dirname(path_otoini_in)
    if not all([oto.cutoff <= 0 for oto in otoini]):
        for oto in otoini:
            path_wav = join(voice_dir, oto.filename)
            sound = AudioSegment.from_file(path_wav, 'wav')
            duration_ms = 1000 * sound.duration_seconds
            absolute_cutoff_position = duration_ms - oto.cutoff
            oto.cutoff = -(absolute_cutoff_position - oto.offset)
        otoini.write(path_otoini_out)


def main(path_otoini):
    """
    もとのファイルを上書き修正する。
    """
    force_otoinifile_cutoff_negative(path_otoini, path_otoini)


if __name__ == '__main__':
    if len(argv) == 1:
        main(input('path_otoini: '))
    else:
        main(argv[1])
