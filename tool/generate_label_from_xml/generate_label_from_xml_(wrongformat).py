#!python3
# coding: utf-8
"""
about module
"""

from glob import glob
from pprint import pprint

import pysinsy


def generate_label(path_xml):
    sinsy = pysinsy.sinsy.Sinsy()
    # Set language to Japanese
    assert sinsy.setLanguages("j", "/usr/local/lib/sinsy/dic")
    assert sinsy.loadScoreFromMusicXML(path_xml)

    is_mono = True
    labels = sinsy.createLabelData(is_mono, 1, 1).getData()
    with open(path_xml.replace('.musicxml', '.lab').replace('.xml', '.lab'), 'w') as f:
        f.writelines(labels)

    # is_mono = False
    # labels = sinsy.createLabelData(is_mono, 1, 1).getData()
    # with open(path_xml.replace('.musicxml', '.full').replace('.xml', '.full'), 'w') as f:
    #     f.writelines(labels)

    sinsy.clearScore()


def main():
    p = input('musicxmlがあるフォルダのPATHを入力してね : ').strip('"')
    p = p.replace('C:\\', '/mnt/c/').replace('D:\\', 'mnt/d/').replace('D:\\', 'mnt/e/')
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