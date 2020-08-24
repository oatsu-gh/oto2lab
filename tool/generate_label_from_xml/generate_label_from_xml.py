#! /usr/bin/env python3
# coding: utf-8
"""
Sinsy をつかって musicxml から
音素ラベル と フルコンテキストラベルを生成するツール。
"""

from glob import glob
from pprint import pprint

import pysinsy


def generate_label(path_xml):
    """
    xml を読み取って
    音素ラベルとフルコンテキストラベルを生成する。
    """
    sinsy = pysinsy.sinsy.Sinsy()
    # Set language to Japanese
    assert sinsy.setLanguages("j", "/usr/local/lib/sinsy/dic")
    assert sinsy.loadScoreFromMusicXML(path_xml)

    is_mono = True
    labels = sinsy.createLabelData(is_mono, 1, 1).getData()
    s = '\n'.join(labels)
    with open(path_xml.replace('.musicxml', '_sinsy.lab').replace('.xml', '_sinsy.lab'), 'w') as f:
        f.write(s)

    is_mono = False
    labels = sinsy.createLabelData(is_mono, 1, 1).getData()
    s = '\n'.join(labels)
    with open(path_xml.replace('.musicxml', '.full').replace('.xml', '.full'), 'w') as f:
        f.write(s)

    sinsy.clearScore()


def main():
    """
    入力ファイルのパスを取得して、変換にかける。
    """
    p = input('musicxmlがあるフォルダのPATHを入力してね (WindowsのPATHでもOK)\n>>> ').strip('"')
    p = p.replace('C:\\', '/mnt/c/').replace('D:\\', '/mnt/d/').replace('E:\\', '/mnt/e/')
    p = p.replace('\\', '/')

    xmlfiles = glob(f'{p}/**/*.musicxml', recursive=True)
    xmlfiles += glob(f'{p}/**/*.xml', recursive=True)

    pprint(xmlfiles)

    for path_xml in xmlfiles:
        print(f'  label generating: {path_xml}')
        generate_label(path_xml)
        print(f'  label generated : {path_xml}')
    print('complete')


if __name__ == '__main__':
    main()
