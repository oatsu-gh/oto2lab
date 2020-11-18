#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 Tarou Shirani
# Copyright (c) 2020 oatsu
"""
Sinsy をつかって musicxml から
音素ラベル と フルコンテキストラベルを生成するツール。
"""
from glob import glob
from os.path import basename, splitext
from pprint import pprint
from shutil import copy
from sys import argv

import pysinsy
from tqdm import tqdm


def copy_and_rename_xml(path_xmldir_in, path_xmldir_out):
    """
    1. 入力するmusicxmlをwslの ~/temp_wsl/ に移動する。
    2. musicxml のファイル名を連番にして Sinsy のエラーを防ぐ
    もとのファイル名を返す
    """
    # xml, musicxml ファイルを全取得
    l_xml = glob(f'{path_xmldir_in}/*.xml') + glob(f'{path_xmldir_in}/*.musicxml')
    # 名前順にソート
    l_xml.sort()
    # 曲名のリストを作る
    l_songname = [splitext(basename(path))[0] for path in l_xml]
    # xml をコピー
    for i, path_xml in enumerate(tqdm(l_xml)):
        copy(path_xml, f'{path_xmldir_out}/{str(i).zfill(6)}.xml')
    return l_songname


def rename_and_copy_lab(path_dir_lab_in, path_dir_lab_out, l_songname):
    """
    連番labを取得
    名前をもとに戻す
    Windowsのディレクトリに移動させる
    """
    l_lab = glob(f'{path_dir_lab_in}/*.lab')
    l_lab.sort()
    l_songname.sort()

    # ファイル名をもとに戻してコピー
    for i, path_lab in enumerate(tqdm(l_lab)):
        songname = l_songname[i]
        copy(path_lab, f'{path_dir_lab_out}/{songname}.lab')


def xml2lab(path_xmldir_in, path_tabledir):
    """
    xml を読み取って lab (full) を生成する。
    xml と同じディレクトリに生成する。
    """

    list_path_xml = glob(f'{path_xmldir_in}/*.musicxml')
    list_path_xml += glob(f'{path_xmldir_in}/*.xml')
    list_path_xml.sort()

    for path_xml in list_path_xml:
        print(path_xml)
        path_lab = path_xml.replace('.musicxml', '.lab').replace('.xml', '.lab')
        sinsy = pysinsy.sinsy.Sinsy()
        # Set language to Japanese
        assert sinsy.setLanguages("j", path_tabledir)
        assert sinsy.loadScoreFromMusicXML(path_xml)
        is_mono = True
        labels = sinsy.createLabelData(is_mono, 1, 1).getData()
        s = '\n'.join(labels)
        with open(path_lab, 'w') as f:
            f.write(s)
        sinsy.clearScore()


def generate_uttlist(path_labdir_in, path_uttlist_out):
    """
    labファイル一覧をもとに uttlist を生成する。
    """
    list_path_labfile = glob(f'{path_labdir_in}/*.lab')
    list_songname = [splitext(basename(path))[0] for path in list_path_labfile]
    s = '\n'.join(list_songname)
    with open(path_uttlist_out, 'w') as f:
        f.write(s)


def main(path_xmldir, path_temp_dir, path_labdir, path_tabledir, path_uttlist):
    """
    入力ファイルのパスを取得して、変換にかける。
    """
    print('path_xmldir   :', path_xmldir)
    print('path_temp_dir :', path_temp_dir)
    print('path_labdir   :', path_labdir)
    print('path_tabledir :', path_tabledir)
    print('path_uttlist  :', path_uttlist)

    print('xml2lab.py: copy_and_rename_xml: copying XML files')
    list_songname = copy_and_rename_xml(path_xmldir, path_temp_dir)
    for i, songname in enumerate(list_songname):
        print(f'{str(i).rjust(3, " ")}: {songname}')

    print('xml2lab.py: xml2lab            : converting XML files to LAB files')
    xml2lab(path_temp_dir, path_tabledir)

    print('xml2lab.py: rename_and_copy_lab: copying LAB files')
    rename_and_copy_lab(path_temp_dir, path_labdir, list_songname)

    print('xml2lab.py: generate_uttlist   : generating uttlist')
    generate_uttlist(path_labdir, path_uttlist)


if __name__ == '__main__':
    main(argv[1], argv[2], argv[3], argv[4], argv[5])
