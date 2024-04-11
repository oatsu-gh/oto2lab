#!/usr/bin/env python3
# Copyright (c) 2021 oatsu
"""
単独音のoto.iniを指定して、「っ」を追加したエイリアスを作る。ENUNU同梱音源用。
"""

from copy import copy

import utaupy


def main():
    otoini = utaupy.otoini.load(input('path_otoini: ').strip('"'))
    new_otoini = utaupy.otoini.OtoIni()
    for oto in otoini:
        new_oto = copy(oto)
        new_oto.alias = oto.alias + 'っ'
        new_otoini.append(oto)
        new_otoini.append(new_oto)
    new_otoini.write('oto_cl.ini')


if __name__ == '__main__':
    main()
