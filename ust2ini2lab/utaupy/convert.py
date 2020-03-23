#!/usr/bin/env python3
# coding: utf-8
"""
UTAU関連ファイルの相互変換
"""
from utaupy import otoini


def main():
    """ここ書く必要なくない？"""
    print('AtomとReaperが好き')


def ust2otoini(ust, name_wav, dt=200, overlap=100):
    """
    UstクラスオブジェクトからOtoIniクラスオブジェクトを生成
    dt     : 左ブランクと先行発声の時間距離
    overlap: オーバーラップと先行発声の距離
    【パラメータ設定図】
    # t-dt           t-overlap      t            length+dt  length+dt    length+dt
    # |  左ブランク  |オーバーラップ|  先行発声  | 固定範囲 | 右ブランク |
    # |(dt-overlap)ms| (overlap)ms  | (length)ms |   0ms    |    0ms     |
    """
    notes = ust.get_values()
    tempo = ust.get_tempo()
    oi = otoini.OtoIni()
    otolist = []
    t = 0
    for note in notes[2:-1]:
        length = note.get_length_ms(tempo)
        oto = otoini.Oto()
        oto.set_filename(name_wav)
        oto.set_alies(note.get_lyric())
        oto.set_lblank(max(t - dt, 0))
        oto.set_overlap(min(length - 20, dt - overlap))
        oto.set_onset(min(length - 10, dt))
        oto.set_fixed(length + dt)
        oto.set_rblank(-(length + dt))  # 負で左ブランク相対時刻, 正で絶対時刻
        otolist.append(oto)
        t += length  # 今のノート終了位置が次のノート開始位置
    oi.set_values(otolist)
    return oi

if __name__ == '__main__':
    main()

if __name__ == '__init__':
    pass
