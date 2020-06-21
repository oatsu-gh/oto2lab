#!/usr/bin/env python3
# coding: utf-8
"""
about module
"""

from glob import glob

import pysinsy


def main():
    p = input('musicxmlがあるフォルダのPATHを入力してね : ')
    xmlfiles = glob(f'{p}/**/*.musicxml', recursive=True)
    xmlfiles += glob(f'{p}/**/*.xml', recursive=True)
    for v in xmlfiles:
        print(v)
    for xml in xmlfiles:
        generate_label(xml)
    print('complete')


def generate_label(xmlpath):
    print(xmlpath)

    sinsy = pysinsy.sinsy.Sinsy()
    # Set language to Japanese
    assert sinsy.setLanguages("j", "/usr/local/lib/sinsy/dic")
    assert sinsy.loadScoreFromMusicXML(xmlpath)

    is_mono = True
    labels = sinsy.createLabelData(is_mono, 1, 1).getData()
    with open(xmlpath + '.lab', 'w') as f:
        f.writelines(labels)

    is_mono = False
    labels = sinsy.createLabelData(is_mono, 1, 1).getData()
    with open(xmlpath + '.full', 'w') as f:
        f.writelines(labels)

    sinsy.clearScore()


if __name__ == '__main__':
    main()
