#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
USTとMusicXMLのテンポが一致するか調べる。
"""
import re
from glob import glob

from utaupy import ust as _ust


def compare_tempo(path_xml, path_ust):
    """
    MusicXMLとUSTを読み取って、BPMを比較する。
    """
    # MusicXMLのテンポ情報を取得
    try:
        with open(path_xml, 'r', encoding='utf-8') as f_xml:
            s = f_xml.read()
    except UnicodeDecodeError:
        with open(path_xml, 'r', encoding='sjis') as f_xml:
            s = f_xml.read()
    tempo_xml = re.findall(r'<sound tempo=".+"/>', s)
    print(tempo_xml)
    tempo_xml = tempo_xml[0].split('"')[1]
    print('tempo_xml:', tempo_xml)
    # USTのテンポ情報を取得
    tempo_ust = _ust.load(path_ust).tempo
    print('tempo_ust:', tempo_ust)
    if int(tempo_xml) != int(tempo_ust):
        print('\n＿人人人人人人人人人人人人人人人人人人人人人人人人＿')
        print('＞[ERROR] MusicXML と UST のテンポが一致しません。＜')
        print('￣Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^￣\n')


def main():
    # 歌唱データベースのフォルダを指定
    singing_database_dir = input('singing_database_dir: ').strip('"')
    # 対象ファイルをリストで取得
    xml_files = glob(f'{singing_database_dir}/**/*.*xml', recursive=True)
    ust_files = glob(f'{singing_database_dir}/**/*.ust', recursive=True)
    xml_files.sort()
    ust_files.sort()
    # ファイル数が一致するかチェック
    assert len(xml_files) == len(
        ust_files), f'MusicXMLファイル数({len(xml_files)})とUSTファイル数({len(ust_files)})が一致しません。'
    # テンポ情報を比較
    for path_xml, path_ust in zip(xml_files, ust_files):
        print('---------------------------------------')
        print('path_xml:', path_xml)
        print('path_ust:', path_ust)
        compare_tempo(path_xml, path_ust)


if __name__ == '__main__':
    main()
